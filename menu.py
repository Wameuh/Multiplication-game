import pygame
import config
import highscores
import games
import landscape


print("lancement du jeu")
#Init stuffs
pygame.init()
pygame.font.init()
win = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Multiplications game ! by Wameuh")

# Clock stuffs
clock = pygame.time.Clock()





def refresh_display_menu(title, buttons):
    win.fill(config.Color["Black"])

    title_text = config.FONT["TITLE_FONT"].render(title, 1, config.Title_color)
    win.blit(title_text, (config.WIDTH//2-title_text.get_width()//2, 10))

    for button in buttons:
        button.draw(win)
    
    data = config.get_data()
    config.stars(data).draw(win)

    pygame.display.update()
    

def button_set(items, mouse_pos):
    number_of_item = len(items)
    space = (config.HEIGHT - 200)//(2*number_of_item+1)
    buttons = [config.Buttons(config.WIDTH//2-config.BUTTON_WIDTH//2, 100+space*(items.index(item)*2+1), config.BUTTON_WIDTH, config.BUTTON_HEIGHT, item) for item in items]
    #overlay
    
    return buttons


def switch_game(ind, title, *items):
    data = config.get_data()
    if ind==0:
        games.play_game(win, config.WIDTH, config.HEIGHT, config.Color, config.FONT, clock, config.FPS)
    elif ind == 1:
        highscores.display_score(win, config.FONT, config.WIDTH, config.HEIGHT, config.Color)
        display_menu(title, *items)
    elif ind==2:
        landscape.landscape_screen(win, data)
        display_menu(title,*items)
    elif ind == 4:
        pygame.quit()
    else:
        display_menu(title, *items)


def display_menu(title, *items):
    loop = True
    while loop:
        mouse_pos = pygame.mouse.get_pos()
        buttons = button_set(items, mouse_pos)
        mouse_on_button = config.button_overlay(buttons, mouse_pos, (config.BUTTON_WIDTH, config.BUTTON_HEIGHT))
        clock.tick(config.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_on_button !=-1 :
                loop = False
        
        refresh_display_menu(title, buttons)
    
    switch_game(mouse_on_button, title, *items)

    display_menu(title, *items)

display_menu("Jeu des multiplications", "Jouer", "Tableau des scores", "Fonds d'écran", "Crédits", "Quitter")




