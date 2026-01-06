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

from py_pubsub.FK_for_RViz2 import IK_2dof

class IK_listener(Node):

    def __init__(self):
        super().__init__('ik_listener')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self) # mantau bagian tf lalu nilainya disimpan di buffer

        # lengan short_arm.urdf yang digunakan untuk perhitungan IK
        self.l1 = 0.7
        self.l2 = 0.5

        self.timer = self.create_timer(0.1, self.tf_callback)
        
        self.get_logger().info('tf listener started')

    def tf_callback(self):
        try:
            t = self.tf_buffer.lookup_transform( # listeing ke tf dari Rviz2-nya
                'base_link',       # hitung dengan dasar jarak dari 'base_link'
                'end_effector',    # target perhitungan adalah ke 'end_effector' terhadap 'base_link'
                rclpy.time.Time()  # ambil info pada waktu persis saat itu juga
            )

            x = t.transform.translation.x # kita cuma butuh informasi X dan Z saja karena sedang FK atau IK 2 dimensi, sementara rotasi terhadap sumbu Y
            z = t.transform.translation.z

            # untuk debugging apakah sudah bisa mendapat info dari tf:
            # self.get_logger().info(f'Posisi End-Effector saat ini: X={x:.2f}, Z={z:.2f}')

            hasil_ik = IK_2dof(self.l1, self.l2, x, z-0.9) # ingat transformasi titik vertikalnya dulu (Z) ke bawah karena ada 'base_link' setinggi 0.9

            # karena mulainya tegak di awal (ditambahkan 90 derajat), maka hasil untuk sudut pertama dikurangi oleh 90 derajat juga
            lower_th1 = (hasil_ik[0, 0]-np.deg2rad(90)) # untuk letak jawaban sudutnya bisa dibuka bagian fungsi 'FK_for_RViz2.py`
            lower_th2 = (hasil_ik[1, 0])

            upper_th1 = (hasil_ik[0, 1]-np.deg2rad(90))
            upper_th2 = (hasil_ik[1, 1])

            self.get_logger().info(f'Pasangan solusi sudut: Lower = [{lower_th1:.2f}, {lower_th2:.2f}] Upper = [{upper_th1:.2f}, {upper_th2:.2f}]')

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
