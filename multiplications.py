import pygame
import math
import os
import numpy


#Init stuffs
pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplications game ! by Wameuh")

# Clock stuffs
FPS = 30
clock = pygame.time.Clock()

#Colors
Black = (0,0,0)
White = (255,255,255)
Grey = (65,65,65)

#Text
ANS_FONT = pygame.font.SysFont('arial', 40)
ASK_FONT = pygame.font.SysFont('arial', 100)
SCORE_FONT = pygame.font.SysFont('arial',20)
RESULT_FONT = pygame.font.SysFont('arial', 100)

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

def graphical_answer(answers):
    retval = []
    gap = (WIDTH - RECT_W*NUM_ANS)/(NUM_ANS+1)
    for i in range(NUM_ANS):
        retval.append(Answer(gap+(gap+RECT_W)*i, -RECT_H, answers[i]))

    return retval

#refresh display
def refresh_display(answers, answers_list, loose):
    win.fill(Black)
    if loose:
        result_text_l1 = RESULT_FONT.render("Perdu !", 1, White)
        result_text_l2 = RESULT_FONT.render("Score : " + str(score), 1, White)
        win.blit(result_text_l1, (WIDTH//2-result_text_l1.get_width()//2, HEIGHT//2-result_text_l1.get_height()-25))
        win.blit(result_text_l2, (WIDTH//2-result_text_l2.get_width()//2, HEIGHT//2+25))
    
    else:
        for answer in answers:
            answer.draw(win)
        
        ask_text = ASK_FONT.render(str(answers_list[NUM_ANS][0])+"x"+str(answers_list[NUM_ANS][1]), 1, White)
        win.blit(ask_text, (WIDTH//2-ask_text.get_width()//2, 400))
        score_text = SCORE_FONT.render("Score : " + str(score), 1, White)
        win.blit(score_text, (10,10))

    pygame.display.update()



#rectangles
RECT_W = 70
RECT_H = 50
VEL_START = 1
score = 0
Vel_current = score/4+1
INCREASE_VEL = 1



class Answer(object):
    def __init__(self,x,y,value):
        self.x = x
        self.y = y
        self.value = value
        self.text = ANS_FONT.render(str(value), 1, White)
    
    def draw(self,win):
        pygame.draw.rect(win, White, (self.x-2, self.y-2, RECT_W+4, RECT_H+4))
        pygame.draw.rect(win, Grey, (self.x, self.y, RECT_W, RECT_H))
        win.blit(self.text, (self.x+(RECT_W-self.text.get_width())/2, self.y))


def main():
    global Vel_current
    global score
    global win
    answers_list = create_answer()
    answers = graphical_answer(answers_list)
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
        

        refresh_display(answers, answers_list, loose)

        if loose:
            Vel_current = VEL_START
            score = 0
            pygame.time.delay(5000)
            break

        if gagne:
            score +=1
            Vel_current = score/4+1
            break
    
    main()

if __name__ == "__main__":
    main()