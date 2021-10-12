import pygame
import config
import games
import random

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
stars = []

def test_top5(score, data):
    retval = 0
    for i in range(5):
        if int(data["highscores"][str(5-i)]["score"]) < score:
            retval = 5-i
    return retval
        
def refresh_screen(win, Color, data, score, buttons, top5, name, step):
    global stars
    moving_sart = 30
    win.fill(Color["Black"])

    perdu_text = config.FONT["LOOSE_FONT"].render("Perdu !", 1, config.Color["White"])
    win.blit(perdu_text, (config.WIDTH//2-perdu_text.get_width()//2, 10))

    score_text = config.FONT["LOOSE_FONT"].render("Score : " + str(score), 1, config.Color["White"])
    win.blit(score_text, (config.WIDTH//2-score_text.get_width()//2, 100))

    if (top5):
        top_text = config.FONT["LOOSE_FONT"].render("TOP " + str(top5) + " !", 1, config.Color["White"])
        win.blit(top_text, (config.WIDTH//2-top_text.get_width()//2, 175))

        enter_name_text = config.FONT["LOOSE_FONT"].render("Indique ton nom", 1, config.Color["White"])
        win.blit(enter_name_text, (config.WIDTH//2-enter_name_text.get_width()//2, 250))

        if len(name) > 0:
            name_text = config.FONT["LOOSE_FONT"].render(name, 1, config.Color["White"])
            win.blit(name_text, (config.WIDTH//4-name_text.get_width()//2, 320))


    for button in buttons:
        if (button.text != "Valider" or top5):
            button.draw(win)
    
    if step<=moving_sart and len(stars)==0:
        for i in range(score):
            stars += [config.stars(data, [config.WIDTH//2+score_text.get_width()//2+random.randint(-20,20), 120+random.randint(-20,20)])]


    if step>moving_sart and len(stars) > 0:
        drawing_stars(stars, data, step-moving_sart,win)
    
    config.stars(data).draw(win)

    pygame.display.update()

def switch(mouse_on_button, win, WIDTH, HEIGHT, Color, FONT, Clock, FPS, data, top5, score, name):
    if mouse_on_button == 0:
        games.play_game(win, WIDTH, HEIGHT, Color, FONT, Clock, FPS)
    elif mouse_on_button == 2:
        pygame.quit()
    elif mouse_on_button == 3:
        if (top5):
            save_hs(data, name, score, top5)
        else:
            loose_screen(win, Color, data, score, WIDTH, HEIGHT, FONT, FPS, Clock)

def init_buttons(WIDTH, HEIGHT):
    buttons = [
            config.Buttons(
                75,
                HEIGHT-100,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Rejouer"
            ),

            config.Buttons(
                WIDTH//2 - BUTTON_WIDTH//2,
                HEIGHT-100,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Menu"
            ),

            config.Buttons(
                WIDTH-225,
                HEIGHT-100,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Quitter"),

            config.Buttons(
                3*config.WIDTH//4-BUTTON_WIDTH,
                320, 
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
                "Valider"
                )
        ]

    return buttons

def save_hs(data, name, score, top5):
    data["highscores"][str(top5)] = {"name":name,"score":score}
    config.save_data(data)
    print(data)

def drawing_stars(stars, data, step, win):
    for i, star in enumerate(stars):
        star.draw_star(win)
        
        if star.coord[1]-20 > 0:
            star.coord[1]-=max(1,(star.coord[1]-10)//30)

        if config.WIDTH-100-star.coord[0] > 0:
            star.coord[0]+=max(1,(config.WIDTH-100-star.coord[0])//15)


        if star.coord[0] == config.WIDTH-100 and star.coord[1] == 20:
            data["stars"]+=1
            config.save_data(data)
            del stars[i]



def loose_screen(win, Color, data, score, WIDTH, HEIGHT, FONT, FPS, Clock):
    data = config.get_data()
    name = "*************"
    top5 = test_top5(score, data)
    loop = True
    step = 0

    while loop:
        
        Clock.tick(FPS)
        step += 1

        buttons = init_buttons(WIDTH, HEIGHT)

        mouse_pos = pygame.mouse.get_pos()
        mouse_on_button = config.button_overlay(buttons, mouse_pos, (BUTTON_WIDTH, BUTTON_HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_on_button != -1:
                loop = False
            if top5 and event.type == pygame.KEYDOWN:
                if name == "*************":
                    name = ""
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    save_hs(data, name, score, top5)
                    mouse_on_button = 3
                    loop = False
                else:
                    name += event.unicode
    

        refresh_screen(win, Color, data, score, buttons, top5, name, step)

    switch(mouse_on_button, win, WIDTH, HEIGHT, Color, FONT, Clock, FPS, data, top5, score, name)
