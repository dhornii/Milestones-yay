import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

""" 
for example with points of: 
- anchor1 = 6 ; 0
- control 1 = 4 ; 8
- control 2 = -4 ; 8
- anchor2 = -10 ; 0 
"""

def lerp(p0, p1, t):

    result = p0 * (1-t) + p1 * t

    return result

def cubic_bezier(anch_1, anch_2, ctrl_1, ctrl_2, t):

    A = lerp(anch_1, ctrl_1, t)
    B = lerp(ctrl_1, ctrl_2, t)
    C = lerp(ctrl_2, anch_2, t)

    D = lerp(A, B, t)
    E = lerp(B, C, t)

    final = lerp(D, E, t)

    return final

""" === Example: Plotting and Using Bezier Curve Function === """

# sample_t = np.linspace(0, 1, 20)

# # points
# start = np.array([0.8, -0.4, -1])
# ctrl1 = np.array([0.8, -0.2, -0.55])
# ctrl2 = np.array([0.8, 0.2, -0.55])
# end = np.array([0.8, 0.4, -1])

# sample_t = sample_t.reshape((-1, 1)) # -1 will automatically calculate the required number of rows to create a vector of t

# trajectory_points = [cubic_bezier(start, end, ctrl1, ctrl2, time) for time in sample_t]

# traject_matrix = np.array(trajectory_points)
# print(trajectory_points)

# fig = plt.figure(figsize=(10,7))
# ax = fig.add_subplot(111, projection='3d')

# # plotting the path result of bezier curve
# ax.plot(traject_matrix[:, 0], traject_matrix[:, 1], traject_matrix[:, 2], label='bezier path', color='blue', linewidth=3)

# # plotting the points acting as the anchor 1, 2 and then the control points 1, 2
# control_points = np.array([start, ctrl1, ctrl2, end])
# ax.scatter(control_points[:, 0], control_points[:, 1], control_points[:, 2], 
#            color='red', s=50, label='Control Points')

# # plotting the points connecting each input (all anchors and controls)
# ax.plot(control_points[:, 0], control_points[:, 1], control_points[:, 2], 
#         color='red', linestyle='--', alpha=0.5)

# # Labels and setup
# ax.set_xlabel('X (Forward)')
# ax.set_ylabel('Y (Lateral)')
# ax.set_zlabel('Z (Height)')
# ax.set_title('3D Leg Swing Trajectory')
# ax.legend()

# # Equalize axis scaling
# ax.set_box_aspect([1,1,1]) 

# plt.show()