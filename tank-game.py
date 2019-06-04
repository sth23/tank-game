"""
Final Project: Tank Game
Author: Sean
Credit: Tutorials
Assignment: Create an old-school turn based tank game
"""

from ggame import App, RectangleAsset, CircleAsset, LineAsset, ImageAsset, Frame, Sprite, LineStyle, Color
import math
import random

# Colors & lines
red = Color(0xff0000, 1.0)
orange = Color(0xffa500, 1.0)
yellow = Color(0xffff00, 1.0)
green = Color(0x00ff00, 1.0)
blue = Color(0x0000ff, 1.0)
purple = Color(0x800080, 1.0)
black = Color(0x000000, 1.0)
white = Color(0xffffff, 1.0)
gray = Color(0x888888, 0.5)
noline = LineStyle(0, black)
whiteline = LineStyle(1, white)

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
                
class Trail(Sprite):
    circ = CircleAsset(1, noline, black)
    
    def __init__(self, position):
        super().__init__(Trail.circ, position)
        self.count = 100
        
    def step(self):
        self.count -= 1
        if self.count == 0:
            self.destroy()
                
class Bullet(Sprite):
    wind = 0
    asset = ImageAsset("blast.png", Frame(0,0,8,8), 8, 'horizontal')
    
    def __init__(self, position, direction, power):
        super().__init__(Bullet.asset, [position[0] - 50 * math.sin(direction), position[1] - 50 * math.cos(direction)], CircleAsset(5))
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
        self.vx += Bullet.wind * 0.005
        self.vy += self.deltavy
        
        Trail((self.x, self.y))
        
        # manage bullet animation
        self.setImage(self.bulletphase%7)
        self.bulletphase += 1
        
class Turrain(Sprite):
    def __init__(self, asset, position):
        super().__init__(asset, position)

class Turret(Sprite):
    def __init__(self, position, player, turn, color):
        super().__init__(RectangleAsset(5, 40, noline, color), position)
        self.vr = 0
        self.maxspin = 0.05
        self.rotation = math.pi
        self.fxcenter = 0.5
        self.fycenter = 0
        self.power = 1
        self.maxpower = 20
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
            if self.power < self.maxpower:
                self.power += 0.25
            print("Power: " + str(self.power))
            
    def powerDown(self, event):
        if self.turn:
            if self.power > 1:
                self.power -= 0.25
            print("Power: " + str(self.power))
        
    def shoot(self, event):
        if self.turn:
            Bullet((self.x + 100 * math.sin(self.rotation), self.y + 100 * math.cos(self.rotation)), self.rotation, self.power)
        
    def step(self):
        self.rotation += self.vr
        if self.rotation < math.pi / 2 or self.rotation > math.pi * 3 / 2:
            self.rotation -= self.vr
        self.vr = 0
        
        
class TankGame(App):
    def __init__(self):
        super().__init__()
        
        TankGame.listenKeyEvent("keyup", "space", self.toggleTurns)
        
        self.player1 = Turret((-20, -20), 1, True, red)
        self.player2 = Turret((-20, -20), 2, False, blue)
        self.loser = []
        
        self.turrainheight = 0
        self.turrainwidth = 15
        self.placePlayers()
        self.createTurrain()
        
    def toggleTurns(self, event):
        if self.player1.turn == True:
            self.player1.turn = False
            self.player2.turn = True
            print("Player 2 turn")
        else:
            self.player1.turn = True
            self.player2.turn = False
            print("Player 1 turn")
            
    def placePlayers(self):
        self.player1.rotation = math.pi
        self.player1.x = random.randint(2, (self.width // self.turrainwidth) // 3)
        self.player1.power = 1
        self.player2.rotation = math.pi
        self.player2.x = random.randint((self.width // self.turrainwidth) * 2 // 3, self.width // self.turrainwidth - 2)
        self.player2.power = 1
            
    def createTurrain(self):
        self.turrainheight = random.randint(self.height // 4, self.height - 200)
        for x in range(0, self.width // self.turrainwidth + 1):
            self.turrainheight = self.turrainheight + random.randint(-40, 40)
            if self.turrainheight > self.height - 10:
                self.turrainheight -= 50
            elif self.turrainheight < 50:
                self.turrainheight += 50
            Turrain(RectangleAsset(self.turrainwidth, self.height * 2, noline, black), (x * self.turrainwidth, self.turrainheight))
            if x == self.player1.x:
                self.player1.x = self.player1.x * self.turrainwidth + self.turrainwidth / 2
                self.player1.y = self.turrainheight
            if x == self.player2.x:
                self.player2.x = self.player2.x * self.turrainwidth + self.turrainwidth / 2
                self.player2.y = self.turrainheight
        Bullet.wind = random.randint(-5,5)
        print(Bullet.wind)
    
    def step(self):
        self.player1.step()
        self.player2.step()
            
        for bullet in self.getSpritesbyClass(Bullet):
            bullet.step()
            if bullet.x < 0 or bullet.x > self.width or bullet.y > self.height:
                bullet.destroy()
            else:
                self.loser = bullet.collidingWithSprites(Turret)
                if self.loser:
                    Explosion((bullet.x, bullet.y))
                    bullet.destroy()
                    if self.loser[0].player == 2:
                        print("Player 1 wins!")
                        self.player1.turn = True
                        self.player2.turn = False
                        print("Player 1 turn")
                    else:
                        print("Player 2 wins!")
                        self.player1.turn = False
                        self.player2.turn = True
                        print("Player 2 turn")
                    self.loser = []
                    self.placePlayers()
                    for x in self.getSpritesbyClass(Turrain):
                        x.destroy()
                    self.createTurrain()
                        
                elif bullet.collidingWithSprites(Turrain):
                    Explosion((bullet.x, bullet.y))
                    bullet.destroy()
                    
        for explosion in self.getSpritesbyClass(Explosion):
            explosion.step()
            
        for trail in self.getSpritesbyClass(Trail):
            trail.step()
            
        # Winner starts next round

myapp = TankGame()
myapp.run()
            