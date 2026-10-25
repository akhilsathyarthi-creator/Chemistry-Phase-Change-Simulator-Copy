#Starter Code

import pygame
from ui_controls import *
import random

pygame.init()

WIDTH = 800
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame UI Controls Activity X")

clock = pygame.time.Clock()
FPS = 60

Temp = 0
current_element = "water"

atoms = []
vector = pygame.math.Vector2

font = pygame.font.SysFont("Comic Sans MS", 24)

# ---------------- TEMPERATURE SLIDER ----------------
def on_t_change(val):
    global Temp
    Temp = int(val)

slider_t = Slider(
    x=600, y=34, w=20, h=250,
    min_value=0, max_value=1000, value=0,
    color="red",
    on_change=on_t_change,
    continuous=True,
    text="Temperature(in Kelvin)",
    orientation="vertical",
    show_value=True,
    value_digits=0
)

# ---------------- RADIO BUTTONS ----------------
def on_radio_change(selected):
    global current_element
    current_element = selected.label

group = RadioGroup(on_change=on_radio_change)

rb1 = RadioButton(540,120,10,color="seagreen",selected=True,label="water",group=group,text_color="red")
rb2 = RadioButton(540,150,10,color="seagreen",selected=False,label="neon",group=group,text_color="blue")
rb3 = RadioButton(540,180,10,color="seagreen",selected=False,label="oxygen",group=group,text_color="yellow")


# ---------------- ELEMENT CLASS ----------------
class Elements():

    def __init__(self,x,y,target):

        self.position = vector(x,y)

        self.velocity = vector(
            random.uniform(-1,1),
            random.uniform(-1,1)
        )

        self.target = target

        self.color = "white"
        self.fp = 0
        self.bp = 0
        self.state = "gas"

    # -------- assign element properties --------
    def Element(self):

        if current_element == "oxygen":
            self.color = "red"
            self.bp = 90.19
            self.fp = 54.36

        elif current_element == "water":
            self.color = "blue"
            self.fp = 273.15
            self.bp = 373.15

        elif current_element == "neon":
            self.color = "cyan"
            self.fp = 24.56
            self.bp = 27.1

    # -------- determine state --------
    def element_state(self):

        if Temp <= self.fp:
            self.state = "solid"

        elif Temp >= self.bp:
            self.state = "gas"

        else:
            self.state = "liquid"

    # -------- movement physics --------
    def Element_move(self):

        # temperature controls violence
        speed = max(Temp / 200, 0.2)

        # ---------- SOLID ----------
        if self.state == "solid":

            # move toward cube lattice
            direction = self.target - self.position
            self.position += direction * 0.1

            # vibration based on temperature
            vibration = vector(
                random.uniform(-1,1),
                random.uniform(-1,1)
            ) * (Temp/200)

            self.position += vibration


        # ---------- LIQUID ----------
        elif self.state == "liquid":

            self.position += self.velocity * speed * 0.5

            # gravity keeps liquid at bottom
            self.velocity.y += 0.05

            if self.position.x <= 0 or self.position.x >= 500:
                self.velocity.x *= -1

            if self.position.y >= 480:
                self.position.y = 480
                self.velocity.y *= -0.3


        # ---------- GAS ----------
        elif self.state == "gas":

            self.position += self.velocity * speed * 2

            if self.position.x <= 0 or self.position.x >= 500:
                self.velocity.x *= -1

            if self.position.y <= 0 or self.position.y >= 480:
                self.velocity.y *= -1


    def draw(self,screen):

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.position.x),int(self.position.y)),
            3
        )


# ---------------- CREATE ATOMS ----------------

grid_size = 8
spacing = 20

for i in range(40):

    x = random.randint(0,400)
    y = random.randint(0,400)

    row = i // grid_size
    col = i % grid_size

    target_x = 100 + col * spacing
    target_y = 460 - row * spacing

    target = vector(target_x,target_y)

    atoms.append(Elements(x,y,target))


widgets = [slider_t,rb1,rb2,rb3]


# ---------------- MAIN LOOP ----------------

running = True

while running:

    pygame.draw.rect(screen,"lightgray",(0,0,500,480))
    pygame.draw.rect(screen,"gray",(500,0,300,480))

    for atom in atoms:

        atom.Element()
        atom.element_state()
        atom.Element_move()
        atom.draw(screen)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        for w in widgets:
            w.handle_event(event)

    for w in widgets:
        w.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()