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
import random
from .Nodes import XmlNode

class Pos(XmlNode):
	pass


class Rot(XmlNode):
	pass


class Col(XmlNode):
	def randomize_color(self):
		self._attribs["r"] = str(random.randrange(0, 255))
		self._attribs["g"] = str(random.randrange(0, 255))
		self._attribs["b"] = str(random.randrange(0, 255))

	def set_color(self, color, replace):
		if replace:
			if int(self._attribs["r"]) != replace[0]:
				return
			if int(self._attribs["g"]) != replace[1]:
				return
			if int(self._attribs["b"]) != replace[2]:
				return
		self._attribs["r"] = str(int(color[0]))
		self._attribs["g"] = str(int(color[1]))
		self._attribs["b"] = str(int(color[2]))


