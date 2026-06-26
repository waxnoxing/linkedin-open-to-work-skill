#!/usr/bin/env python3
"""
combo_unique.py — Get fresh LinkedIn profiles (Open to Work, individual, Indonesia)

Usage:
  python3 combo_unique.py              # get 5 profiles
  python3 combo_unique.py [count]      # get N profiles
  python3 combo_unique.py 10 --force-search  # force fresh search first
  python3 combo_unique.py 5 --json     # JSON output for AMD pipeline
"""

import json, random, sys, re
from pathlib import Path
from datetime import datetime

SKILL_DIR = Path.home() / ".hermes/skills/social-media/linkedin-open-to-work"
SCRIPTS_DIR = SKILL_DIR / "scripts"
DATA_DIR = SKILL_DIR / "data"
ADDRESS_FILE = DATA_DIR / "address.txt"
CITIES_UNIV_FILE = DATA_DIR / "cities_univ.json"
GPU_USE_CASES_FILE = Path.home() / ".hermes/data/gpu_use_cases.json"
SENT_FILE = DATA_DIR / "sent_profiles.json"
AMD_SENT_FILE = Path.home() / ".hermes/skills/social-media/amd-register-sugab/data/sent_amd_profiles.json"

sys.path.insert(0, str(SCRIPTS_DIR))
from search_li import do_refresh, get_fresh_profiles, mark_sent, normalise_url, extract_name_from_url


def load_addresses():
    """Load address database."""
    if not ADDRESS_FILE.exists():
        return []
    addresses = []
    for line in open(ADDRESS_FILE):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split('|')
        if len(parts) >= 5:
            addresses.append({
                'address1': parts[0].strip(),
                'address2': parts[1].strip(),
                'city': parts[2].strip(),
                'province': parts[3].strip(),
                'zip': parts[4].strip(),
            })
    return addresses


def load_cities_univ():
    """Load city -> university mapping."""
    if not CITIES_UNIV_FILE.exists():
        return {}
    return json.load(open(CITIES_UNIV_FILE))


def load_gpu_use_cases():
    """Load GPU use case templates."""
    if not GPU_USE_CASES_FILE.exists():
        return [
            "I am learning AI agent development and need GPU access to complete my school projects and improve my grades.",
            "As a computer science student, I am building an AI agent for my final project and need GPU resources.",
            "I am studying artificial intelligence and working on a school assignment that requires GPU computing.",
            "I need GPU access for my university coursework in machine learning and deep learning.",
            "As a student learning AI development, I require GPU resources for my academic projects.",
            "I am a graduate student researching AI agents for my thesis and need GPU access.",
            "I am taking a course on artificial intelligence and need GPU access for assignments.",
            "As part of my computer science degree, I am developing an AI-powered application that needs GPU.",
            "I am learning about autonomous AI agents in my university program and need GPU resources.",
            "I need GPU resources for my academic projects in the AI field to improve my grades.",
        ]
    return json.load(open(GPU_USE_CASES_FILE))


def match_university(city, cities_univ):
    """Match city with university."""
    city_lower = city.lower()
    for key, unis in cities_univ.items():
        if key.lower() == city_lower:
            return random.choice(unis)
    # Fallback: Jakarta universities
    return random.choice(["Universitas Negeri Jakarta", "Universitas Mercu Buana", "Universitas Trisakti"])


def get_all_sent_urls():
    """Get all sent URLs from both LI and AMD trackers."""
    sent = set()
    for f in [SENT_FILE, AMD_SENT_FILE]:
        if f.exists():
            data = json.load(open(f))
            for p in data:
                url = p.get('url', '')
                if url:
                    sent.add(normalise_url(url))
                # Also track by name
                name = p.get('name', '')
                if name:
                    sent.add(name.lower().strip())
    return sent


def format_profile(profile, addresses, cities_univ, gpu_cases):
    """Format a single profile with address + university."""
    url = profile.get('url', '')
    name = profile.get('name', extract_name_from_url(url))

    # Pick random address
    if addresses:
        addr = random.choice(addresses)
        city = addr['city']
        address1 = addr['address1']
        address2 = addr['address2']
        province = addr['province']
        zipcode = addr['zip']
    else:
        city = 'Jakarta'
        address1 = 'Jl. Sudirman No. 1'
        address2 = ''
        province = 'DKI Jakarta'
        zipcode = '10220'

    university = match_university(city, cities_univ)
    gpu_case = random.choice(gpu_cases)

    # Build email: firstnamelastname@domain (lowercase, no dots)
    name_clean = re.sub(r'[^a-zA-Z]', '', name).lower()
    email = f"{name_clean}@ubsi.biz.id"

    return {
        'name': name,
        'first_name': name.split()[0] if name.split() else name,
        'last_name': ' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
        'url': url,
        'email': email,
        'city': city,
        'province': province,
        'address1': address1,
        'address2': address2,
        'zip': zipcode,
        'university': university,
        'gpu_case': gpu_case,
        'phone': f"628{random.randint(100000000, 999999999)}",
    }


