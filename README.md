# Pytential-Fields

#### Note: A web application version of this program is available at www.lehett.net/PotentialFieldVisualizer.

<p>Potential field simulations are one method for solving robotic pathfinding problems. In this simulation, the cell in which the robot resides in the potential field represents the velocity with which the robot would move on its next time step.</p>
<p>Potential fields can be easily implemented via NumPy arrays. The starting potential field with no schemas applied to it is simply a zero-state, where all of the cells contain the velocity vector [0, 0]. However, by adding new schemas, such as repulsion, attraction, or target direction, you can begin to create a field that represents where a robot should go. In each of these schemas, a potential field that solves that problem alone is constructed. Then, this field is added to the current field that the robot is using. By layering potential fields in this way, you can create a potential field that solves the pathfinding problem given.</p>
<p>In this Python project, I wanted to explore how potential fields change as you add different schemas. The display is handled via PyGame, and is capable of displaying a potential field as a grid of arrows pointing in the direction of the velocity, with their size representing the magnitude of the vector.</p>

![Example Potential Field](https://github.com/jlehett/Pytential-Fields/blob/master/images/potentialfield.png)

An example potential field diagram produced with the program.

## How to Use

<p>First, you must initialize the pygame display which handles the PyGame window code. You may also want to specify a field size in this section and use that as the display dimensions.</p>

```python
from display import Display

FIELD_SIZE = (1600, 1000)

display = Display(FIELD_SIZE, windowTitle='Potential Field Testing')
```

<p>You must also initialize the potential field itself.</p>

```python
import potentialField as pf

potentialField = pf.PotentialField(FIELD_SIZE)
```

<p>Then you can add any schemas you would like to the potential field, with specified properties. Schemas control how the potential field changes. Schemas can include things like repulsion from a specified point, attraction to a point, flow towards a specified direction, and more. Schemas can be added to the potential field using the <i>addSchema()</i> function provided by the <i>PotentialField</i> class.</p>
<p><i>addSchema()</i> takes 1 type argument and then as many kwargs as the schema type calls for. The constants representing each schema type and the kwargs each schema takes will be specified below.</p>

```python
"""
IN_DIRECTION causes the potential field to flow in the direction specified by the kwargs. Magnitude represents the strength this
schema has on the field, and angle is the angle given in radians in which the field should flow.
"""
potentialField.addSchema(
  pf.IN_DIRECTION,
  magnitude=__float__, angle=__float__
)

"""
TO_TARGET causes the potential field to flow towards a coordinate specified by the kwargs. As opposed to ATTRACT, this schema will 
have a greater magnitude the further away it is from the target and it will slow down as it gets closer to the target. TargetPos 
represents the specified coordinate the field should flow towards, minVel represents the minimum strength this schema has on the
field, and maxVel represents the maximum strength this schema has on the field.
"""
potentialField.addSchema(
  pf.TO_TARGET,
  targetPos=__(float, float)__, minVel=__float__, maxVel=__float__
)

"""
REPULSE causes the potential field to flow away from a coordinate specified by the kwargs. RepulsePos represents the specified 
coordinate the field should flow away from, radius represents the influence size the schema has on the potential field, minVel 
represents the minimum strength this schema has on the field, and maxVel represents the maximum strength this schema has on the
field.
"""
potentialField.addSchema(
  pf.REPULSE,
  repulsePos=__(float, float)__, radius=__float__, minVel=__float__, maxVel=__float__
)

"""
ATTRACT causes the potential field to flow towards a coordinate specified by the kwargs. As opposed to TO_TARGET, this schema will
have a smaller magnitude the further away it is from the target and it will speed up as it gets closer to the target. AttractPos 
represents the specified coordinate the field should flow towards, radius represents the influence size the schema has on the 
potential field, minVel represents the minimum strength this schema has on the field, and maxVel represents the maximum strength 
this schema has on the field.
"""
potentialField.addSchema(
  pf.ATTRACT,
  attractPos=__(float, float)__, radius=__float__, minVel=__float__, maxVel=__float__
)

"""
CENTER_VERTICAL pushes the potential field towards the center of the screen, vertically, as if constricted through a hallway. 
BorderRadius represents the size of the 'hallway', and maxVel represents the maximum strength this schema has on the field.
"""
potentialField.addSchema(
  pf.CENTER_VERTICAL,
  borderRadius=__float__, maxVel=__float__
)

"""
CENTER_HORIZONTAL pushes the potential field towards the center of the screen, horizontally, as if constricted through a hallway. 
BorderRadius represents the size of the 'hallway', and maxVel represents the maximum strength this schema has on the field.
"""
potentialField.addSchema(
  pf.CENTER_HORIZONTAL,
  borderRadius=__float__, maxVel=__float__
)

"""
RANDOM_NOISE introduces random noise into the field with the hopes of preventing a robot from getting stuck in a zero-sum state.
MaxVel represents the maximum strength this schema has on the field.
"""
potentialField.addSchema(
  pf.RANDOM_NOISE,
  maxVel=__float__
)
```

<p>Once you are done adding schemas, you can choose to clamp the field down to a certain maximum magnitude with the <i>clampField</i> function:</p>

```python
potentialField.clampField(15.0)   # Where 15.0 is the maximum magnitude of the field
```

<p>From there, the standard way to display the potential field is given below:</p>

```python
# Import the PyGame library
import pygame

# Main loop for refreshing the display
while True:
  # Handle events for quitting the simulation
  event = pygame.event.poll()
  if event.type == pygame.QUIT:
    break
  if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_ESCAPE:
      break
    if event.key == pygame.K_q:
      break
  
  # Clear the screen to black before rendering next frame
  display.clearScreen()
  
  # Draw the potential field to the screen
  pf.drawPotentialField(
    display.getScreen(),
    FIELD_SIZE,
    stride=(20, 20)
  )
  
  # Update the display to show the current frame
  display.updateScreen()
  
# Shut down the pygame display
display.shutDown()
```
