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
from py_pubsub.FK_for_RViz2 import FK_3dof


class FK_Publisher(Node):

    def __init__(self):
        super().__init__('fk_publisher')

        self.l1 = 0.7
        self.l2 = 0.5
        self.l3 = 0.3

        self.subscription = self.create_subscription(
            JointState,
            'joint_states',    # subscribe ke topic joint_states buat dapet informasi rotasi (rad) yang diberikan oleh joint_state_publisher_gui
            self.listener_callback,
            10)
        
        self.publisher_ = self.create_publisher(Pose, 'end_effector_pose', 10)
        self.get_logger().info('FK publisher started')

    def listener_callback(self, msg):
        
        th1 = msg.position[0] # ambil setiap info rad dari joint_state_publisher_gui, urutannya sesuai gui dari atas ke bawah
        th2 = msg.position[1]
        th3 = msg.position[2]

        Result_Matrix = FK_3dof(self.l1, self.l2, self.l3, th1, th2, th3) # hitung hasil FK dari info di gui-nya

        # karena rotasi di sumbu Y, artinya sekarang horizontal adalah sumbu X sementara vertikal adalah sumbu Z
        x_pos = float(Result_Matrix[0, 2])            # letak posisi horizontal di baris pertama kolom ke-3 matriks
        y_pos = 0.0
        z_pos = float(Result_Matrix[1, 2]) + 0.9      # letak posisi vertikal ada di baris ke-2 kolom ke-3 matriks, ingat ada tambahan 0.9 karena translasi oleh 'base_line'

        pose_msg = Pose() # bikin objek Pose
        pose_msg.position.x = x_pos    # isi setiap informasi position objek Pose
        pose_msg.position.y = y_pos    
        pose_msg.position.z = z_pos    

        self.publisher_.publish(pose_msg)    # publish ke topic 'end_effector_pose'
        self.get_logger().info(f'End Effector: X={x_pos:.2f}, Y={y_pos:.2f}, Z={z_pos:.2f}') # tulis di terminal (tempat node berjalan) buat informasi langsung
        
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
