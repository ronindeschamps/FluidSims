import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

x = np.linspace(0, 10, 100)
y = np.linspace(0, 20, 100)

plt.plot(x, y, 'o')
plt.ylabel('some numbers')
plt.grid(True)
plt.show()