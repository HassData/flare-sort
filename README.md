# flare-sort
script to sort flares into folders
## Overview

This script organizes flare files downloaded from the internet by copying them into folders named after the agent. Each new flare for an agent is given an incremented number. The script also cleans up the zip folder after processing.

## Usage

You can run the script manually using:

```bash
nohup python3 flare_sort.py &
```

This will keep the script running in the background, but you will need to restart it each time your computer reboots.

## Automation

To run the script automatically on macOS startup, you can use a LaunchAgent with a `.plist` file. Place the `.plist` in `~/Library/LaunchAgents` and configure it to run the script at login.

## Features

- Copies flare files into agent-specific folders
- Numbers each flare iteration
- Cleans up processed zip files
- Supports manual and automatic execution