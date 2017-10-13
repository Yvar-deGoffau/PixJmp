#!/usr/bin/env python

import pygame,os,sys

class Game:
 wzoom=5
 hzoom=5
 cheat=False
 ghosting=160
 def init(self):
  pass

 def __init__(self):
  pygame.mixer.pre_init(22000, -16, 1, 512) #against the lag
  pygame.mixer.init()
  pygame.init()
  self.display=pygame.display.set_mode((192*self.wzoom,144*self.hzoom))
  self.screen=pygame.Surface((192,144))
   #the display is the surface the user sees, the screen the one on which the system draws

  self.entities=[]
  self.font=Font()
   #this is the list of entities
  self.init()
  self.scrollx=self.scrolly=0

 def reg_entity(self,entity):
  if entity not in self.entities: #security check
   self.entities.append(entity)

 def update(self):
  #first, we update ourself
  self.cheatdoupdate=False
  for event in pygame.event.get():
   if event.type==pygame.QUIT: #the user pressed on the button with the cross
    pygame.quit()  #close the video subsystem
    sys.exit()  #and terminate the program
   if event.type==pygame.KEYDOWN:
    if event.key==pygame.K_ESCAPE:  #same thing
     pygame.quit()
     sys.exit()
    if event.key==pygame.K_SPACE:
     self.cheatdoupdate=True
    if event.key==pygame.K_RETURN:
     if self.player.diesound:
      self.player.beeper.play(self.player.diesound)
     else:
      print "\b"
     self.world.reload_level()
     self.player.x=self.player.y=1
     self.player.deads+=1

  #and now, we update all the entities
  if not self.cheat or (self.cheat and self.cheatdoupdate):
   for entity in self.entities:
    entity.update()

 def next_level(self):
  pygame.quit()
  print "You Won"
  sys.exit()

 def get_at(self,pos): #this function looks if there is anything at the given position
  xpos,ypos=pos
  results=[]
  for entity in self.entities:
   x,y=entity.get_pos()
   w,h=entity.get_size()
   if x<xpos<x+w and y<ypos<y+h:
    results.append(entity)
  return results

 def render(self):
  scrollx,scrolly=self.player.get_pos()
  scrollx-=12
  scrolly-=8
  if scrollx>self.world.level.get_width()-24:
   scrollx=self.world.level.get_width()-24
  if scrolly>self.world.level.get_height()-16:
   scrolly=self.world.level.get_height()-16
  if scrollx<0:
   scrollx=0
  if scrolly<0:
   scrolly=0
  scrollx=-scrollx
  scrolly=-scrolly
  self.scrollx=(self.scrollx+scrollx)/2.0
  self.scrolly=(self.scrolly+scrolly)/2.0

  #self.screen.fill((0,255,128))
   #first, render all entities
  for entity in self.entities:
   surface=entity.render()
   surface.set_alpha(self.ghosting)
    #and then, get their position
   x,y=entity.get_pos()
   x*=8
   y*=8
   y+=8
    #if we want to do some scrolling, put the code here... 
   x+=int(self.scrollx-0.5)*8
   y+=int(self.scrolly-0.5)*8
    #and now, we blit the entity at the appropriete place
   self.screen.blit(surface,(x,y))
   #and last, we blit the text
  self.screen.fill((0,255,128),(0,0,192,8))
  self.screen.fill((0,255,128),(0,128+8,192,8))
  self.font.draw(self.screen,self.world.get_title().upper(),(1,128+8))
  string="LEVEL:"+str(self.world.lvl)+" "
  if self.cheat:
   string+="CHEAT"
  string+="DEADS:"+str(self.player.deads)
  
  self.font.draw(self.screen,string,(1,0))
   #stretch the screen to the display
  pygame.transform.scale(self.screen,self.display.get_size(),self.display)
   #and flip
  pygame.display.flip()

 def run(self):
  while 1:
   clock=pygame.time.Clock()
   self.update()
   self.render()
   clock.tick(16)

class Font:
 def __init__(self):
  self.image=pygame.image.load("gfx/font.bmp")
  self.image.set_colorkey((0,0,0))
  self.font={}
  for y in range(self.image.get_height()/8):
   for x in range(self.image.get_width()/6):
    char=chr(x+y*(self.image.get_width()/6))
    shadow=pygame.Surface((6,8))
    shadow.fill((0,160,112))
    shadow.blit(self.image,(-6*x,-8*y))
    front=pygame.Surface((6,8))
    front.fill((0,64,64))
    front.blit(self.image,(-6*x,-8*y))
    shadow.set_colorkey((255,255,255))
    front.set_colorkey((255,255,255))
    shape=pygame.Surface((6,8))
    shape.fill((0,255,128))
    shape.blit(shadow,(0,0))
    #shape.blit(front,(-1,-1))
    self.font[char]=shape
    del front
    del shadow

 def draw(self,surface,text,pos=(0,0),maxwidth=-1):
  text=text.split("\n")
  y=pos[1]
  for row in text:
   x=pos[0]
   for char in row:
    surface.blit(self.font[char],(x,y))
    x+=6
   y+=8

class Entity:
 surface=pygame.Surface((1,1))
 def init(self,*args,**kwargs):
  pass
 def __init__(self,game,x=0,y=0,*args,**kwargs):
  self.game=game
  self.game.reg_entity(self)
  self.x=x
  self.y=y
  self.w,self.h=self.surface.get_size()
  self.init(*args,**kwargs)
 def update(self):
  pass
 def render(self):
  return self.surface
 def get_pos(self):
  return self.x,self.y
 def get_size(self):
  return self.w,self.h

