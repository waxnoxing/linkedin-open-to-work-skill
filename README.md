# LinkedIn Open to Work Skill

Multi-engine LinkedIn profile search (Indonesia, Open to Work, individual only) → AMD registration JSON generator.

## Quick Start

```bash
# 1. Install dependencies (Python 3.11+, no external deps)
# All stdlib only: subprocess, json, re, random, pathlib, datetime

# 2. Generate N fresh LinkedIn profiles + AMD JSON
python3 scripts/amd_register_json.py 10 --domain ubsi.biz.id

# 3. ZIP results
python3 -c "
import zipfile, glob, os
src = '.'
zipf = '/tmp/linkedin-json.zip'
with zipfile.ZipFile(zipf, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in glob.glob(f'{src}/amd-register-*.json'):
        z.write(f, os.path.basename(f))
for f in glob.glob(f'{src}/amd-register-*.json'):
    os.remove(f)
print(zipf)
"

# 4. Send via Telegram (Hermes)
hermes send -t telegram "10 linkedin JSON MEDIA:/tmp/linkedin-json.zip"
```

## Directory Structure

```
linkedin-open-to-work-skill/
├── SKILL.md                    # Main skill documentation
├── scripts/
│   ├── search_li.py            # Multi-engine search (DDG, Yahoo, Bing, Brave)
│   ├── combo_unique.py         # Search + dedup + city-univ matching
│   └── amd_register_json.py    # AMD registration JSON generator
├── data/
│   ├── address.txt             # Indonesian addresses (pipe-delimited)
│   ├── cities_univ.json        # City → university mapping
│   ├── linkedin_cache.json     # Auto-generated search cache
│   └── sent_profiles.json      # Dedup tracking
└── amd-register-sugab-scripts/
    └── amd_register_json.py    # Standalone AMD JSON generator
```

## Search Engines (Fallback Chain)

1. **DuckDuckGo Lite** — most reliable on AWS IP
2. **Yahoo** — via curl
3. **Bing** — via curl
4. **Brave** — via curl

## Filter: Individual Only

- ❌ Companies (PT, CV, Group, Community)
- ❌ Recruiting/Hiring pages
- ❌ Job listing sites
- ✅ Individual profiles only

## City → University Matching

City from address → university in same city. 17+ Indonesian cities mapped.

## Email Format

`firstnamelastname@ubsi.biz.id` — lowercase, no dots, concatenated

## GPU Use Cases

10 templates, all "AI agent + school + grades" theme, English. Randomly assigned.

## Dedup

- `sent_profiles.json` — combo output tracking
- `sent_amd_profiles.json` — AMD JSON output tracking
- Both checked before output

## Integration with Hermes

When user asks for "N linkedin lengkap":
1. Run `amd_register_json.py N --domain <domain>`
2. ZIP results
3. `hermes send -t telegram "MEDIA:/tmp/file.zip"`

## License

MIT
