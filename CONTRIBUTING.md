# Contributing to SimpleX Themes

Thank you for your interest in contributing a theme! This guide will help you add a new theme to the repository.

## Ways to Contribute

### 1. GitHub Pull Request (Recommended)

1. Fork the repository
2. Create a new branch: `git checkout -b add-theme-name`
3. Add your theme file to `themes/` directory
4. Add 4 screenshots to `screenshots/` directory
5. Generate the index.md file using the automation script
6. Update README.md to include your theme
7. Submit a pull request

### 2. Send a Patch by Email

See [git-send-email.io](https://git-send-email.io/) for instructions.

### 3. Manual Upload

1. Create your theme in the SimpleX Chat app
2. Export your theme to a file
3. Join the SimpleX Themes group and upload your theme

## Theme File Requirements

### Naming Convention

Theme files should follow this pattern:
- `SxC_themeName.theme` (e.g., `SxC_myTheme.theme`)
- Use underscores instead of spaces
- Maximum length: 50 characters for the theme name

### Theme File Format

```yaml
base: "BLACK"  # or "WHITE"
colors:
  accent: "#ffa698b4"
  accentVariant: "#ff584858"
  secondary: "#ffecece1"
  secondaryVariant: "#ff9c6e9c"
  background: "#ff180818"
  menus: "#ff281028"
  title: "#ff807088"
  accentVariant2: "#ff98a8a8"
  sentMessage: "#e5503858"
  sentReply: "#ff281028"
  receivedMessage: "#e287758b"
  receivedReply: "#ff3e293e"
wallpaper:
  scale: 1.0
  scaleType: "fill"
  background: "#ff070707"
  tint: "#00ffffff"
```

## Automating Theme Addition

We've created a script to help automate adding new themes:

```bash
python3 scripts/add_theme.py themes/SxC_yourTheme.theme
```

This script will:
- Validate your theme file format
- Generate the `resources/SxC_yourTheme_index.md` file
- Provide instructions for the next steps

### Screenshot Requirements

Each theme needs 4 screenshots (JPG format, 120px width in the index):

**Naming patterns supported:**
- `SxC_themeName01.jpg`, `SxC_themeName02.jpg`, etc.
- `SxC_themeName-v101.jpg`, `SxC_themeName-v102.jpg`, etc.

### Taking Screenshots

To take screenshots for your theme:

1. **Android Emulator**: Use the built-in screen recording or take screenshots
2. **Physical Device**: Use your device's screenshot functionality
3. **SimpleX Chat**: Navigate through the app to capture all color variations

## Theme Validation

When you submit a pull request, our GitHub Actions workflow will automatically:

- Validate that theme files have the required `base:` field
- Check for required color fields
- Verify that screenshots exist for new themes

## Need Help?

- Join the [SimpleX Themes group](https://simplex.chat/contact#/?v=2-7&smp=smp%3A%2F%2Fhpq7_4gGJiilmz5Rf-CswuU5kZGkm_zOIooSw6yALRg%3D%40smp5.simplex.im%2FjwFqICow91mcVNxBF2GXXF5Uq4H27goC%23%2F%3Fv%3D1-3%26dh%3DMCowBQYDK2VuAyEAOYs_RwIB67iDC_ORPmBpp-oED4Ric3oYkID4kdkMdGs%253D%26srv%3Djjbyvoemxysm7qxap7m5d5m35jzv5qq6gnlv7s4rsn7tdwwmuqciwpid.onion&data=%7B%22type%22%3A%22group%22%2C%22groupLinkId%22%3A%22jpatHRdLkjwNmbWBc-VWcg%3D%3D%22%7D) for support
- Open an issue on GitHub if you encounter problems
