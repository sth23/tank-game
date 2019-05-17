"""
Final Project: Tank Game
Author: Sean
Credit: Tutorials
Assignment: Create an old-school turn based tank game
"""

from ggame import App, RectangleAsset, CircleAsset, LineAsset, ImageAsset, Frame, Sprite, LineStyle, Color
import math
import random

class Explosion(Sprite):
    asset = ImageAsset("explosion1.png", Frame(0,0,128,128), 10, 'horizontal')
    
    def __init__(self, position):
        super().__init__(Explosion.asset, position)
        self.fxcenter = self.fycenter = 0.5
        self.countup = 0
        self.countdown = 10
        
    def step(self):
        # Manage explosion animation
        if self.countup < 10:
            self.setImage(self.countup%10)
            self.countup += 1
        else:
            self.setImage(self.countdown%10)
            self.countdown -= 1
            if self.countdown == 0:
                self.destroy()
                
class Bullet(Sprite):
    asset = ImageAsset("blast.png", Frame(0,0,8,8), 8, 'horizontal')
    
    def __init__(self, position, direction):
        super().__init__(Bullet.asset, [position[0] - 50 * math.sin(direction), position[1] - 50 * math.cos(direction)], CircleAsset(10))
        self.speed = 10
        self.vx = self.speed * math.sin(direction)
        self.vy = self.speed * math.cos(direction)
        self.deltavy = 5
        self.vr = 0
        self.fxcenter = self.fycenter = 0.5
        self.bulletphase = 0
        
    def step(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.deltavy
        
        # manage bullet animation
        self.setImage(self.bulletphase%7)
        self.bulletphase += 1

class Turret(Sprite):
    black = Color(0, 1)
    noline = LineStyle(0, black)
    rect = RectangleAsset(5, 40, noline, black)
    
    def __init__(self, position, player):
        super().__init__(Turret.rect, position)
        self.maxspin = 0.05
        self.rotation = math.pi
        self.fxcenter = 0.5
        self.fycenter = 0
        self.power = 0
        self.player = player
        
        # Rotate right/left
        TankGame.listenKeyEvent("keydown", "left arrow", self.aimLeftOn)
        TankCommandGame.listenKeyEvent("keydown", "right arrow", self.aimRightOn)
        
        # Adjust power
        TankCommandGame.listenKeyEvent("keydown", "up arrow", self.powerUp)
        TankCommandGame.listenKeyEvent("keydown", "down arrow", self.powerDown)
        
        # Shoot
        TankCommandGame.listenKeyEvent("keydown", "space", self.shoot)
        
    def aimRight(self, event):
        self.vr = -self.maxspin
        
    def aimLeftOn(self, event):
        self.vr = self.maxspin
        
    def powerUp(self, event):
        if self.power < 20:
            self.power += 1
            
    def powerDown(self, event):
        if self.power > 1:
            self.power -= 1
        
    def shoot(self, event):
        Bullet((self.x + 80 * math.sin(self.rotation), self.y + 80 * math.cos(self.rotation)), self.rotation)
        
    def step(self):
        self.rotation += self.vr
        if self.rotation < math.pi / 2 or self.rotation > math.pi * 3 / 2:
            self.rotation -= self.vr
        self.vr = 0
        
        
class TankGame(App):
    def __init__(self):
        super().__init__()
        self.playerturn = 1
        
        TankGame.listenKeyEvent("keydown", "space", self.toggleTurns)
        
        self.player1 = Turret((10,10), 1)
        self.player2 = Turret((100, 100), 2)
        
    def toggleTurns(self, event):
        if self.playerturn == 1:
            self.playerturn == 2
        else:
            self.playerturn == 1
    
    def step(self):
        if self.playerturn == 1:
            self.player1.step()
        elif self.playerturn == 2:
            self.player2.step()
            
myapp = TankGame()
myapp.run()
            