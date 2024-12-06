import pygame
import sys # for exiting

# set some constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650
BACKGROUND = (13,24,36)
PLAYER1_COLOR = (100,219,243)
PLAYER2_COLOR = (222,162,82)
PLAYER1_TRAIL = (192,240,251)
PLAYER2_TRAIL = (255,231,45)
CELL_SIZE = 5
MAX_SIZE = 200

# initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mixer.init()
player1_pos = [0, 0]
player2_pos = [179, 129]
p1_visited = []
p2_visited = []

# FUNCTIONS
# define the grid
def grid():
    # draw vertical lines
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (13,24,36), (x, 0), (x, SCREEN_HEIGHT)) # surface, color, start point, end point
    for y in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (13,24,36), (0, y), (SCREEN_WIDTH, y))

# function to check if there's a collision
def check_collision():
    # if there's a collison, display the winner
    if player1_pos in p2_visited or player2_pos in p1_visited:
        return True

    return False

# function to display the winner
def display_winner(message):
    font = pygame.font.Font(None, 70)
    winner_text = font.render(message, True, (255, 255, 255))
    restart_text = font.render("Press Any Key To Restart", True, (255, 255, 255))

    text_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(winner_text, text_rect)
    screen.blit(restart_text, restart_rect)

# game logic function
def game_logic():
    # put the player in the correct cells in the grid by saying how far up/down and left/right the player is in terms of pixels
    p1_pixel_x = player1_pos[0] * CELL_SIZE
    p1_pixel_y = player1_pos[1] * CELL_SIZE

    p2_pixel_x = player2_pos[0] * CELL_SIZE
    p2_pixel_y = player2_pos[1] * CELL_SIZE

    # color the visited cells
    for pos in p1_visited:
        x1 = pos[0] * CELL_SIZE
        y1 = pos[1] * CELL_SIZE
        pygame.draw.rect(screen, PLAYER1_TRAIL, (x1, y1, CELL_SIZE, CELL_SIZE))

    for pos in p2_visited:
        x2 = pos[0] * CELL_SIZE
        y2 = pos[1] * CELL_SIZE
        pygame.draw.rect(screen, PLAYER2_TRAIL, (x2, y2, CELL_SIZE, CELL_SIZE))

    # set movement keys for both players
    keys = pygame.key.get_pressed() #get current state of all keys

    # format for setting keys below
    # if keys[pygame.K_*]:   --> * is the key being set
    # playerx_pos[1 or 0] += or -= 1    --> logic for setting the position of playerx up or down by one, depending on the key pressed.
    # Also, the top of the grid is lower numbers, left side of the grid is lower numbers. So going up would be -= 1.

    # player 1 controls (wasd)
    if keys[pygame.K_a] and player1_pos[0] > 0:
        player1_pos[0] -= 1
    if keys[pygame.K_d] and player1_pos[0] < (SCREEN_WIDTH // CELL_SIZE) - 1:
        player1_pos[0] += 1
    if keys[pygame.K_w] and player1_pos[1] > 0:
        player1_pos[1] -= 1
    if keys[pygame.K_s] and player1_pos[1] < (SCREEN_HEIGHT // CELL_SIZE) - 1:
        player1_pos[1] += 1
    
    # player 2 controls (arrow keys)
    if keys[pygame.K_LEFT] and player2_pos[0] > 0:
        player2_pos[0] -= 1
    if keys[pygame.K_RIGHT] and player2_pos[0] < (SCREEN_WIDTH // CELL_SIZE) - 1:
        player2_pos[0] += 1
    if keys[pygame.K_UP] and player2_pos[1] > 0:
        player2_pos[1] -= 1
    if keys[pygame.K_DOWN] and player2_pos[1] < (SCREEN_HEIGHT // CELL_SIZE) - 1:
        player2_pos[1] +=1

    # add the current position to the list of visited positions, and if there are too many already in the list,
    p1_visited.append(player1_pos[:])
    if len(p1_visited) > MAX_SIZE:
        p1_visited.pop(0)

    p2_visited.append(player2_pos[:])
    if len(p2_visited) > MAX_SIZE:
        p2_visited.pop(0)

    # create physical player (the "car" or whatever) and draw it
    pygame.draw.rect(screen, PLAYER1_COLOR, (p1_pixel_x, p1_pixel_y, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, PLAYER2_COLOR, (p2_pixel_x, p2_pixel_y, CELL_SIZE, CELL_SIZE))

# main function
def main():
    global player1_pos, player2_pos, p1_visited, p2_visited

    # set up game window
    pygame.display.set_caption("Tron")

    # set up music
    pygame.mixer.music.load("ghost-coast-2030-20822.mp3")
    pygame.mixer.music.play(-1, 14)

    clock = pygame.time.Clock() # set clock speed
    running = True # variable to control main game loop
    game_over = False
    winner = None

    while running: # game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BACKGROUND)
        grid()

        # GAME LOGIC GOES HERE
        if not game_over:
            game_logic()
            if check_collision():
                game_over = True
                winner = "Orange Wins!" if player1_pos in p2_visited else "Blue Wins!"
        else:
            display_winner(winner)
            pygame.display.flip()


            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    if event.type == pygame.KEYDOWN:
                        waiting = False

            # reset the game
            game_over= False
            winner = None
            player1_pos = [0, 0]
            player2_pos = [179, 129]
            p1_visited.clear()
            p2_visited.clear()



        pygame.display.flip() # update the screen
        clock.tick(30) # limit fps to 60

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()