import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Generate sample data
np.random.seed(42)
steps = 200
x = np.arange(steps)
price = np.cumsum(np.random.randn(steps)) + 50
line2 = np.cumsum(np.random.randn(steps)) + 55
line3 = np.cumsum(np.random.randn(steps)) + 45
line4 = np.cumsum(np.random.randn(steps)) + 60
line5 = np.cumsum(np.random.randn(steps)) + 40

# Set up the figure with dark theme
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 6))

# Initial plot
main_line, = ax.plot([], [], color='magenta', lw=2, label='Price')
line2_plot, = ax.plot([], [], color='cyan', lw=1.5, linestyle='--', label='Line 2')
line3_plot, = ax.plot([], [], color='lime', lw=1.5, linestyle=':', label='Line 3')
line4_plot, = ax.plot([], [], color='red', lw=1.5, linestyle='-.', label='Line 4')
line5_plot, = ax.plot([], [], color='yellow', lw=1.5, linestyle='-', label='Line 5')

ax.set_xlim(0, steps)
ax.set_ylim(30, 70)
ax.set_xlabel('Time')
ax.set_ylabel('Price')
ax.set_title('Animated Trading Chart')
ax.legend(loc='upper left')

# Animation function
def animate(i):
    main_line.set_data(x[:i], price[:i])
    line2_plot.set_data(x[:i], line2[:i])
    line3_plot.set_data(x[:i], line3[:i])
    line4_plot.set_data(x[:i], line4[:i])
    line5_plot.set_data(x[:i], line5[:i])
    return main_line, line2_plot, line3_plot, line4_plot, line5_plot

ani = FuncAnimation(fig, animate, frames=steps, interval=30, blit=True)

plt.show()
