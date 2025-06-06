#!/usr/bin/env python3
import pygame
import os
import time
import sys

image_folder = "/home/pi-guest-user/share"


def load_images(folder_path):
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if not f.startswith('.') and f.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp"))]
    return image_files
def display_images(screen, image_path):
    try:
        # Use module-level screen_width and screen_height.
        # Add a check in case they weren't set, though the main block should handle this.
        if screen_width is None or screen_height is None:
            print("Error: Screen dimensions not properly initialized. Using fallback 1920x1080 for this image.")
            current_sw, current_sh = 1920, 1080
        else:
            current_sw, current_sh = screen_width, screen_height

        image = pygame.image.load(image_path)
        original_width = image.get_width()
        original_height = image.get_height()

        if original_height == 0: # Avoid division by zero
            print(f"Warning: Image {image_path} has zero height. Skipping scaling.")
            # Optionally display a placeholder or skip
            return

        # Calculate the new width to maintain aspect ratio when fitting to screen_height
        aspect_ratio = original_width / original_height
        new_height = current_sh
        new_width = int(new_height * aspect_ratio)

        # If the new width is greater than screen_width (e.g. for very wide images),
        # then scale to fit screen_width instead, maintaining aspect ratio.
        if new_width > current_sw:
            new_width = current_sw
            if aspect_ratio == 0: # Avoid division by zero if original_width was also 0
                new_height = current_sh # or some other default
            else:
                new_height = int(new_width / aspect_ratio)

        # Ensure dimensions are positive
        new_width = max(1, new_width)
        new_height = max(1, new_height)

        scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))

        # Calculate coordinates to center the image
        pos_x = (current_sw - new_width) // 2
        pos_y = (current_sh - new_height) // 2

        screen.fill((0, 0, 0))  # Fill screen with black before blitting new image
        screen.blit(scaled_image, (pos_x, pos_y))
        pygame.display.flip()
    except pygame.error as e:
        print(f"Error in display_images (Pygame error): {e} for image {image_path}")
    except Exception as ex:
        print(f"An unexpected error occurred in display_images: {ex} for image {image_path}")
if __name__ == "__main__":
    global screen_width, screen_height

    #parse command line argument for monitor ID
    if len(sys.argv) < 2:
        print("monitor_id should be 0 for left TV or 1 for right TV.")
        print("Usage: python3 your_script.py <monitor_id>")
        sys.exit(1)

    try:
        monitor_id = int(sys.argv[1])
        if monitor_id not in [0, 1]:
            raise ValueError("monitor_id should be 0 or 1.")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    #default delay
    delay_seconds = 10
    if len(sys.argv) > 2:
        try:
            user_delay = int(sys.argv[2])
            if user_delay > 0:
                delay_seconds = int(user_delay)
            else:
                print(f"warning: delay must be a positive integer. Using default {delay_seconds} seconds.")
        except ValueError:
            print(f"Error: invalid value for delay '{sys.argv[2]}'. Must be an integer. Using default {delay_seconds} seconds.")

    pygame.init()

    # --- BEGIN: Dynamically set screen_width and screen_height ---
    try:
        # Try using pygame.display.get_desktop_sizes() (Pygame 1.9.5+)
        desktop_sizes = pygame.display.get_desktop_sizes()

        if not desktop_sizes:
            raise pygame.error("Pygame could not detect any desktop sizes.")

        if monitor_id >= len(desktop_sizes):
            print(f"Warning: monitor_id {monitor_id} is out of range. Available displays: {len(desktop_sizes)} (0 to {len(desktop_sizes)-1}).")
            if len(desktop_sizes) > 0:
                print("Attempting to use primary display (ID 0).")
                screen_width, screen_height = desktop_sizes[0]
                monitor_id = 0 # Update monitor_id to reflect actual usage
            else: # Should not be reached if the 'not desktop_sizes' check above is robust
                raise pygame.error("No displays found after attempting to use primary display.")
        else:
            screen_width, screen_height = desktop_sizes[monitor_id]

        print(f"Using determined resolution for display {monitor_id}: {screen_width}x{screen_height}")

    except AttributeError:
        # pygame.display.get_desktop_sizes() is not available (older Pygame versions)
        print("Warning: pygame.display.get_desktop_sizes() not available. Trying alternative method (temporary fullscreen).")
        try:
            # This attempts to create a fullscreen window on the target display to get its dimensions.
            # The 'display' parameter in set_mode must be correctly handled by your Pygame backend (e.g., X11).
            print(f"Attempting to determine resolution for display {monitor_id} via temporary fullscreen window.")
            temp_screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, display=monitor_id)
            screen_width = temp_screen.get_width()
            screen_height = temp_screen.get_height()
            pygame.display.quit()  # Quit this temporary display context
            pygame.init()        # Re-initialize Pygame as quit() uninitializes modules
            print(f"Determined resolution for display {monitor_id} via temp fullscreen: {screen_width}x{screen_height}")
        except pygame.error as e_alt:
            print(f"Error determining screen size via temporary fullscreen: {e_alt}")
            print("Falling back to hardcoded 1920x1080.")
            screen_width, screen_height = 1920, 1080
    except pygame.error as e:
        print(f"Pygame error while getting desktop sizes: {e}")
        print("Falling back to hardcoded 1920x1080.")
        screen_width, screen_height = 1920, 1080

    # Final fallback if dimensions are still not set (should ideally not happen with above logic)
    if screen_width is None or screen_height is None:
        print("Critical Error: Screen dimensions could not be determined. Using default 1920x1080.")
        screen_width, screen_height = 1920, 1080
    # --- END: Dynamically set screen_width and screen_height ---

    image_list = load_images(image_folder)
    num_images = len(image_list)

    if num_images == 0:
        #TODO add a default image to display when no images are present
        print("no images to display")
        pygame.quit()
        sys.exit(0)

    try:
        current_screen = pygame.display.set_mode((screen_width,screen_height),pygame.FULLSCREEN, display=monitor_id)
    except pygame.error as e:
        print(f"Error initializing display {monitor_id}: {e}")
        print("Make sure your Raspberry Pi's OS is configured for dual displays and that the 'display' argument matches an available X11 display.")
        pygame.quit()
        sys.exit(1)

    current_image_index = 0 if monitor_id == 0 else (1 % num_images) #ensure initial index is valid if num_images is 1

    #timer variables
    delay_milliseconds = delay_seconds * 1000
    last_image_update_time = pygame.time.get_ticks() - delay_milliseconds #show first image immediately
    clock = pygame.time.Clock()#pygame clock  for managing frame rate

    print(f"Image Slideshow Monitor {monitor_id}")
    print("Press ESC to quit.")
    print(f"Image display delay: {delay_seconds} seconds.")
    running = True

    while running:
        #if number of images changes reload the list
        if len(load_images(image_folder)) != num_images:
            image_list = load_images(image_folder)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #closes window with Escape
                running = False
        current_time = pygame.time.get_ticks()
        if current_time - last_image_update_time >= delay_milliseconds:
            if num_images > 0:
                display_images(current_screen, image_list[current_image_index % num_images])
                current_image_index += 1
                last_image_update_time = current_time

        #limit the loop to a reasonable frame rate to avoid excessive CPU usage
        #this also affects how often events are checked 30-60 fps is typical
        clock.tick(30)

    pygame.quit()
