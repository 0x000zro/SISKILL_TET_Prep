#!/usr/bin/env python3
"""
SISKILL Content OTA Version Sync Utility
Automates incrementing the pedagogy content version in master_manifest.json
so that installed Android apps detect and download new content via GitHubContentSyncService.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

MASTER_MANIFEST_PATH = Path("app/src/main/assets/bundled_content/master_manifest.json")
BRAND_CONFIG_PATH = Path("app/src/main/assets/bundled_content/brand_config.json")

def bump_semver(version: str) -> str:
    parts = version.split(".")
    if len(parts) == 3 and all(p.isdigit() for p in parts):
        major, minor, patch = map(int, parts)
        return f"{major}.{minor}.{patch + 1}"
    return f"{version}.1"

def main():
    parser = argparse.ArgumentParser(description="Bump SISKILL content version for Over-The-Air GitHub sync.")
    parser.add_argument("--version", type=str, help="Specify exact new version (e.g., 1.0.1)")
    parser.add_argument("--push", action="store_true", help="Automatically commit and push version bump to GitHub")
    parser.add_argument("--message", type=str, default="", help="Optional commit message description")
    args = parser.parse_args()

    if not MASTER_MANIFEST_PATH.exists():
        print(f"[-] Error: {MASTER_MANIFEST_PATH} not found.")
        sys.exit(1)

    with open(MASTER_MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    current_version = data.get("version", "1.0.0")
    new_version = args.version if args.version else bump_semver(current_version)

    print(f"[*] Current content version : {current_version}")
    print(f"[+] Bumping to version      : {new_version}")

    data["version"] = new_version
    with open(MASTER_MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[✓] Updated {MASTER_MANIFEST_PATH}")

    # Also sync brand config if needed
    if BRAND_CONFIG_PATH.exists():
        with open(BRAND_CONFIG_PATH, "r", encoding="utf-8") as f:
            brand = json.load(f)
        brand["content_version"] = new_version
        with open(BRAND_CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(brand, f, ensure_ascii=False, indent=2)
        print(f"[✓] Updated {BRAND_CONFIG_PATH}")

    if args.push:
        commit_msg = args.message if args.message else f"Content OTA bump: v{new_version}"
        print(f"\n[*] Committing and pushing version v{new_version} to GitHub...")
        subprocess.run(["git", "add", str(MASTER_MANIFEST_PATH), str(BRAND_CONFIG_PATH)], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print(f"\n[✓] Deployed v{new_version} to GitHub! Mobile apps will now pull this update.")
    else:
        print("\n[*] To publish to GitHub, run:")
        print(f"    git add {MASTER_MANIFEST_PATH}")
        print(f"    git commit -m \"Content OTA bump: v{new_version}\"")
        print("    git push origin main")

if __name__ == "__main__":
    main()
