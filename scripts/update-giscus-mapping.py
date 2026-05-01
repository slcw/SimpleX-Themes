#!/usr/bin/env python3
"""Update giscus front matter to use family IDs."""
import os
import re

# Mapping from filename to family giscus ID
FAMILY_MAP = {
    # Nightshade family
    "SxC_Nightshade": "nightshade",
    "SxC_Nightshade-v1": "nightshade",
    "SxC_Nightshade-v1_5": "nightshade",
    "SxC_Nightshade-v2": "nightshade",
    "SxC_Nightshade-v2_1": "nightshade",
    "SxC_Nightshade-v2_2": "nightshade",
    "SxC_Nightshade-v2_3": "nightshade",
    "SxC_NightshadeTransparent-v1_5": "nightshade",
    "SxC_NightshadeTransparent-v2": "nightshade",
    "SxC_nightswatch-v2": "nightshade",
    "SxC_nightswatch-v3": "nightshade",
    # AMOLED
    "SxC_AMOLEDblack-v1": "amoled-black",
    "SxC_AMOLEDblackV2": "amoled-black",
    # Catppuccin
    "SxC_catppuccinMocha-v1": "catppuccin",
    "SxC_catppuccinMocha-v2": "catppuccin",
    "SxC_catppuccinLatte": "catppuccin",
    "SxC_catppuccinFrappe": "catppuccin",
    "SxC_catppuccinMacchiato": "catppuccin",
    # Green
    "SxC_green-v1": "green",
    "SxC_green-v2": "green",
    "SxC_greenPlus-v1": "green",
    "SxC_greenPlus-v1_5": "green",
    "SxC_greenNight-v1": "green",
    # Dusk
    "SxC_dusk": "dusk",
    "SxC_dusk-v2": "dusk",
    # CPN
    "SxC_CPN_Hacking-v1": "cpn",
    "SxC_CPN_Hacking-v2": "cpn",
    "SxC_CPN_iMessage-v1": "cpn",
    "SxC_CPN_iMessage-v2": "cpn",
    "SxC_CPN_synthwave": "cpn",
    "SxC_CPN_vaporwave": "cpn",
    # Camo
    "SxC_camoGreen-v1": "camo",
    "SxC_camoGreen-v1_5": "camo",
    "SxC_camoGreen-v2": "camo",
    "SxC_camoCobalt": "camo",
    "SxC_camoUrban": "camo",
    # WhatsApp
    "SxC_whatsappDark": "whatsapp",
    "SxC_whatsappGreen-v1": "whatsapp",
    "SxC_whatsappGreen-v2": "whatsapp",
    "SxC_whatsappLight-v3": "whatsapp",
    # The Shining
    "SxC_The_Shining": "the-shining",
    "SxC_The_Shining-v1": "the-shining",
    "SxC_The_Shining-v2": "the-shining",
    # Sandy Symphony
    "SxC_sandySymphony-v1": "sandy-symphony",
    "SxC_sandySymphony-v2": "sandy-symphony",
    # Other themes
    "SxC_dark": "dark",
    "SxC_light": "light",
    "SxC_dracula": "dracula",
    "SxC_solarizedDarkish": "solarized-darkish",
    "SxC_joker": "joker",
    "SxC_monaLisa": "mona-lisa",
    "SxC_auroraSunset": "aurora-sunset",
    "SxC_binary": "binary",
    "SxC_blackSand": "black-sand",
    "SxC_blue": "blue",
    "SxC_cyan": "cyan",
    "SxC_purple": "purple",
    "SxC_red": "red",
    "SxC_yellow": "yellow",
    "SxC_electricBlue": "electric-blue",
    "SxC_darkBlueGold": "dark-blue-gold",
    "SxC_darkGreen": "dark-green",
    "SxC_doubleTrouble": "double-trouble",
    "SxC_girly": "girly",
    "SxC_hotdog": "hot-dog",
    "SxC_goodSimplex": "good-simplex",
    "SxC_simplexDefault": "simplex-default",
    "SxC_sessionDark": "session-dark",
    "SxC_lazySunday": "lazy-sunday",
    "SxC_leaves": "leaves",
    "SxC_batPhone": "bat-phone",
    "SxC_bananaSplit": "banana-split",
    "SxC_badWitchLite": "bad-witch-lite",
    "SxC_cassiniMidnight": "cassini-midnight",
    "SxC_cat": "cat",
    "SxC_GR8estMNSTRS": "gr8est-mnstrs",
    "SxC_IT_Slate": "it-slate",
    "SxC_japaneSea": "japane-sea",
    "SxC_lobster": "lobster",
    "SxC_mocca": "mocca",
    "SxC_mossNoir": "moss-noir",
    "SxC_noAMOLED": "no-amoled",
    "SxC_pinkPanther": "pink-panther",
    "SxC_psychedeRick": "psychedelick",
    "SxC_RadicalSquadron-Razor": "radical-squadron",
    "SxC_RalphWrecksSimpleX": "ralph-wrecks-simplex",
    "SxC_random": "random",
    "SxC_Sage-Dust": "sage-dust",
    "SxC_smurf": "smurf",
    "SxC_Soft_Twilight_1.0": "soft-twilight",
    "SxC_Totoro-ify": "totoro-ify",
    "SxC_W_I_D_E": "w-i-d-e",
    "SxC_2024XMRSimpleX": "2024-xmr-simplex",
    "SxC_3aRule": "3a-rule",
}

resources_dir = "/home/z/Projekty/SxC-themes/resources"

for filename in os.listdir(resources_dir):
    if not filename.endswith("_index.md"):
        continue
    
    # Extract theme key (remove _index.md)
    theme_key = filename.replace("_index.md", "")
    
    if theme_key not in FAMILY_MAP:
        print(f"Skipping (no mapping): {filename}")
        continue
    
    giscus_id = FAMILY_MAP[theme_key]
    filepath = os.path.join(resources_dir, filename)
    
    with open(filepath, "r") as f:
        content = f.read()
    
    # Check if already has giscus
    if "giscus:" in content:
        # Update existing giscus
        content = re.sub(r'^---\n.*?\ngiscus:.*?\n---', f'---\ngiscus: {giscus_id}\n---', content, flags=re.MULTILINE | re.DOTALL)
    else:
        # Add new giscus
        content = f"---\ngiscus: {giscus_id}\n---\n" + content
    
    with open(filepath, "w") as f:
        f.write(content)
    
    print(f"Updated: {filename} -> {giscus_id}")