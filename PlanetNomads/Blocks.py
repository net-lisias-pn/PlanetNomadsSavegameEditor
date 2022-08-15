'''
Created on Aug 15, 2022

@author: lisias
'''
class Block:
	types = {
		1: "Full Armor Block",
		2: "Corner Armor Block",
		3: "Compact Battery Rack",
		4: "Cockpit 2x3",
		5: "Reinforced Wall",
		6: "Armor Corner Slope - Inverted",
		7: "Armor Corner Slope - Long Inverted",
		8: "Armor Corner Slope",
		9: "Armor Slope Long",
		10: "Armor Slope Corner (Long)",
		11: "Armor Slope",
		#12 active
		13: "Conveyor L-Section",
		14: "Conveyor",
		15: "Conveyor T-Section",
		16: "Conveyor X-Section",
		#17 probly active block
		18: "Wheel",
		19: "Compact Container",
		20: "Bio Generator",
		21: "Reinforced Wall with Light",
		22: "Reinforced Wall - Short",
		23: "Reinforced Wall Corner",
		24: "Reinforced Wall Outer Corner",
		25: "Base Foundation (double height)",
		26: "Raised Floor",
		#27
		28: "Compact Medbay",
		29: "Medium Refinery",
		#30
		#31
		32: "Reinforced Wall with Door",
		33: "Ceiling Panel",
		34: "Suspension",
		#35 probly active
		36: "Jack tool",
		37: "Hover Jack",
		38: "Railing",
		39: "Short Railing",
		40: "Stairs",
		41: "Beacon",
		42: "Uranium Generator",
		43: "Ceiling Light",
		44: "Indoor Light",
		45: "Search Light - Front Mount",
		46: "Search Light - Top Mount",
		47: "Large Container",
		48: "Fence",
		49: "Fence Corner",
		50: "Ramp",
		51: "Inner Wall with Doors",
		52: "Reinforced Wall Exterior/Interior Joint",
		53: "Short inner wall",
		54: "Inner Wall",
		55: "Windowed Outer Wall",
		56: "Solar Beacon",
		57: "Escape pod",

		61: "Base Foundation",

		64: "Emergency 3D printer",

		66: "Hinge",
		68: "Rotating Plate",
		71: "Item Dispenser",
		73: "Mining Machine",
		76: "Medium Armory",
		78: "Medium Medbay",
		79: "Escape Pod (broken)",  # 3k health
		80: "Radar",  # 300 health
		81: "Winch",
		82: "Winch Shackle",
		83: "Thruster",  # 300 health
		84: "Tank",  # 250 health
		85: "Big Tank",  # 750 health
		86: "Sloped Arc Corner",
		87: "Corner Arc",
		88: "Arc Block",
		#89
		90: "Wreck Container",
		91: "Wreck Beacon",
		92: "Cockpit 3x3",
		93: "Rounded Cockpit 2x3",
		94: "Buggy Wheel",
		95: "Mobile Base Wheel",
		96: "Large Suspension",
		97: "Rounded Cockpit 3x3",
		98: "Switchboard",
		100: "Hover Pad",
		101: "Floating Foundation",
		114: "Air Blade",
		126: "Glassed Cockpit 3x3",
	}

	def __init__(self, item_type: int):
		self.item_type = item_type

	def get_name(self):
		if self.item_type in self.names:
			return self.names[self.item_type]

		return "unknown block type {}".format(self.item_type)

