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
		12: "Medium 3D Printer",
		13: "Conveyor L-Section",
		14: "Conveyor",
		15: "Conveyor T-Section",
		16: "Conveyor X-Section",

		18: "Wheel",
		19: "Compact Container",
		20: "Bio Generator",
		21: "Reinforced Wall with Light",
		22: "Reinforced Wall - Short",
		23: "Reinforced Wall Corner",
		24: "Reinforced Wall Outer Corner",
		25: "Base Foundation (double height) *MIA*",
		26: "Raised Floor",
		27: "Compact Armory",
		28: "Compact Medbay",
		29: "Medium Refinery",
		30: "Compact FAD Machine",
		31: "Stasis Chamber",
		32: "Reinforced Wall with Door",
		33: "Ceiling Panel",
		34: "Suspension",

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
		51: "Inner Wall Doorway",
		52: "Reinforced Wall Exterior/Interior Joint",
		53: "Short inner wall",
		54: "Inner Wall",
		55: "Windowed Outer Wall",
		56: "Solar Beacon",
		57: "Escape pod",                           # Can't be constructed

		61: "Base Foundation",

		63: "Medium Greenhouse",
		64: "Emergency 3D printer",
		65: "Medium FAD Machine",
		66: "Hinge",

		68: "Rotating Plate",

		70: "Reinforced Wall Ext/Int Conveyor Joint",
		71: "Item Dispenser",

		73: "Mining Machine",
		74: "Large Greenhouse",

		76: "Medium Armory",

		78: "Medium Medbay",
		79: "Escape Pod (broken)",                  # 3k health. Can't be constructed
		80: "Radar",                                # 300 health. Can't be constructed.
		81: "Winch",
		82: "Winch Shackle",
		83: "Thruster",                             # 300 health. Can't be constructed.
		84: "Tank",                                 # 250 health. Can't be constructed.
		85: "Big Tank",                             # 750 health. Can't be constructed.
		86: "Sloped Arc Corner",
		87: "Corner Arc",
		88: "Arc Block",

		90: "Wreck Container",                      # Can't be constructed
		91: "Wreck Beacon",                         # Can't be constructed
		92: "Cockpit 3x3",
		93: "Rounded Cockpit 2x3",
		94: "Buggy Wheel",
		95: "Mobile Base Wheel",
		96: "Large Suspension",
		97: "Rounded Cockpit 3x3",
		98: "Switchboard",
		99: "Terminal",
		100: "Hover Pad",
		101: "Floating Foundation",

		106: "Radar",

		114: "Air Blade",

		118: "Conveyor 1x4",
		119: "Conveyor 1x8",
		120: "Large Air Blade",

		124: "Solar Panels",
		125: "Water Pump",
		126: "Glassed Cockpit 3x3",
		127: "Sloped Solar Panels",
		128: "Flat Solar Panels",
		129: "Conveyor 1x8",
		130: "Small Deuterium Generator",
		131: "Deuterium Generator",
		132: "Ceiling Panel Conveyor Joint",
		133: "Conveyor Six Section",
		134: "Short Inner Wall Conveyor Joint",

		144: "Cabinet",

		147: "Armor Arc - Kickstarter",             # Kickstarter part. Not available for non kickstarters
		148: "Armor Arc Corner - Kickstarter",      # Kickstarter part. Not available for non kickstarters
		149: "Armor Arc Slope Corner - Kickstarter", # Kickstarter part. Not available for non kickstarters
		150: "Armor Corner - Kickstarter",          # Kickstarter part. Not available for non kickstarters
		151: "Armor Corner Inverted - Kickstarter", # Kickstarter part. Not available for non kickstarters
		152: "Armor Corner Long - Kickstarter",     # Kickstarter part. Not available for non kickstarters
		153: "Armor Corner Slope - Kickstarter",    # Kickstarter part. Not available for non kickstarters
		154: "Full Armor Block - Kickstarter",      # Kickstarter part. Not available for non kickstarters
		155: "Amor Ramp - Kickstarter",             # Kickstarter part. Not available for non kickstarters
		156: "Armor Ramp Slope - Kickstarter",      # Kickstarter part. Not available for non kickstarters
		157: "Armor Slope - Kickstarter",           # Kickstarter part. Not available for non kickstarters
		158: "Basic Wall Mk2 - Kickstarter",        # Kickstarter part. Not available for non kickstarters
		159: "Basic Wall - Kickstarter",            # Kickstarter part. Not available for non kickstarters

		161: "Short Basic Slope Wall (with tube) - Kickstarter",  # Kickstarter part. Not available for non kickstarters
		162: "Short Basic Slope Wall - Kickstarter",              # Kickstarter part. Not available for non kickstarters
		163: "Connection Wall - Kickstarter",                     # Kickstarter part. Not available for non kickstarters
		164: "Short Basic Slope Corner Wall - Kickstarter",       # Kickstarter part. Not available for non kickstarters
		165: "Corner Wall - Kickstarter",           # Kickstarter part. Not available for non kickstarters
		166: "Basic Wall with Door - Kickstarter",  # Kickstarter part. Not available for non kickstarters
		167: "Short Basic Slope Wall 1x4",
		168: "Pylon with light",
		169: "Outer Window with (band)",            # Kickstarter part. Not available for non kickstarters
		170: "Outer Window",
		171: "Slope Outer Window",
		172: "Short Basic Pylon - Kickstarter",     # Kickstarter part. Not available for non kickstarters
		173: "Small Plant Pot",
		174: "Replicator",
		175: "Short Basic Slope Pylon - Kickstarter",  # Kickstarter part. Not available for non kickstarters
		176: "Basic Wall 3x7 - Kickstarter",           # Kickstarter part. Not available for non kickstarters
		177: "Base Foundation - Kickstarter",          # Kickstarter part. Not available for non kickstarters
		178: "Half Stairs",
		179: "Stairs Joint",
		180: "One step stairs",
		181: "Ceiling Panel - Kickstarter",         # Kickstarter part. Not available for non kickstarters
		182: "Corner Railing",
		183: "Corner Outer Window",
		184: "Interior Cockpit",

		188: "Control Panel",
		189: "Thermoregulator",

		191: "Hybrid Replicator",

		196: "Compact 3D Printer",

		203: "Brann Trophy",
		204: "Namiku Trophy",
		205: "Nossal Trophy",
		206: "Godillo Trophy",
		207: "Xenotaur Trophy",
		208: "Cerbul Trophy",

		216: "Autonomous Water Purifier",
		217: "Armor Arc Slope Corner - Long",
		218: "Armor Corner - Long",
		219: "Armor Corner - Inverted - Big",
		220: "Armor Corner - Inverted - Variation",

		222: "Armor Corner Slope - Big",
		223: "Armor Full - Half Slope",
		224: "Armor Half Corner Slope",
		225: "Armor Half Ramp - Long",

		227: "Armor Half Slope",
		228: "Armor Corner Slope - Small",
		229: "Window Corner Slope",
		230: "Window Flat",
		231: "Window Flat - Long",
		232: "Window Ramp - Long",
		233: "Window Ramp Slope - Long",
		234: "Window Slope",

		236: "Teleport",
	}

	def __init__(self, item_type: int):
		self.item_type = item_type

	def get_name(self):
		if self.item_type in self.names:
			return self.names[self.item_type]

		return "unknown block type {}".format(self.item_type)

