#!/usr/bin/env bash

set -Eeuo pipefail

REMOTE_USER="ubuntu"
REMOTE_HOST="195.148.23.192"
REMOTE_DIR="/home/ubuntu/website-backups"

SOURCE_DIR="/var/www/html"
SSH_KEY="/root/.ssh/backup_key"
LOG_FILE="/var/log/website-backup.log"

TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
BACKUP_DIR="$REMOTE_DIR/$TIMESTAMP"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

REMOTE="$REMOTE_USER@$REMOTE_HOST"

log "Starting backup: $TIMESTAMP"

ssh -i "$SSH_KEY" "$REMOTE" "mkdir -p '$BACKUP_DIR'"

rsync -rlptD \
    -e "ssh -i $SSH_KEY" \
    "$SOURCE_DIR/" \
    "$REMOTE:$BACKUP_DIR/"

ssh -i "$SSH_KEY" "$REMOTE" \
    "touch '$BACKUP_DIR/.backup-complete'"

ssh -i "$SSH_KEY" "$REMOTE" \
    "find '$REMOTE_DIR' -mindepth 2 -maxdepth 2 \
    -name '.backup-complete' -printf '%h\n' |
    sort -r | tail -n +3 |
    while IFS= read -r dir; do rm -rf -- \"\$dir\"; done"

log "SUCCESS: Backup completed: $TIMESTAMP"