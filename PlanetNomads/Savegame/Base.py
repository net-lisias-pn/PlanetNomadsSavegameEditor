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
from .Nodes import XmlNode

class BasePosition(XmlNode):
	def move_by(self, vector, active_blocks):
		x = float(self._attribs["X"])
		y = float(self._attribs["Y"])
		z = float(self._attribs["Z"])
		self._attribs["X"] = "{:0.5f}".format(x + vector[0])
		self._attribs["Y"] = "{:0.5f}".format(y + vector[1])
		self._attribs["Z"] = "{:0.5f}".format(z + vector[2])


class BaseRotation(XmlNode):
	pass


class BaseBounds(XmlNode):
	def move_by(self, vector, active_blocks):
		x = float(self._attribs["MinX"])
		y = float(self._attribs["MinY"])
		z = float(self._attribs["MinZ"])
		self._attribs["MinX"] = "{:0.5f}".format(x + vector[0])
		self._attribs["MinY"] = "{:0.5f}".format(y + vector[1])
		self._attribs["MinZ"] = "{:0.5f}".format(z + vector[2])
		x = float(self._attribs["MaxX"])
		y = float(self._attribs["MaxY"])
		z = float(self._attribs["MaxZ"])
		self._attribs["MaxX"] = "{:0.5f}".format(x + vector[0])
		self._attribs["MaxY"] = "{:0.5f}".format(y + vector[1])
		self._attribs["MaxZ"] = "{:0.5f}".format(z + vector[2])


