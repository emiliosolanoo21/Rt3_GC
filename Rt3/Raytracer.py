import pygame
from pygame.locals import * 
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 512
height = 512

pygame.init()

screen = pygame.display.set_mode((width,height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE | pygame.SCALED)
screen.set_alpha(None)

raytracer = Raytracer(screen)

#Se puede usar cualquier formato de imagen.
#hdri-hub.com
#raytracer.envMap = pygame.image.load("images/day.jpg")
raytracer.rtClearColor(0.25,0.25,0.25)

#Carga de texturas
couch1Texture = pygame.image.load("images/couch1.jpg")
couch2Texture = pygame.image.load("images/couch2.jpg")
flowTexture = pygame.image.load("images/flow.jpg")

#Carga de materiales
couch1 = Material(texture = couch1Texture, spec = 20, ks = 0.01)
couch2 = Material(texture = couch2Texture, spec = 20, ks = 0.01)
reflectFlow = Material(texture = flowTexture, spec = 64, ks = 0.1, matType= REFLECTIVE)

concrete = Material(diffuse=(0.5,0.5,0.5))
c1 = Material(diffuse=(0.67,0.83,0.78))
c2 = Material(diffuse=(0.890,746,0.37))
c3 = Material(diffuse=(0.26,0.35,0.26))
c4 = Material(diffuse=(0.59,0.98,0.35))

#Colocacion de paredes
raytracer.scene.append(Plane(position=(0,-2,0), normal = (0,1,-0.02), material = c1))
raytracer.scene.append(Plane(position=(0,5,0), normal = (0,1,0.2), material = c2))
raytracer.scene.append(Plane(position=(4,0,0), normal = (1,0,0.2), material = c3))
raytracer.scene.append(Plane(position=(-4,0,0), normal = (1,0,-0.2), material = c4))
raytracer.scene.append(Plane(position=(0,0,-20), normal = (0,0,0.2), material = concrete))

#Colocacion de cubos
raytracer.scene.append(AABB(position=(1.5,-0.5,-5), size = (1.5,1.5,1.5), material = couch1))
raytracer.scene.append(AABB(position=(-1.5,-0.5,-5), size = (1.25,1.25,1.25), material = couch2))

#Colocacion de disco
raytracer.scene.append(Disk(position=(0,1,-5), normal = (0,1,0), radius= 2, material= reflectFlow))

#iluminacion minima del ambiente
raytracer.lights.append(AmbientLight(intensity=0.3))
raytracer.lights.append(DirectionalLight(direction=(1,1,-2), intensity=0.95))
raytracer.lights.append(PointLight(point=(0,0,-5), intensity=150, color= (1,1,1)))

raytracer.rtClear()
raytracer.rtRender()

print("\nTiempo de renderizado:", pygame.time.get_ticks() / 1000, "segundos")

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning=False

rect = pygame.Rect(0,0,width,height)
sub = screen.subsurface(rect)
pygame.image.save(sub, "result.jpg")
                
pygame.quit()           