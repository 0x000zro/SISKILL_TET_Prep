import json
import os

MASTER_MANIFEST = "UPTET_CTET/Paper_1_and_2/master_manifest.json"
BRAND_CONFIG_FILE = "UPTET_CTET/Paper_1_and_2/brand_config.json"
SOCIAL_LINKS_FILE = "UPTET_CTET/Paper_1_and_2/social_links.json"

# 1. Update or Create brand_config.json
brand_info = {
    "brand_name": "SISKILL",
    "full_title": "SISKILL: Super Intelligence Skill",
    "tagline": "Super Intelligence Skill to Crack CTET & UPTET",
    "domain": "siskill.in",
    "website_url": "https://siskill.in",
    "support_email": "support@siskill.in",
    "android": {
        "package_name": "in.siskill.app",
        "app_name": "SISKILL Exam Prep",
        "deep_link_scheme": "https",
        "deep_link_host": "siskill.in"
    },
    "api_endpoints": {
        "content_base_url": "https://siskill.in/content/",
        "sync_manifest_url": "https://raw.githubusercontent.com/0x000zro/SISKILL_TET_Prep/main/UPTET_CTET/Paper_1_and_2/master_manifest.json",
        "github_mirror_fallback": "https://raw.githubusercontent.com/0x000zro/SISKILL_TET_Prep/main/"
    }
}

with open(BRAND_CONFIG_FILE, "w", encoding="utf-8") as f:
    json.dump(brand_info, f, ensure_ascii=False, indent=2)
print(f"[OK] Created Brand Configuration: {BRAND_CONFIG_FILE}")

# 2. Update master_manifest.json with SISKILL branding
if os.path.exists(MASTER_MANIFEST):
    with open(MASTER_MANIFEST, "r", encoding="utf-8") as f:
        master = json.load(f)

    master["brand"] = brand_info["brand_name"]
    master["tagline"] = brand_info["tagline"]
    master["official_domain"] = brand_info["domain"]
    master["support_email"] = brand_info["support_email"]
    master["package_name"] = brand_info["android"]["package_name"]

    with open(MASTER_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(master, f, ensure_ascii=False, indent=2)
    print(f"[OK] Updated {MASTER_MANIFEST} with SISKILL identity.")
else:
    print(f"[WARN] {MASTER_MANIFEST} not found. Skipping manifest patch.")

# 3. Create social_links.json adhering to social-links.schema.json
social_links = {
    "support_email": "support@siskill.in",
    "channels": [
        {
            "platform": "Website",
            "handle_name": "Official Portal",
            "url": "https://siskill.in",
            "is_official": True
        },
        {
            "platform": "Telegram",
            "handle_name": "SISKILL Official",
            "url": "https://t.me/siskill_official",
            "is_official": True
        },
        {
            "platform": "YouTube",
            "handle_name": "SISKILL Academy",
            "url": "https://youtube.com/@siskill",
            "is_official": True
        },
        {
            "platform": "WhatsApp",
            "handle_name": "SISKILL Alerts",
            "url": "https://whatsapp.com/channel/siskill",
            "is_official": True
        }
    ]
}

with open(SOCIAL_LINKS_FILE, "w", encoding="utf-8") as f:
    json.dump(social_links, f, ensure_ascii=False, indent=2)
print(f"[OK] Created Social & Support Links: {SOCIAL_LINKS_FILE}")

print("\nSISKILL.in integration completed successfully!")
