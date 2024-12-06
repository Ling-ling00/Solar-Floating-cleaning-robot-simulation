import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseArray, Pose
from gz.msgs.pose_stamped_pb2 import PoseStamped
from gz.transport import Node as GzNode

class GzToRosBridge(Node):
    def __init__(self):
        super().__init__('gz_to_ros_bridge')
        
        # ROS publisher
        self.ros_publisher = self.create_publisher(PoseArray, '/gazebo/default/pose/info', 10)
        
        # Gazebo subscriber
        self.gz_node = GzNode()
        self.gz_node.subscribe('/gazebo/default/pose/info', self.gz_callback)

    def gz_callback(self, gz_msg):
        # Convert Gazebo message to ROS PoseArray
        ros_msg = PoseArray()
        for pose in gz_msg.pose:
            ros_pose = Pose()
            ros_pose.position.x = pose.position.x
            ros_pose.position.y = pose.position.y
            ros_pose.position.z = pose.position.z
            ros_pose.orientation.x = pose.orientation.x
            ros_pose.orientation.y = pose.orientation.y
            ros_pose.orientation.z = pose.orientation.z
            ros_pose.orientation.w = pose.orientation.w
            ros_msg.poses.append(ros_pose)
        
        # Publish to ROS 2
        self.ros_publisher.publish(ros_msg)

def main(args=None):
    rclpy.init(args=args)
    node = GzToRosBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
