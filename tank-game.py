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
    
    def __init__(self, position, direction, power):
        super().__init__(Bullet.asset, [position[0] - 50 * math.sin(direction), position[1] - 50 * math.cos(direction)], CircleAsset(10))
        self.speed = power
        self.vx = self.speed * math.sin(direction)
        self.vy = self.speed * math.cos(direction)
        self.deltavy = 0.1
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
    
    def __init__(self, position, player, turn):
        super().__init__(Turret.rect, position)
        self.vr = 0
        self.maxspin = 0.05
        self.rotation = math.pi
        self.fxcenter = 0.5
        self.fycenter = 0
        self.power = 0
        self.player = player
        self.turn = turn
        
        # Rotate right/left
        TankGame.listenKeyEvent("keydown", "left arrow", self.aimLeftOn)
        TankGame.listenKeyEvent("keydown", "left arrow", self.aimLeftOff)
        TankGame.listenKeyEvent("keydown", "right arrow", self.aimRightOn)
        TankGame.listenKeyEvent("keydown", "right arrow", self.aimRightOff)
        
        # Adjust power
        TankGame.listenKeyEvent("keydown", "up arrow", self.powerUp)
        TankGame.listenKeyEvent("keydown", "down arrow", self.powerDown)
        
        # Shoot
        TankGame.listenKeyEvent("keydown", "space", self.shoot)
        
    def aimRightOn(self, event):
        if self.turn:
            self.vr = -self.maxspin
        
    def aimRightOff(self, event):
        if self.turn:
            self.vr = 0
        
    def aimLeftOn(self, event):
        if self.turn:
            self.vr = self.maxspin
        
    def aimLeftOff(self, event):
        if self.turn:
            self.vr = 0
        
    def powerUp(self, event):
        if self.turn:        
            if self.power < 20:
                self.power += 0.5
                print(self.power)
            
    def powerDown(self, event):
        if self.turn:
            if self.power > 1:
                self.power -= 0.5
                print(self.power)
        
    def shoot(self, event):
        if self.turn:
            Bullet((self.x + 80 * math.sin(self.rotation), self.y + 80 * math.cos(self.rotation)), self.rotation, self.power)
        
    def step(self):
        self.rotation += self.vr
        if self.rotation < math.pi / 2 or self.rotation > math.pi * 3 / 2:
            self.rotation -= self.vr
        self.vr = 0
        
        
class TankGame(App):
    def __init__(self):
        super().__init__()
        
        TankGame.listenKeyEvent("keyup", "space", self.toggleTurns)
        
        self.player1 = Turret((100,100), 1, True)
        self.player2 = Turret((200, 200), 2, False)
        
    def toggleTurns(self, event):
        if self.player1.turn == True:
            self.player1.turn = False
            self.player2.turn = True
        else:
            self.player1.turn = True
            self.player2.turn = False
    
    def step(self):
        self.player1.step()
        self.player2.step()
            
        for bullet in self.getSpritesbyClass(Bullet):
            bullet.step()
            if bullet.x < 0 or bullet.x > self.width or bullet.y > self.height:
                bullet.destroy()
            else:
                for x in bullet.collidingWithSprites(Turret)
                    Explosion((bullet.x, bullet.y))
            
        # Winner starts next round

myapp = TankGame()
myapp.run()
            