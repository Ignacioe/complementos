import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

NUM = 250

fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})

x = np.array([[p0x], [pfx]])
y = np.array([[p0y], [pfy]])
plt.plot(x, y)

ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

plt.show()
