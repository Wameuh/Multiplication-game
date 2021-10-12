import pygame
import config


def refresh_screen(win, backward, zoom, miniatures, buttons_unlock, buttons_choose, data, button_back):
    win.fill(config.Color["Black"])


    title = config.FONT["TITLE_FONT"].render("Fonds d'écran", 1, config.Color["White"])
    win.blit(title, (config.WIDTH//2-title.get_width()//2, 10))

    backward.draw(win)

    for image in miniatures:
        image.draw_mini(
                win,
                data["landscape"][image.number]
            )

    if zoom > 0:
        miniatures[zoom-1].draw_half(win, data["landscape"][str(zoom)])
        if data["landscape"][str(zoom)]:
            for button in buttons_choose:
                button.draw(win)
        elif data["stars"] >= 100:
            for button in buttons_unlock:
                button.draw(win)
        else:
            button_back[0].draw(win)

    
    config.stars(data).draw(win)
    pygame.display.update()

def unlock(data, number):
    print(number)
    data["landscape"][str(number)]=True
    data["stars"] -= 100
    config.save_data(data)
    print(data)

def choose(data, number):
    print(number)
    data["landscape"]["used"]=number
    print(data)
    config.save_data(data)

def landscape_screen(win, data):
    loop = True
    miniatures = []
    zoom = 0
    for line in range(4):
        for column in range(5):
            image = config.landscape(
                    "image"+str((column+1)+5*(line))+".jpg",
                    (
                        100+column*(config.landscape_mini_width+(config.WIDTH - 5*config.landscape_mini_width-200)//4),
                        75+line*(config.landscape_mini_height+(config.HEIGHT-4*config.landscape_mini_height-75-125)//3)
                    )
                )
            miniatures.append(image)
    while loop:
        mouse_pos = pygame.mouse.get_pos()

        backward = config.Buttons(config.WIDTH//2-100, config.HEIGHT-100, 200,50, "Retour")
        mouse_on_button_backward = config.button_overlay([backward], mouse_pos,(200, 50))

        buttons_unlock = []
        buttons_unlock.append(config.Buttons(config.WIDTH//2-220, config.HEIGHT-60, 200,50,"Débloquer"))
        buttons_unlock.append(config.Buttons(config.WIDTH//2+20, config.HEIGHT-60, 200,50,"Retour"))
        mouse_on_button_unlock = config.button_overlay(buttons_unlock, mouse_pos,(200, 50))

        buttons_choose = []
        buttons_choose.append(config.Buttons(config.WIDTH//2-220, config.HEIGHT-60, 200,50,"Utiliser"))
        buttons_choose.append(config.Buttons(config.WIDTH//2+20, config.HEIGHT-60, 200,50,"Retour"))
        mouse_on_button_choose = config.button_overlay(buttons_choose, mouse_pos,(200, 50))

        button_back =[]
        button_back.append(config.Buttons(config.WIDTH//2-100, config.HEIGHT-60, 200,50,"Retour"))
        mouse_on_button_back = config.button_overlay(button_back, mouse_pos,(200, 50))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if zoom >0:
                    if not data["landscape"][str(zoom)] and mouse_on_button_unlock == 1:
                        zoom = 0
                    elif data["landscape"][str(zoom)] and mouse_on_button_choose == 1:
                        zoom = 0
                    elif data["landscape"]["used"] == zoom and mouse_on_button_back == 0:
                        zoom = 0
                    elif not data["landscape"][str(zoom)] and mouse_on_button_unlock == 0:
                        unlock(data, zoom)
                    elif data["landscape"][str(zoom)] and mouse_on_button_choose == 0:
                        choose(data,zoom)
                        zoom = 0
                elif mouse_on_button_backward != -1:
                    loop = False
                else:
                    for image in miniatures:
                        if (mouse_pos[0]>image.coord_mini[0] and mouse_pos[1]>image.coord_mini[1] and mouse_pos[0] < image.coord_mini[0]+config.landscape_mini_width and mouse_pos[1]<image.coord_mini[1]+config.landscape_mini_height):
                            zoom = int(image.number)
    
        refresh_screen(win, backward, zoom, miniatures, buttons_unlock, buttons_choose, data, button_back)
        