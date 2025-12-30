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
import numpy as np

from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from py_pubsub.FK_for_RViz2 import IK_3dofspec

class IK_listener(Node):

    def __init__(self):
        super().__init__('ik_listener')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.l1 = 0.25
        self.l2 = 0.55
        self.l3 = 0.7149

        self.timer = self.create_timer(0.1, self.tf_callback)
        
        self.get_logger().info('tf listener started')

    def tf_callback(self):
        try:
            t = self.tf_buffer.lookup_transform(
                'base_link',
                'end_effector',
                rclpy.time.Time()
            )

            x = t.transform.translation.x
            y = t.transform.translation.y
            z = t.transform.translation.z

            # untuk debugging apakah sudah bisa mendapat info dari tf:
            # self.get_logger().info(f'Posisi End-Effector saat ini: X={x:.2f}, Z={z:.2f}')

            hasil_ik = IK_3dofspec(self.l1, self.l2, self.l3, x, y, z)

            # sudut coxa, femur, tibia
            th_c = hasil_ik[0]
            th_f = hasil_ik[1]
            th_t = hasil_ik[2]

            self.get_logger().info(f'Pasangan solusi sudut: [{th_c:.2f}, {th_f:.2f}, {th_t:.2f}]')

        except:
            self.get_logger().info(f'stand bye')

def main(args=None):
    rclpy.init(args=args)

    ik_listener = IK_listener()

    rclpy.spin(ik_listener)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ik_listener.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
