'''
Created on Aug 15, 2022

@author: lisias

		This file is part of PlanetNomadsSavegameEditor /L
			© 2022 LisiasT
			© 2017-2018 black silence

		PlanetNomadsSavegameEditor /L is licensed as follows:
				* GPL 2.0 : https://www.gnu.org/licenses/gpl-2.0.txt

		PlanetNomadsSavegameEditor /L is distributed in the hope that it will be useful,
		but WITHOUT ANY WARRANTY; without even the implied warranty of
		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

		You should have received a copy of the GNU General Public License 2.0
		along with PlanetNomadsSavegameEditor /L. If not, see <https://www.gnu.org/licenses/>.
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
