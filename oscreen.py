import sys
import os
import pygame
import math
import time
import random
from pygame.locals	import *
from pygame.gfxdraw	import *
from math2		import *
from drawable 		import Drawable
from linalg		import *

MAX_DEPTH = 300;
CLEAR_PIXEL = (255, 0, 0, MAX_DEPTH)


tempVert1 = createVecPoint(0,0,0)
tempVert2 = createVecPoint(0,0,0)
tempVert3 = createVecPoint(0,0,0)


class OScreen(object):
	def __init__(self, gs, resW, resH, outW, outH):
		self.gs = gs
		self.resolutionWidth = resW
		self.resolutionHeight = resH
		self.drawResolution = self.drawWidth,self.drawHeight = outW,outH


		self.R = 255
		self.G = 255
		self.B = 255
		self.tex = pygame.image.load("img/test.bmp")
		self.texW = self.tex.get_width()
		self.texH = self.tex.get_height()
		
		self.near = .1
		self.far = MAX_DEPTH
		self.doFog = True


		self.viewMat = createMat16(0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)
		self.projMat = createMat16(0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)
		self.modelMat = createMat16(0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)
		self.completeMat = createMat16(0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0)
		setMatIdentity(self.completeMat)

		self.pixels = [None] * self.resolutionWidth
		for x in range(0, self.resolutionWidth):
			self.pixels[x] = [None] * self.resolutionHeight
			for y in range(0, self.resolutionHeight):
				self.pixels[x][y] = [0,0,0,0]

		self._img = pygame.Surface( (self.resolutionWidth,self.resolutionHeight) ).convert_alpha()
		self.rect = self._img.get_rect()


	def setXYtoTuple(self, x, y, tup):
		self.setXYtoRGBD(x, y, tup[0], tup[1], tup[2], tup[3])

	def setXYtoRGBD(self, x, y, r, g, b, depth):
		x = int(x)
		y = int(y)

		if x < 0 or x >= self.resolutionWidth or y < 0 or y >= self.resolutionHeight:
			return
		self.fastXYtoRGBD(x,y,r,g,b,depth)



	def fastXYtoTuple(self, x, y, tup):
		self.fastXYtoRGBD(x, y, tup[0], tup[1], tup[2], tup[3])

	def fastXYtoRGBD(self, x, y, r, g, b, depth):
		if depth >= self.near and depth <= self.far:
			pix = self.pixels[x][y]

			if depth < pix[3]:
				pix[0] = r
				pix[1] = g
				pix[2] = b
				pix[3] = depth

	def forceXYtoTuple(self, x, y, tup):
		self.forceXYtoRGBD(x,y, tup[0], tup[1], tup[2], tup[3])

	def forceXYtoRGBD(self, x, y, r, g, b, depth):
		pix = self.pixels[x][y]
		pix[0] = r
		pix[1] = g
		pix[2] = b
		pix[3] = depth


	def clear(self):
		for x in range(0, self.resolutionWidth):
			for y in range(0, self.resolutionHeight):
				pix = self.pixels[x][y]
				pix[0] = CLEAR_PIXEL[0]
				pix[1] = CLEAR_PIXEL[1]
				pix[2] = CLEAR_PIXEL[2]
				pix[3] = CLEAR_PIXEL[3]

	def tick(self, input):
		pass

	def clearStatic(self):
		for x in range(0, self.resolutionWidth):
			for y in range(0, self.resolutionHeight):
				val = 255*rnd()
				self.setXYtoRGBD(x,y, val, val, val, 0)

	def draw3dFloor(self, x1,y1,x2,y2, z):
		self.drawQuad(x1,y1,z,0,0,  x2,y1,z,1,0,  x2,y2,z,1,1,  x1,y2,z,0,1)
	def draw3dWall(self, x1,y1,z1, x2,y2,z2):
		self.drawQuad(x1,y1,z1,0,0,  x2,y2,z1,1,0,  x2,y2,z2,1,1,  x1,y1,z2,0,1)

		
	def drawQuad(self, x1,y1,z1,u1,v1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3,  x4,y4,z4,u4,v4):
		self.drawTriangle(x1,y1,z1,u1,u1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3)
		self.drawTriangle(x3,y3,z3,u3,v3,  x4,y4,z4,u4,v4,  x1,y1,z1,u1,v1)

	def drawPoint(self, x,y,z):
		set4(tempVert1, x,y,z,1)
		multMatVec(self.completeMat, tempVert1, tempVert1)

		
	def drawTriangle(self, x1,y1,z1,u1,v1,  x2,y2,z2,u2,v2,  x3,y3,z3,u3,v3):
		set4(tempVert1, x1,y1,z1,1)
		set4(tempVert2, x2,y2,z2,1)
		set4(tempVert3, x3,y3,z3,1)

		multMatVec(self.completeMat, tempVert1, tempVert1)
		multMatVec(self.completeMat, tempVert2, tempVert2)
		multMatVec(self.completeMat, tempVert3, tempVert3)
		
		#printVec(tempVert1)
		#printVec(tempVert2)
		#printVec(tempVert3)
		
		ow1 = w1 = tempVert1[3]
		w1 = -abs(w1)
		x1 = tempVert1[0]/w1
		y1 = tempVert1[1]/w1
		z1 = tempVert1[2] #/w1

		ow2 = w2 = tempVert2[3]				
		w2 = -abs(w2)
		x2 = tempVert2[0]/w2
		y2 = tempVert2[1]/w2
		z2 = tempVert2[2] #/w2
		
		ow3 = w3 = tempVert3[3]
		w3 = -abs(w3)
		x3 = tempVert3[0]/w3
		y3 = tempVert3[1]/w3
		z3 = tempVert3[2] #/w3
		
		print str(ow1) + ", " + str(ow2) + ", " + str(ow3)
		
		if(ow1 > 0 and ow2 > 0 and ow3 > 0):
			return
		
		if (z1 < self.near and z2 < self.near and z3 < self.near) or (z1 > self.far and z2 > self.far and z3 > self.far):
			return
			
		miX = (x1 if x1 < x3 else x3) if x1 < x2 else (x2 if x2 < x3 else x3)
		miY = (y1 if y1 < y3 else y3) if y1 < y2 else (y2 if y2 < y3 else y3)
		maX = (x1 if x1 > x3 else x3) if x1 > x2 else (x2 if x2 > x3 else x3)
		maY = (y1 if y1 > y3 else y3) if y1 > y2 else (y2 if y2 > y3 else y3)		

		miX = int(0 if miX < 0 else miX)
		miY = int(0 if miY < 0 else miY)
		maX = int(maX if maX < self.resolutionWidth else self.resolutionWidth)
		maY = int(maY if maY < self.resolutionHeight else self.resolutionHeight)

		x21 = x2-x1
		x31 = x3-x1
		y21 = y2-y1
		y31 = y3-y1

		az = y21*(z3-z1) - y31*(z2-z1)
		bz = -x21*(z3-z1) + x31*(z2-z1)
		c = x21*y31 - x31*y21
		
		au = y21*(u3-u1) - y31*(u2-u1)
		bu = -x21*(u3-u1) + x31*(u2-u1)
		
		av = y21*(v3-v1) - y31*(v2-v1)
		bv = -x21*(v3-v1) + x31*(v2-v1)

		area = .5*(-y2*x3 + y1*(-x2+x3) + x1*(y2-y3) + x2*y3)
		
		if area == 0:
			return
		
		for y in range(miY,maY):
			for x in range(miX,maX):
				s = 1/(2*area)*(y1*x3 - x1*y3 + y31*x - x31*y)
				t = 1/(2*area)*(x1*y2 - y1*x2 - y21*x + x21*y)
				
				if 0 <= s and s <= 1 and 0 <= t and t <= 1 and s+t <= 1:
					depth = -(z1 + (az*(x-x1) + bz*(y-y1))/-c)
					
					u = int(self.texW * (u1 + (au*(x-x1) + bu*(y-y1))/-c))
					v = int(self.texH * (u1 + (av*(x-x1) + bv*(y-y1))/-c))
					
					if u >= 0 and u < self.texW and v >= 0 and v < self.texH:
						col = self.tex.get_at((u, v))
						self.R = col[0]
						self.G = col[1]
						self.B = col[2]
					else:
						self.R = 0
						self.G = 255
						self.B = 0						
										
					#maybe??
					depth *= -1
					self.fastXYtoRGBD(x,y, self.R,self.G,self.B, depth)

	def compileArrays(self):
		multMatMat(self.projMat, self.viewMat, self.completeMat)
		multMatMat(self.completeMat, self.modelMat, self.completeMat)		
					
	def finalize(self):
		self.clear();
		
		setMatIdentity(self.modelMat)
		setMatIdentity(self.viewMat)
		setMatIdentity(self.projMat)
		
		pl = self.gs.player
		
		frX = pl.x
		frY = pl.y
		frZ = pl.z
		
		#setMatLook(self.viewMat, frX,frY,frZ, toX,toY,toZ, 0,0,1)
		#addMatRotationZ(self.viewMat, 90)
		
		# CAMERA ROTATION
		addMatRotationX(self.viewMat, 90)
		addMatRotationZ(self.viewMat, -pl.dir)
		addMatRotationZ(self.viewMat, -90)
		addMatTranslation(self.viewMat, -pl.x,-pl.y,-pl.z)
		addMatRotationZ(self.viewMat, 90)
		
		
		# PROJECTION
		addMatTranslation(self.projMat, self.resolutionWidth/2, self.resolutionHeight/2,0)
		addMatScale(self.projMat, 1,1,-1)
		addMatPerspective2(self.projMat, self.resolutionWidth/self.resolutionHeight, 1.76, self.far, self.near) #5

		t = 50
		s = 30
		self.compileArrays()


		self.draw3dWall(-t,-t,t, -t,t, -s)
		
		
		
		#print()
		#self.draw3dFloor(-t,-t,t,t, -s)
		
		addMatTranslation(self.modelMat, 0,150,0)		
		#addMatRotationX(self.modelMat, epoch()*40)
		#addMatRotationY(self.modelMat, epoch()*50)
		addMatRotationZ(self.modelMat, epoch()*50)
		
		self.compileArrays()
		self.drawPoint(0,0,0)

		self.R = 0
		self.G = 0
		self.B = 255

		#self.draw3dWall(-s,-s,-s, s,-s,s)
		#self.draw3dWall(-s,s,-s, s,s,s)
		#self.draw3dWall(-s,-s,-s, -s,s,s)
		#self.draw3dWall(s,-s,-s, s,s,s)
		
		self.R = 0
		self.G = 255
		self.B = 0	
		#self.draw3dFloor(-s,-s,s,s, -s)				
		#self.draw3dFloor(-s,-s,s,s, s)

		
		# WHERE THE MAGIC HAPPENS
		for x in range(0, self.resolutionWidth):
			for y in range(0, self.resolutionHeight):
				pix = self.pixels[x][y]
				
				val = 1
				if self.doFog:
					val = (self.far-pix[3])/(self.far-self.near)
				
				pixel(self._img, x,y, (val*pix[0], val*pix[1], val*pix[2]))

		self.img = pygame.transform.scale(self._img, self.drawResolution) #smoothscale
		self.rect = self.img.get_rect()
		
	def draw(self, screen):
		self.finalize()
		screen.blit(self.img, self.rect)