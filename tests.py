import numpy as np

vector = [1, 1]

# mod = np.sqrt(vector[0]**2 + vector[1]**2)
mod = np.linalg.norm(vector)

print(mod)

vector = vector/mod

print(vector)