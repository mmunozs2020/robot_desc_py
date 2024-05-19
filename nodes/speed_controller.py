import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile
from rclpy.duration import Duration

class SpeedController(Node):
    def __init__(self):
        super().__init__('speed_controller')
        self.duration = 15.0
        self.max_speed = 1.5
        self.axis_time = 5.0
        self.acceleration = 0.3

        qos_profile = QoSProfile(depth=10)
        self.publisher_ = self.create_publisher(Twist, '/robot_base_control/cmd_vel_unstamped', qos_profile)
        
        self.timer_ = self.create_timer(0.05, self.timer_callback)
        self.start_time = self.get_clock().now()

    def timer_callback(self):
        current_time = self.get_clock().now()
        elapsed_duration = current_time - self.start_time
        elapsed_time = elapsed_duration.nanoseconds / 1e9

        speed = 0.0
        if elapsed_time < self.axis_time:
            speed = elapsed_time * self.acceleration
        elif elapsed_time > (self.axis_time * 2):
            speed = self.max_speed - (elapsed_time - (self.axis_time * 2)) * self.acceleration
        else:
            speed = self.max_speed

        msg = Twist()
        msg.linear.x = speed
        msg.angular.z = 0.0
        self.publisher_.publish(msg)
        self.get_logger().info(f'[{elapsed_time}] Publicando velocidad: {msg.linear.x}')

        if elapsed_time >= self.duration:
            self.get_logger().info('Tiempo máximo alcanzado. Deteniendo el nodo.')
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = SpeedController()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
