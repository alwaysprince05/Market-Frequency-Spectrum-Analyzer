import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Generate sample data (simulating price movement)
np.random.seed(42)
steps = 200
x = np.arange(steps)
y = np.cumsum(np.random.randn(steps))
z = np.linspace(0, 10, steps)

# Set up the figure and 3D axis with dark theme
plt.style.use('dark_background')
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

# Initial plot
line, = ax.plot([], [], [], lw=2, color='cyan')
ax.set_xlim(0, steps)
ax.set_ylim(np.min(y)-5, np.max(y)+5)
ax.set_zlim(0, 10)
ax.set_xlabel('Time')
ax.set_ylabel('Price')
ax.set_zlabel('Depth')
ax.set_title('3D Animated Line Graph')

# Animation function
def animate(i):
    line.set_data(x[:i], y[:i])
    line.set_3d_properties(z[:i])
    return line,

ani = FuncAnimation(fig, animate, frames=steps, interval=30, blit=True)

plt.show()
