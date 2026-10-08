#!/usr/bin/env bash
# ==============================================================================
# SISKILL_TET_Prep - GitHub Sync Helper Script
# Usage:
#   bash git_sync.sh            # Complete 2-way sync (pull remote + push local)
#   bash git_sync.sh pull       # Pull latest updates from GitHub
#   bash git_sync.sh push "msg" # Commit and push local changes to GitHub
#   bash git_sync.sh status     # Check sync status with GitHub
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

BRANCH="main"
REMOTE="origin"

echo "=================================================="
echo "  SISKILL_TET_Prep — GitHub Sync Engine"
echo "=================================================="

# Verify git repository
if [ ! -d ".git" ]; then
    echo "[-] Error: Git repository not initialized. Run 'bash setup_github.sh' first."
    exit 1
fi

ACTION="${1:-sync}"
COMMIT_MSG="$2"

case "$ACTION" in
    status)
        echo "[*] Fetching latest refs from $REMOTE..."
        git fetch "$REMOTE" "$BRANCH" --quiet || true
        LOCAL_HASH=$(git rev-parse HEAD 2>/dev/null || echo "empty")
        REMOTE_HASH=$(git rev-parse "$REMOTE/$BRANCH" 2>/dev/null || echo "empty")

        echo ""
        echo "[*] Local Branch  : $BRANCH ($LOCAL_HASH)"
        echo "[*] Remote Branch : $REMOTE/$BRANCH ($REMOTE_HASH)"
        echo ""

        if [ "$LOCAL_HASH" = "$REMOTE_HASH" ]; then
            echo "[✓] Local and GitHub are in perfect sync!"
        else
            BEHIND=$(git rev-list --count HEAD.."$REMOTE/$BRANCH" 2>/dev/null || echo 0)
            AHEAD=$(git rev-list --count "$REMOTE/$BRANCH"..HEAD 2>/dev/null || echo 0)
            echo "[!] Status: Ahead by $AHEAD commit(s), Behind by $BEHIND commit(s)."
        fi

        echo ""
        git status -s
        ;;

    pull)
        echo "[+] Pulling latest changes from GitHub ($REMOTE/$BRANCH)..."
        git pull --rebase "$REMOTE" "$BRANCH"
        echo "[✓] Pull complete!"
        ;;

    push)
        if [ -z "$COMMIT_MSG" ]; then
            COMMIT_MSG="Sync update: $(date '+%Y-%m-%d %H:%M:%S')"
        fi

        echo "[+] Staging files..."
        git add .

        if git diff --staged --quiet; then
            echo "[*] No local changes to commit."
        else
            echo "[+] Committing changes: '$COMMIT_MSG'..."
            git commit -m "$COMMIT_MSG"
        fi

        echo "[+] Pushing to GitHub ($REMOTE/$BRANCH)..."
        git push -u "$REMOTE" "$BRANCH"
        echo "[✓] Successfully pushed to GitHub!"
        ;;

    sync|*)
        echo "[1/3] Pulling remote updates..."
        git pull --rebase "$REMOTE" "$BRANCH" || {
            echo "[!] Pull conflict or network issue. Proceeding with caution..."
        }

        echo "[2/3] Staging local modifications..."
        git add .

        if git diff --staged --quiet; then
            echo "[*] No new changes to commit."
        else
            if [ -z "$COMMIT_MSG" ]; then
                COMMIT_MSG="Content & sync update: $(date '+%Y-%m-%d %H:%M:%S')"
            fi
            echo "[+] Committing: '$COMMIT_MSG'..."
            git commit -m "$COMMIT_MSG"
        fi

        echo "[3/3] Pushing to GitHub ($REMOTE/$BRANCH)..."
        git push -u "$REMOTE" "$BRANCH"
        echo ""
        echo "=================================================="
        echo "  Sync Complete! Local repo & GitHub are in sync."
        echo "=================================================="
        ;;
esac
