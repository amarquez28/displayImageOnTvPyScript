#!/bin/bash

export DISPLAY=:0
# Use the full path to your Python script
PYTHON_SCRIPT="/path/to/python_script.py"
LOG_FILE="/tmp/slideshow_monitor0.log"

# --- Variables for Monitor 0 ONLY ---
TITLE_MON0="Image Slideshow Monitor 0"
MON0_X=0
MON0_Y=0
SCREEN_WIDTH_MON0=1920
SCREEN_HEIGHT_MON0=1080
MON0_GEOM="0,${MON0_X},${MON0_Y},${SCREEN_WIDTH_MON0},${SCREEN_HEIGHT_MON0}"
# ------------------------------------

echo "--- Start Script for Monitor 0 ---" > "$LOG_FILE"
date >> "$LOG_FILE"

# Launch the Python script for Monitor 0 in the background
/usr/bin/python3 "$PYTHON_SCRIPT" 0 10 >> "$LOG_FILE" 2>&1 &

# Wait for the window to initialize
echo "Waiting 20 seconds..." >> "$LOG_FILE"
sleep 20

# Find and position the window
echo "Attempting to position window: '$TITLE_MON0'" >> "$LOG_FILE"
if wmctrl -l | grep -qF "$TITLE_MON0"; then
    echo "SUCCESS: Window found. Moving." >> "$LOG_FILE"
    wmctrl -r "$TITLE_MON0" -e "$MON0_GEOM"
else
    echo "FAILURE: Window not found." >> "$LOG_FILE"
    wmctrl -l >> "$LOG_FILE" # Log what wmctrl sees for debugging
fi

echo "--- End Script for Monitor 0 ---" >> "$LOG_FILE"
