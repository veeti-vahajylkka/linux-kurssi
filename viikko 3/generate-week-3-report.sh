#!/usr/bin/env bash

# Week 3 - Server Status Report

REPORT_DIR="/var/www/sivusto/viikko3"
REPORT_FILE="$REPORT_DIR/index.html"

# Collect server information
GENERATED_AT=$(date '+%Y-%m-%d %H:%M:%S %Z (UTC%:z)')
UPTIME_TEXT=$(uptime -p)

# Extract root filesystem usage percentage
DISK_USAGE=$(df -P / | awk 'NR == 2 {gsub(/%/, "", $5); print $5}')

# Collect RAM information in MiB
MEM_TOTAL=$(free -m | awk '/^Mem:/ {print $2}')
MEM_AVAILABLE=$(free -m | awk '/^Mem:/ {print $7}')

# Determine disk space status
get_disk_status() {
    local usage=$1

    if (( usage < 80 )); then
        echo "OK"
    else
        echo "WARNING"
    fi
}

# Allow testing of both branches without changing disk usage
if [[ "${1:-}" == "--test" ]]; then
    for value in 50 80 90; do
        echo "${value}%: $(get_disk_status "$value")"
    done
    exit 0
fi

DISK_STATUS=$(get_disk_status "$DISK_USAGE")

# Create report directory if it does not exist
mkdir -p "$REPORT_DIR"

# Generate HTML in a temporary file
TEMP_FILE=$(mktemp "$REPORT_DIR/.report.XXXXXX")

trap 'rm -f "$TEMP_FILE"' EXIT

cat > "$TEMP_FILE" <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Week 3 – Server Status Report</title>

    <style>
        :root {
            color-scheme: dark;
            --background: #101713;
            --surface: #19231d;
            --surface-hover: #202d25;
            --green: #4ade80;
            --green-muted: #86efac;
            --text: #e5eee7;
            --text-muted: #9aaa9f;
            --border: #34443a;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: system-ui, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 0 20px;
            line-height: 1.6;
            background: var(--background);
            color: var(--text);
        }

        h1, h2 {
            color: var(--green);
        }

        h1 {
            font-size: 2.2rem;
            margin-bottom: 8px;
        }

        h2 {
            font-size: 1.4rem;
            margin-top: 0;
        }

        h3 {
            color: var(--green-muted);
        }

        header {
            margin-bottom: 32px;
        }

        header p {
            color: var(--text-muted);
        }

        section {
            margin: 24px 0;
            padding: 28px;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }

        th, td {
            padding: 14px 12px;
            text-align: left;
            border: none;
            border-bottom: 1px solid var(--border);
        }

        th {
            color: var(--green-muted);
            font-weight: 600;
        }

        td {
            color: var(--text);
        }

        tbody tr:hover,
        table tr:hover {
            background: var(--surface-hover);
        }

        tr:last-child th,
        tr:last-child td {
            border-bottom: none;
        }

        .ok {
            color: var(--green);
            font-weight: bold;
        }

        .warning {
            color: #f87171;
            font-weight: bold;
        }

        code {
            background: #26352b;
            color: var(--green-muted);
            padding: 3px 7px;
            border-radius: 5px;
            overflow-wrap: anywhere;
        }

        .note {
            color: var(--text-muted);
        }

        li {
            margin: 8px 0;
        }

        footer {
            margin-top: 32px;
            padding: 16px 0;
            border-top: 1px solid var(--border);
        }

        @media (max-width: 600px) {
            body {
                margin: 20px auto;
                padding: 0 12px;
            }

            section {
                padding: 18px;
            }

            th, td {
                padding: 10px 8px;
                font-size: 0.9rem;
            }
        }
    </style>
</head>

<body>

<header>
    <h1>Server Status Report</h1>
    <p>Week 3: Linux command line and Bash scripting</p>
    <p>
        This page provides an automatically updated overview
        of my Ubuntu server.
    </p>
</header>

