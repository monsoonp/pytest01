# PythonScript.py
import random
# Import a library of functions called 'pygame'
import pygame
import math
# Initialize the game engine
t = pygame.init()

# Define some colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (0, 255,   0)
RED = (255,   0,   0)
BLUE = (0,   0, 255)

PI = math.pi

# 화면 사이즈, 튜플 형식
size = (700, 500)
# 화면 띄우기
screen = pygame.display.set_mode(size)
# 화면 제목
pygame.display.set_caption("Crawler")

# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
rect_x = 50
rect_y = 50
# Speed and direction of rectangle
rect_change_x = 5
rect_change_y = 5
swap = True
# Create an empty array
snow_list = []
for i in range(50):
    x = random.randrange(0, 500)
    y = random.randrange(0, 400)
    snow_list.append([x, y])

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            print("pygame Quit.")
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            print("User pressed a key.")
        elif event.type == pygame.KEYUP:
            print("User let go of a key.")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("User pressed a mouse button")
    # --- Game logic should go here

    # First, clear the screen to white. Don't put other drawing commands

    # above this, or they will be erased with this command. 화면 지우기
    screen.fill(BLACK)  # Clear the screen and set the screen background

    # --- Drawing code should go here ##############
    pygame.draw.rect(screen, WHITE, [rect_x, rect_y, 50, 50])
    pygame.draw.rect(screen, RED, [rect_x + 10, rect_y + 10, 30, 30])

    rect_x += rect_change_x
    rect_y += rect_change_y
    # Bounce the rectangle if needed
    if rect_y > 450 or rect_y < 0:
        rect_change_y = rect_change_y * -1
    if rect_x > 650 or rect_x < 0:
        rect_change_x = rect_change_x * -1

    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Calibri', 25, True, False)
    # Render the text. "True" means anti-aliased text.
    # Black is the color. The variable BLACK was defined
    # above as a list of [0, 0, 0]
    # Note: This line creates an image of the letters,
    # but does not put it on the screen yet.
    text = font.render("My text : "+str(snow_list[0][0]), True, WHITE)
    # Put the image of the text on the screen at 250x250
    screen.blit(text, [150, 450])

    # let it snow
    # for i in range(50):
    #     x = random.randrange(0, 400)
    #     y = random.randrange(0, 400)
    #     pygame.draw.circle(screen, WHITE, [x, y], 2)
    # Process each snow flake in the list
    for i in range(len(snow_list)):

        # Draw the snow flake
        pygame.draw.circle(screen, WHITE, snow_list[i], 2)

        # Move the snow flake down one pixel
        snow_list[i][1] += 1

        # If the snow flake has moved off the bottom of the screen
        if snow_list[i][1] > 400:
            # Reset it just above the top
            y = random.randrange(-50, -10)
            snow_list[i][1] = y
            # Give it a new x position
            x = random.randrange(0, 500)
            snow_list[i][0] = x

    # --- Go ahead and update the screen with what we've drawn. 화면 뒤집기
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)

#  close the window and quit.
pygame.quit()
