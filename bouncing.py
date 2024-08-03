import os 
import pygame as pg
import random
import keyboard as keys
import pymunk as pm



class player:
  
    def __init__(self, space):
        width = 40
        height = 40
        moment_player = pm.moment_for_box(100, (width, height))
        self.body = pm.Body(100, moment_player, pm.Body.DYNAMIC)
        self.body.position = (250, 250)
        self.shape = pm.Poly.create_box(self.body, (40, 40))
        self.shape.elasticity = 0.5
        self.shape.elasticity = 0.5
        space.add(self.body, self.shape)
    
    
    def move(self, direction, speed):
        if direction == "left":
            self.body.velocity = (-speed, 0)
        elif direction == "right":
            self.body.velocity = (speed, 0)
        elif direction == "up":
            self.body.velocity = (0, -speed)
        elif direction == "down":
            self.body.velocity = (0, speed)
            
    def draw(self, screen):
        pos_x = int(self.body.position.x) - 20
        pos_y = int(self.body.position.y) - 20
        pg.draw.rect(screen, (23, 200, 80), (pos_x, pos_y, 40, 40))
    
def create_ball(space, x, y):
  body = pm.Body(0.05, 0.1, pm.Body.DYNAMIC)
  body.position = (x, y)
  shape = pm.Circle(body, 3)
  shape.elasticity = .10
  shape.friction = 0.01
  space.add(body, shape)
  return shape

def draw_balls(balls, screen):
  for ball in balls:
    pos_x = int(ball.body.position.x)
    pos_y = int(ball.body.position.y)
    pg.draw.circle(screen, (23, 70, 205), (pos_x, pos_y), 3)    
    
def main():
  
  pg.init()
  
  clock = pg.time.Clock()
  clock.tick(60)
  
  space = pm.Space()
  space.gravity = (0, 100)
  
  screen = pg.display.set_mode((1000, 1000))
  
  floor = pm.Body(100, 5, pm.Body.STATIC)
  floor.position = (0, 950)
  floor_shape = pm.Poly(floor, [(0, 0), (1000, 0), (1000, 50), (0, 50)])
  floor_shape.elasticity = 0.2
  space.add(floor, floor_shape)
  
  celling = pm.Body(100, 100, pm.Body.STATIC)
  celling.position = 0, 0
  celling_s = pm.Poly(celling, [(0,0), (1000, 0), (1000, 50),  (0, 50)])
  celling_s.elasticity = 0.2
  space.add(celling, celling_s)
  
  
  wall_l = pm.Body(100, 100, pm.Body.STATIC)
  wall_l.position = (950, 0)
  wall_l_s = pm.Poly(wall_l, [(0,0), (50, 0), (50, 1000), (0, 1000)])
  wall_l_s.elasticity = 0.2
  space.add(wall_l, wall_l_s)
  
  wallr = pm.Body(100, 100, pm.Body.STATIC)
  wallr.position = (0, 0)
  wallr_s = pm.Poly(wallr, [(0,0), (50, 0), (50, 1000), (0, 1000)])
  wallr_s.elasticity = 0.2
  space.add(wallr, wallr_s)
  
  balls = []
  player1 = player(space)
  
  for i in range(100, 900, 1):
        balls.append(create_ball(space, i, 300))
  for i in range(100, 900, 1):
        balls.append(create_ball(space, i, 400))
  for i in range(100, 900, 1):
        balls.append(create_ball(space, i, 500))

  running = True
  while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                for i in range(100):
                    balls.append(create_ball(space, 500, 500))
            if event.key == pg.K_LEFT:
                player1.move("left", 200)
            if event.key == pg.K_RIGHT:
                player1.move("right", 200)
            if event.key == pg.K_UP:
                player1.move("up", 200)
            if event.key == pg.K_DOWN:
                player1.move("down", 200)
                
    
    space.step(1/52)    
    screen.fill((123, 28, 83))
    pg.draw.rect(screen, (255, 255, 255), (0, 950, 1000, 1000))
    pg.draw.rect(screen, (255, 255, 255), (950, 0, 1000, 1000))
    pg.draw.rect(screen, (255, 255, 255), (0, 0, 50, 1000))
    pg.draw.rect(screen, (255, 255, 255), (0, 0, 1000, 50))

    draw_balls(balls, screen)
    player1.draw(screen)

    clock.tick(60)
    
    pg.display.update()

main()