import pygame
import os
import random
import time

image_folder = "/home/pi-guest-user/share"
screen_width = 1920
screen_height = 1080
delay_range = (5,10) #min and max dely in seconds
print(pygame.display.list_modes())

def load_images(image_folder):
    image_files = [os.path.join(image_folder,f) for f in os.listdir(image_folder) if f.lower().endswith((".png",".jpg",",jpeg",".gif",".bmp"))]
    random.shuffle(image_files)
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
    pygame.init()

    image_list = load_images(image_folder)
    num_images = len(image_list)

    if num_images < 1:
        print("no images to display")
        pygame.quit()
        exit()


    #if you have dual displays configures on the pi's OS
    #you might need to experiment with display flags and positioning
    screenL = pygame.display.set_mode((screen_width,screen_height), pygame.FULLSCREEN, display = 0)
    screenR = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, display=1)

    image_pointer_leftTV = 0
    image_pointer_rightTV = 1
    #start with different images

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

            delay = random.uniform(*delay_range)
            #display image on TV 1
            display_images(screenL, image_list[image_pointer_leftTV % num_images])
            time.sleep(delay)
            image_pointer_leftTV += 1

            #display image on TV 2
            display_images(screenR, image_list[image_pointer_leftTV % num_images])
            time.sleep(delay)
            image_pointer_rightTV += 1


    pygame.quit()