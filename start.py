import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from websocket import create_connection
import threading

# Data
fig, ax = plt.subplots(figsize=(8, 4), subplot_kw=dict(polar=True))

theta = np.linspace(0, np.pi, 50, endpoint=False)
width = np.pi / 50  

ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi)
ax.set_xticklabels([])
values = []

ws = create_connection("ws://10.176.69.179:6969")

def read_from_websocket():
    global values
    while True:
        message = ws.recv()
        print(f"Received: {message}")
        values.append(float(message)) 
        
threading.Thread(target=read_from_websocket, daemon=True).start()

def update(num):
    ax.clear()
    ax.bar(theta[:len(values)], values, width=width, bottom=0.0)
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi)
    ax.set_xticklabels([])

ani = animation.FuncAnimation(fig, update, frames=range(50), repeat=True, interval=500)
plt.show()

