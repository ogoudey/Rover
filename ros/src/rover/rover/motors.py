import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

from gpiozero import Motor
from gpiozero import Device
from gpiozero.pins.lgpio import LGPIOFactory

Device.pin_factory = LGPIOFactory()

class MyMotor:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        self.motor = Motor(num1, num2)

    def forward(self):
        self.motor.forward()
        print("motor with pin ", str(self.num1), str(self.num2), "forward")
    def backward(self):
        self.motor.backward()
        print("motor with pin ", str(self.num1), str(self.num2), "backward")
    def stop(self):
        self.motor.stop()
        print("motor with pin ", str(self.num1), str(self.num2), "stopping")

class Motors(Node):
    def __init__(self):
        super().__init__('motors')
        
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.dumbly_actuate, 10)

        self.motor_bl = MyMotor(17, 27)
        self.motor_fl = MyMotor(22, 23)
        self.motor_br = MyMotor(24, 25)
        self.motor_fr = MyMotor(5, 6)
        
        self.all_motors = [self.motor_bl, self.motor_fl, self.motor_br, self.motor_fr]
        self.right_motors = [self.motor_br, self.motor_fr]
        self.left_motors = [self.motor_bl, self.motor_fl]

        
    def dumbly_actuate(self, msg):
        if msg.linear.x > 0.1:
            for motor in self.all_motors:
                motor.forward()
        elif msg.angular.z > 0.1:
            for motor in self.left_motors:
                motor.forward()
            if msg.angular.z > 0.5:
                for motor in self.right_motors:
                    motor.backward()
            else:
                for motor in self.right_motors:
                    motor.stop()
        elif msg.angular.z < -0.1:
            for motor in self.right_motors:
                motor.forward()
            if msg.angular.z < -0.5:
                for motor in self.left_motors:
                    motor.backward()
            else:
                for motor in self.right_motors:
                    motor.stop()
        elif msg.linear.x < -0.1:
            for motor in self.all_motors:
                motor.backward()
        else:
            for motor in self.all_motors:
                motor.stop()

                
            
            
    
def main(args=None):
    rclpy.init(args=args)
    m = Motors()
    rclpy.spin(m)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
        
        
