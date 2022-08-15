'''
Created on Aug 15, 2022

@author: lisias
'''
try:
	from mpl_toolkits.mplot3d import Axes3D  # Required for projection='3d'
	import matplotlib.pyplot as plt
	import numpy as np
	enable_map = True
except ImportError:
	enable_map = False

def draw(savegame, selected_machine_id:int):
	# Based on https://stackoverflow.com/questions/11140163/python-matplotlib-plotting-a-3d-cube-a-sphere-and-a-vector
	plt.style.use('seaborn-whitegrid')
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	# see https://github.com/fabro66/GAST-Net-3DPoseEstimation/issues/51
	#ax.set_aspect("equal")
	ax.set_box_aspect([1,1,1])

	# Draw a sphere to mimic a planet
	u = np.linspace(0, 2 * np.pi, 100)
	v = np.linspace(0, np.pi, 100)
	x = savegame.get_planet_size() * np.outer(np.cos(u), np.sin(v))
	y = savegame.get_planet_size() * np.outer(np.sin(u), np.sin(v))
	z = savegame.get_planet_size() * np.outer(np.ones(np.size(u)), np.cos(v))
	ax.plot_surface(x, y, z, rcount=18, ccount=21, alpha=0.1)

	colors = {"Base": "blue", "Vehicle": "orange", "Construct": "grey", "Selected": "red"}
	markers = {"Base": "^", "Vehicle": "v", "Construct": ".", "Selected": "v"}
	machines = savegame.machines
	coords = {}
	for m in machines:
		c = m.get_coordinates()
		mtype = m.get_type()
		if m.identifier == selected_machine_id:
			mtype = "Selected"
		if mtype not in coords:
			coords[mtype] = {"x": [], "y": [], "z": []}
		coords[mtype]["x"].append(c[0])
		coords[mtype]["y"].append(c[2])  # Flip y/z
		coords[mtype]["z"].append(c[1])
	for mtype in coords:
		ax.scatter(np.array(coords[mtype]["x"]), np.array(coords[mtype]["y"]), np.array(coords[mtype]["z"]),
				c=colors[mtype], marker=markers[mtype], label=mtype)

	player = savegame.get_player_position()
	ax.scatter(np.array(player[0]), np.array(player[2]), np.array(player[1]), c="red", marker="*", label="Player")

	ax.grid(False)  # Hide grid lines
	ax.legend()
	plt.show()

