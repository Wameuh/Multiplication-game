import pygame
import config


def refresh_display_score(data, win, FONT, HEIGHT, WIDTH, Color, backward):
    win.fill(Color["Black"])

    title = FONT["TITLE_FONT"].render("Tableau des scores", 1, Color["White"])
    win.blit(title, (WIDTH//2-title.get_width()//2, 10))

    try:

        for highscore in data["highscores"]:
            highscore_name = FONT["HS_FONT"].render(data["highscores"][highscore]["name"], 1, Color["White"])
            win.blit(highscore_name, (100, 50 + int(highscore)*75))

            win.blit(FONT["HS_FONT"].render(":", 1, Color["White"]), (WIDTH//2, 50 + int(highscore)*75))

            highscore_score = FONT["HS_FONT"].render(str(data["highscores"][highscore]["score"]), 1, Color["White"])
            win.blit(highscore_score, (WIDTH-100-highscore_score.get_width(),  50 + int(highscore)*75))


    except KeyError as e:
        no_data_text = FONT["HS_FONT"].render("Pas de meilleur score enregistré", 1, Color["White"])
        win.blit(no_data_text, (WIDTH//2-no_data_text.get_width()//2, HEIGHT//2))

    backward.draw(win)

     
    config.stars(data).draw(win)
    pygame.display.update()

def display_score(win, FONT, WIDTH, HEIGHT, Color):
    loop = True
    
    data = config.get_data()
    while loop:
        
        mouse_pos = pygame.mouse.get_pos()
        backward = config.Buttons(WIDTH//2-100, HEIGHT-100, 200,50, "Retour")
        mouse_on_button = config.button_overlay([backward], mouse_pos,(200, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and mouse_on_button != -1:
                loop = False
    
        refresh_display_score(data, win, FONT, HEIGHT, WIDTH, Color, backward)

