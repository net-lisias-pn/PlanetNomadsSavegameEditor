'''
Created on Aug 15, 2022

@author: lisias
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


