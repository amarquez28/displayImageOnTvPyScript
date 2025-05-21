import pygame
import os
import random
import time
import sys

image_folder = "/home/pi-guest-user/share"
screen_width = 1920
screen_height = 1080
delay_range = (2, 7)


def load_images(folder_path):
    image_files = [os.path.join(folder_path,f) for f in os.listdir(folder_path) if f.lower().endswith((".png",".jpg",".jpeg",".gif",".bmp"))]
    #random.shuffle(image_files)
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
            raise ValueError
    except ValueError:
        print("Error: monitor_id must be 0 or 1.")
        sys.exit(1)

    pygame.init()

    image_list = load_images(image_folder)
    num_images = len(image_list)

    if num_images < 1:
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

    current_image_index = random.randint(0, num_images - 1) # Start randomly for more asynchronicity
    last_display_time = time.time()
    next_delay = random.uniform(*delay_range)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        current_time = time.time()
        if current_time - last_display_time >= next_delay:
            display_images(current_screen, image_list[current_image_index % num_images])
            current_image_index += 1
            last_display_time = current_time
            next_delay = random.uniform(*delay_range) # Get new random delay for next image


    pygame.quit()
