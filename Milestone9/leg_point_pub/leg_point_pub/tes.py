import numpy as np

cur_x = 0
cur_y = 0.1666603
cur_z = -0.047929 - 0.08694 # sekarang harusnya coxa sudah sejajar Z-nya dengan base link 

rot_x = np.cos( (3 / 6) * np.pi) * cur_x + np.sin( (3 / 6) * np.pi) * cur_y - 0.08663
rot_y = -np.sin( (3 / 6) * np.pi) * cur_x + np.cos( (3 / 6) * np.pi) * cur_y

print(rot_x, rot_y, cur_z)

# 0.025, 0, -0.06344 coxa to femur, coxa as ref
# 0.055, 0, 0 femur to tibia, femur as ref
# 0, 0, -0,071429 tibia to end, tibia as ref