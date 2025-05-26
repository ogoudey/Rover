import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


# from custom messages import the custom message

import pygame

class KeyboardInput(Node):
    def __init__(self):
        super().__init__('keyboard_input')
        
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        
        pygame.init()
        
        screen = pygame.display.set_mode((400,300))
        pygame.display.set_caption("Key Press")
        screen.fill((0,0,0))

        clock = pygame.time.Clock()
        
        effort = Effort()
        while True:
            pygame.event.get()
            pressed = pygame.key.get_pressed()
            msg = Twist()
            if pressed[pygame.K_UP]:
                effort.forward()
            if pressed[pygame.K_DOWN]:
                effort.backward()               
            if pressed[pygame.K_RIGHT]:
                effort.right()
            if pressed[pygame.K_LEFT]:
                effort.left()
                
            
            msg = Twist()
            msg.linear.x, msg.angular.z = effort.twist()
            print(msg.linear.x, msg.angular.z)
            self.publisher.publish(msg)
            
            effort.decay()
            pygame.display.flip()
            clock.tick(60) # hz
        pygame.quit()

class Effort:
    def __init__(self):
        self.turn = 0
        self.forw = 0
        
        self.turn_acceleration = 0.01 # Ultimately proportional to [-1, 1] of motor
        self.forward_acceleration = 0.01
        self.brake = 0.1
        
    def twist(self):
        return float(self.forw), float(self.turn)

    def decay(self):
        self.turn *= 0.99
        self.forw *= 0.99


        
    def right(self):
        self.turn += self.turn_acceleration

    def left(self):
        self.turn -= self.turn_acceleration
        
    def forward(self):
        self.forw += self.forward_acceleration
        
    def backward(self):
        if self.forw < 0:
            self.forw -= self.forward_acceleration/2
        else:
            self.forw -= self.brake
        
def main(args=None):
    rclpy.init(args=args)
    kbi = KeyboardInput()
    rclpy.spin(kbi)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
