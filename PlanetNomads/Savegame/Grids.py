'''
Created on Aug 15, 2022

@author: lisias
'''
from .Nodes import MachineNode

class Grid(MachineNode):
	"""Every machine has 1 Grid which contains 1 Blocks"""
	def get_expected_children_types(self):
		return ['Blocks', 'BasePosition', 'BaseRotation', 'BaseBounds', 'DistancePhysicsFreezeData']


class SubGrid(Grid):
	pass
