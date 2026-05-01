#!/usr/bin/env python3
"""Add giscus front matter to resource files."""
import os
import re

# Mapping from file pattern to giscus ID
THEME_MAP = {
    "SxC_Nightshade": "nightshade",
    "SxC_Nightshade-v2": "nightshade-v2",
    "SxC_Nightshade-v2_1": "nightshade-v2_1",
    "SxC_Nightshade-v2_2": "nightshade-v2_2",
    "SxC_Nightshade-v2_3": "nightshade-v2_3",
    "SxC_AMOLEDblack-v1": "amoled-black",
    "SxC_AMOLEDblackV2": "amoled-black-v2",
    "SxC_catppuccinMocha-v2": "catppuccin-mocha-v2",
    "SxC_catppuccinLatte": "catppuccin-latte",
    "SxC_catppuccinFrappe": "catppuccin-frappe",
    "SxC_catppuccinMacchiato": "catppuccin-macchiato",
    "SxC_green-v2": "green-v2",
    "SxC_greenPlus-v1": "green-plus-v1",
    "SxC_greenPlus-v1_5": "green-plus-v1_5",
    "SxC_greenNight-v1": "green-night-v1",
    "SxC_dusk": "dusk",
    "SxC_dusk-v2": "dusk-v2",
    "SxC_dark": "dark",
    "SxC_light": "light",
    "SxC_dracula": "dracula",
    "SxC_solarizedDarkish": "solarized-darkish",
    "SxC_joker": "joker",
    "SxC_monaLisa": "mona-lisa",
    "SxC_auroraSunset": "aurora-sunset",
}

resources_dir = "/home/z/Projekty/SxC-themes/resources"

for filename in os.listdir(resources_dir):
    if not filename.endswith("_index.md"):
        continue
    
    # Extract theme key from filename
    theme_key = filename.replace("_index.md", "")
    
    if theme_key not in THEME_MAP:
        print(f"Skipping (no mapping): {filename}")
        continue
    
    giscus_id = THEME_MAP[theme_key]
    filepath = os.path.join(resources_dir, filename)
    
    with open(filepath, "r") as f:
        content = f.read()
    
    # Check if already has giscus
    if "---" in content and content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            front_matter = parts[1]
            if "giscus:" in front_matter:
                print(f"Skipping (has giscus): {filename}")
                continue
            # Add giscus to existing front matter
            new_front = front_matter.rstrip() + f"\ngiscus: {giscus_id}\n"
            content = parts[0] + "---" + new_front + "---" + parts[2]
        else:
            # No front matter, create new
            content = f"---\ngiscus: {giscus_id}\n---\n" + content
    else:
        content = f"---\ngiscus: {giscus_id}\n---\n" + content
    
    with open(filepath, "w") as f:
        f.write(content)
    
    print(f"Added giscus: {filename} -> {giscus_id}")