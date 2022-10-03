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
