import pygame
import pygame.gfxdraw
import numpy as np
import matplotlib.backends.backend_agg as agg
import pylab

pygame.init()

displaySize = (1200,800)
surfaceSize = (1200,2200)
surface = pygame.surface.Surface(surfaceSize)
font = pygame.font.SysFont("monospace",16)
scroll_y = 0
    
class izvor:
    def __init__(self,x,y,u):
        self.x = x # pozicija X
        self.y = y # pozicija Y
        self.u = u # napon u voltima
        
    def draw(self): # metoda za crtanje simbola
        text.print(self.u,self.x+14,self.y-6,center=False)

        pygame.draw.line(surface,(0,0,0),(self.x-10,self.y),(self.x+10,self.y),2) # gornju crtu
        pygame.draw.line(surface,(0,0,0),(self.x-6,self.y+6),(self.x+6,self.y+6),4) # doljnju crtu
        
class switch:
    def __init__(self,x,y):
        self.x = x # pozicija X
        self.y = y # pozicija Y
        self.on = False # Stanje
        
    def update(self): # metoda za mjenjanje stanja sklopke
        self.on = not self.on
            
    def draw(self): # metoda za crtanje simbola
        ## kontakti
        pygame.draw.circle(surface,(0,0,0),(self.x,self.y),2) 
        pygame.draw.circle(surface,(0,0,0),(self.x-12,self.y-8),2)
        pygame.draw.circle(surface,(0,0,0),(self.x-12,self.y+8),2)
        ## smjer
        if self.on:
            pygame.draw.line(surface,(0,0,0),(self.x-1,self.y-1),(self.x-12,self.y-8),2)
        else:
            pygame.draw.line(surface,(0,0,0),(self.x-1,self.y-1),(self.x-12,self.y+6),2)
            
class otpornik:
    def __init__(self,x,y,r):
        self.x = x # pozicija X
        self.y = y # pozicija Y
        self.r = r # otpor u Ohm
        
    def draw(self): # metoda za crtanje simbola
        text.print(self.r,self.x+14,self.y-22,(0,0,255))

        pygame.draw.rect(surface,(0,0,0),(self.x,self.y-7,28,14),1) # tijelo
        
class kondenzator:
    def __init__(self,x,y,c):
        self.x = x # pozicija X
        self.y = y # pozicija Y
        self.c = c # kapacitet u F
        
    def draw(self): # metoda za crtanje
        text.print(self.c,self.x+3,self.y-22,(255,0,0))

        pygame.draw.line(surface,(0,0,0),(self.x,self.y-10),(self.x,self.y+10),1) # gornja crta
        pygame.draw.line(surface,(0,0,0),(self.x+6,self.y-10),(self.x+6,self.y+10),1) # doljnja crta
        
class zavojnica:
    def __init__(self,x,y,l):
        self.x = x # pozicija X
        self.y = y # pozicija Y
        self.l = l # induktivitet u H
        
    def draw(self): # metoda za crtanje
        text.print(self.l,self.x+24,self.y-16,(255,0,0))
        ## simbol
        pygame.gfxdraw.arc(surface,self.x+6,self.y+6,6,180,0,(0,0,0))
        pygame.gfxdraw.arc(surface,self.x+18,self.y+6,6,180,0,(0,0,0))
        pygame.gfxdraw.arc(surface,self.x+30,self.y+6,6,180,0,(0,0,0))
        pygame.gfxdraw.arc(surface,self.x+42,self.y+6,6,180,0,(0,0,0))
        
class wire:
    def __init__(self,points,w=2):
        self.p = points # cvorovi
        self.w = w # debljina zice
        
    def draw(self): # metoda za crtanje
        pygame.draw.lines(surface,(0,0,0),False,self.p,self.w)

