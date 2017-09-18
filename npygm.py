import pygame
import time
import random

pygame.init()

disp_width = 800
disp_height = 600
car_width = 94

gameDisp = pygame.display.set_mode((disp_width, disp_height))

pygame.display.set_caption('my first game')
clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
blue = (0, 0, 255)

pause = False
carImg = pygame.image.load('Capture.png')

def quit_game():
    pygame.quit()
    quit()

def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisp, ac, (x, y, w, h))
        if action!=None  and click[0]==1:
            action()
##            if action=="play":
##                game_loop()
##            elif action== "quit" :
##                quit_game()

    else:
        pygame.draw.rect(gameDisp, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 15)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + w / 2), (y + h / 2))
    gameDisp.blit(textSurf, textRect)


def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score :  " + str(count), True, black)
    gameDisp.blit(text, (0, 0))


def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisp, color, [thingx, thingy, thingw, thingh])


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 80)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((disp_width / 2), (disp_height / 2))
    gameDisp.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_intro()


def crash(num):
    gameDisp.fill(white)
    message_display('You Score ' + str(num))


def car(x, y):
    gameDisp.blit(carImg, (x, y))


def unpause():
    global pause
    pause = False
    

def paused():
    global pause
    
    while pause:

        for events in pygame.event.get():

            if events.type == pygame.QUIT:
                quit_game()

        gameDisp.fill(white)
        pygame.draw.rect(gameDisp, red, [200, 600, 30, 70])
        largeText = pygame.font.Font('freesansbold.ttf', 80)
        TextSurf, TextRect = text_objects(' Paused ', largeText)
        TextRect.center = ((disp_width / 2), (disp_height / 2))
        gameDisp.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()


        button("CONTINUE", 150, 450, 140, 40, green, bright_green , unpause)
        button("QUIT GAME", 570, 450, 80, 140, red, bright_red, quit_game)

        pygame.display.update()

        clock.tick(15)


def game_intro():
    intro = True
    while intro:

        for events in pygame.event.get():

            if events.type == pygame.QUIT:
                quit_game()

        gameDisp.fill(white)
        pygame.draw.rect(gameDisp, red, [200, 600, 30, 70])
        largeText = pygame.font.Font('freesansbold.ttf', 80)
        TextSurf, TextRect = text_objects('race fuss', largeText)
        TextRect.center = ((disp_width / 2), (disp_height / 2))
        gameDisp.blit(TextSurf, TextRect)

        mouse = pygame.mouse.get_pos()


        button("PLAY", 150, 450, 80, 40, green, bright_green , game_loop)
        button("QUIT", 570, 450, 80, 40, red, bright_red, quit_game)

        pygame.display.update()

        clock.tick(15)


def game_loop():
    x = disp_width * .45
    y = disp_height * .68
    x_change = 0

    thing_startx = random.randrange(0, disp_width)
    thing_starty = -600
    thing_speed = 5
    thing_width = 100
    thing_height = 100

    dodged = 0

    gameExit = False

    while not gameExit:

        for events in pygame.event.get():

            if events.type == pygame.QUIT:
               quit_game()

            if events.type == pygame.KEYDOWN:
                
                if events.key == pygame.K_LEFT:
                    x_change = -10
                    

                if events.key == pygame.K_RIGHT:
                    x_change = 10

                if events.key== pygame.K_UP:
                    pause= True
                    paused()


            if events.type == pygame.KEYUP:

                if events.key == pygame.K_LEFT or events.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        gameDisp.fill(white)
        car(x, y)
        things_dodged(dodged)

        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed

        if thing_starty > disp_height:
            thing_starty = 0 - thing_height
            c = x - thing_width
            d = x + car_width + thing_width
            if c < 0:
                c = 0
            if d > disp_width:
                d = disp_width-thing_width
            thing_startx = random.randrange(c, d)
            dodged += 1
            thing_speed+=1


        if x > disp_width - car_width or x < 0:
            crash(dodged)

        if y < thing_starty + thing_height:
            if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
                crash(dodged)

        pygame.display.update()
        clock.tick(60)


game_intro()
game_loop()
quit_game()
