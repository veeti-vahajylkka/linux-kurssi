# Server Infrastructure

This repository contains configuration and application files for a two-server infrastructure setup.

## Servers

| Server | IP address | Role |
|---|---|---|
| Server A | 195.148.20.90 | Primary server |
| Server B | 195.148.23.192 | Backup server and MySQL replica |

## Website backups

- Backup script: `backups/backup-website.sh`
- Schedule: Every hour, at minute 0.
- Cron configuration: `backups/root-crontab.txt`
- Backup source: Server A, `/var/www/html`
- Backup destination: Server B, `/home/ubuntu/website-backups`
- The script retains the two most recent successful backups.

## MySQL replication

- Server A is the MySQL primary.
- Server B is the MySQL replica.
- Replication uses MySQL binary logs.
- Server B has `read_only` and `super_read_only` enabled.
- Sanitised configuration example: `mysql/replication.cnf.example`

## Server B application

The Flask application is stored in `server-b/app.py`.

It reads the replicated visitor count from the local MySQL database. It does not modify the database.

## Security

This repository must not contain:
- Database passwords.
- `.env` files.
- SSH private keys.
- Replication account passwords.
- Database dumps.
- Private certificates or other secret credentials.