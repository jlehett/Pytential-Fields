"""
    External Library Imports
"""

import numpy as np
import pygame
import math


"""
    DEFINE CONSTANTS
"""

IN_DIRECTION = 0
TO_TARGET = 1
REPULSE = 2
ATTRACT = 3
CENTER_VERTICAL = 4
CENTER_HORIZONTAL = 5
RANDOM_NOISE = 6

LINE_WIDTH = 3


"""
    Aux Functions
"""

@np.vectorize
def cvtRange(x, in_min, in_max, out_min, out_max):
    """
        Convert a value, x, from its old range of
        (in_min to in_max) to the new range of
        (out_min to out_max)
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def drawArrow(surface, startCoord, endCoord):
    """
        Draw an arrow via pygame.
    """
    A = startCoord
    B = endCoord
    dir_ = (B[0] - A[0], B[1] - A[1])
    dir_mag = math.sqrt(dir_[0]**2 + dir_[1]**2)
    H = dir_mag / 4.0
    W = H * 2.0
    if dir_mag == 0:
        dir_mag = 0.00001
    dir_ = (dir_[0] / dir_mag, dir_[1] / dir_mag)

    q = (dir_[1], -dir_[0])

    C = (
        B[0] - (H * dir_[0]) + (W * q[0]/2.0),
        B[1] - (H * dir_[1]) + (W * q[1]/2.0)
    )

    D = (
        B[0] - (H * dir_[0]) - (W * q[0]/2.0),
        B[1] - (H * dir_[1]) - (W * q[1]/2.0)
    )

    pygame.draw.line(
        surface, (255, 255, 255), A, B, LINE_WIDTH
    )
    pygame.draw.line(
        surface, (255, 255, 255), B, C, LINE_WIDTH
    )
    pygame.draw.line(
        surface, (255, 255, 255), B, D, LINE_WIDTH
    )



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
                drawArrow(
                    surface, 
                    (startPixelX, startPixelY),
                    (endPixelX, endPixelY)
                )
    
    def clampField(self, maxVel):
        """
            Clamp potential field such that the magnitude does not
            exceed maxVel
        """
        magnitudeField = np.sqrt(
            self.field[:, :, 0] ** 2 + self.field[:, :, 1] ** 2
        )
        magnitudeField = np.clip(
            magnitudeField, 0.000001, math.inf
        )
        normalField = np.zeros(
            (self.fieldSize[0], self.fieldSize[1], 2)
        )
        normalField[:, :, 0] = self.field[:, :, 0] / magnitudeField
        normalField[:, :, 1] = self.field[:, :, 1] / magnitudeField
        magnitudeField = np.clip(magnitudeField, 0, maxVel)
        self.field[:, :, 0] = normalField[:, :, 0] * magnitudeField
        self.field[:, :, 1] = normalField[:, :, 1] * magnitudeField

    def addSchema(self, type, **kwargs):
        """
            Add schema to the potential field by adding the new vector
            field to the current vector field
        """
        if type == IN_DIRECTION:
            self.field += self.inDirectionSchema(kwargs)
        if type == TO_TARGET:
            self.field += self.toTargetSchema(kwargs)
        if type == REPULSE:
            self.field += self.repulseSchema(kwargs)
        if type == ATTRACT:
            self.field += self.attractSchema(kwargs)
        if type == CENTER_VERTICAL:
            self.field += self.centerVerticalSchema(kwargs)
        if type == CENTER_HORIZONTAL:
            self.field += self.centerHorizontalSchema(kwargs)
        if type == RANDOM_NOISE:
            self.field += self.randomNoiseSchema(kwargs)
    
    def inDirectionSchema(self, kwargs):
        """
            Add schema that goes in the specified direction.
            
            kwargs should contain:
                magnitude (float)
                angle (float) -- in radians
        """
        field = np.ones(
            (self.fieldSize[0], self.fieldSize[1], 2)
        )
        field *= np.array(
            [math.cos(kwargs['angle']),
            math.sin(kwargs['angle'])]
        )
        field *= kwargs['magnitude']
        return field

    def toTargetSchema(self, kwargs):
        """
            Add schema that goes in the specified direction.

            kwargs should contain:
                targetPos (float, float)
                minVel (float)
                maxVel (float)
        """
        targetPos = kwargs['targetPos']
        # Create coordinate array to find distance
        x = np.linspace(0, self.fieldSize[0]-1, self.fieldSize[0])
        y = np.linspace(0, self.fieldSize[1]-1, self.fieldSize[1])
        meshgrid = np.meshgrid(x, y, sparse=False, indexing='ij')
        # Find distance from coordinate to target
        meshgridX = meshgrid[0] - targetPos[0]
        meshgridY = meshgrid[1] - targetPos[1]
        # Create field out of these distance calculations
        field = np.zeros(
            (self.fieldSize[0], self.fieldSize[1], 2)
        )
        field[:, :, 0] = meshgridX
        field[:, :, 1] = meshgridY
        # Clamp the values of the field.
        magnitudeField = np.sqrt(
            field[:, :, 0] ** 2 + field[:, :, 1] ** 2
        )
        magnitudeField = np.clip(
            magnitudeField, 0.0000001, math.inf
        )
        normalField = np.zeros(
            (self.fieldSize[0], self.fieldSize[1], 2)
        )
        normalField[:, :, 0] = field[:, :, 0] / magnitudeField
        normalField[:, :, 1] = field[:, :, 1] / magnitudeField
        magnitudeField = np.clip(
            magnitudeField, kwargs['minVel'], kwargs['maxVel']
        )
        field[:, :, 0] = normalField[:, :, 0] * -magnitudeField
        field[:, :, 1] = normalField[:, :, 1] * -magnitudeField
        return field
        
    def repulseSchema(self, kwargs):
        """
            Add schema that avoids a specified coordinate.

            kwargs should contain:
                repulsePos (float, float)
                radius (float)
                minVel (float)
                maxVel (float)
        """
        repulsePos = kwargs['repulsePos']
        # Create coordinate array to find distance
        x = np.linspace(0, self.fieldSize[0]-1, self.fieldSize[0])
        y = np.linspace(0, self.fieldSize[1]-1, self.fieldSize[1])
        meshgrid = np.meshgrid(x, y, sparse=False, indexing='ij')
        # Find distance from target to coordinate
        meshgridX = meshgrid[0] - repulsePos[0]
        meshgridY = meshgrid[1] - repulsePos[1]
        # Create field out of these distance calculations
        field = np.zeros(
            (self.fieldSize[0], self.fieldSize[1], 2)
        )
        field[:, :, 0] = meshgridX
        field[:, :, 1] = meshgridY
        # Create magnitude field representing these distances
        magnitudeField = np.sqrt(
            field[:, :, 0] ** 2 + field[:, :, 1] ** 2
        )
        magnitudeField = np.clip(
            magnitudeField, 0.0000001, math.inf
        )
        # Create normal field
        normalField = np.zeros(
            (self.fieldSize[0], self.fieldSize[1], 2)
        )
        normalField[:, :, 0] = field[:, :, 0] / magnitudeField
        normalField[:, :, 1] = field[:, :, 1] / magnitudeField
        # Adjust magnitude field to fit radius parameter
        magnitudeField[
            np.where(magnitudeField <= kwargs['radius'])
        ] = cvtRange(magnitudeField[
            np.where(magnitudeField <= kwargs['radius'])
        ], 0, kwargs['radius'], kwargs['maxVel'], kwargs['minVel'])
        magnitudeField[
            np.where(magnitudeField > kwargs['radius'])
        ] = 0
        # Create final field
        field[:, :, 0] = normalField[:, :, 0] * magnitudeField
        field[:, :, 1] = normalField[:, :, 1] * magnitudeField
        return field 

    def attractSchema(self, kwargs):
        """
            Add schema that avoids a specified coordinate.

            kwargs should contain:
                attractPos (float, float)
                radius (float)
                minVel (float)
                maxVel (float)
        """
        attractPos = kwargs['attractPos']
        # Create coordinate array to find distance
        x = np.linspace(0, self.fieldSize[0]-1, self.fieldSize[0])
        y = np.linspace(0, self.fieldSize[1]-1, self.fieldSize[1])
        meshgrid = np.meshgrid(x, y, sparse=False, indexing='ij')
        # Find distance from target to coordinate
        meshgridX = attractPos[0] - meshgrid[0]
        meshgridY = attractPos[1] - meshgrid[1]
        # Create field out of these distance calculations
        field = np.zeros(
            (self.fieldSize[0], self.fieldSize[1], 2)
        )
        field[:, :, 0] = meshgridX
        field[:, :, 1] = meshgridY
        # Create magnitude field representing these distances
        magnitudeField = np.sqrt(
            field[:, :, 0] ** 2 + field[:, :, 1] ** 2
        )
        magnitudeField = np.clip(
            magnitudeField, 0.0000001, math.inf
        )
        # Create normal field
        normalField = np.zeros(
            (self.fieldSize[0], self.fieldSize[1], 2)
        )
        normalField[:, :, 0] = field[:, :, 0] / magnitudeField
        normalField[:, :, 1] = field[:, :, 1] / magnitudeField
        # Adjust magnitude field to fit radius parameter
        magnitudeField[
            np.where(magnitudeField <= kwargs['radius'])
        ] = cvtRange(magnitudeField[
            np.where(magnitudeField <= kwargs['radius'])
        ], 0, kwargs['radius'], kwargs['maxVel'], kwargs['minVel'])
        magnitudeField[
            np.where(magnitudeField > kwargs['radius'])
        ] = 0
        # Create final field
        field[:, :, 0] = normalField[:, :, 0] * magnitudeField
        field[:, :, 1] = normalField[:, :, 1] * magnitudeField
        return field 

    def centerVerticalSchema(self, kwargs):
        """
            Add schema that pushes the potential field towards the
            center of the screen, vertically.

            kwargs should contain:
                borderRadius (float)
                maxVel (float)
        """
        # Create field
        field = np.zeros(
            (self.fieldSize[0], self.fieldSize[1], 2)
        )
        # Set center-pushing values
        field[:, :kwargs['borderRadius'], 1] = kwargs['maxVel']
        field[:, -kwargs['borderRadius']:, 1] = -kwargs['maxVel']
        return field

    def centerHorizontalSchema(self, kwargs):
        """
            Add schema that pushes the potential field towards the
            center of the screen, horizontally.

            kwargs should contain:
                borderRadius (float)
                maxVel (float)
        """
        # Create field
        field = np.zeros(
            (self.fieldSize[0], self.fieldSize[1], 2)
        )
        # Set center-pushing values
        field[:kwargs['borderRadius'], :, 0] = kwargs['maxVel']
        field[-kwargs['borderRadius']:, :, 0] = -kwargs['maxVel']
        return field

    def randomNoiseSchema(self, kwargs):
        """
            Add schema that introduces random noise into the field
            with the hopes of preventing a robot from getting stuck.

            kwargs should contain:
                maxVel (float)
        """
        # Create random field
        field = np.random.rand(
            self.fieldSize[0], self.fieldSize[1], 2
        )
        field[:, :, 0] = cvtRange(
            field[:, :, 0], 0.0, 1.0, -1.0, 1.0
        )
        field[:, :, 1] = cvtRange(
            field[:, :, 1], 0.0, 1.0, -1.0, 1.0
        )
        # Get magnitude field
        magnitudeField = np.sqrt(
            field[:, :, 0] ** 2 + field[:, :, 1] ** 2
        )
        magnitudeField = np.clip(
            magnitudeField, 0.0000001, math.inf
        )
        # Create normal field
        normalField = np.zeros(
            (self.fieldSize[0], self.fieldSize[1], 2)
        )
        normalField[:, :, 0] = field[:, :, 0] / magnitudeField
        normalField[:, :, 1] = field[:, :, 1] / magnitudeField
        # Re-scale the normal field
        field[:, :, 0] = normalField[:, :, 0] * kwargs['maxVel']
        field[:, :, 1] = normalField[:, :, 1] * kwargs['maxVel']
        return field



"""
    Testing
