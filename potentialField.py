"""
    External Library Imports
"""

import numpy as np
import pygame
import math


"""
    Aux Functions
"""

def cvtRange(x, in_min, in_max, out_min, out_max):
    """
        Convert a value, x, from its old range of
        (in_min to in_max) to the new range of
        (out_min to out_max)
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


"""
    Potential Field Class
"""

class PotentialField:
    def __init__(self, fieldSize):
        """
            Class that holds info about potential fields, and is capable
            of displaying them to a pygame display.
        """
        self.fieldSize = fieldSize
        # Create Numpy array to store the potential field information.
        # The last axis holds 2 values representing a vector, [x, y].
        self.field = np.zeros(
            (fieldSize[0], fieldSize[1], 2)
        )

        self.field += np.random.normal(
            0, 10, (fieldSize[0], fieldSize[1], 2)
        )
    
    def drawPotentialField(self, surface, surfaceSize, stride=(3, 3)):
        """
            Draw the potential field to the pygame surface.

            stride dictates how many potential cells to skip in
            between drawing
        """
        # Iterate through the field with proper strides
        bufferX = math.floor(stride[0] / 2.0)
        bufferY = math.floor(stride[1] / 2.0)
        for fieldX in range(bufferX, self.fieldSize[0] - bufferX, stride[0]):
            for fieldY in range(bufferY, self.fieldSize[1] - bufferY, stride[1]):
                # Grab the field vector for the cell
                fieldVector = self.field[fieldX, fieldY]
                # Determine the x and y coordinate for the origin of the
                # potential line segment.
                startPixelX = math.floor(cvtRange(fieldX, 0, self.fieldSize[0],
                                    0, surfaceSize[0]))
                startPixelY = math.floor(cvtRange(fieldY, 0, self.fieldSize[1],
                                    0, surfaceSize[1]))
                # Determine the x and y coordinate for the end point of the
                # potential line segment.
                endPixelX = math.floor(startPixelX + fieldVector[0])
                endPixelY = math.floor(startPixelY + fieldVector[1])
                # Draw the vector to the pygame surface
                if startPixelX == endPixelX and startPixelY == endPixelY:
                    pygame.draw.circle(
                        surface, (255, 255, 255),
                        (startPixelX, startPixelY), 
                        math.floor(min(stride[0]/8.0, stride[1]/8.0))
                    )
                else:
                    pygame.draw.line(
                        surface, (255, 255, 255),
                        (startPixelX, startPixelY), (endPixelX, endPixelY)
                    )



"""
    Testing
"""

if __name__ == '__main__':
    from display import Display

    display = Display((500, 500), windowTitle='Potential Field')
    pf = PotentialField((500, 500))
    
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
            
        display.clearScreen()

        pf.drawPotentialField(
            display.getScreen(),
            (500, 500),
            stride=(20, 20)
        )

        display.updateScreen()

    display.shutDown()