import pygame 
import time 
import math

pygame.init()

Width = 1000
Height = 800

Screen = pygame.display.set_mode([Width,Height])

fps = 60 
Timer = pygame.time.Clock()

WallThickness = 10
Gravity = 0.5
BounceStop = 0.3 

MouseTrajectory = [] 

#retention means that the ball doesn't come back to the same level on every tab, and it shouldn't.
class Ball: 
    def __init__(self, x_pos, y_pos, radius, color, mass, retention, y_speed, x_speed, friction): 
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.retention = retention
        self.y_speed = y_speed
        self.x_speed = x_speed
        self.selected = False
        self.friction = friction

    def draw(self):
        self.circle = pygame.draw.circle(Screen,self.color,(self.x_pos,self.y_pos),self.radius)
    
    def check_gravity(self):
        if not self.selected: 
            if self.y_pos < Height - self.radius - (WallThickness/2):
                self.y_speed += Gravity
            else: 
                # when it's really close to the surface
                # if my total speed is less than 0.3, I'm just gonna stop. 
                if self.y_speed > BounceStop: 
                    self.y_speed = self.y_speed * -1 * self.retention # retention values needs to be among 0 and 1 
                elif abs(self.y_speed) <= BounceStop: 
                    self.y_speed = 0 
            if (self.x_pos < self.radius + (WallThickness/2) and self.x_speed < 0) or (self.x_pos > Width - self.radius - (WallThickness/2) and self.x_speed > 0): 
                #the condition above cause the ball to bounce
                self.x_speed *= -1 * self.retention
                if abs(self.x_speed) <= BounceStop:
                    self.x_speed = 0 
            # For the fraction on surface
            if self.y_speed == 0 and self.x_speed != 0: 
                if self.x_speed > 0: 
                    self.x_speed -= self.friction
                elif self.x_speed < 0: 
                    self.x_speed += self.friction

        if self.selected: 
            if (self.x_pos < self.radius + (WallThickness/2)) or (self.x_pos > Width - self.radius - (WallThickness/2) or (self.y_pos > Height-self.radius-(WallThickness/2))):
                    self.selected = False  
            self.x_speed = x_push
            self.y_speed = y_push   
        return self.y_speed
    
    def UpdatePos(self,mouse): 
        if not self.selected: 
            self.y_pos += self.y_speed
            self.x_pos += self.x_speed
        else: 
            self.x_pos = mouse[0]
            self.y_pos = mouse[1]

    def check_select(self, pos): # pos is going to be the cordination of the mouse when I press the button. 
        self.selected = False
        if self.circle.collidepoint(pos): 
            self.selected = True 
        return self.selected

    
def WallBorder():
    left = pygame.draw.line(Screen, 'white',(0,0),(0,Height),WallThickness)
    right = pygame.draw.line(Screen, 'white',(Width,0),(Width,Height),WallThickness)
    top = pygame.draw.line(Screen, 'white',(0,0),(Width,0),WallThickness)
    bottom = pygame.draw.line(Screen, 'white',(0,Height),(Width,Height),WallThickness)
    return left,right, top, bottom

def CalculationMotionVector(): 
    x_speed = 0 
    y_speed = 0
    if len(MouseTrajectory) > 10: 
        x_speed = (MouseTrajectory[-1][0] - MouseTrajectory[0][0]) / len(MouseTrajectory)
        y_speed = (MouseTrajectory[-1][1] - MouseTrajectory[0][1]) / len(MouseTrajectory)
    return x_speed, y_speed

def CheckCollision(ball1,ball2): 
        DifferenceX = ball2.x_pos - ball1.x_pos
        DifferenceY = ball2.y_pos - ball1.y_pos
        Distance = math.sqrt((ball1.x_pos-ball2.x_pos)**2 + (ball1.y_pos-ball2.y_pos)**2)

        if Distance <= ball1.radius + ball2.radius:
            #calculating collision angle
            CollisionAngle = math.atan2(DifferenceY,DifferenceX)

            #calculate total velocity of each ball
            TotalVelocityFor1 = math.sqrt(ball1.x_speed**2+ball1.y_speed**2)
            TotalVelocityFor2 = math.sqrt(ball2.x_speed**2 + ball2.y_speed**2)

            #calculate collision angle for each ball
            Angle1 = math.atan2(ball1.y_speed, ball1.x_speed)
            Angle2 = math.atan2(ball2.y_speed, ball2.x_speed)

            #calculating new velocities after collision
            NewSpeedX1 = TotalVelocityFor2 * math.cos(Angle2 - CollisionAngle)
            NewSpeedY1 = TotalVelocityFor2 * math.sin(Angle2 - CollisionAngle)
            NewSpeedX2 = TotalVelocityFor1 * math.cos(Angle1 - CollisionAngle)
            NewSpeedY2 = TotalVelocityFor1 * math.sin(Angle1 - CollisionAngle)

            #Updating velocities and positions
            ball1.x_speed = NewSpeedX1
            ball1.y_speed = NewSpeedY1
            ball2.x_speed = NewSpeedX2
            ball2.y_speed = NewSpeedY2

            #Move balls slightly apart to avoid sticking
            overlap = (ball1.radius + ball2.radius - Distance) / 2.0
            ball1.x_pos -= overlap * math.cos(CollisionAngle)
            ball1.y_pos -= overlap * math.sin(CollisionAngle)
            ball2.x_pos += overlap * math.cos(CollisionAngle)
            ball2.y_pos += overlap * math.sin(CollisionAngle)


        return False

Ball1 = Ball(Width/2,Height/2,50,'green',100,.7,0,0,0.02)
Ball2 = Ball(Width/3,Height/3,40,'red',100,.7,0,0,0.02)
Balls = [Ball1,Ball2]
run = True 

while run: 
    Timer.tick(fps)
    Screen.fill('black')
    MouseCoord = pygame.mouse.get_pos()
    MouseTrajectory.append(MouseCoord)

    if len(MouseTrajectory) > 20: 
        MouseTrajectory.pop(0)

    x_push, y_push = CalculationMotionVector()

    walls = WallBorder()
    Ball1.draw()
    Ball2.draw()
    Ball1.UpdatePos(MouseCoord)
    Ball2.UpdatePos(MouseCoord)
    Ball1.y_speed = Ball1.check_gravity()
    Ball2.y_speed = Ball2.check_gravity()
    CheckCollision(Ball1,Ball2)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if event.button == 1: 
                # event.pos gives the cord of the mouse when it's clicked
                if Ball1.check_select(event.pos) or Ball2.check_select(event.pos): 
                    active_select = True 
        if event.type == pygame.MOUSEBUTTONUP: 
            if event.button == 1:
                active_select = False
                for i in range(len(Balls)): 
                    Balls[i].check_select((-1500,-1500)) # ball's select status is reset
    pygame.display.flip()
pygame.quit()