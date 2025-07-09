# flaresort

A script to organize flare files into agent-specific folders.

## Overview

`flaresort` helps you manage flare files by sorting them into folders named after each agent. Each new flare is numbered sequentially. The script also removes processed zip files.

## Usage

Run the script manually in the background:

```bash
nohup python3 flare_sort.py &
```

**Note:** You must restart the script after each reboot if running manually.

## (Optional) Automating on macOS

To run the script automatically at login, use a LaunchAgent:

1. Create a `.plist` file (e.g., `com.username.flaresort.plist`) in `~/Library/LaunchAgents`.
2. Configure the `.plist`:

    - **PYTHONPATH:**  
      Set to your Python site-packages directory.  
      Find it with:  
      ```bash
      python3 -m site
      ```
      Example:  
      `/Users/yourname/.pyenv/versions/X.X.X/lib/pythonX.X/site-packages`

    - **ProgramArguments:**  
      - First: Full path to your Python interpreter  
      - Second: Full path to `flare_sort.py`  
      Example:
      ```xml
      <string>/Users/yourname/.pyenv/versions/X.X.X/bin/python</string>
      <string>/Users/yourname/path/to/flare_sort.py</string>
      ```

3. Load the agent:
    ```bash
    launchctl load ~/Library/LaunchAgents/com.username.flaresort.plist
    ```

4. To unload:
    ```bash
    launchctl unload ~/Library/LaunchAgents/com.username.flaresort.plist
    ```

5. Check status:
    ```bash
    launchctl list | grep flaresort
    ```

## Features

- Sorts flare files into agent folders
- Numbers each flare per agent
- Cleans up processed zip files
- Supports manual and automatic execution