"""

if __name__ == '__main__':
    from display import Display

    FIELD_SIZE = (1600, 1000)

    display = Display(FIELD_SIZE, windowTitle='Potential Field')
    pf = PotentialField(FIELD_SIZE)

    pf.addSchema(
        CENTER_VERTICAL,
        borderRadius=200, maxVel=1000.0
    )
    
    pf.addSchema(
        REPULSE,
        repulsePos=(FIELD_SIZE[0] * 1.0/5.0, 350),
        minVel=0, maxVel=40, radius=250
    )

    pf.addSchema(
        REPULSE,
        repulsePos=(FIELD_SIZE[0] * 2.0/5.0, 650),
        minVel=0, maxVel=40, radius=250
    )

    pf.addSchema(
        REPULSE,
        repulsePos=(FIELD_SIZE[0] * 3.0/5.0, 500),
        minVel=0, maxVel=40, radius=250
    )

    pf.addSchema(
        IN_DIRECTION,
        magnitude=20.0, angle=0.0
    )

    pf.addSchema(
        RANDOM_NOISE,
        maxVel=3.0
    )

    pf.clampField(15.0)
    
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break
            if event.key == pygame.K_q:
                break
            
        display.clearScreen()

        pf.drawPotentialField(
            display.getScreen(),
            FIELD_SIZE,
            stride=(20, 20)
        )

        display.updateScreen()

    display.shutDown()