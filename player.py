#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pygame

MOVE_SPEED = 10
WIDTH = 45
HEIGHT = 35
COLOR = "#888888"
JUMP_POWER = 12
GRAVITY = 0.5


class Player(sprite.Sprite):
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.xvel = 0
		self.startX = x
		self.startY = y
		self.image1 = pygame.image.load('C:/Users/Daria/PycharmProjects/bounce_project/ball1.jpg')
		self.image = pygame.transform.scale(self.image1, (45, 35))
		self.image.set_colorkey((255, 255, 255))
		self.rect = Rect(x, y, WIDTH, HEIGHT)
		self.yvel = 0
		self.onGround = False
	
	def update(self, left, right, up, platforms):
		if up:
			if self.onGround:
				self.yvel = -JUMP_POWER
		if left:
			self.xvel = -MOVE_SPEED  # Лево
		
		if right:
			self.xvel = MOVE_SPEED  # Право
		
		if not (left or right):
			self.xvel = 0
		
		if not self.onGround:
			self.yvel += GRAVITY
		
		self.onGround = False
		self.rect.y += self.yvel
		self.collide(0, self.yvel, platforms)
		
		self.rect.x += self.xvel
		self.collide(self.xvel, 0, platforms)
	
	def collide(self, xvel, yvel, platforms):
		for p in platforms:
			if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
				
				if xvel > 0:  # если движется вправо
					self.rect.right = p.rect.left
				
				if xvel < 0:  # если движется влево
					self.rect.left = p.rect.right
				
				if yvel > 0:  # если падает вниз
					self.rect.bottom = p.rect.top
					self.onGround = True
					self.yvel = 0
				
				if yvel < 0:  # если движется вверx
					self.rect.top = p.rect.bottom
					self.yvel = 0
