'''
Created on Aug 15, 2022

@author: lisias
'''
from collections import OrderedDict
import xml.etree.ElementTree as ETree

class XmlNode:
	"""Basic XML node"""
	def __init__(self, node):
		from . import CLASSES
		self.type = node.tag
		self._attribs = OrderedDict()
		self._children = []
		for a in node.attrib:
			self._attribs[a] = node.attrib[a]
		expected_children = self.get_expected_children_types()
		for item in node:
			if item.tag in expected_children:
				self._children.append(CLASSES[item.tag](item))  # Create object from class name
			else:
				print("Unexpected children type %s" % item.tag)

	def get_attribs(self):
		"""Get attributes in the original order, much easier to diff xml this way"""
		return self._attribs

	def get_children(self):
		return self._children

	def build_xml(self, xml):
		sub = ETree.SubElement(xml, self.type, self.get_attribs())
		for c in self._children:
			c.build_xml(sub)

	def get_expected_children_types(self):
		return []


class MachineNode(XmlNode):
	def get_active_block_ids(self):
		res = []
		for c in self._children:
			try:
				res.extend(c.get_active_block_ids())
			except AttributeError:
				pass  # Class doesn't have active blocks
		return res

	def is_grounded(self):
		for c in self.get_children():
			try:
				if c.is_grounded():
					return True
			except AttributeError:
				pass
		return False

	def has_cockpit(self):
		for x in self.get_children():
			try:
				if x.has_cockpit():
					return True
			except AttributeError:
				pass
		return False

	def has_generator(self):
		for c in self.get_children():
			try:
				if c.has_generator():
					return True
			except AttributeError:
				pass
		return False

	def has_hoverjack(self):
		for c in self.get_children():
			try:
				if c.has_hoverjack():
					return True
			except AttributeError:
				pass
		return False

	def get_name(self, active_block_data):
		for c in self.get_children():
			try:
				name = c.get_name(active_block_data)
				if name != "":
					return name
			except AttributeError:
				pass
		return ""

	def get_expected_children_types(self):
		return ['Grid']

	def move_by(self, vector, active_block_data):
		for c in self._children:
			try:
				c.move_by(vector, active_block_data)
			except AttributeError:
				pass

	def randomize_color(self):
		for c in self._children:
			try:
				c.randomize_color()
			except AttributeError:
				pass

	def set_color(self, color, replace):
		for c in self._children:
			try:
				c.set_color(color, replace)
			except AttributeError:
				pass



