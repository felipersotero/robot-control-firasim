import numpy as np

p1 = [0, 0]
p2 = [10, 0]
p3 = [10, 10]
p4 = [0, 10]
p5 = [5, 5]

ally = [77, 58]
ball = [75, 65]
goal = [0, 65]

# ally = [70, 60]
# ball = [75, 65]
# goal = [0, 65]

# ally = [115, 105]
# ball = [75, 65]
# goal = [0, 65]

# ally = [70, 65]
# ball = [75, 65]
# goal = [0, 65]

# ally = p3
# ball = p4
# goal = p2

dx_gamma = ball[0] - ally[0]
dy_gamma = ball[1] - ally[1]
gamma = np.arctan2(dy_gamma, dx_gamma)

dx_theta_g = goal[0] - ball[0]
dy_theta_g = goal[1] - ball[1]
theta_g = np.arctan2(dy_theta_g, dx_theta_g)

print(f"gamma {np.rad2deg(gamma)}°")
print(f"theta_g {np.rad2deg(theta_g)}°")

# if abs(gamma) + abs(theta_g) > np.pi:
#     print("if")
#     beta = -(2*np.pi - abs(theta_g) - abs(gamma))
# else:
#     print("else")
#     beta = theta_g - gamma

beta = theta_g - gamma

# print(f"beta {np.rad2deg(beta)}°")

beta = (beta + np.pi) % (2 * np.pi) - np.pi

print(f"beta {np.rad2deg(beta)}°")
