'''
Created on Aug 15, 2022

@author: lisias
'''
from typing import Text
import shutil, os

from PlanetNomads import Savegame

def exists(filename:Text) -> bool:
	"""
	Check if a backup exists for the given file
	:param filename: Filename with absolute path
	:return: bool
	"""
	return os.path.exists(filename + ".bak")

def create(current_file:str):
	shutil.copy2(current_file, current_file + ".bak")

def restore(current_file:str, savegame:Savegame):
	shutil.copy2(current_file + ".bak", current_file)
	savegame.reset()
