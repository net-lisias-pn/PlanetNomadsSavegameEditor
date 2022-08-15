'''
Created on Aug 15, 2022

@author: lisias
'''
import platform
import os

def solve_savedir() -> str:
	os_name = platform.system()
	if os_name == "Linux":
		return os.path.expanduser("~/.config/unity3d/Craneballs/PlanetNomads/")
	elif os_name == "Windows":
		return os.path.expanduser("~\AppData\LocalLow\Craneballs\PlanetNomads")
	elif os_name == "Darwin":
		return os.path.expanduser("~/Libraty/Application Support/unity.Craneballs.PlanetNomads/Saves")
	else:
		return os.path.expanduser("~")
