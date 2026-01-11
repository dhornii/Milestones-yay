# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState
from geometry_msgs.msg import Pose
from py_pubsub.FK_for_RViz2 import FK_3dofspec_loky


class FK_Publisher(Node):

    def __init__(self):
        super().__init__('fk_publisher')

        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.listener_callback,
            10)
        
        self.get_logger().info('FK started')

    def listener_callback(self, msg):

        for leg in range(6):
            sudut_from_base = (1 + 2 * leg) / 6

            th1 = msg.position[leg * 3]
            th2 = msg.position[leg * 3 + 1]
            th3 = msg.position[leg * 3 + 2]

            fk_result = FK_3dofspec_loky(th1, th2, th3, sudut_from_base)

            x = float(fk_result[0])
            y = float(fk_result[1])
            z = float(fk_result[2])

            self.get_logger().info(f'Leg {leg + 1}: X={x:.4f}, Y={y:.4f}, Z={z:.4f}')
        
        # th1_2 = msg.position[0] # leg 2
        # th2_2 = msg.position[1]
        # th3_2 = msg.position[2]

        # th1_6 = msg.position[3] # leg 6
        # th2_6 = msg.position[4]
        # th3_6 = msg.position[5]

        # leg2_result = FK_3dofspec(th1_2, th2_2, th3_2, 3/6)
        # leg6_result = FK_3dofspec(th1_6, th2_6, th3_6, 11/6)

        # x_leg2 = float(leg2_result[0])
        # y_leg2 = float(leg2_result[1])
        # z_leg2 = float(leg2_result[2])

        # x_leg6 = float(leg6_result[0])
        # y_leg6 = float(leg6_result[1])
        # z_leg6 = float(leg6_result[2])

        # self.get_logger().info(f'Leg 2: X={x_leg2:.4f}, Y={y_leg2:.4f}, Z={z_leg2:.4f}')
        # self.get_logger().info(f'Leg 6: X={x_leg6:.4f}, Y={y_leg6:.4f}, Z={z_leg6:.4f}')
        
def main(args=None):
    rclpy.init(args=args)

    fk_publisher = FK_Publisher()

    rclpy.spin(fk_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    fk_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

# == Dari Tutorial ROS2 ==
# import rclpy
# from rclpy.node import Node

# from std_msgs.msg import String


# class MinimalPublisher(Node):

#     def __init__(self):
#         super().__init__('minimal_publisher')
#         self.publisher_ = self.create_publisher(String, 'topic', 10)
#         timer_period = 0.5  # seconds
#         self.timer = self.create_timer(timer_period, self.timer_callback)
#         self.i = 0

#     def timer_callback(self):
#         msg = String()
#         msg.data = 'Hello World: %d' % self.i
#         self.publisher_.publish(msg)
#         self.get_logger().info('Publishing: "%s"' % msg.data)
#         self.i += 1


# def main(args=None):
#     rclpy.init(args=args)

#     minimal_publisher = MinimalPublisher()

#     rclpy.spin(minimal_publisher)

#     # Destroy the node explicitly
#     # (optional - otherwise it will be done automatically
#     # when the garbage collector destroys the node object)
#     minimal_publisher.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()