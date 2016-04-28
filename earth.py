import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from math2		import *
from drawable 		import Drawable
from explosion 		import Explosion
from earthchunk 	import EarthChunk


class Earth(Drawable):
	def isDead(self):
		return self.hp <= 0
	def damage(self, amt):
		self.hp -= amt



	def __init__(self, gameSpace, x, y):
		super(Earth, self).__init__(gameSpace, x,y, "img/earth.png", 1,1)
		
		self.r = self.sprite.w/2
		self.hpPrev = self.hp = 100

		# Load Sounds
		self.sndExplosion = pygame.mixer.Sound("snd/explosion.ogg")
		self.sndRumbling = pygame.mixer.Sound("snd/laserHit.ogg")
		self.sndRumbling.set_volume(0)
		self.sndRumbling.play(loops=-1)

	
	def tick(self, input):
		# Set radius based on width and scale
		self.r = (self.sprite.w - 16)*self.spriteScale/2

		# If just died, then play exploding animation
		if self.hpPrev > 0 and self.hp <= 0:
			# Play explosion sound
			self.sndExplosion.play()
			
			# Create 50 earth chunks, flying off in random directions
			i = 0
			while i < 50:
				r = random.random()*self.r
				dir = random.random()*360
				self.gs.instanceAppend(EarthChunk(self.gs, self.x+lenX(r,dir), self.y+lenY(r,dir), dir))
				
				i += 1;

			# Create explosion animation object
			self.gs.instanceAppend(Explosion(self.gs, self.x, self.y-50))

		# If alive, set rumbling volume based on hp and slowly replenish hp
		if self.hp > 0:
			self.sndRumbling.set_volume((100-self.hp)/100);
			self.hp += .5

		# If dead, stop rumbling sound altogether
		else:
			self.sndRumbling.stop();

		
		# Update previous hp and contain hp within bounds
		self.hpPrev = self.hp
		self.hp = contain(0,self.hp,100)

		# Tick super method
		super(Earth, self).tick(input)


	def draw(self, screen):

		# Only draw if still alive
		if self.hp > 0:		
			hpFrac = 1-self.hp/100
		
			ranF = 32*hpFrac
			ran = random.randint(0, int(ranF) )

			# Calculate small, random amounts to add to position
			ranX = random.randint(-ran,ran)
			ranY = random.randint(-ran,ran)
			ranSc = random.random()*ranF/100
			
			# Modify position/scale temporarily by small amount for shaking effect
			self.x += ranX
			self.y += ranY
			self.spriteScale += ranSc


			# Get image w/ scale and angle applied
			img = self.sprite.get(self.x, self.y, self.spriteIndex, self.spriteAngle, self.spriteScale);


			# Fade red w/ additive blending
			img[0].fill((int(255*hpFrac),0,0,255), special_flags=BLEND_RGB_ADD)

			# Darken in G/B Channels w/ multiplicative blending 
			dark = int(255 - 128*(hpFrac))
			img[0].fill((255,dark,dark,255), special_flags=BLEND_RGB_MULT)


			# Get Deathstar image
			ds = self.gs.deathstar
			dsImg = ds.sprite.get(ds.x-self.sprite.rect.left + 16,ds.y-self.sprite.rect.top + 32, ds.spriteIndex, ds.spriteAngle, ds.spriteScale)
			# Draw Deathstar shadow w/ subtractive blending, at 64/255 = 25% alpha
			dsImg[0].fill((255,255,255,64), special_flags = BLEND_RGBA_SUB)
			img[0].blit(dsImg[0], dsImg[1])
			

			# FINALLY, blit colored/shadowed image to screen
			screen.blit(img[0], img[1])
			

			# Return position/scale to normal
			self.x -= ranX
			self.y -= ranY
			self.spriteScale -= ranSc
