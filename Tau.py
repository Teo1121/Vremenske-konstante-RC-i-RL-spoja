import pygame
import pygame.gfxdraw
import numpy as np
import matplotlib.backends.backend_agg as agg # use own implementation
import pylab
from time import time

pygame.init()

displaySize = (1200,950)
surfaceSize = (1200,2150)
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

        self.I = 0
        self.U = 0
    def draw(self): # metoda za crtanje
        text.print(self.c,self.x+3,self.y-22,(255,0,0))

        pygame.draw.line(surface,(0,0,0),(self.x,self.y-10),(self.x,self.y+10),1) # gornja crta
        pygame.draw.line(surface,(0,0,0),(self.x+6,self.y-10),(self.x+6,self.y+10),1) # doljnja crta

        # smijer struje
        pygame.draw.line(surface,(220,100,20),(self.x+int(self.I/3),self.y+16),(self.x-int(self.I/3),self.y+16))
        pygame.draw.rect(surface,(220,100,20),(self.x+int(self.I/3),self.y+14,5,5))
        
    def update(self,state,t):
        if state: # punjenje
            self.U = 100*(1-np.e**(-t/1)) # napon u postocima i tau u intervalima od 1 s
            self.I = 100*np.e**(-t/1)
        else:
            self.U = 100*np.e**(-t/1)
            self.I = -100*np.e**(-t/1)
        
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

        # smijer struje
        pygame.draw.line(surface,(220,100,20),(self.x+24+int(self.I/3),self.y+16),(self.x+24-int(self.I/3),self.y+16))
        pygame.draw.rect(surface,(220,100,20),(self.x+22+int(self.I/3),self.y+14,5,5))
        
    def update(self,state,t):
        if state: # punjenje
            self.I = 100*(1-np.e**(-t/1)) # napon u postocima i Tau u intervalima od 1 s
            self.U = 100*np.e**(-t/1)
        else:
            self.I = 100*np.e**(-t/1)
            self.U = -100*(1-np.e**(-t/1))
        
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
    # metoda za ispis    
    def pr(self,center = False):
        if center:
            rect = self.string.get_rect()
            surface.blit(self.string,(self.x-rect.width//2,self.y-rect.height//2))
        else:
            surface.blit(self.string,(self.x,self.y))
    # staticka matoda         
    def print(text,x,y,color=(0,0,0),center=True):
        text = font.render(text,True,color)
        rect = text.get_rect()
        surface.blit(text,(x-rect.width//2, y-rect.height//2) if center else (x,y))
     # metode za upis    
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

        self.precision = 100
        self.time = np.linspace(0,6,self.precision)
        
        self.chargingPoz = [((-0.368**x)+1)*100 for x in self.time]
        self.chargingNeg = [((0.368**x)-1)*100  for x in self.time]

        self.dischargingPoz = [(0.368**x)*100 for x in self.time]
        self.dischargingNeg = [(-0.368**x)*100  for x in self.time]
        
        self.data = None
        self.size = None
        
    def draw(self):
        if self.data != None and self.size != None:
            graph = pygame.image.fromstring(self.data, self.size, "RGB")
            surface.blit(graph,(self.x,self.y))
        
    def update(self,charging,tp,sec):
        self.fig.clf()
        ax = self.fig.gca()
        ax.set_xlabel("Vrijeme (Tau)", fontsize=12)
        ax.set_ylabel("Napon (% od maksimalnog)",fontsize=12)
        ax.hlines(0, xmin=0, xmax=6, color='black')
        
        if charging:
            ax.vlines(1, ymin=0, ymax=100, color='gray')
            if tp == "RC":
                ax.hlines(63.2, xmin=0, xmax=6, color='gray')
                ax.plot(self.time[:int(sec*self.precision/6)],self.dischargingPoz[:int(sec*self.precision/6)])
                ax.plot(self.time[:int(sec*self.precision/6)],self.chargingPoz[:int(sec*self.precision/6)])
            elif tp == "RL":
                ax.hlines(36.8, xmin=0, xmax=6, color='gray')
                ax.plot(self.time[:int(sec*self.precision/6)],self.chargingPoz[:int(sec*self.precision/6)])
                ax.plot(self.time[:int(sec*self.precision/6)],self.dischargingPoz[:int(sec*self.precision/6)])
        else:
            ax.vlines(1, ymin=-100, ymax=100, color='gray')
            if tp == "RC":
                ax.hlines(36.8, xmin=0, xmax=6, color='gray')
                ax.plot(self.time[:int(sec*self.precision/6)],self.dischargingNeg[:int(sec*self.precision/6)])
                ax.plot(self.time[:int(sec*self.precision/6)],self.dischargingPoz[:int(sec*self.precision/6)])
            elif tp == "RL":
                ax.hlines(-36.8, xmin=0, xmax=6, color='gray')
                ax.plot(self.time[:int(sec*self.precision/6)],self.dischargingPoz[:int(sec*self.precision/6)])
                ax.plot(self.time[:int(sec*self.precision/6)],self.dischargingNeg[:int(sec*self.precision/6)])

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
    global scroll_y
    sklopkaRC.update()
    sklopkaRL.update()
    
    start = time()
    while time() - start < 6:
        kondenzator.update(sklopkaRC.on,time()-start)
        zavojnica.update(sklopkaRL.on,time()-start)
        RCgraf.update(sklopkaRC.on,"RC",time()-start)
        RLgraf.update(sklopkaRL.on,"RL",time()-start)
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 4:
                    scroll_y = 0
                elif e.button == 5:
                    scroll_y = displaySize[1]-surfaceSize[1]
        draw()
    kondenzator.update(sklopkaRC.on,6)
    zavojnica.update(sklopkaRL.on,6)
    RCgraf.update(sklopkaRC.on,"RC",6)
    RLgraf.update(sklopkaRL.on,"RL",6)
    draw()
    
    
def draw():
    surface.fill((255,255,255))
    
    izvorRC.draw()
    sklopkaRC.draw()
    otpornikRC.draw()
    kondenzator.draw()
    for zica in RCzice:
        zica.draw()
        
    TauRC.pr()
    RCgraf.draw()
    
    granica.draw()

    izvorRL.draw()
    sklopkaRL.draw()
    otpornikRL.draw()
    zavojnica.draw()
    for zica in RLzice:
        zica.draw()

    TauRL.pr()
    RLgraf.draw()

    display.blit(surface,(0,scroll_y))
    pygame.display.update()

display = pygame.display.set_mode((800,22))

otpor = validInput("Upisi vrijednost otpornika(Ohm):")
kapacitet = validInput("Upisi vrijednost kondenzatora(F):")
induktivitet = validInput("Upisi vrijednost zavojnice(H):")
    
pygame.display.quit()
pygame.display.init()

display = pygame.display.set_mode(displaySize)

TauRC = float(otpor*kapacitet)
TauRC = "Jedan Tau u RC spoju traje "+str(TauRC)+" sec"
TauRC = text(TauRC,20,120)

TauRL = induktivitet/otpor
TauRL = "Jedan Tau u RL spoju traje "+str(TauRL)+" sec"
TauRL = text(TauRL,20,1320)

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
                
                    
