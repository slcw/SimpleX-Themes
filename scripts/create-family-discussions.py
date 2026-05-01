#!/usr/bin/env python3
"""Group themes by family and create discussions."""
import subprocess
import time
import requests

TOKEN = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
REPO_ID = "R_kgDOMoOy9A"
CAT_ID = "DIC_kwDOMoOy9M4CvYxA"
API_URL = "https://api.github.com/graphql"

# Theme families - group by base name, versions together
THEME_FAMILIES = {
    # Nightshade family
    "Nightshade": ["Nightshade", "Nightshade Transparent", "Nightshade v1", "Nightshade v1.5", "Nightshade v2", "Nightshade v2.1", "Nightshade v2.2", "Nightshade v2.3", "Nightshade v3"],
    # AMOLED Black
    "AMOLED Black": ["AMOLED Black", "AMOLED Black v1", "AMOLED Black v2"],
    # Catppuccin family
    "Catppuccin": ["Catppuccin Mocha", "Catppuccin Latte", "Catppuccin Frappe", "Catppuccin Macchiato", "Catppuccin Mocha v1", "Catppuccin Mocha v2"],
    # Green family
    "Green": ["Green", "Green v1", "Green v2", "Green Plus", "Green Plus v1", "Green Plus v1.5", "Green Night", "Green Night v1"],
    # Dusk family  
    "Dusk": ["Dusk", "Dusk v2", "Dusk v3"],
    # CPN family
    "CPN": ["CPN Hacking", "CPN iMessage", "CPN Synthwave", "CPN Vaporwave"],
    # Camo family
    "Camo": ["Camo Green", "Camo Green v1", "Camo Green v1.5", "Camo Green v2", "Camo Cobalt", "Camo Urban"],
    # WhatsApp family
    "WhatsApp": ["WhatsApp Dark", "WhatsApp Green", "WhatsApp Green v1", "WhatsApp Green v2", "WhatsApp Light"],
    # The Shining
    "The Shining": ["The Shining", "The Shining v1", "The Shining v2"],
    # Sandy Symphony
    "Sandy Symphony": ["Sandy Symphony", "Sandy Symphony v1", "Sandy Symphony v2"],
    # CPN (without space)
    "CPN_": ["CPN Hacking v1", "CPN Hacking v2", "CPN iMessage v1", "CPN iMessage v2"],
    # Other unique themes - one per family
    "Dark": ["Dark"],
    "Light": ["Light"],
    "Dracula": ["Dracula"],
    "Joker": ["Joker"],
    "Mona Lisa": ["Mona Lisa"],
    "Aurora Sunset": ["Aurora Sunset"],
    "Solarized Darkish": ["Solarized Darkish"],
    "Binary": ["Binary"],
    "Black Sand": ["Black Sand"],
    "Blue": ["Blue"],
    "Cyan": ["Cyan"],
    "Purple": ["Purple"],
    "Red": ["Red"],
    "Yellow": ["Yellow"],
    "Electric Blue": ["Electric Blue"],
    "Dark Blue Gold": ["Dark Blue Gold"],
    "Dark Green": ["Dark Green"],
    "Double Trouble": ["Double Trouble"],
    "Girly": ["Girly"],
    "Green Night": ["Green Night"],
    "Hot Dog": ["Hot Dog"],
    "Good SimpleX": ["Good SimpleX"],
    "Simplex Default": ["Simplex Default"],
    "Session Dark": ["Session Dark"],
    "Lazy Sunday": ["Lazy Sunday"],
    "Leaves": ["Leaves"],  
    "Bat Phone": ["Bat Phone"],
    "Banana Split": ["Banana Split"],
    "Bad Witch Lite": ["Bad Witch Lite"],
    "Cassini Midnight": ["Cassini Midnight"],
    "Cat": ["Cat"],
    "GR8est MNSTRS": ["GR8est MNSTRS"],
    "IT Slate": ["IT Slate"],
    "Japane Sea": ["Japane Sea"],
    "Lobster": ["Lobster"],
    "Mocca": ["Mocca"],
    "Moss Noir": ["Moss Noir"],
    "No AMOLED": ["No AMOLED"],
    "Pink Panther": ["Pink Panther"],
    "Psychedelick": ["Psychedelick"],
    "Radical Squadron": ["Radical Squadron"],
    "Ralph Wrecks SimpleX": ["Ralph Wrecks SimpleX"],
    "Random": ["Random"],
    "Sage Dust": ["Sage Dust"],
    "Smurf": ["Smurf"],
    "Soft Twilight": ["Soft Twilight"],
    "Totoro-ify": ["Totoro-ify"],
    "W I D E": ["W I D E"],
    "2024 XMR SimpleX": ["2024 XMR SimpleX"],
    "3a Rule": ["3a Rule"],
}

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json"
}

# Check existing
resp = requests.post(API_URL, headers=headers, json={
    "query": """{repository(owner:"oSoWoSo",name:"SimpleX-Themes"){discussions(first:100){nodes{number title}}}}"""
})
existing = [d["title"] for d in resp.json()["data"]["repository"]["discussions"]["nodes"]]
print(f"Existing: {len(existing)} discussions")

# Create discussions for each family
for family, variants in THEME_FAMILIES.items():
    title = f"[Theme] {family}"
    
    if title in existing:
        print(f"Exists: {title}")
        continue
    
    body = f"Theme discussion for {family} and its variants.\n\n" + "\n".join([f"- {v}" for v in variants])
    
    query = """
    mutation CreateDiscussion($input: CreateDiscussionInput!) {
      createDiscussion(input: $input) {
        discussion {
          number
          title
        }
      }
    }
    """
    
    variables = {
        "input": {
            "repositoryId": REPO_ID,
            "categoryId": CAT_ID,
            "title": title,
            "body": body
        }
    }
    
    response = requests.post(API_URL, headers=headers, json={"query": query, "variables": variables})
    
    if response.status_code == 200:
        data = response.json()
        if "errors" in data:
            print(f"Error: {title} -> {data['errors']}")
        elif "data" in data and data.get("data", {}).get("createDiscussion"):
            num = data["data"]["createDiscussion"]["discussion"]["number"]
            print(f"Created: {title} (#{num})")
        else:
            print(f"Failed: {title}")
    else:
        print(f"HTTP Error: {title} -> {response.status_code}")
    
    time.sleep(1)

print(f"\nTotal families: {len(THEME_FAMILIES)}")