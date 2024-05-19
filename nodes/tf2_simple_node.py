import rclpy
from rclpy.node import Node
import tf2_ros
from geometry_msgs.msg import TransformStamped

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.tf_broadcaster = tf2_ros.StaticTransformBroadcaster(self)

    def publish_static_transforms(self):
        static_transformStamped = TransformStamped()
        static_transformStamped.header.stamp = self.get_clock().now().to_msg()
        static_transformStamped.header.frame_id = 'map'
        static_transformStamped.child_frame_id = 'odom'
        static_transformStamped.transform.translation.x = 0.0
        static_transformStamped.transform.translation.y = 0.0
        static_transformStamped.transform.translation.z = 0.0
        static_transformStamped.transform.rotation.x = 0.0
        static_transformStamped.transform.rotation.y = 0.0
        static_transformStamped.transform.rotation.z = 0.0
        static_transformStamped.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(static_transformStamped)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    while rclpy.ok():
        node.publish_static_transforms()
        rclpy.spin_once(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
