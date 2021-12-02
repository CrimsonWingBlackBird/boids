from tkinter import *
import math
import numpy as np
from vector2D import Vector2D


class Boid():

    # Initializes the boid
    def __init__(self, x, y, width, height):
        self.position = Vector2D(x, y)
        vec = (np.random.rand(2) - 0.5)*10
        self.velocity = Vector2D(*vec)
        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector2D(*vec)

    # Draws the boid on the canvas
    def show(self, canvas):
        radius = 3
        coord = (self.position.x - radius, self.position.y - radius,
                 self.position.x + radius, self.position.y + radius)
        canvas.create_oval(coord, fill="red")

    # Calls the behavior functions
    def behavior(self, boids):
        self.cohesion(boids)
        self.seperation(boids)
        self.alignment(boids)

    # Makes the boids stick together.
    def cohesion(self, boids):
        neighborList = self.neighborBoids(boids, 50)
        averageNeighborList = Vector2D(0, 0)
        for boid in neighborList:
            averageNeighborList += boid.position
        averageNeighborList = averageNeighborList/len(neighborList)
        self.velocity += 0.05*(averageNeighborList-self.position)

    # Makes the boids not get too close
    def seperation(self, boids):
        neighborList = self.neighborBoids(boids, 20)
        averageNeighborList = Vector2D(0, 0)
        for boid in neighborList:
            averageNeighborList += boid.position
        averageNeighborList = averageNeighborList/len(neighborList)
        self.velocity += 0.20*(self.position - averageNeighborList)

    # Makes the boids go in the same direction as their neighbors
    def alignment(self, boids):
        neighborList = self.neighborBoids(boids, 50)
        averageNeighborList = Vector2D(0, 0)
        for boid in neighborList:
            averageNeighborList += boid.velocity
        averageNeighborList = averageNeighborList/len(neighborList)
        self.acceleration += 0.05*(averageNeighborList-self.velocity)

    # Steers the boids away from the edges
    # NEED TO UPDATE USING sizeX AND sizeY
    def edges(self):
        if (self.position.x >= 900):
            self.acceleration.x -= 1
        if (self.position.x <= 100):
            self.acceleration.x += 1
        if (self.position.y >= 900):
            self.acceleration.y -= 1
        if (self.position.y <= 100):
            self.acceleration.y += 1

    # Pushes velocity and position changes to boids
    def update(self):
        self.applySpeedLimit()
        self.position += self.velocity
        self.velocity += self.acceleration
        self.acceleration = Vector2D(0, 0)

    # Stops the boids from going too fast
    def applySpeedLimit(self):
        if (self.velocity.mag() > 10):
            self.velocity = self.velocity.normalize()
            self.velocity = self.velocity*10
        pass

    # Finds the distance between two vectors
    def distance(self, vector1, vector2):
        differenceVector = vector1 - vector2
        return differenceVector.mag()

    # Finds boids nearby, in a certain radius
    def neighborBoids(self, boids, radius):
        neighborList = []
        for boid in boids:
            distance = self.distance(self.position, boid.position)
            if (distance <= radius):
                neighborList.append(boid)
        return neighborList
