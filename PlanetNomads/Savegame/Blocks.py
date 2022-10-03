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

import xml.etree.ElementTree as ETree

from PlanetNomads.Blocks import Block as AbstractBlock
from .Nodes import MachineNode

class Block(MachineNode,AbstractBlock):

	def is_grounded(self):
		return "Ground" in self._attribs and self._attribs["Ground"] == "true"

	def get_active_block_id(self):
		if "ActiveID" in self._attribs:
			return int(self._attribs["ActiveID"])
		return None

	def get_active_block_ids(self):
		result = []
		active_id = self.get_active_block_id()
		if active_id:
			result.append(active_id)
		result.extend(super(Block, self).get_active_block_ids())
		return result

	def get_active_block(self, active_blocks):
		aid = self.get_active_block_id()
		if aid:
			if aid == 0:
				pass
			elif aid in active_blocks:
				return active_blocks[aid]
			else:
				# Avoid crash if active block did not load. Why is it missing though?
				print("Active block %i not found" % aid)
		return None

	def get_name(self, active_blocks):
		active_block = self.get_active_block(active_blocks) # type: ActiveBlock
		if active_block:
			name = active_block.get_name()
			if name:
				return name
		return super().get_name(active_blocks)

	def has_cockpit(self):
		if self._attribs["ID"] in ("4", "92", "93", "97", "126"):
			return True
		return super().has_cockpit()

	def has_generator(self):
		if self._attribs["ID"] in ("20", "42"):
			return True
		return super().has_generator()

	def has_hoverjack(self):
		if self._attribs["ID"] == "37":
			return True
		return super().has_hoverjack()

	def get_expected_children_types(self):
		return ['Pos', 'Col', 'Rot', 'SubGrid']

	def move_by(self, vector, active_blocks):
		super().move_by(vector, active_blocks)
		active_block = self.get_active_block(active_blocks)
		if not active_block:
			return
		active_block.move_by(vector)


class ActiveBlock:
	def __init__(self, xml):
		self.root = ETree.fromstring(xml)
		self.name = self.root.attrib.get("Name", "")
		self.changed = False

	def get_xml_string(self):
		return ETree.tostring(self.root, "unicode")

	def get_name(self):
		return self.name

	def move_by(self, vector):
		for node in self.root:
			if node.tag != "Module":
				continue
			if node.attrib["Type"] != "PositionModule":
				continue
			position = node[0][0].text
			x, y, z = [float(i) for i in position.split(";")]
			node[0][0].text = "{:0.3f};{:0.3f};{:0.3f}".format(x + vector[0], y + vector[1], z + vector[2])
			self.changed = True


class Blocks(MachineNode):
	def get_expected_children_types(self):
		return ['Block']

