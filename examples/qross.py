from .framework import (Framework, Keys, main)
from .bridge import create_bridge
from math import sqrt
import math
from Box2D.b2 import (world)
from Box2D import (b2Color,b2CircleShape, b2EdgeShape, b2FixtureDef, b2PolygonShape,
                    b2_pi)



class MotorJoint (Framework):
    name = "MotorJoint"
    description = 'g to stop/go'
    count = 800


    def __init__(self):
       Framework.__init__(self)


       ground = self.world.CreateStaticBody(
             position=(0,0),
              shapes=b2PolygonShape(box=(1000,1)),
       )

       a=14.5
       b=12.2
       vertices=[]
       for i in range(16):
           ell_x=a*math.cos(22.5*i*math.pi/180)
           ell_y=b*math.sin(22.5*i*math.pi/180)

           vertices.append((ell_x,ell_y))

       self.qross = self.world.CreateDynamicBody(
           position=(0, 20),
           allowSleep=True,
           fixtures=b2FixtureDef(density=2.0, friction=0.6,
                                 shape=b2PolygonShape(vertices=vertices),),
       )

       self.ball = self.world.CreateStaticBody(
           fixtures=b2FixtureDef(
               shape=b2CircleShape(radius=2.2),
               density=1.0),
           bullet=True,
           position=(0, 1000))


       leg = self.world.CreateDynamicBody(
           position=(0, 20),
           allowSleep=True,
           fixtures=b2FixtureDef(density=2.0, friction=0.0,
                                 shape=b2PolygonShape(vertices=[(20,1.3),
                                     (0,1.3),
                                     (0,0),
                                     (20,0)]),),
       )

       self.world.CreateRevoluteJoint(
           bodyA=leg,
           bodyB=self.qross,
           anchor=(0, 20),
       )


       self.joint = self.world.CreateMotorJoint(bodyA=leg, bodyB=self.qross,
                                 maxForce=0, maxTorque=500000)

       self.go = False
       self.time = 0.0

    def Keyboard(self, key):                         
        if key == Keys.K_g:
            self.go = not self.go



    def Step(self, settings):
        Framework.Step(self, settings)

        if self.go and settings.hz > 0.0:
            self.time += 1.0 / settings.hz

        linear_offset =self.qross.position# (6 * sin(2.0 * self.time), 8.0 +
                         #4.0 * sin(1.0 * self.time))
        angular_offset = -2.0 * self.time
        center=[self.qross.position]
        print(type(center))

        self.joint.linearOffset = linear_offset#linear_offset
        self.joint.angularOffset = angular_offset

        renderer = self.renderer
        renderer.DrawPoint(renderer.to_screen(
            linear_offset), 4, b2Color(0.9, 0.9, 0.9))
        self.viewCenter=(self.qross.position)



   
if __name__ == "__main__":
    main(MotorJoint)



