import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from websocket import create_connection
import threading
import json

fig, ax = plt.subplots(figsize=(15, 10), subplot_kw=dict(polar=True))
theta = np.linspace(0, np.pi, 50, endpoint=False)
width = np.pi / 50
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi)
ax.set_xticklabels([])
values = []

ws = create_connection("ws://192.168.9.119:6969")

def read_from_websocket():
    global values
    degree = 2.0
    while True:
        message = ws.recv()
        data = json.loads(message)
        print(f"Received: {data}")
        if data['type'] == 'degree':
            print(f"Motor position: {data['value']} degrees")
            degree = data['value']
            if degree >= 170:
                values.clear()
        elif data['type'] == 'distance':
            print(f"Distance: {data['value']} cm")
            distance = data['value']
            values.append((degree, distance))


threading.Thread(target=read_from_websocket, daemon=True).start()

def update(num):
    ax.clear()
    for value in values:
        degree, distance = value
        ax.bar(np.deg2rad(degree), distance, width=width, bottom=0.0)
    ax.set_theta_direction(-1)
    ax.set_theta_offset(np.pi)
    ax.set_xticklabels([])
    ax.set_ylim(0,250)

ani = animation.FuncAnimation(fig, update, frames=range(50), repeat=True)
plt.show()
