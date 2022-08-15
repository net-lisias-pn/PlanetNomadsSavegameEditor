'''
Created on Aug 15, 2022

@author: lisias
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


