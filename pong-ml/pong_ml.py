#!/usr/bin/env python
# Modified from http://www.pygame.org/project-Very+simple+Pong+game-816-.html

import numpy
import pygame
from pygame.locals import *
from sys import exit
import random
from pong_agent import pong_agent
from pong_agent import MLPongAgent
import ml_model
import datasets
import pygame.surfarray as surfarray
import matplotlib.pyplot as plt
import data_collect


class pong:
    pygame.init()
    model = ml_model.generate_model(datasets.load('up-only'))
    agent = MLPongAgent(model)

    screen = pygame.display.set_mode((640, 480), 0, 32)

    # Creating 2 bars, a ball and background.
    back = pygame.Surface((640, 480))
    background = back.convert()
    background.fill((0, 0, 0))
    bar = pygame.Surface((10, 50))
    bar1 = bar.convert()
    bar1.fill((255, 255, 255))
    bar2 = bar.convert()
    bar2.fill((255, 255, 255))
    circ_sur = pygame.Surface((15, 15))
    circ = pygame.draw.circle(circ_sur, (255, 255, 255), ((int)(15 / 2), (int)(15 / 2)), (int)(15 / 2))
    circle = circ_sur.convert()
    circle.set_colorkey((0, 0, 0))

    # some definitions
    bar1_x, bar2_x = 10. , 620.
    bar1_y, bar2_y = 215. , 215.
    circle_x, circle_y = 307.5, 232.5
    bar1_move, bar2_move = 0. , 0.
    speed_x, speed_y, speed_circ = 250., 250., 250.
    bar1_score, bar2_score = 0, 0

    # clock and font objects
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("calibri", 40)

    # ML objects
    session_training_data = []

    frame_num = 0

    done = False
    input_opcode = 0

    def play(self, done):
        while done == False:       
            self.frame_num += 1
            '''
            input_opcode:
                0 = noop
                1 = move up
                2 = move down
            '''
            frame_tensor = data_collect.FrameData(self.frame_num, self.input_opcode, self.bar1_y, self.circle_x, self.circle_y).to_processed_tensor()

            self.agent.move(frame_tensor)
            time_passed = self.clock.tick(30)
            time_sec = time_passed / 1000.0
            ai_speed = self.speed_circ * time_sec
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop
                
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        print("Hi!")
                        input_opcode = 1
                        self.bar1_move = -ai_speed
                    elif event.key == K_DOWN:
                        input_opcode = 2
                        self.bar1_move = ai_speed
                elif event.type == KEYUP:
                    if event.key == K_UP:
                        input_opcode = 0
                        self.bar1_move = 0.
                    elif event.key == K_DOWN:
                        input_opcode = 0
                        self.bar1_move = 0.   
            
            score1 = self.font.render(str(self.bar1_score), True, (255, 255, 255))
            score2 = self.font.render(str(self.bar2_score), True, (255, 255, 255))

            self.screen.blit(self.background, (0, 0))
            frame = pygame.draw.rect(self.screen, (255, 255, 255), Rect((5, 5), (630, 470)), 2)
            middle_line = pygame.draw.aaline(self.screen, (255, 255, 255), (330, 5), (330, 475))
            self.screen.blit(self.bar1, (self.bar1_x, self.bar1_y))
            self.screen.blit(self.bar2, (self.bar2_x, self.bar2_y))
            self.screen.blit(self.circle, (self.circle_x, self.circle_y))
            self.screen.blit(score1, (250., 210.))
            self.screen.blit(score2, (380., 210.))

            self.bar1_y += self.bar1_move
                
            # movement of circle
            
                
            self.circle_x += self.speed_x * time_sec
            self.circle_y += self.speed_y * time_sec
            
            
            # AI of the computer.
            if self.circle_x >= 305.:
                if not self.bar2_y == self.circle_y + 7.5:
                    if self.bar2_y < self.circle_y + 7.5:
                        self.bar2_y += ai_speed
                    if  self.bar2_y > self.circle_y - 42.5:
                        self.bar2_y -= ai_speed
                else:
                    self.bar2_y == self.circle_y + 7.5
            
            # Safety out of bound reset
            if self.bar1_y >= 420.:
                self.bar1_y = 420.
            elif self.bar1_y <= 10. :
                self.bar1_y = 10.
            if self.bar2_y >= 420.:
                self.bar2_y = 420.
            elif self.bar2_y <= 10.:
                self.bar2_y = 10.
                
            # Simple Bar collision
            if self.circle_x <= self.bar1_x + 10.:
                if self.circle_y >= self.bar1_y - 7.5 and self.circle_y <= self.bar1_y + 42.5:
                    self.circle_x = 20.
                    self.speed_x = -self.speed_x
            if self.circle_x >= self.bar2_x - 15.:
                if self.circle_y >= self.bar2_y - 7.5 and self.circle_y <= self.bar2_y + 42.5:
                    self.circle_x = 605.
                    self.speed_x = -self.speed_x
                        
            # Detects North South bounds
            if self.circle_y <= 10.:
                self.speed_y = -self.speed_y
                self.circle_y = 10.
            elif self.circle_y >= 457.5:
                self.speed_y = -self.speed_y
                self.circle_y = 457.5
            
            # Win condition.
            if self.circle_x < 5.:
                self.bar2_score += 1
                self.circle_x, self.circle_y = 320., 232.5
                self.bar1_y, self.bar_2_y = 215., 215.
            elif self.circle_x > 620.:
                self.bar1_score += 1
                self.circle_x, self.circle_y = 307.5, 232.5
                self.bar1_y, self.bar2_y = 215., 215.
            
            self.session_training_data.append(data_collect.FrameData(self.frame_num, self.input_opcode, self.bar1_y, self.circle_x, self.circle_y))


            # image_data = pygame.surfarray.array3d(pygame.display.get_surface())
            # if done == True:
            #     plt.imshow(image_data)
            #     plt.show()

            pygame.display.update()

game = pong()
game.play(game.done)

data_collect.serialize_data(game.session_training_data)

pygame.quit()
