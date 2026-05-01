import fs from "fs";
import { graphql } from "@octokit/graphql";

const THEMES_FILE = "data/themes.json";
const OUTPUT_FILE = "data/popular.json";
const REPO_OWNER = "oSoWoSo";
const REPO_NAME = "SimpleX-Themes";

const themes = JSON.parse(fs.readFileSync(THEMES_FILE, "utf8"));

const graphqlAuth = graphql.defaults({
  headers: {
    authorization: `token ${process.env.GITHUB_TOKEN}`,
  },
});

async function getDiscussionStats(discussionNumber) {
  const query = `
    query($owner: String!, $name: String!, $number: Int!) {
      repository(owner: $owner, name: $name) {
        discussion(number: $number) {
          createdAt
          comments {
            totalCount
          }
          reactionGroups {
            content
            users {
              totalCount
            }
          }
        }
      }
    }
  `;

  const result = await graphqlAuth(query, {
    owner: REPO_OWNER,
    name: REPO_NAME,
    number: discussionNumber,
  });

  return result.repository.discussion;
}

function calculateScore(discussion, reactions) {
  const likes = reactions.THUMBS_UP || 0;
  const hearts = reactions.HEART || 0;
  const rockets = reactions.ROCKET || 0;
  const comments = discussion.comments.totalCount;

  const created = new Date(discussion.createdAt).getTime();
  const ageDays = (Date.now() - created) / 1000 / 60 / 60 / 24;

  // Weighted score: likes=1, hearts=2, rockets=3, comments=1.5
  // Decay over time to favor newer themes
  const rawScore = likes + hearts * 2 + rockets * 3 + comments * 1.5;
  const score = rawScore / Math.pow(ageDays + 2, 1.3);

  return {
    likes,
    hearts,
    rockets,
    comments,
    score: Number(score.toFixed(2)),
  };
}

const results = [];

for (const theme of themes) {
  console.log(`Processing: ${theme.name} (discussion #${theme.discussion})`);

  try {
    const discussion = await getDiscussionStats(theme.discussion);

    const reactions = {};
    for (const group of discussion.reactionGroups) {
      reactions[group.content] = group.users.totalCount;
    }

    const stats = calculateScore(discussion, reactions);

    results.push({
      id: theme.id,
      name: theme.name,
      ...stats,
    });
  } catch (error) {
    console.error(`Error fetching ${theme.name}:`, error.message);
    results.push({
      id: theme.id,
      name: theme.name,
      likes: 0,
      hearts: 0,
      rockets: 0,
      comments: 0,
      score: 0,
    });
  }
}

// Sort by score descending
results.sort((a, b) => b.score - a.score);

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(results, null, 2));

console.log(`Generated ${OUTPUT_FILE} with ${results.length} themes`);