<section>
    <h2>Current server status</h2>

    <table>
        <thead>
            <tr>
                <th>Information</th>
                <th>Value</th>
            </tr>
        </thead>

        <tbody>
            <tr>
                <th>Report generated</th>
                <td>$GENERATED_AT</td>
            </tr>

            <tr>
                <th>Server uptime</th>
                <td>$UPTIME_TEXT</td>
            </tr>

            <tr>
                <th>Root filesystem disk usage</th>
                <td>$DISK_USAGE%</td>
            </tr>

            <tr>
                <th>Disk space status</th>
                <td class="$([ "$DISK_STATUS" = "OK" ] && echo ok || echo warning)">
                    $DISK_STATUS
                </td>
            </tr>

            <tr>
                <th>Total RAM</th>
                <td>$MEM_TOTAL MiB</td>
            </tr>

            <tr>
                <th>Available RAM</th>
                <td>$MEM_AVAILABLE MiB</td>
            </tr>
        </tbody>
    </table>

    <p>
        Disk space status is OK below 80% usage
        and WARNING at 80% or above.
    </p>

    <p class="note">
        This report is automatically regenerated every minute.
    </p>
</section>

<section>
    <h2>Commands used</h2>

    <ul>
        <li>
            <code>date</code>:
            Displays the current date, time and timezone.
        </li>

        <li>
            <code>uptime -p</code>:
            Displays how long the server has been running.
        </li>

        <li>
            <code>df -P / | awk 'NR == 2 {print $5}'</code>:
            Uses a pipe to pass filesystem information to awk,
            which extracts the root filesystem usage percentage.
        </li>

        <li>
            <code>free -m</code>:
            Displays RAM information in MiB.
        </li>
    </ul>
</section>

<section>
    <h2>How the script works</h2>

    <p>
        The Bash script collects server information using Linux
        commands. Command substitution, using $(...), stores
        the command output in variables.
    </p>

    <p>
        The get_disk_status function accepts the disk usage
        percentage as an argument. An if statement checks
        whether the value is below 80.
    </p>

    <p>
        Values below 80 produce OK. Values of 80 or higher
        produce WARNING.
    </p>

    <p>
        The script generates an HTML file using a heredoc.
        It first writes to a temporary file and then replaces
        index.html, ensuring that Nginx serves a completed report.
    </p>
</section>

<section>
    <h2>Scheduling</h2>

    <p>
        A cron job runs the Bash script once every minute
        as the root user.
    </p>

    <p>
        The cron job is configured in /etc/cron.d/week3-report.
        Cron starts automatically when Ubuntu boots, so
        report generation continues after a reboot.
    </p>
</section>

<section>
    <h2>Test results</h2>

    <h3>Syntax check</h3>
    <p>
        The script passed the Bash syntax check using
        <code>bash -n /usr/local/bin/generate-week3-report.sh</code>.
        No syntax errors were reported.
    </p>

    <h3>Disk space status tests</h3>

    <table>
        <tr>
            <th>Test input</th>
            <th>Expected result</th>
            <th>Actual result</th>
        </tr>

        <tr>
            <td>50%</td>
            <td>OK</td>
            <td>OK</td>
        </tr>

        <tr>
            <td>80%</td>
            <td>WARNING</td>
            <td>WARNING</td>
        </tr>

        <tr>
            <td>90%</td>
            <td>WARNING</td>
            <td>WARNING</td>
        </tr>
    </table>

    <h3>Automatic updates</h3>
    <p>
        2026-11-14 13:41:01

        <br>

        2026-11-14 13:42:01
    </p>

    <h3>Reboot test</h3>
    <p>
        The website opened and automatic updates continued after
        rebooting the virtual machine.
    </p>
</section>

<section>
    <h2>Problem solved or something learned</h2>

    <p>
        Timezone was wrong. The report generated value was
        in UTC+0, and had to be changed to Europe/Helsinki.

        <br>

        <code>sudo timedatectl set-timezone Europe/Helsinki</code> sets the correct timezone.
    </p>
</section>

<footer>
    <p class="note">
        Week 3 – Linux Server Administration
    </p>
</footer>

</body>
</html>
EOF

# Set permissions so Nginx can read the report
chmod 644 "$TEMP_FILE"

# Atomically replace the previous report
mv "$TEMP_FILE" "$REPORT_FILE"

trap - EXIT