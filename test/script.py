# script.py
# import random
# Import a library of functions called 'pygame'
import pygame
import math
# Initialize the game engine
t = pygame.init()
print(t)

# Define some colors
BLACK = (0,   0,   0)
# WHITE = (255, 255, 255)
WHITE = (0xFF, 0xFF, 0xFF)
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
    screen.fill(WHITE)  # Clear the screen and set the screen background

    # --- Drawing code should go here ##############
    pygame.draw.rect(screen, RED, [55, 50, 20, 25], 0)  # 원점(x,y), 너비, 높이
    # Draw on the screen a green line from (0, 0) to (100, 100)
    # that is 5 pixels wide.
    pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
    # Draw a rectangle
    pygame.draw.rect(screen, BLACK, [20, 20, 250, 100], 2)
    # Draw an ellipse, using a rectangle as the outside boundaries
    pygame.draw.ellipse(screen, BLACK, [20, 20, 250, 100], 2)

    # Draw on the screen several lines from (0, 10) to (100, 110)
    # 5 pixels wide using a while loop
    for y_offset in range(0, 100, 10):
        pygame.draw.line(screen, RED, [0, 10 + y_offset], [100, 110 + y_offset], 5)

    # Draw an arc as part of an ellipse. Use radians to determine what
    # angle to draw.
    pygame.draw.arc(screen, GREEN, [100, 250, 150, 150], PI / 2, PI, 2)
    pygame.draw.arc(screen, BLACK, [100, 250, 150, 150], 0, PI / 2, 2)
    pygame.draw.arc(screen, RED, [100, 250, 150, 150], 3 * PI / 2, 2 * PI, 2)
    pygame.draw.arc(screen, BLUE, [100, 250, 150, 150], PI, 3 * PI / 2, 2)

    # This draws a triangle using the polygon command
    pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)
    # For this code, make sure to have a line that says
    # "import math" at the top of your program. Otherwise
    # it won't know what math.sin is.
    for i in range(200):
        radians_x = i / 20
        radians_y = i / 6

        x = int(75 * math.sin(radians_x)) + 200
        y = int(75 * math.cos(radians_y)) + 200

        pygame.draw.line(screen, BLACK, [x, y], [x + 5, y], 5)

    for x_offset in range(30, 300, 30):
        pygame.draw.line(screen, BLACK, [x_offset, 100], [x_offset - 10, 90], 2)
        pygame.draw.line(screen, BLACK, [x_offset, 90], [x_offset - 10, 100], 2)

    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Calibri', 25, True, False)
    # Render the text. "True" means anti-aliased text.
    # Black is the color. The variable BLACK was defined
    # above as a list of [0, 0, 0]
    # Note: This line creates an image of the letters,
    # but does not put it on the screen yet.
    text = font.render("My text : "+str(123), True, BLACK)
    # Put the image of the text on the screen at 250x250
    screen.blit(text, [150, 450])

    # --- Go ahead and update the screen with what we've drawn. 화면 뒤집기
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)

#  close the window and quit.
pygame.quit()
