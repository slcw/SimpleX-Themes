#!/usr/bin/env python3
"""Create discussions for theme families."""
import subprocess, time, requests

TOKEN = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
API_URL = "https://api.github.com/graphql"
REPO_ID = "R_kgDOMoOy9A"
CAT_ID = "DIC_kwDOMoOy9M4CvYxA"

# Group by families (matching exact filename roots)
FAMILIES = {
    "Nightshade": ["Nightshade", "NightshadeTransparent-v1_5", "NightshadeTransparent-v2", "Nightshade-v1", "Nightshade-v1_5", "Nightshade-v2", "Nightshade-v2_1", "Nightshade-v2_2", "Nightshade-v2_3", "nightswatch-v2", "nightswatch-v3"],
    "AMOLED Black": ["AMOLEDblack-v1", "AMOLEDblackV2"],
    "Catppuccin": ["catppuccinMocha-v1", "catppuccinMocha-v2", "catppuccinLatte", "catppuccinFrappe", "catppuccinMacchiato"],
    "Green": ["green-v1", "green-v2", "greenPlus-v1", "greenPlus-v1_5", "greenNight-v1"],
    "Dusk": ["dusk", "dusk-v2"],
    "CPN": ["CPN_Hacking-v1", "CPN_Hacking-v2", "CPN_iMessage-v1", "CPN_iMessage-v2", "CPN_synthwave", "CPN_vaporwave"],
    "Camo": ["camoGreen-v1", "camoGreen-v1_5", "camoGreen-v2", "camoCobalt", "camoUrban"],
    "WhatsApp": ["whatsappDark", "whatsappGreen-v1", "whatsappGreen-v2", "whatsappLight-v3"],
    "The Shining": ["The_Shining", "The_Shining-v1", "The_Shining-v2"],
    "Sandy Symphony": ["sandySymphony-v1", "sandySymphony-v2"],
    "Dark": ["dark"],
    "Light": ["light"],
    "Dracula": ["dracula"],
    "Solarized Darkish": ["solarizedDarkish"],
    "Joker": ["joker"],
    "Mona Lisa": ["monaLisa"],
    "Aurora Sunset": ["auroraSunset"],
    "Binary": ["binary"],
    "Black Sand": ["blackSand"],
    "Blue": ["blue"],
    "Cyan": ["cyan"],
    "Purple": ["purple"],
    "Red": ["red"],
    "Yellow": ["yellow"],
    "Electric Blue": ["electricBlue"],
    "Dark Blue Gold": ["darkBlueGold"],
    "Dark Green": ["darkGreen"],
    "Double Trouble": ["doubleTrouble"],
    "Girly": ["girly"],
    "Hot Dog": ["hotdog"],
    "Good SimpleX": ["goodSimplex"],
    "Simplex Default": ["simplexDefault"],
    "Session Dark": ["sessionDark"],
    "Lazy Sunday": ["lazySunday"],
    "Leaves": ["leaves"],
    "Bat Phone": ["batPhone"],
    "Banana Split": ["bananaSplit"],
    "Bad Witch Lite": ["badWitchLite"],
    "Cassini Midnight": ["cassiniMidnight"],
    "Cat": ["cat"],
    "GR8est MNSTRS": ["GR8estMNSTRS"],
    "IT Slate": ["IT_Slate"],
    "Japane Sea": ["japaneSea"],
    "Lobster": ["lobster"],
    "Mocca": ["mocca"],
    "Moss Noir": ["mossNoir"],
    "No AMOLED": ["noAMOLED"],
    "Pink Panther": ["pinkPanther"],
    "Psychedelick": ["psychedeRick"],
    "Radical Squadron": ["RadicalSquadron-Razor"],
    "Ralph Wrecks SimpleX": ["RalphWrecksSimpleX"],
    "Random": ["random"],
    "Sage Dust": ["Sage-Dust"],
    "Smurf": ["smurf"],
    "Soft Twilight": ["Soft_Twilight_1.0"],
    "Totoro-ify": ["Totoro-ify"],
    "W I D E": ["W_I_D_E"],
    "2024 XMR SimpleX": ["2024XMRSimpleX"],
    "3a Rule": ["3aRule"],
}

headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json", "Accept": "application/vnd.github+json"}

# Get existing
resp = requests.post(API_URL, headers=headers, json={
    "query": """{repository(owner:"oSoWoSo",name:"SimpleX-Themes"){discussions(first:100){nodes{number title}}}}"""
})
existing = [d["title"] for d in resp.json()["data"]["repository"]["discussions"]["nodes"]]
print(f"Existing: {len(existing)}")

for family, variants in FAMILIES.items():
    title = f"[Theme] {family}"
    if title in existing:
        print(f"Exists: {title}")
        continue
    body = f"Theme discussion for **{family}** family.\n\nVariants:\n" + "\n".join([f"- SxC_{v}.theme" for v in variants])
    
    query = """mutation CreateDiscussion($input: CreateDiscussionInput!) {createDiscussion(input: $input){discussion{number title}}}"""
    variables = {"input": {"repositoryId": REPO_ID, "categoryId": CAT_ID, "title": title, "body": body}}
    
    r = requests.post(API_URL, headers=headers, json={"query": query, "variables": variables})
    data = r.json()
    if "errors" in data:
        print(f"Error: {title}")
    elif data.get("data", {}).get("createDiscussion"):
        print(f"Created: {title} (#{data['data']['createDiscussion']['discussion']['number']})")
    else:
        print(f"Failed: {title}")
    time.sleep(1)

print(f"\nTotal: {len(FAMILIES)} families")