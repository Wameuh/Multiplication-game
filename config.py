import pygame
import json

WIDTH, HEIGHT = 800, 600
FPS = 30
pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))

#Colors
Color = {
    "Black" :(0,0,0),
    "White":(255,255,255),
    "Grey" : (65,65,65),
    "Shiny_grey" : (125,125,125)
}

star_color =  Color["White"]

#Size of things
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 50

#Title
Title_color = Color["White"]

#Buttons
Button_color = Color["Grey"]
Button_color_over = Color["Black"]
Button_border_color = Color["White"]
Button_border_width = 2
button_text_color = Color["White"]



def button_overlay(buttons, mouse_pos, button_size):
    mouse_on_button = -1

    for button in buttons:
        if (mouse_pos[1] > button.y and mouse_pos[1] < button.y+button_size[1]) and (mouse_pos[0] > button.x and mouse_pos[0] < button.x+button_size[0]):
            buttons[buttons.index(button)].color = Color["Shiny_grey"]
            mouse_on_button = buttons.index(button)
    
    return mouse_on_button



#Fonts

pygame.font.init()
FONT = {
    "TITLE_FONT":pygame.font.SysFont('arial', 50),
    "SUBTITLE_FONT":pygame.font.SysFont('arial', 20),
    "BUTTON_FONT":pygame.font.SysFont('arial', 30),
    "HS_FONT":pygame.font.SysFont('arial', 40),
    "ANS_FONT":pygame.font.SysFont('arial', 40),
    "ASK_FONT":pygame.font.SysFont('arial', 100),
    "LOOSE_FONT":pygame.font.SysFont('arial',50),
    "SCORE_FONT":pygame.font.SysFont('arial',20),
    "RESULT_FONT":pygame.font.SysFont('arial', 100),
    "STAR_FONT":pygame.font.SysFont('arial',20)
    }


class Buttons(object):
    def __init__(self,x ,y, width, height, text):
        if len(text)>0:
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text
            self.color = Color["Grey"]
        else:
            self.x = 0
            self.y = 0
            self.width = 0
            self.height = 0
            self.text = text
            self.color = Color["Grey"]
        
    
    def draw(self,win):
        text = FONT["BUTTON_FONT"].render(str(self.text), 1, button_text_color)
        pygame.draw.rect(win, Button_border_color, (self.x-2, self.y-2, self.width+4, self.height+4))
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        win.blit(text, (self.x+(self.width-text.get_width())/2, self.y+(self.height-text.get_height())//2))



def get_data():
    data = {}

    try:
        with open("highscores.json", "r") as file:
            try:
                data = json.load(file)
            except ValueError as e:
                pass
    except FileNotFoundError:
        data = {
            "highscores": {
                "1": {
                    "name": "*", "score": 0
                    },
                 "2": {
                     "name": "*", "score": 0
                     },
                 "3": {
                     "name": "*", "score": 0
                     },
                "4": {
                    "name": "*", "score": 0
                    },
                "5": {
                    "name": "*", "score": 0
                    }
                },
            "stars": 0,
            "landscape":{
                "used":0,

            }
        }
        for i in range(20):
            data["landscape"][i+1] = False

        save_data(data)

    return data


def save_data(data):
    with open("highscores.json", "w", encoding = 'utf-8') as file:
        file.write(json.dumps(data))

#landscape
landscape_mini_width = WIDTH//7
landscape_mini_height = HEIGHT//7
landscape_half_width = WIDTH//4*3
landscape_half_height = HEIGHT//4*3

class landscape:
    def __init__(self, name, coord =()):
        self.name = name
        self.number = name[5:-4]
        self.coord_mini = coord
    
    def draw(self,win):
        try :
            self.image_full = pygame.image.load("./landscape_full/image"+self.number+".png")
        except FileNotFoundError:
            self.image = pygame.image.load("./landscape/"+self.name).convert()
            self.image_full = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
            pygame.image.save(self.image_full, "./landscape_full/image"+self.number+".png")
        win.blit(self.image_full, (0,0))
    
    def draw_mini(self,win, valid):
        try:
            self.image_mini = pygame.image.load("./landscape_mini/image"+self.number+".png")
        except FileNotFoundError:
            image_full = pygame.image.load("./landscape/"+self.name).convert()
            self.image_mini = pygame.transform.scale(image_full, (landscape_mini_width, landscape_mini_height))
            pygame.image.save(self.image_mini, "./landscape_mini/image"+self.number+".png")
            print("enregistrement de l'image numérp" + str(self.number))

        win.blit(self.image_mini, self.coord_mini)

        if not valid:
            pygame.draw.line(win, Color["Black"], self.coord_mini, (self.coord_mini[0]+landscape_mini_width,self.coord_mini[1]+landscape_mini_height),10)
            pygame.draw.line(win, Color["Black"], (self.coord_mini[0], self.coord_mini[1]+landscape_mini_height),(self.coord_mini[0]+landscape_mini_width,self.coord_mini[1]),10)

    def draw_half(self,win, valid):
        image_full = pygame.image.load("./landscape/"+self.name).convert()
        self.image_half = pygame.transform.scale(image_full, (landscape_half_width, landscape_half_height))
        
        win.blit(self.image_half, ((WIDTH-landscape_half_width)//2, 75))
        pygame.draw.rect(win, Color["Black"], ((WIDTH-landscape_half_width)//2, 75+landscape_half_height, landscape_half_width, HEIGHT-landscape_half_height))
        pygame.draw.rect(win, Color["Black"], (landscape_half_width+(WIDTH-landscape_half_width)//2, 75, landscape_half_width,landscape_half_height))

        if not valid:
            cost_text = FONT["STAR_FONT"].render("100", 1, Color["White"])
            win.blit(cost_text,((WIDTH-landscape_half_width)//2+landscape_half_width+10, HEIGHT//2-cost_text.get_height()))
            star = pygame.transform.scale(pygame.image.load("star.png").convert_alpha(), (20,20))
            win.blit(star, ((WIDTH-landscape_half_width)//2+landscape_half_width+10+2+cost_text.get_width(), HEIGHT//2-cost_text.get_height()))


class stars:
    def __init__(self, data, coord=[]):
        self.image = pygame.transform.scale(pygame.image.load("star.png").convert_alpha(), (20,20))
        self.number = data["stars"]
        self.coord = coord

    def draw(self, win):
        win.blit(self.image, (WIDTH-100, 20))
        star_text = FONT["STAR_FONT"].render(": " + str(self.number), 1, star_color)
        win.blit(star_text, (WIDTH - 75, 20))
    
    def draw_star(self, win):
        win.blit(self.image,(self.coord[0], self.coord[1]))

    def __repr__(self):
        return f"({self.coord[0]},{self.coord[1]})"