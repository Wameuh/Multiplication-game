import pygame
import numpy
import loose as loose_page
import config


#Size of things
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 50
RECT_W = 70
RECT_H = 50


#numbers
numbers = []
for i in range(10):
    for j in range(10):
        numbers.append([i+1,j+1,(i+1)*(j+1)])

#answers
NUM_ANS = 3
def create_answer():

    result_place = numpy.random.choice(numpy.array(NUM_ANS))
    result = numbers[numpy.random.choice(100)]

    retval = []

    deviation = []
    for i in range(15):
        deviation.append(result[2]+i+1)
        if result[2]-i-1 > 1:
            deviation.append(result[2]-i-1)

    for i in range(NUM_ANS):
        if i == result_place:
            retval.append(result[2])
        else:
            retval.append(numpy.random.choice(deviation))

    retval.append(result)
    retval.append(result_place)
    return retval

def graphical_answer(answers, WIDTH, FONT, Color):
    retval = []
    gap = (WIDTH - RECT_W*NUM_ANS)/(NUM_ANS+1)
    for i in range(NUM_ANS):
        retval.append(Answer(gap+(gap+RECT_W)*i, -RECT_H, answers[i], FONT, Color))

    return retval

#refresh display
def refresh_display_game(answers, answers_list, loose, win, FONT, WIDTH, HEIGHT, Color, data, clock):
    win.fill(Color["Black"])
    if data["landscape"]["used"] > 0:
        config.landscape("image"+str(data["landscape"]["used"])+".jpg").draw(win)

    for answer in answers:
        answer.draw(win, Color)
        
    ask_text = FONT["ASK_FONT"].render(str(answers_list[NUM_ANS][0])+"x"+str(answers_list[NUM_ANS][1]), 1, Color["White"])
    win.blit(ask_text, (WIDTH//2-ask_text.get_width()//2, 400))
    score_text = FONT["SCORE_FONT"].render("Score : " + str(score), 1, Color["White"])
    win.blit(score_text, (10,10))
    
    config.stars(data).draw(win)
    
    ##  Afficher FPS -> win.blit(config.FONT["STAR_FONT"].render(str(int(clock.get_fps())), 0, config.Color["White"]), (10,config.HEIGHT-50))
    pygame.display.update()

#rectangles
VEL_START = 2
score = 0
Vel_current = numpy.log(2*score+1)+VEL_START+score/4
INCREASE_VEL = 1



class Answer(object):
    def __init__(self,x,y,value, FONT, Color):
        self.x = x
        self.y = y
        self.value = value
        self.text = FONT["ANS_FONT"].render(str(value), 1, Color["White"])
    
    def draw(self,win, Color):
        pygame.draw.rect(win, Color["White"], (self.x-2, self.y-2, RECT_W+4, RECT_H+4))
        pygame.draw.rect(win, Color["Grey"], (self.x, self.y, RECT_W, RECT_H))
        win.blit(self.text, (self.x+(RECT_W-self.text.get_width())/2, self.y))

def play_game(win, WIDTH, HEIGHT, Color, FONT, clock, FPS):
    global Vel_current
    global score
    data = config.get_data()

    if Vel_current == VEL_START:
        score = 0
    
    print(Vel_current)
    answers_list = create_answer()
    answers = graphical_answer(answers_list, WIDTH, FONT, Color)
    gagne = False
    loose = False
    while True:
        clock.tick(FPS)
        for answer in answers:
            answer.y += Vel_current
            if answer.y + RECT_H > HEIGHT:
                loose = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if (answers[answers_list[NUM_ANS+1]].x < mouse_pos[0] < answers[answers_list[NUM_ANS+1]].x + RECT_W) and (
                    answers[answers_list[NUM_ANS+1]].y < mouse_pos[1] < answers[answers_list[NUM_ANS+1]].y + RECT_H):
                    gagne = True
            if event.type == pygame.KEYDOWN:
                
                if event.unicode == str(answers_list[NUM_ANS+1]+1):
                    gagne = True


        refresh_display_game(answers, answers_list, loose, win, FONT, WIDTH, HEIGHT, Color, data, clock)

        if loose:
            Vel_current = VEL_START
            break

        if gagne:
            score +=1
            Vel_current = numpy.log(2*score+1)+VEL_START+score/4
            break
    
    if gagne:
        play_game(win, WIDTH, HEIGHT, Color, FONT, clock, FPS)
    
    if loose:
        loose_page.loose_screen(win, Color, data, score, WIDTH, HEIGHT, FONT, FPS, clock)




