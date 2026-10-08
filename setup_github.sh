#!/usr/bin/env bash
# ==============================================================================
# SISKILL_TET_Prep - Automated GitHub Setup & Push Script
# ==============================================================================

set -e

REPO_NAME="SISKILL_TET_Prep"
DEFAULT_GITHUB_USER="0x000zro"

echo "=================================================="
echo "  SISKILL_TET_Prep: GitHub Setup & Push Helper"
echo "=================================================="

# Ensure Git is installed
if ! command -v git &> /dev/null; then
    echo "[-] Error: 'git' is not installed. Please run: pkg install git"
    exit 1
fi

# Move to the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[*] Working directory: $(pwd)"

# 1. Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "[+] Initializing new Git repository..."
    git init -b main
else
    echo "[*] Existing Git repository detected."
    # Ensure branch is main
    CURRENT_BRANCH="$(git branch --show-current 2>/dev/null || echo '')"
    if [ "$CURRENT_BRANCH" != "main" ] && [ -n "$CURRENT_BRANCH" ]; then
        git branch -M main
    fi
fi

# 2. Check / configure user name & email
GIT_NAME="$(git config user.name || echo '')"
GIT_EMAIL="$(git config user.email || echo '')"

if [ -z "$GIT_NAME" ]; then
    read -p "Enter your Git Name (default: $DEFAULT_GITHUB_USER): " INPUT_NAME
    GIT_NAME="${INPUT_NAME:-$DEFAULT_GITHUB_USER}"
    git config --global user.name "$GIT_NAME"
fi

if [ -z "$GIT_EMAIL" ] || [ "$GIT_EMAIL" = "your-email@example.com" ]; then
    read -p "Enter your GitHub email address: " INPUT_EMAIL
    if [ -n "$INPUT_EMAIL" ]; then
        git config --global user.email "$INPUT_EMAIL"
    fi
fi

echo "[*] Git User : $(git config user.name)"
echo "[*] Git Email: $(git config user.email)"

# 3. Configure Remote URL
REMOTE_URL="$(git remote get-url origin 2>/dev/null || echo '')"

if [ -z "$REMOTE_URL" ]; then
    echo ""
    echo "[?] GitHub Remote Options:"
    echo "    1) HTTPS: https://github.com/${DEFAULT_GITHUB_USER}/${REPO_NAME}.git (Recommended)"
    echo "    2) SSH  : git@github.com:${DEFAULT_GITHUB_USER}/${REPO_NAME}.git"
    echo "    3) Custom URL"
    read -p "Select option [1/2/3] (default: 1): " REMOTE_CHOICE

    case "$REMOTE_CHOICE" in
        2)
            REMOTE_URL="git@github.com:${DEFAULT_GITHUB_USER}/${REPO_NAME}.git"
            ;;
        3)
            read -p "Enter custom remote URL: " REMOTE_URL
            ;;
        *)
            REMOTE_URL="https://github.com/${DEFAULT_GITHUB_USER}/${REPO_NAME}.git"
            ;;
    esac

    git remote add origin "$REMOTE_URL"
    echo "[+] Added remote origin: $REMOTE_URL"
else
    echo "[*] Existing remote origin found: $REMOTE_URL"
fi

# 4. Check if GitHub CLI is available to create the repo if it doesn't exist
if command -v gh &> /dev/null && gh auth status &> /dev/null; then
    echo ""
    read -p "Create repository on GitHub using gh CLI? (y/N): " CREATE_GH
    if [[ "$CREATE_GH" =~ ^[Yy]$ ]]; then
        read -p "Make repository public? (Y/n): " IS_PUBLIC
        VISIBILITY="--public"
        if [[ "$IS_PUBLIC" =~ ^[Nn]$ ]]; then
            VISIBILITY="--private"
        fi
        echo "[+] Creating GitHub repository '${REPO_NAME}'..."
        gh repo create "${REPO_NAME}" $VISIBILITY --source=. --remote=origin || true
    fi
fi

# 5. Stage and Commit
echo ""
echo "[+] Staging files (respecting .gitignore)..."
git add .

if git diff --staged --quiet; then
    echo "[*] Working directory clean. Nothing new to commit."
else
    echo "[+] Committing files..."
    git commit -m "Initial commit: SISKILL_TET_Prep Android app and pedagogical framework"
fi

# 6. Push to GitHub
echo ""
echo "=================================================="
echo "  Ready to Push to GitHub"
echo "=================================================="
echo "Remote URL: $(git remote get-url origin)"
echo "Branch    : main"
echo ""

read -p "Proceed with 'git push -u origin main'? (Y/n): " CONFIRM_PUSH
if [[ ! "$CONFIRM_PUSH" =~ ^[Nn]$ ]]; then
    echo "[+] Pushing to GitHub..."
    git push -u origin main
    echo ""
    echo "=================================================="
    echo "  Successfully pushed SISKILL_TET_Prep to GitHub!"
    echo "=================================================="
else
    echo "[*] Push skipped. When ready, run:"
    echo "    git push -u origin main"
fi
