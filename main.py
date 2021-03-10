import pygame          #we import the pygame module in order to use its functions
import os            #we import the os module for reasons that i dont remember lol but do it anyway
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 


WHITE = (255, 255, 255) #255 is max value of color, 0-255 inclusively. 255 is white
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)    #this is pulling a font to display on screen and choosing size
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60      # this sets the fps the game will run at
VEL = 8  #how fast the spaceship moves
BULLET_VEL = 10
MAX_BULLETS = 20


SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40   #setting the size of the spaceship. ((0, 0) is always the top left of the screen))

YELLOW_HIT = pygame.USEREVENT + 1       # USEREVENT is an integer so we add 1 and 2 to the codes to make it a random number
RED_HIT = pygame.USEREVENT + 2


YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) 

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):         #the def draw window is how we create the surface that we see, fill is the background and blits are the spaceships 
    WIN.blit(SPACE, (0, 0))       #in this code, the fill has to come before blit or else you wont see the image
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE) #the 1 is for anti-aliasing. you always put 1 there.
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))  
    WIN.blit(yellow_health_text, (10, 10))  #we dont need to add width on this one because yellow player is left side of screen so 10, 10 is good position.

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  
    WIN.blit(RED_SPACESHIP, (red.x, red.y))         #WIN blits are how you place the image on the surface. this makes the spaceships appear.

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  #left 
            yellow.x -= VEL       #when coding the directional movement like this, you use -= and +=  for both the x and y coordinate
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  #right
            yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  #up
            yellow.y -= VEL           # the "and" statement with the VEL and everything is to prevent the spaceship from crossing the middle border.
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  #down  also, the -15 is cuz spaceship goes off the bottom a bit
            yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  #left 
            red.x -= VEL             # To use the arrow keys, use pygame.K_up, K_down, K_left, k_right
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #right
            red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:    #up
            red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  #down
            red.y += VEL
        

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):    #.colliderect is a good way for object collision like bullets, however it only works if both objects are rectangles i.e. Rect()
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)     #this gets rid of bullet after it hits player
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):    #.colliderect is a good way for object collision like bullets, however it only works if both objects are rectangles i.e. Rect()
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)     #this gets rid of bullet after it hits player
        elif bullet.x < 0:
            red_bullets.remove(bullet)     



def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)   # 5 seconds




def main ():            #this is the main game while loop
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)    #These define where the spaceship is, ((X, Y, Width, Height) of the object))
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)   #we already have width/heigth as a variable so we can use that here.
 
    red_bullets = [] 
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)     #im pretty sure anything that happens ingame has to be within clock.tick
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)  #size and placement of bullet.
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_l and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)  #size and placement of bullet.
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"    
        if yellow_health <= 0:
            winner_text = "Red wins!"   

        if winner_text != "":
            draw_winner(winner_text)
            break



        keys_pressed = pygame.key.get_pressed() #you must use this code to be able to press multiple keys at a time.
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
    
    main()
 

if __name__ == "__main__": # this code is necessary so we dont accidentaly call other main variables
    main()


