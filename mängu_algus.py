#https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=306s
import pygame
import sys
import pygame.freetype
from pygame.sprite import Sprite
import pygame.rect
from enum import Enum
import random

#värvid
hele_roosa=(245,148,148)
hele_lilla=(204,153,255)
tume_lilla=(178,102,255)
valge=(255,255,255)
must=(0,0,0)
punane=(255,0,0)
sinine=(0,0,225)
roheline=(0,225,128)
tume_roosa=(225,0,255)

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
    number=False
    

class ShapeElement(Sprite):
    def __init__(self, asetus, kujund, suurus, värv, hover_scale=1.2, action=None):
        super().__init__()
        
        self.hiir_hover = False
        self.action = action
        self.kujund = kujund 
        self.suurus = suurus
        self.värv = värv
        self.asetus=asetus
        
        if kujund=="ruut":
            self.default_surface = self._create_shape_surface(suurus, värv)
            self.hover_surface = self._create_shape_surface(int(suurus * hover_scale), värv)
            self.images = [self.default_surface, self.hover_surface]
            self.rects = [
                self.default_surface.get_rect(center=asetus),
                self.hover_surface.get_rect(center=asetus),
            ]
            self.rect = self.rects[0]

    def _create_shape_surface(self, suurus, värv):
        surface = pygame.Surface((suurus, suurus), pygame.SRCALPHA) 
        if self.kujund == "ruut":
            pygame.draw.rect(surface, värv, (0, 0, suurus, suurus),border_radius=10)
        return surface

    @property
    def image(self):
        return self.images[1] if self.hiir_hover else self.images[0]

    def update(self, mouse_pos, mouse_up):
        self.rect = self.rects[1] if self.hiir_hover else self.rects[0]
        if self.rect.collidepoint(mouse_pos):
            self.hiir_hover = True
            if mouse_up:
                return self.action
        else:
            self.hiir_hover = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
   
   

def create_süda(size, color, alpha,x,y):
    icon = pygame.Surface((size, size), pygame.SRCALPHA)  # Enable alpha channel
    südame_suurus=size/2*1.5
    icon.fill((0, 0, 0, 0))  # Fully transparent background
    cx, cy = südame_suurus // 2, südame_suurus // 2  # Center of the icon
    left_circle = (cx - size // 6, cy - size // 8)
    right_circle = (cx + size // 6, cy - size // 8)
    bottom_tip = (cx, cy + size // 3)
    pygame.draw.circle(icon, color + (alpha,), left_circle, size // 4.75)
    pygame.draw.circle(icon, color + (alpha,), right_circle, size // 4.75)
    pygame.draw.polygon(icon, color + (alpha,), [
        (cx - size // 3, cy),
        bottom_tip,
        (cx + size // 3, cy),
    ])
    return icon,(x-cx,y-cy)
        
       


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
    pealkiri=UIElement(
        asetus=(400,100),
        fondi_suurus=60,
        taustavärv=hele_lilla,
        teksti_värv=valge,
        tekst="Vali värv!",
        action=None
        )
    
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
    
    valiku_taust=(100,200,600,200)
    värvid=[ShapeElement(asetus=(200,300),kujund="ruut",suurus=100,värv=punane,action="Valisid punase!"),
            ShapeElement(asetus=(325,300),kujund="ruut",suurus=100,värv=sinine,action="Valisid sinise!"),
            ShapeElement(asetus=(450,300),kujund="ruut",suurus=100,värv=roheline,action="Valisid rohelise!"),
            ShapeElement(asetus=(575,300),kujund="ruut",suurus=100,värv=tume_roosa,action="Valisid roosa!")
            ]
    global valitud_värv
    valitud_värv=None
    while True:
        mouse_up=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONUP and event.button==1:
                mouse_up=True
        screen.fill(hele_lilla)
        pealkiri.draw(screen)
        return_action=return_nupp.update(pygame.mouse.get_pos(),mouse_up)
        if return_action is not None:
            return return_action
        return_nupp.draw(screen)
        play_action=play.update(pygame.mouse.get_pos(),mouse_up)
        if play_action is not None:
            return play_action
        play.draw(screen)
        pygame.draw.rect(screen,valge,valiku_taust,border_radius=20) 
        for värv in värvid:
            värv.draw(screen)
            värv.update(pygame.mouse.get_pos(),mouse_up)
            if mouse_up:
                x,y=pygame.mouse.get_pos()
                värvi_ala=pygame.Rect(värv.asetus[0]-50,värv.asetus[1]-50,värv.suurus*1.2,värv.suurus*1.2)
                if värvi_ala.collidepoint(x,y):
                    valitud_värv=värv.värv
            värv.draw(screen)
        pygame.display.flip()

def bingo_ekraan(screen):
    pealkiri=UIElement(asetus= (100, 40), fondi_suurus=50, taustavärv=hele_roosa, teksti_värv=valge,tekst="BINGO!",action=None)
    kaardi_taust=(125,80,550,500)
    numbri_taust=(200,10,400,60)
    bingo=bingokaart()
    olnud_number=None
    global valitud_värv
    kas_valitud=[]
    for i in range(5):
        valik=[]
        for j in range(5):
            valik.append(False)
        kas_valitud.append(valik)
   
    while True:
        mouse_up=False

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONUP and event.button==1:
                mouse_up=True
                mx,my=pygame.mouse.get_pos()
                for i in range(5):
                        for j in range(5):
                            x=200+j*100
                            y=123.5+i*100
                            ruudu_ala=pygame.Rect(x,y,40,40)
                            if ruudu_ala.collidepoint(mx,my):
                                    kas_valitud[i][j]=not kas_valitud[i][j]
    


        screen.fill(hele_roosa)
        pygame.draw.rect(screen,valge,kaardi_taust,border_radius=20)
        pealkiri.draw(screen)
        pygame.draw.rect(screen, valge,numbri_taust,border_radius=20)
        y=123.5
        for i in range(len(bingo)):
            x=200
            for j in range(len(bingo[i])):
                number=UIElement((x,y),bingo[i][j],35,valge,must, action=mängu_olek.number)
                number.draw(screen) 
                number.update(pygame.mouse.get_pos(),mouse_up)
                number.draw(screen)
                if kas_valitud[i][j]==True:
                    kujund,asukoht=create_süda(100,valitud_värv,128,x,y)
                    screen.blit(kujund,asukoht)
                x+=100
            y+=100

        numbri_nupp = UIElement(asetus=(400, 40), tekst="Uus number:", fondi_suurus=20, taustavärv=valge, teksti_värv=hele_roosa, action=vaheta_number)
        numbri_nupp.draw(screen)
        if olnud_number is not None:
            olnud_number.draw(screen)
        uusnumber=numbri_nupp.update(pygame.mouse.get_pos(),mouse_up)
        if uusnumber is not None:
            number = UIElement(asetus=(500, 40), tekst=uus_number(set()), fondi_suurus=20, taustavärv=valge, teksti_värv=hele_roosa, action=None)
            number.draw(screen)
            olnud_number=number

        
        pygame.display.flip()

def uus_number(olnud_numbrid):
    kõik_numbrid = set(range(1, 76))
    numbreid_alles = kõik_numbrid - olnud_numbrid
    if numbreid_alles == {}:
        print('Numbrid on otsas!')
        return None
    else: 
        number = random.choice(list(numbreid_alles))
        olnud_numbrid.add(number)
        print(f'uus number on {number}')
        return str(number)

def vaheta_number():
    number = uus_number(set())
    return number
        
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