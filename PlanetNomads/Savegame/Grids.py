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
from .Nodes import MachineNode

class Grid(MachineNode):
	"""Every machine has 1 Grid which contains 1 Blocks"""
	def get_expected_children_types(self):
		return ['Blocks', 'BasePosition', 'BaseRotation', 'BaseBounds', 'DistancePhysicsFreezeData']


class SubGrid(Grid):
	pass