class Pixel:
 def __init__(self,w,h):
  a=pygame.Surface((w,h))
  a.fill((0,255,128))
  a.fill((0,128,96),(2,2,w-2,h-2))
  a.fill((0,64,64),(1,1,w-2,h-2))
  b=pygame.Surface((w,h))
  b.fill((0,255,128))
  b.fill((0,240,124),(2,2,w-2,h-2))
  b.fill((0,224,120),(1,1,w-2,h-2))
  self.image=[a,b]

 def draw(self,surface,pos,val):
  surface.blit(self.image[val&1],pos)

class World(Entity):
 surface=pygame.Surface((192,128))
 def init(self):
  self.titles=[]
  for level in sorted(os.listdir("lvl")):
   self.titles.append(level)
  self.pixel=Pixel(8,8)
  self.lvl=0 #modify this to start at another level
  self.reload_level()
  self.level.set_colorkey((0,0,0))
  self.fallingblocks=[]
 def get_title(self):
  return self.titles[self.lvl][5:-4]
 def get_at(self,pos):
  return self.level.get_at(pos)!=(0,0,0)
 def set_at(self,pos,val):
  if val==0:
   self.level.set_at(pos,(0,0,0))
  else:
   self.fallingblocks.append(pos)
   self.level.set_at(pos,(255,255,255))
 def update(self):
  for x,y in self.fallingblocks:
   if y+1>=self.level.get_height():
    self.set_at((x,y),0)
   elif self.get_at((x,y+1))==0:
    self.set_at((x,y),0)
    self.set_at((x,y+1),1)
   self.fallingblocks.remove((x,y))
 def next_level(self):
  self.lvl+=1
  self.reload_level()
 def reload_level(self):
  cont=1
  while cont:
   try:
    self.level=pygame.image.load("lvl/"+self.titles[self.lvl])
    cont=0
   except pygame.error:
    print "Cannot load level "+str(self.lvl)+": "+self.titles[self.lvl]
    self.lvl+=1
    continue
  self.level.set_colorkey((0,0,0))
  self.surface=pygame.Surface((self.level.get_width()*8,self.level.get_height()*8))
  self.game.scrollx=self.game.scrolly=0
 def render(self):
  for y in range(self.level.get_height()):
   for x in range(self.level.get_width()):
    self.pixel.draw(self.surface,(x*8,y*8),self.level.get_at((x,y))==(0,0,0))
  return self.surface

class Player(Entity):
 surface=pygame.Surface((8,8))
 def init(self,*args,**kwargs):
  self.x=self.y=1
  self.jump=0
  self.push=0
  self.deads=0
  self.surface.fill((0,255,128))
  self.surface.fill((0,128,96),(2,2,8-2,8-2))
  self.surface.fill((0,64,64),(1,1,8-2,8-2))
  self.surface.set_at((2,2),(0,192,112))
  self.surface.set_at((5,2),(0,192,112))
  for x in range(2,6):
   self.surface.set_at((x,5),(0,192,112))
  self.beeper=pygame.mixer.Channel(0)
  try:
   self.jmpsound=pygame.mixer.Sound("snd/jmp.wav")
   self.diesound=pygame.mixer.Sound("snd/die.wav")
   self.winsound=pygame.mixer.Sound("snd/win.wav")
   self.pshsound=pygame.mixer.Sound("snd/psh.wav")
  except Exception:
   self.jmpsound=None
   self.diesound=None
   self.winsound=None
   self.pshsound=None
   print "Unable to load sound"
  #self.climb=0

 def update(self):
  keys=pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
   self.move(-1,0)
  if keys[pygame.K_RIGHT]:
   self.move(1,0)
  try:
   if self.game.world.get_at((self.x,self.y+1)):
    self.jump=5
  except IndexError:
   pass
  if self.jump>0:
   if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
    self.move(0,-1)
    if not self.beeper.get_busy():
     if self.jmpsound:
      self.beeper.play(self.jmpsound)
   self.jump-=1
  else:
   self.move(0,1)
  if self.x>=self.game.world.level.get_width():
   self.x=self.y=1
   self.jump=0
   if self.winsound:
    self.beeper.play(self.winsound)
   else:
    print "\b"
   self.game.world.next_level()
  if self.y>=self.game.world.level.get_height():
   self.x=self.y=1
   self.deads+=1
   if self.diesound:
    self.beeper.play(self.diesound)
   else:
    print "\b"
  #print self.jump

 def move(self,xvect,yvect):
  x=self.x+xvect
  y=self.y+yvect
  if self.push:
   self.push=0
   return
  #print x,y,
  try:
   if self.game.world.get_at((x,y)):
    try:
     if self.game.world.get_at((self.x,self.y+1)) and not self.game.world.get_at((x+xvect,y)):
      self.game.world.set_at((x,y),0)
      self.game.world.set_at((x+xvect,y),1)
      if self.pshsound:
       self.beeper.play(self.pshsound)
      else:
       print "\b"
      self.push=1
      return
     else:
      #print "#"
      return
    except IndexError:
     return
  except IndexError:
   pass
  #print "O"
  self.x=x
  self.y=y

class NewGame(Game):
 def init(self):
  self.world=World(self)
  self.player=Player(self)

if __name__=="__main__":
 NewGame().run()
