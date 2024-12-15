#https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=306s
import pygame
import sys
import pygame.freetype
from pygame.sprite import Sprite
import pygame.rect
from enum import Enum
import random

hele_roosa=(245,148,148)
tume_roosa=(238,125,125)
hele_lilla=(204,153,255)
tume_lilla=(178,102,255)
valge=(255,255,255)
must=(0,0,0)

def loo_tekstiga_kast(tekst,fondi_suurus,taustavärv,teksti_värv):
    font=pygame.freetype.SysFont("Courier",fondi_suurus,bold=True)
    surface,_=font.render(text=tekst,fgcolor=teksti_värv,bgcolor=taustavärv)
    return surface.convert_alpha()

class UIElement(Sprite):
    def __init__(self, asetus, tekst, fondi_suurus,taustavärv,teksti_värv,action):

        super().__init__()

        self.hiir_hover=False
        self.taustavärv = taustavärv
        self.action=action
        
        default_image=loo_tekstiga_kast(tekst, fondi_suurus,taustavärv,teksti_värv)
        highlighted_image=loo_tekstiga_kast(tekst, fondi_suurus*1.2,taustavärv,teksti_värv)
        self.images=[
            default_image,
            highlighted_image
            ]
        self.rects=[
            default_image.get_rect(center=asetus),
            highlighted_image.get_rect(center=asetus)
            ]
        self.rect=self.rects[0]

    @property
    def image(self):
        return self.images[1] if self.hiir_hover else self.images[0]
    
    def update(self, mouse_pos,mouse_up):
        self.rects[1] if self.hiir_hover else self.rects[0]
        if self.rect.collidepoint(mouse_pos):
            self.hiir_hover=True
            if mouse_up:
                return self.action
        else:
            self.hiir_hover=False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class mängu_olek(Enum):
    tiitel=0
    start=1
    play=2
    quit=-1


def stardiekraan(screen):
    start=UIElement(asetus= (400, 400), fondi_suurus=30, taustavärv=hele_roosa, teksti_värv=valge,tekst="Start",action=mängu_olek.start)
    quit=UIElement(asetus= (400, 500), fondi_suurus=30, taustavärv=hele_roosa, teksti_värv=valge,tekst="Quit",action=mängu_olek.quit)
    pealkiri=UIElement(asetus= (400, 200), fondi_suurus=50, taustavärv=hele_roosa, teksti_värv=valge,tekst="BINGO!",action=None)


    while True:
        mouse_up=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONUP and event.button==1:
                mouse_up=True
        
        screen.fill(hele_roosa)
        pealkiri.draw(screen)
        quit_action=quit.update(pygame.mouse.get_pos(),mouse_up)

        if quit_action==mängu_olek.quit:
            pygame.quit()
            sys.exit()
        quit.draw(screen)
        start_action=start.update(pygame.mouse.get_pos(),mouse_up)
        if start_action==mängu_olek.start:
            return start_action
        start.draw(screen)
        pygame.display.flip()

def vali_ikoon(screen):
    return_nupp=UIElement(
        asetus=(100,560),
        fondi_suurus=30,
        taustavärv=hele_lilla,
        teksti_värv=valge,
        tekst="Return",
        action=mängu_olek.tiitel
        )
    
    play=UIElement(
        asetus=(700,560),
        fondi_suurus=30,taustavärv=hele_lilla,
        teksti_värv=valge,
        tekst="Play",
        action=mängu_olek.play
        )
    while True:
        mouse_up=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONUP and event.button==1:
                mouse_up=True
        screen.fill(hele_lilla)
        return_action=return_nupp.update(pygame.mouse.get_pos(),mouse_up)
        if return_action is not None:
            return return_action
        return_nupp.draw(screen)
        play_action=play.update(pygame.mouse.get_pos(),mouse_up)
        if play_action is not None:
            return play_action
        play.draw(screen)
        pygame.display.flip()


        


def bingo_ekraan(screen):
    pealkiri=UIElement(asetus= (400, 40), fondi_suurus=50, taustavärv=hele_roosa, teksti_värv=valge,tekst="BINGO!",action=None)
    kaardi_taust=(100,80,600,500)
    bingokaart_numbrid=bingokaart()
    
    while True:
        mouse_up=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(hele_roosa)
        pygame.draw.rect(screen,valge,kaardi_taust,border_radius=20)
        pealkiri.draw(screen)
        x=120
        y=100
        for rida in bingokaart_numbrid:
            for number in rida:
                numbri_ruut=UIElement((x,y),number,40,valge,must, action=None)
                numbri_ruut.draw(screen)
                x+=120
            y+=100
     
        pygame.display.flip()
        
def bingokaart():
    kaart = []
    olnud_numbrid = set()
    for rida in range(5):
        rea_numbrid = []
        for veerg in range(5):
            if rida == 2 and veerg == 2:
                rea_numbrid.append('o')
            elif veerg == 0:
                while True:
                    number = random.randint(1, 15)
                    if number not in olnud_numbrid:
                        rea_numbrid.append(str(number))
                        olnud_numbrid.add(number)
                        break
                    else:
                        continue
            elif veerg == 1:
                while True:
                    number = random.randint(16, 30)
                    if number not in olnud_numbrid:
                        rea_numbrid.append(str(number))
                        olnud_numbrid.add(number)
                        break
                    else:
                        continue
            elif veerg == 2:
                while True:
                    number = random.randint(31, 45)
                    if number not in olnud_numbrid:
                        rea_numbrid.append(str(number))
                        olnud_numbrid.add(number)
                        break
                    else:
                        continue
            elif veerg == 3:
                while True:
                    number = random.randint(46, 60)
                    if number not in olnud_numbrid:
                        rea_numbrid.append(str(number))
                        olnud_numbrid.add(number)
                        break
                    else:
                        continue
            elif veerg == 4:
                while True:
                    number = random.randint(61, 75)
                    if number not in olnud_numbrid:
                        rea_numbrid.append(str(number))
                        olnud_numbrid.add(number)
                        break
                    else:
                        continue
        kaart.append(rea_numbrid)
    return kaart


def main():
    pygame.init()
    mäng=mängu_olek.tiitel
    ekraan=pygame.display.set_mode((800, 600))
    clock=pygame.time.Clock()
    while True:
        if mäng==mängu_olek.tiitel:
            mäng=stardiekraan(ekraan)
        if mäng==mängu_olek.start:
            mäng=vali_ikoon(ekraan)
        if mäng==mängu_olek.play:
            mäng==bingo_ekraan(ekraan)
        if mäng==mängu_olek.quit:
            mäng=stardiekraan(ekraan)

        clock.tick(60)
        


main()