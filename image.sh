#this works for two 1920x1080 displays that are side by side to each other
#!/bin/bash

export DISPLAY=:0
# Ensure this path is correct for your uploaded script
PYTHON_SCRIPT="/full/path/to/your/image_script.py"
DELAY_SECONDS=10 # Or whatever you prefer
LOG_FILE="/tmp/slideshow_autostart_wmctrl.log"

# Window titles (MUST MATCH what you set with pygame.display.set_caption)
TITLE_MON0="Image Slideshow Monitor 0"
TITLE_MON1="Image Slideshow Monitor 1"

# Monitor geometry (X,Y,Width,Height for wmctrl's -e option)
# YOU MUST DETERMINE THESE VALUES using 'xrandr'
# <gravity>,<x>,<y>,<width>,<height>
# Example for two 1920x1080 monitors:
MON0_X=0
MON0_Y=0
MON1_X=1920 # If monitor 1 is to the right of monitor 0
MON1_Y=0

# SCREEN_WIDTH and SCREEN_HEIGHT should match your monitor's actual resolution
# Your Python script now dynamically determines this, which is great.
# For wmctrl, you specify the target monitor's full dimensions.
# If both are 1920x1080, use those.
SCREEN_WIDTH_MON0=1920 # Example for monitor 0
SCREEN_HEIGHT_MON0=1080 # Example for monitor 0
SCREEN_WIDTH_MON1=1920 # Example for monitor 1
SCREEN_HEIGHT_MON1=1080 # Example for monitor 1


MON0_GEOM="0,${MON0_X},${MON0_Y},${SCREEN_WIDTH_MON0},${SCREEN_HEIGHT_MON0}"
MON1_GEOM="0,${MON1_X},${MON1_Y},${SCREEN_WIDTH_MON1},${SCREEN_HEIGHT_MON1}"

echo "--------------------------------------" > "$LOG_FILE"
date >> "$LOG_FILE"
echo "Starting slideshows with wmctrl positioning..." >> "$LOG_FILE"

position_window() {
    local title="$1"
    local geom="$2"
    local attempts=0
    local max_attempts=15

    echo "Attempting to position window: '$title' to geometry $geom" >> "$LOG_FILE"
    
    while ! wmctrl -l | grep -qF "$title"; do
        sleep 1
        attempts=$((attempts + 1))
        if [ "$attempts" -ge "$max_attempts" ]; then
            echo "Error: Window '$title' not found after $max_attempts seconds." >> "$LOG_FILE"
            return 1
        fi
    done
    
    echo "Window '$title' found. Moving to $geom." >> "$LOG_FILE"
    wmctrl -r "$title" -e "$geom"
    echo "Command to move '$title' executed." >> "$LOG_FILE"
    return 0
}

# Launch Python scripts
/usr/bin/python3 "$PYTHON_SCRIPT" 0 "$DELAY_SECONDS" >> "$LOG_FILE" 2>&1 &
/usr/bin/python3 "$PYTHON_SCRIPT" 1 "$DELAY_SECONDS" >> "$LOG_FILE" 2>&1 &

echo "Waiting for windows to initialize..." >> "$LOG_FILE"
sleep 5 

position_window "$TITLE_MON0" "$MON0_GEOM" &
position_window "$TITLE_MON1" "$MON1_GEOM" &

wait
echo "Slideshow positioning attempts finished." >> "$LOG_FILE"