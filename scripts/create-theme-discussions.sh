#!/usr/bin/env bash
#
# Create discussions for themes.
#
# Usage: ./scripts/create-theme-discussions.sh [start_number]
#

TOKEN=$(gh auth token)
REPO_ID="R_kgDOMoOy9A"
CAT_ID="DIC_kwDOMoOy9M4CvYxA"
API_URL="https://api.github.com/graphql"

# Theme list - shortname -> fullname
declare -A THEMES=(
  ["nightshade"]="Nightshade"
  ["nightshade-v2"]="Nightshade v2"
  ["nightshade-v2_1"]="Nightshade v2.1"
  ["nightshade-v2_2"]="Nightshade v2.2"
  ["nightshade-v2_3"]="Nightshade v2.3"
  ["amoled-black"]="AMOLED Black"
  ["amoled-black-v2"]="AMOLED Black v2"
  ["catppuccin-mocha-v2"]="Catppuccin Mocha v2"
  ["catppuccin-latte"]="Catppuccin Latte"
  ["catppuccin-frappe"]="Catppuccin Frappe"
  ["catppuccin-macchiato"]="Catppuccin Macchiato"
  ["green-v2"]="Green v2"
  ["green-plus-v1"]="Green Plus v1"
  ["green-plus-v1_5"]="Green Plus v1.5"
  ["green-night-v1"]="Green Night v1"
  ["dusk"]="Dusk"
  ["dusk-v2"]="Dusk v2"
  ["dark"]="Dark"
  ["light"]="Light"
  ["dracula"]="Dracula"
  ["solarized-darkish"]="Solarized Darkish"
  ["joker"]="Joker"
  ["mona-lisa"]="Mona Lisa"
  ["aurora-sunset"]="Aurora Sunset"
)

# Check existing discussions
EXISTING=$(curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"query":"{repository(owner:\"oSoWoSo\",name:\"SimpleX-Themes\"){discussions(first:100){nodes{number title}}}}"' \
  "$API_URL" | jq -r '.data.repository.discussions.nodes[].title' 2>/dev/null)

# Create discussions
for shortname in "${!THEMES[@]}"; do
  fullname="${THEMES[$shortname]}"
  title="[Theme] $fullname"
  
  # Check if already exists
  if echo "$EXISTING" | grep -q "^${title}$"; then
    echo "Skipping: $title (already exists)"
    continue
  fi
  
  # Create discussion
  body="Theme discussion, reactions and popularity tracking.\n\nTheme file: themes/SxC_${shortname}.theme"
  
  result=$(curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
    -d "{\"query\":\"mutation{createDiscussion(input:{repositoryId:\\\"$REPO_ID\\\",categoryId:\\\"$CAT_ID\\\",body:\\\"$body\\\",title:\\\"$title\\\"}){discussion{number title}}}}\"}" \
    "$API_URL")
  
  if echo "$result" | jq -e '.data.createDiscussion' >/dev/null 2>&1; then
    num=$(echo "$result" | jq -r '.data.createDiscussion.discussion.number')
    echo "Created: $title (#$num)"
  else
    err=$(echo "$result" | jq -r '.errors[0].message')
    echo "Error creating $title: $err"
  fi
  
  sleep 1
done