## classa za ispis i upis velicina
class text:
    def __init__(self,text,x,y,color=(0,0,0)):
        self.x = x
        self.y = y
        self.text = text
        self.input = ""
        self.string = font.render(text,True,color)
    def pr(self,center = False):
        if center:
            rect = self.string.get_rect()
            surface.blit(self.string,(self.x-rect.width//2,self.y-rect.height//2))
        else:
            surface.blit(self.string,(self.x,self.y))
    def print(text,x,y,color=(0,0,0),center=True):
        text = font.render(text,True,color)
        rect = text.get_rect()
        surface.blit(text,(x-rect.width//2, y-rect.height//2) if center else (x,y))
        
    def removelast(self):
        self.input = self.input[:-1]
        self.string = font.render(self.text+self.input,True,(0,0,0))
    def append(self,char):
        self.input += char
        self.string = font.render(self.text+self.input,True,(0,0,0))
    def set_pos(self,x,y):
        self.x = x
        self.y = y

## classa za prikaz grapha
class graph:
    def __init__(self,x,y,w,h,dpi=100):
        self.x = x # pozicija X
        self.y = y # pozicija Y
        self.w = w # sirina
        self.h = h # visina
        self.fig = pylab.figure(figsize=(w/dpi,h/dpi), 
                   dpi=dpi, )
        
        self.chargingPoz = [((-0.368**x)+1)*100 for x in np.linspace(0,6,100)]
        self.chargingNeg = [((0.368**x)-1)*100  for x in np.linspace(0,6,100)]

        self.dischargingPoz = [(0.368**x)*100 for x in np.linspace(0,6,100)]
        self.dischargingNeg = [(-0.368**x)*100  for x in np.linspace(0,6,100)]
        
        self.data = None
        self.size = None
        
    def draw(self):
        if self.data != None and self.size != None:
            graph = pygame.image.fromstring(self.data, self.size, "RGB")
            surface.blit(graph,(self.x,self.y))
        
    def update(self,charging,tp):
        self.fig.clf()
        ax = self.fig.gca()
        ax.set_xlabel("Vrijeme (Tao)", fontsize=12)
        ax.set_ylabel("Napon (% od maksimalnog)",fontsize=12)
        ax.hlines(0, xmin=0, xmax=6, color='black')
        
        if charging:
            ax.vlines(1, ymin=0, ymax=100, color='gray')
            if tp == "RC":
                ax.hlines(63.2, xmin=0, xmax=6, color='gray')
                ax.plot(np.linspace(0,6,100),self.dischargingPoz)
                ax.plot(np.linspace(0,6,100),self.chargingPoz)
            elif tp == "RL":
                ax.hlines(36.8, xmin=0, xmax=6, color='gray')
                ax.plot(np.linspace(0,6,100),self.chargingPoz)
                ax.plot(np.linspace(0,6,100),self.dischargingPoz)
        else:
            ax.vlines(1, ymin=-100, ymax=100, color='gray')
            if tp == "RC":
                ax.hlines(36.8, xmin=0, xmax=6, color='gray')
                ax.plot(np.linspace(0,6,100),self.dischargingNeg)
                ax.plot(np.linspace(0,6,100),self.dischargingPoz)
            elif tp == "RL":
                ax.hlines(-36.8, xmin=0, xmax=6, color='gray')
                ax.plot(np.linspace(0,6,100),self.dischargingPoz)
                ax.plot(np.linspace(0,6,100),self.dischargingNeg)

        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        
        self.size = canvas.get_width_height()
        self.data = renderer.tostring_rgb()

def Input(string):
    typing = True
    txt = text(string,2,2)
    while typing:
        surface.fill((255,255,255))
        txt.pr()
        display.blit(surface,(0,0))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    txt.removelast()
                elif e.key <= 57 and e.key >= 48 or e.key == pygame.K_PERIOD:
                    txt.append(chr(e.key))
                elif e.key >= pygame.K_KP1 and e.key < pygame.K_KP0:
                    txt.append(chr(e.key+pygame.K_0-pygame.K_KP1+1))
                elif e.key == pygame.K_KP0:
                    txt.append('0')
                elif e.key == pygame.K_KP_PERIOD:
                    txt.append('.')
                elif e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    typing = False
    return txt.input
def validInput(string):
    while True:
        try:
            ret = eval(Input(string))
        except SyntaxError:
            continue
        if ret != 0.0:
            return ret
def update():
    sklopkaRC.update()
    sklopkaRL.update()
    RCgraf.update(sklopkaRC.on,"RC")
    RLgraf.update(sklopkaRL.on,"RL")
    
def draw():
    surface.fill((255,255,255))
    
    izvorRC.draw()
    sklopkaRC.draw()
    otpornikRC.draw()
    kondenzator.draw()
    for zica in RCzice:
        zica.draw()
        
    TaoRC.pr()
    RCgraf.draw()
    
    granica.draw()

    izvorRL.draw()
    sklopkaRL.draw()
    otpornikRL.draw()
    zavojnica.draw()
    for zica in RLzice:
        zica.draw()

    TaoRL.pr()
    RLgraf.draw()

display = pygame.display.set_mode((800,22))

otpor = validInput("Upisi vrijednost otpornika(Ohm):")
kapacitet = validInput("Upisi vrijednost kondenzatora(F):")
induktivitet = validInput("Upisi vrijednost zavojnice(H):")
    
pygame.display.quit()
pygame.display.init()

display = pygame.display.set_mode(displaySize)

TaoRC = float(otpor*kapacitet)
TaoRC = "Jedan tao u RC spoju traje "+str(TaoRC)+" sec"
TaoRC = text(TaoRC,20,120)

TaoRL = induktivitet/otpor
TaoRL = "Jedan tao u RL spoju traje "+str(TaoRL)+" sec"
TaoRL = text(TaoRL,20,1320)

izvorRC = izvor(20,70,"10V")
otpornikRC = otpornik(150,35,str(otpor)+" Ohm")
kondenzator = kondenzator(300,35,str(kapacitet)+" F")
sklopkaRC = switch(90,36)

RCzice = [wire(((20,70),(20,27),(77,27))),
          wire(((90,35),(150,35))),
          wire(((178,35),(300,35))),
          wire(((306,35),(348,35),(348
                                   ,100),(20,100),(20,75))),
          wire(((77,43),(77,100)))]

RCgraf = graph(20,150,1200,800)


granica = wire(((0,1150),(1200,1150)),10)


izvorRL = izvor(20,1270,"10V")
otpornikRL = otpornik(150,1235,str(otpor)+" Ohm")
zavojnica = zavojnica(275,1230,str(induktivitet)+" H")
sklopkaRL = switch(90,1236)

RLzice = [wire(((20,1270),(20,1227),(77,1227))),
          wire(((90,1235),(150,1235))),
          wire(((178,1235),(275,1235))),
          wire(((323,1235),(348,1235),(348,1300),(20,1300),(20,1275))),
          wire(((77,1243),(77,1300)))]

RLgraf = graph(20,1350,1200,800)

update()
draw()
display.blit(surface,(0,scroll_y))
pygame.display.update()

while True:
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 4:
                scroll_y = min(scroll_y + 50,0)
            elif e.button == 5:
                scroll_y = max(scroll_y - 50,displaySize[1]-surfaceSize[1])
            display.blit(surface,(0,scroll_y))
            pygame.display.update()
                
        elif e.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                update()
                draw()
                display.blit(surface,(0,scroll_y))
                pygame.display.update()
                    