def print_profile(p):
    """Print profile in label:value format."""
    print(f"Name       : {p['name']}")
    print(f"LinkedIn   : {p['url']}")
    print(f"Email      : {p['email']}")
    print(f"City       : {p['city']}")
    print(f"Province   : {p['province']}")
    print(f"University : {p['university']}")
    print(f"Address 1  : {p['address1']}")
    print(f"Address 2  : {p['address2']}")
    print(f"Zip        : {p['zip']}")
    print(f"Phone      : {p['phone']}")
    print(f"Alasan     : {p['gpu_case']}")
    print()


def main():
    args = sys.argv[1:]
    count = 5
    force_search = '--force-search' in args
    json_output = '--json' in args
    amd_json = '--amd-json' in args or '--json-send' in args
    domain = 'ubsi.biz.id'
    password = 'PasswordKuat!1'
    is_send = '--json-send' in args

    # Parse count
    for a in args:
        if a.isdigit():
            count = int(a)
            break

    if '--count' in args:
        try:
            idx = args.index('--count')
            count = int(args[idx + 1])
        except:
            pass

    # Parse domain
    if '--domain' in args:
        try:
            idx = args.index('--domain')
            domain = args[idx + 1]
        except:
            pass

    # Always search fresh — no stock/cache-first
    print(f"[combo_unique] Searching fresh profiles...")
    do_refresh(target_count=max(count * 3, 30))

    # Get fresh profiles (exclude already sent)
    profiles = get_fresh_profiles(count=count, exclude_sent=True)

    if not profiles:
        print("[combo_unique] Still no fresh profiles found.")
        sys.exit(1)

    # Load data
    addresses = load_addresses()
    cities_univ = load_cities_univ()
    gpu_cases = load_gpu_use_cases()

    # Format
    results = []
    for profile in profiles[:count]:
        p = format_profile(profile, addresses, cities_univ, gpu_cases)
        results.append(p)

    # Output
    if json_output:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif amd_json:
        # Generate AMD JSON files
        amd_dir = Path.home() / ".hermes/skills/social-media/amd-register-sugab"
        for i, p in enumerate(results, 1):
            safe_name = re.sub(r'[^a-zA-Z0-9]', '_', p['name'])
            filename = f"amd-register-{safe_name}.json"
            
            amd_json_data = {
                "profiles": [{
                    "name": "AMD Create Account",
                    "urlPattern": "amd.com",
                    "inputs": [
                        {"key": "location", "label": "Location / Country"},
                        {"key": "jobFunction", "label": "Job Function"},
                        {"key": "productNeeded", "label": "Product Needed"},
                        {"key": "affiliationType", "label": "Affiliation Type"},
                        {"key": "howToUse", "label": "How do you plan to use", "default": p['gpu_case']}
                    ],
                    "steps": [
                        {
                            "name": "Langkah 1 – Buat Akun",
                            "fields": [
                                {"label": "First Name", "value": p['first_name']},
                                {"label": "Last Name", "value": p['last_name']},
                                {"label": "E-mail", "value": p['email']},
                                {"label": "Preferred Language", "value": "English"},
                            ]
                        },
                        {
                            "name": "Langkah 2 – Aktivasi (pakai Access Token)",
                            "fields": [
                                {"label": "Access Token", "value": "[[token]]"},
                                {"label": "Password", "value": password},
                                {"label": "Confirm Password", "value": password},
                            ]
                        },
                        {
                            "name": "Langkah 3 – Lengkapi Profil",
                            "fields": [
                                {"label": "First Name", "value": p['first_name']},
                                {"label": "Last Name", "value": p['last_name']},
                                {"label": "E-mail", "value": p['email']},
                                {"label": "Company Name", "value": p['university']},
                                {"label": "Address 1", "value": p['address1']},
                                {"label": "Address 2", "value": p['address2']},
                                {"label": "Location / Country", "value": "Indonesia"},
                                {"label": "City", "value": p['city']},
                                {"label": "State/Province", "value": p['province']},
                                {"label": "Postal Code", "value": p['zip']},
                                {"label": "Phone", "value": p['phone']},
                                {"label": "Job Function", "value": "Student"},
                                {"label": "Product Needed", "value": "AMD Dev Cloud"},
                                {"label": "Affiliation Type", "value": "Student"},
                                {"label": "How do you plan to use", "value": p['gpu_case']},
                                {"label": "Profile 1", "value": p['url']},
                            ]
                        }
                    ]
                }]
            }
            
            with open(amd_dir / filename, 'w') as f:
                json.dump(amd_json_data, f, indent=2, ensure_ascii=False)
            print(f"Generated: {filename} ({p['name']})")
        
        # Update AMD sent tracking
        amd_sent_file = amd_dir / "data" / "sent_amd_profiles.json"
        amd_sent = []
        if amd_sent_file.exists():
            amd_sent = json.load(open(amd_sent_file))
        for p in results:
            amd_sent.append({
                'name': p['name'],
                'url': p['url'],
                'sent_at': datetime.now().isoformat()
            })
        amd_sent_file.parent.mkdir(parents=True, exist_ok=True)
        json.dump(amd_sent, open(amd_sent_file, 'w'), indent=2)
        
        print(f"\n[combo_unique] {len(results)} AMD JSON files generated.")

    else:
        for p in results:
            print_profile(p)

    # Mark sent
    mark_sent([{'name': p['name'], 'url': p['url']} for p in results])
    if not is_send:
        print(f"[combo_unique] Sent {len(results)} profiles, marked as used.")


if __name__ == '__main__':
    main()
