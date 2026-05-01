#!/usr/bin/env python3
import json
import os
import subprocess
import time
import requests

TOKEN = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
REPO_ID = "R_kgDOMoOy9A"
CAT_ID = "DIC_kwDOMoOy9M4CvYxA"
API_URL = "https://api.github.com/graphql"

THEMES = {
    "nightshade": "Nightshade",
    "nightshade-v2": "Nightshade v2",
    "nightshade-v2_1": "Nightshade v2.1",
    "nightshade-v2_2": "Nightshade v2.2", 
    "nightshade-v2_3": "Nightshade v2.3",
    "amoled-black": "AMOLED Black",
    "amoled-black-v2": "AMOLED Black v2",
    "catppuccin-mocha-v2": "Catppuccin Mocha v2",
    "catppuccin-latte": "Catppuccin Latte",
    "catppuccin-frappe": "Catppuccin Frappe",
    "catppuccin-macchiato": "Catppuccin Macchiato",
    "green-v2": "Green v2",
    "green-plus-v1": "Green Plus v1",
    "green-plus-v1_5": "Green Plus v1.5",
    "green-night-v1": "Green Night v1",
    "dusk": "Dusk",
    "dusk-v2": "Dusk v2",
    "dark": "Dark",
    "light": "Light",
    "dracula": "Dracula",
    "solarized-darkish": "Solarized Darkish",
    "joker": "Joker",
    "mona-lisa": "Mona Lisa",
    "aurora-sunset": "Aurora Sunset",
}

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json"
}

# Check existing discussions
resp = requests.post(API_URL, headers=headers, json={
    "query": """{repository(owner:"oSoWoSo",name:"SimpleX-Themes"){discussions(first:100){nodes{number title}}}}"""
})
existing = [d["title"] for d in resp.json()["data"]["repository"]["discussions"]["nodes"]]
print(f"Existing discussions: {len(existing)}")

for shortname, fullname in THEMES.items():
    title = f"[Theme] {fullname}"
    
    if title in existing:
        print(f"Skipping: {title} (exists)")
        continue
    
    body = f"Theme discussion, reactions and popularity tracking.\n\nTheme file: themes/SxC_{shortname}.theme"
    
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