#!/usr/bin/env python3
import pygame
import os
import time
import sys

image_folder = "/home/pi-guest-user/share"
#these dimensions are for a 1080p monitor
screen_width = 1920
screen_height = 1080


def load_images(folder_path):
    image_files = [os.path.join(folder_path,f) for f in os.listdir(folder_path) if f.lower().endswith((".png",".jpg",".jpeg",".gif",".bmp"))]
    return image_files
def display_images(screen, image_path):
    try:
        image = pygame.image.load(image_path)
        scaled_image = pygame.transform.scale(image, (screen_width, screen_height))
        screen.blit(scaled_image, (0, 0))
        pygame.display.flip()
    except pygame.error as e:
        print("error in load display function: ",e)

if __name__ == "__main__":
    #parse command line argument for monitor ID
    if len(sys.argv) < 2:
        print("Usage: python3 your_script.py <monitor_id>")
        print("monitor_id should be 0 for left TV or 1 for right TV.")
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

    print(f"Starting slideshow on display {monitor_id}. Press ESC to quit.")
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
