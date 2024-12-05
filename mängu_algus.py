import pygame
import sys

pygame.init()
ekr_laius=500
ekr_pikkus=600
stardi_ekraan=pygame.display.set_mode((ekr_laius,ekr_pikkus))
pygame.display.set_caption("BINGO")

roosa=(245,148,148)
valge=(255,255,255)
must=(0,0,0)



def start_screen():
    stardi_ekraan.fill(roosa)
    nimi=input("Sisesta oma nimi:")
    font=pygame.font.SysFont("arial",40)
    mängu_tiitel=font.render("Bingo",True,valge)
    stardi_nupp=font.render("Start",True,valge)
    stardi_ekraan.blit(mängu_tiitel, (ekr_laius/2 - mängu_tiitel.get_width()/2, ekr_pikkus/2 - mängu_tiitel.get_height()/2))
    stardi_ekraan.blit(stardi_nupp, (ekr_laius/2 - stardi_nupp.get_width()/2, ekr_pikkus/2 + stardi_nupp.get_height()/2))
    pygame.display.update()

mäng=True
while mäng:
    for event in pygame.event.get(): 
       if event.type == pygame.QUIT:
           mäng=False
    start_screen()

pygame.quit()