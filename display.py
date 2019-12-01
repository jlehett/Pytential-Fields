"""
    External Library Imports
"""

import pygame


"""
    CONSTANTS
"""

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


"""
    Display Class
"""

class Display:
    def __init__(self, windowSize, isFullscreen=False, 
                 windowTitle="Display"):
        """
            Create the pygame display for showing the potential fields.
        """
        # Initialize pygame
        pygame.init()
        # Setup the pygame screen with specified options
        self.windowSize = windowSize
        if isFullscreen:
            self.screen = pygame.display.set_mode(
                windowSize, pygame.FULLSCREEN
                )
        else:
            self.screen = pygame.display.set_mode(
                windowSize
            )
        # Setup the pygame display title
        pygame.display.set_caption(windowTitle)

    def getScreen(self):
        """
            Return the pygame window for display purposes.
        """
        return self.screen

    def getScreenDimensions(self):
        """
            Return the screen pixel dimensions in (x, y) format.
        """
        return self.windowSize

    def shutDown(self):
        """
            Shut down the pygame display.
        """ 
        pygame.quit()

    def updateScreen(self):
        """
            Update the pygame display
        """
        pygame.display.flip()
    
    def changeWindowTitle(self, title):
        """
            Change the title of the pygame display window.
        """
        pygame.display.set_caption(title)

    def clearScreen(self, backgroundColor=BLACK):
        """
            Fill the screen with the defined background color
            (default is black)
        """
        self.screen.fill(backgroundColor)


""" 
    Testing
"""

if __name__ == '__main__':
    display = Display((500, 500), windowTitle='Hello There')
    
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
            
        display.clearScreen()

        pygame.draw.circle(display.getScreen(), WHITE, (250, 250), 100)

        display.updateScreen()

    display.shutDown()