import p5
import math
import numpy as np
from Vector2D import Vector2D

class Boid():

    def __init__(self, x, y, width, height):
        self.position = Vector2D(x,y)

        vec = (np.random.rand(2) - 0.5)*10
        self.velocity = Vector2D(*vec)

        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector2D(*vec)

    def show(self):
        p5.stroke(255)
        p5.circle((self.position.x, self.position.y), 3)

    def behavior(self, boids):
        self.cohesion(boids)
        self.seperation(boids)
        self.alignment(boids)

    def cohesion(self, boids):
        neighborList = self.neighborBoids(boids, 50)
        averageNeighborList = Vector2D(0,0)
        for boid in neighborList:
            averageNeighborList += boid.position
        averageNeighborList  = averageNeighborList/len(neighborList)
        self.velocity += averageNeighborList-self.position

    def seperation(self, boids):
        neighborList = self.neighborBoids(boids, 20)
        averageNeighborList = Vector2D(0,0)
        for boid in neighborList:
            averageNeighborList += boid.position
        averageNeighborList  = averageNeighborList/len(neighborList)
        self.velocity += self.position - averageNeighborList

    def alignment(self, boids):
        neighborList = self.neighborBoids(boids, 50)
        averageNeighborList = Vector2D(0,0)
        for boid in neighborList:
            averageNeighborList += boid.velocity
        averageNeighborList  = averageNeighborList/len(neighborList)
        self.acceleration += averageNeighborList-self.velocity


    def edges(self):
        if (self.position.x>=950):
            self.acceleration.x -= 1
        if (self.position.x<=50):
            self.acceleration.x += 1
        if (self.position.y>=950):
            self.acceleration.y -= 1
        if (self.position.y<=50):
            self.acceleration.y += 1

    def update(self):
        self.applySpeedLimit()
        self.position += self.velocity
        self.velocity += self.acceleration
        self.acceleration = Vector2D(0,0)

    def applySpeedLimit(self):
        if (self.velocity.mag() > 10):
            self.velocity = self.velocity.normalize()
            self.velocity = self.velocity*10
        pass

    def mag(self, vector):
        return math.sqrt(vector.x**2+vector.y**2)

    def distance(self, vector1, vector2):
        differenceVector = vector1 - vector2
        return differenceVector.mag()

    def neighborBoids(self, boids, radius):
        neighborList = []
        for boid in boids:
            distance = self.distance(self.position, boid.position)
            if (distance <= radius):
                neighborList.append(boid)
        return neighborList
