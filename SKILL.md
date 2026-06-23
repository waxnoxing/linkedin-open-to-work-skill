# LinkedIn Open to Work — Fresh Search (Indonesia, Individual Only)

Setiap diminta, search **langsung fresh** dari search engines. Tidak pakai cache lama.

## Cara Pakai

### Search + Get Profiles
```bash
# Search fresh + get profiles
python3 ~/.hermes/skills/social-media/linkedin-open-to-work/scripts/combo_unique.py 10

# Search fresh terus (skip cache)
python3 ~/.hermes/skills/social-media/linkedin-open-to-work/scripts/combo_unique.py 10 --force-search

# JSON output (buat AMD pipeline)
python3 ~/.hermes/skills/social-media/linkedin-open-to-work/scripts/combo_unique.py 5 --json

---

## ⚡ Quick Action (Default)

Ketika user minta "N linkedin lengkap":

1. Search fresh + generate JSON:
```bash
python3 ~/.hermes/skills/social-media/amd-register-sugab/scripts/amd_register_json.py N --domain ubsi.biz.id
```
2. ZIP + kirim file:
```bash
python3 -c "
import zipfile, glob, os
src = '$HOME/.hermes/skills/social-media/amd-register-sugab'
zipf = '/tmp/linkedin-N.zip'
with zipfile.ZipFile(zipf, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in glob.glob(f'{src}/amd-register-*.json'):
        z.write(f, os.path.basename(f))
for f in glob.glob(f'{src}/amd-register-*.json'):
    os.remove(f)
print(zipf)
"
```
3. `hermes send -t telegram "N linkedin JSON MEDIA:/tmp/linkedin-N.zip"`

**Default:** domain `ubsi.biz.id`, individual only, fresh search.
```

### AMD Registration JSON
```bash
# Generate 1 JSON
python3 ~/.hermes/skills/social-media/amd-register-sugab/scripts/amd_register_json.py

# Generate N JSON
python3 ~/.hermes/skills/social-media/amd-register-sugab/scripts/amd_register_json.py 5

# Custom domain + password
python3 ~/.hermes/skills/social-media/amd-register-sugab/scripts/amd_register_json.py 3 --domain ubsi.biz.id --password "MyPass!1"
```

### Manual Search Refresh
```bash
python3 ~/.hermes/skills/social-media/linkedin-open-to-work/scripts/search_li.py --refresh --count 50
```

## Filter: Individual Only

- ❌ Perusahaan (PT, CV, Group, Community)
- ❌ Recruiting/Hiring pages
- ❌ Job listing sites (Jobstreet, Kalibrr, Glints)
- ✅ Individual profiles only

Query pool otomatis exclude kata kunci perusahaan.

## City → University Matching

City dari address → universitas di kota yang sama.

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

## Output Format

```
Name       : Andi Bulan Rahma Nabila
LinkedIn   : https://www.linkedin.com/in/andi-bulan-rahma-nabila-5a5926298
Email      : andibulanrahmanabila@sugabdemy.app
City       : Depok
Province   : Jawa Barat
University : Universitas Gunadaram
Address 1  : Jl. Raya Bogor Km. 30
Address 2  : Depok
Zip        : 16518
Phone      : 628477428449
Alasan     : As a student learning AI development...
```

## Email Format
`firstnamelastname@ubsi.biz.id` — lowercase, no dots, concatenated

## Data Files
```
~/.hermes/skills/social-media/linkedin-open-to-work/
├── scripts/
│   ├── search_li.py        # multi-engine search
│   └── combo_unique.py     # search + dedup + format
└── data/
    ├── address.txt         # Indonesian addresses
    ├── cities_univ.json    # city → university mapping
    ├── linkedin_cache.json # auto-generated
    └── sent_profiles.json  # auto-generated

~/.hermes/skills/social-media/amd-register-sugab/
├── scripts/
│   └── amd_register_json.py
└── data/
    └── sent_amd_profiles.json
```

## Dedup
- `sent_profiles.json` — pernah dikirim via combo
- `sent_amd_profiles.json` — pernah dikirim via AMD JSON
- Keduanya di-check sebelum output

## Search Engines (fallback)
1. DuckDuckGO Lite (most reliable on AWS IP)
2. Yahoo
3. Bing
4. Brave
