#!/bin/bash

export DISPLAY=:0
# Use the full path to your Python script
PYTHON_SCRIPT="/path/to/python_script.py"
LOG_FILE="/tmp/slideshow_monitor1.log"

# --- Variables for Monitor 1 ONLY ---
TITLE_MON1="Image Slideshow Monitor 1"
#this value is the offset the image should be displayed, in this case monitor 1 is to the right of monitor 0
MON1_X=1920
MON1_Y=0
SCREEN_WIDTH_MON1=1920
SCREEN_HEIGHT_MON1=1080
MON1_GEOM="0,${MON1_X},${MON1_Y},${SCREEN_WIDTH_MON1},${SCREEN_HEIGHT_MON1}"
# ------------------------------------

echo "--- Start Script for Monitor 1 ---" > "$LOG_FILE"
date >> "$LOG_FILE"

# Launch the Python script for Monitor 1 in the background
/usr/bin/python3 "$PYTHON_SCRIPT" 1 10 >> "$LOG_FILE" 2>&1 &

# Wait for the window to initialize
echo "Waiting 20 seconds..." >> "$LOG_FILE"
sleep 20

# Find and position the window
echo "Attempting to position window: '$TITLE_MON1'" >> "$LOG_FILE"
if wmctrl -l | grep -qF "$TITLE_MON1"; then
    echo "SUCCESS: Window found. Moving." >> "$LOG_FILE"
    wmctrl -r "$TITLE_MON1" -e "$MON1_GEOM"
else
    echo "FAILURE: Window not found." >> "$LOG_FILE"
    wmctrl -l >> "$LOG_FILE" # Log what wmctrl sees for debugging
fi

echo "--- End Script for Monitor 1 ---" >> "$LOG_FILE"
