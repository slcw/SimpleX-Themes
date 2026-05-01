# Plán implementace Giscus + Popularity

## Shrnutí

Tento dokument popisuje kroky pro přidání Giscus podpory pro komentáře a hodnocení u každého tématu, plus systém popularity tracking.

---

## 1. GitHub konfigurace (vyžaduje tvou akci)

### 1.1 Zapni Discussions
1. Jdi na https://github.com/oSoWoSo/SimpleX-Themes/settings
2. V sekci "Features" zaškrtni "Discussions"

### 1.2 Nainstaluj Giscus
1. Jdi na https://giscus.app
2. Klikni "Install" a autorizuj pro repozitář

### 1.3 Vytvoř Discussions kategorii
1. V repozitáři jdi na Discussions
2. Edit categories → New category
3. Jméno: `Themes`
4. Slug: `themes`
5. Emoji: 🎨

### 1.4 Získej Giscus IDs
1. Jdi na https://giscus.app/config
2. Vyplň repo: `oSoWoSo/SimpleX-Themes`
3. Vyber kategorii "Themes"
4. Zkopíruj `data-repo-id` a `data-category-id`

### 1.5 Aktualizuj _config.yml
Přidej do `_config.yml`:
```yaml
giscus:
  repo_id: "R_kgDOG..."
  category: "Themes"
  category_id: "DIC_kwDOF..."
```

---

## 2. Vytvoř témata v Discussions

Pro každé téma vytvoř discussion:

```
Title: [Theme] Nightshade
Body:
# Nightshade

Theme discussion, reactions and popularity tracking.

Theme file: themes/SxC_Nightshade.theme
```

Zapiš si číslo discussion pro každé téma do `data/themes.json`.

---

## 3. Aktualizuj data/themes.json

Nahraď ukázkové údaje skutečnými čísly discussions:

```json
[
  {
    "id": "nightshade",
    "name": "Nightshade",
    "discussion": 1
  }
  // ... další témata
]
```

---

## 4. Spusť popularity workflow

1. Jdi na Actions → Generate popularity
2. Klikni "Run workflow"
3. Workflow stáhne reaction data z každé discussion
4. Vytvoří `data/popular.json`

---

## 5. Frontend integration

### 5.1 Giscus na stránce tématu
V layout souboru přidej:
```liquid
{% include giscus.html %}
```

A v front matter každého tématu:
```yaml
---
giscus: nightshade
---
```

### 5.2 Zobrazení popularity
Přidej sekci pro zobrazení like/heart/rocket/comment count na stránce tématu.

---

## 6. Cron aktualizace

Workflow běží každou hodinu a aktualizuje popularity data.

---

## Soubory k dispozici

Vytvořené soubory:
- `data/themes.json` - mapování témat na discussions
- `.github/workflows/popularity.yml` - GitHub Action
- `scripts/generate-popularity.js` - generátor popularity
- `_includes/giscus.html` - Giscus embed

---

## Další vylepšení (budoucí)

- Weekly rankings
- Recommendation engine
- "Theme of the week"
- User collections
- RSS feeds
- Popularity grafy