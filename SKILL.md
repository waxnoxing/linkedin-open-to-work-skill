---
name: linkedin-open-to-work
description: "Fresh-on-demand LinkedIn profile search (Indonesia, Open to Work, individual only). Multi-engine search + 5-layer company filter + city-univ matching + AMD JSON pipeline."
---

# LinkedIn Open to Work — Fresh Search (Indonesia, Individual Only)

Setiap diminta, search **langsung fresh** dari search engines. Tidak pakai cache lama.

## ⚡ Quick Action (Default)

Ketika user minta "N linkedin lengkap" → execute immediately (see `references/workflow-fresh-search.md`):

```bash
python3 ~/.hermes/skills/social-media/amd-register-sugab/scripts/amd_register_json.py N --domain ubsi.biz.id
```
Then ZIP + `hermes send -t telegram "MEDIA:/tmp/linkedin-N.zip"`

**Default:** domain `ubsi.biz.id`, individual only, fresh search, no confirmation needed.

## Cara Pakai

### Search + Get Profiles
```bash
python3 ~/.hermes/skills/social-media/linkedin-open-to-work/scripts/combo_unique.py 10
python3 ~/.hermes/skills/social-media/linkedin-open-to-work/scripts/combo_unique.py 10 --force-search
python3 ~/.hermes/skills/social-media/linkedin-open-to-work/scripts/combo_unique.py 5 --json
```

### AMD Registration JSON
```bash
python3 ~/.hermes/skills/social-media/amd-register-sugab/scripts/amd_register_json.py N --domain ubsi.biz.id
```

### Manual Search Refresh
```bash
python3 ~/.hermes/skills/social-media/linkedin-open-to-work/scripts/search_li.py --refresh --count 50
```

## Filter: Individual Only (5-Layer)

1. **Query-level**: `-company -pt -cv -perusahaan` di semua query
2. **Slug pattern**: reject single-word, starts/ends with company suffix (ltd, inc, corp, group, tbk, pt, cv)
3. **Extracted name check**: 60+ keywords (hotel, restaurant, consulting, agency, bank, insurance, trading, farming, etc.)
4. **Word count**: reject 1-word names (<15 char) or 5+ word names
5. **Generic slugs**: open-to-work, welcome, jobs, career

## City → University Matching

| City | Universities |
|------|-------------|
| Jakarta | UNJ, Mercu Buana, Trisakti, Nasional, Terbuka, BINUS |
| Depok | UI, Gunadarma, BSI |
| Bandung | ITB, UNPAD, UPI, Parahyangan |
| Surabaya | UNAIR, ITS, Ubaya, Petra |
| Yogyakarta | UGM, UMY, UNY, UII |
| Semarang | UNDIP, Unnes, Dian Nuswantoro |
| Malang | UB, UNM, UMM |
| Medan | USU, Unimed, UMSU |
| Lhokseumawe | UNIMAL |

## Email Format
`firstnamelastname@ubsi.biz.id` — lowercase, no dots, concatenated

## Data Files
```
~/.hermes/skills/social-media/linkedin-open-to-work/
├── scripts/
│   ├── search_li.py        # multi-engine search
│   └── combo_unique.py     # search + dedup + format
├── data/
│   ├── address.txt         # Indonesian addresses
│   ├── cities_univ.json    # city → university mapping
│   ├── linkedin_cache.json # auto-generated
│   └── sent_profiles.json  # auto-generated
└── references/
    └── workflow-fresh-search.md

~/.hermes/skills/social-media/amd-register-sugab/
├── scripts/
│   └── amd_register_json.py
└── data/
    └── sent_amd_profiles.json
```

## Dedup
- `sent_profiles.json` — combo output tracking
- `sent_amd_profiles.json` — AMD JSON output tracking

## Search Engines (fallback)
1. DuckDuckGo Lite (most reliable on AWS IP)
2. Yahoo
3. Bing
4. Brave
