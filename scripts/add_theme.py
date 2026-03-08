#!/usr/bin/env python3
"""
Script to automate adding a new theme to the SimpleX Themes repository.

This script:
1. Validates the theme file format
2. Generates the index.md file for the resources/ directory
3. Provides guidance on taking screenshots

Usage:
    python3 add_theme.py <theme_file.theme>
"""

import os
import sys
import re
from pathlib import Path


def extract_theme_name(theme_filename):
    """Extract theme name from filename."""
    # Remove .theme extension
    name = theme_filename.replace('.theme', '')
    # Remove SxC_ prefix if present
    if name.startswith('SxC_'):
        name = name[4:]
    # Replace underscores with spaces for display name
    display_name = name.replace('_', ' ')
    return name, display_name


def extract_theme_properties(theme_file_path):
    """Extract theme properties from theme file."""
    with open(theme_file_path, 'r') as f:
        content = f.read()
    
    # Extract colors and wallpaper properties
    properties = {}
    
    # Extract base
    base_match = re.search(r'base:\s*"([^"]+)"', content)
    if base_match:
        properties['base'] = base_match.group(1)
    
    # Extract colors
    colors = {}
    color_keys = ['accent', 'accentVariant', 'secondary', 'secondaryVariant', 
                 'background', 'menus', 'title', 'accentVariant2', 
                 'sentMessage', 'sentReply', 'receivedMessage', 'receivedReply']
    
    for key in color_keys:
        match = re.search(rf'{key}:\s*"([^"]+)"', content)
        if match:
            colors[key] = match.group(1)
    
    if colors:
        properties['colors'] = colors
    
    # Extract wallpaper
    wallpaper = {}
    wallpaper_keys = ['scale', 'scaleType', 'background', 'tint']
    
    for key in wallpaper_keys:
        match = re.search(rf'{key}:\s*"([^"]+)"', content)
        if match:
            wallpaper[key] = match.group(1)
        else:
            match = re.search(rf'{key}:\s*([0-9.]+)', content)
            if match:
                wallpaper[key] = match.group(1)
    
    if wallpaper:
        properties['wallpaper'] = wallpaper
    
    return properties


def generate_index_md(theme_filename, theme_properties):
    """Generate the index.md content for a theme."""
    name, display_name = extract_theme_name(theme_filename)
    
    # Build theme properties section
    props_text = []
    props_text.append('```')
    props_text.append(f'base: "{theme_properties.get("base", "Unknown")}"')
    
    if 'colors' in theme_properties:
        props_text.append('colors:')
        for key, value in theme_properties['colors'].items():
            props_text.append(f'  {key}: "{value}"')
    
    if 'wallpaper' in theme_properties:
        props_text.append('wallpaper:')
        for key, value in theme_properties['wallpaper'].items():
            props_text.append(f'  {key}: "{value}"')
    
    props_text.append('```')
    
    # Generate screenshot links
    screenshot_links = []
    for i in range(1, 5):
        screenshot_name = f"SxC_{name}{i:02d}.jpg"
        screenshot_links.append(f'<a href="../screenshots/{screenshot_name}" target="_blank">\n'
                               f'        <img src="../screenshots/{screenshot_name}" width="120">\n'
                               f'</a>')
    
    index_content = f"""![SxC Theme Archive Banner](../resources/SxC_themeBanner.png)

# {display_name}

* Download [{display_name}](../themes/{theme_filename})

{screenshot_links[0]}&nbsp;&nbsp;&nbsp;
{screenshot_links[1]}
<br>
{screenshot_links[2]}&nbsp;&nbsp;&nbsp;
{screenshot_links[3]}

----
### Theme Properties

{chr(10).join(props_text)}

* [Return Home](../)
"""
    return index_content, name


def validate_theme_file(theme_file_path):
    """Validate that the theme file exists and has correct format."""
    if not os.path.exists(theme_file_path):
        print(f"Error: Theme file '{theme_file_path}' does not exist.")
        return False
    
    if not theme_file_path.endswith('.theme'):
        print(f"Error: Theme file must have .theme extension.")
        return False
    
    # Check if file is valid YAML format (basic check)
    with open(theme_file_path, 'r') as f:
        content = f.read()
    
    if 'base:' not in content:
        print(f"Error: Theme file does not appear to be a valid theme file (missing 'base:' field).")
        return False
    
    return True


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    theme_file = sys.argv[1]
    
    # Get the repository root (parent of scripts directory)
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent
    
    # Validate theme file
    theme_file_path = theme_file
    if not os.path.isabs(theme_file):
        # Try relative to current dir first, then relative to repo root
        if os.path.exists(theme_file):
            theme_file_path = os.path.abspath(theme_file)
        else:
            theme_file_path = repo_root / theme_file
    
    if not validate_theme_file(theme_file_path):
        sys.exit(1)
    
    # Extract theme properties
    theme_properties = extract_theme_properties(theme_file_path)
    
    # Generate index.md
    index_content, theme_name = generate_index_md(os.path.basename(theme_file), theme_properties)
    
    # Save index.md to resources directory
    resources_dir = repo_root / 'resources'
    index_file = resources_dir / f'SxC_{theme_name}_index.md'
    
    with open(index_file, 'w') as f:
        f.write(index_content)
    
    print(f"Successfully generated: {index_file}")
    print()
    print("Next steps:")
    print(f"1. Add screenshots to screenshots/ directory:")
    print(f"   - SxC_{theme_name}01.jpg")
    print(f"   - SxC_{theme_name}02.jpg")
    print(f"   - SxC_{theme_name}03.jpg")
    print(f"   - SxC_{theme_name}04.jpg")
    print(f"2. Add the theme file to themes/ if not already there")
    print(f"3. Update README.md to include the new theme")
    print()
    print("To take screenshots, you can use:")
    print("- Android emulator with screen recording")
    print("- Screen capturing on device")
    print("- Ask in the SimpleX Chat theme group for automation tips")


if __name__ == '__main__':
    main()
