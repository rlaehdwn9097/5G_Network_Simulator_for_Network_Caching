import math
import numpy as np
from matplotlib import pyplot as plt

figure, axes = plt.subplots()

a = 0
b = 0
r = 3

circle = plt.Circle((a, b), 3, fill=True)
axes.add_artist(circle)

t = 0
cnt = 0
while cnt < 200:
    t = np.random.uniform(0, 360)
    d = np.random.uniform(r)
    #positions.append((r * math.cos(t) + a, r * math.sin(t) + b))
    plt.scatter(d * math.cos(t) + a, d * math.sin(t) + b)
    cnt += 1

plt.show()