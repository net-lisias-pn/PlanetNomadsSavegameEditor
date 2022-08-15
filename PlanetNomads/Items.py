'''
Created on Aug 15, 2022

@author: lisias
'''

class Item:
	names = {
		33: "Battery",
		49: "Carbon",
		51: "Aluminium",
		52: "Silicium",
		56: "Iron",
		57: "Titanium",
		58: "Gold",
		59: "Silver",
		60: "Cobalt",
		61: "Uranium",
		62: "Xaenite",
		63: "Enriched Uranium",
		64: "Deuterium",
		65: "Xaenite Rod",
		67: "Plating",
		68: "Composite Plating",
		69: "Basic Frame",
		70: "Reinforced Frame",
		72: "Glass Components",
		73: "Standard Electronics",
		74: "SuperConductive Electronics",
		75: "Quantum Electronics",
		76: "Standard Mechanical Components",
		77: "SuperAlloy Mechanical",
		78: "Composite Parts",
		79: "Advanced Composite Parts",
		80: "Fabric Mk1",
		81: "Fabric Mk2",
		82: "ALM",
		83: "Advanced ALM",
		84: "Super ALM",
		86: "Fruitage",
		87: "Dirty Water",
		88: "Herbs",
		89: "Raw Meat",
		90: "Purified Water",
		91: "Electrolytes Water",
		92: "Nutrition Capsules",
		93: "Super Food",
		95: "Bandages",
		96: "Stimulation Injection",
		108: "Exploration Suit Mk2",
		109: "Exploration Suit Mk3",
		110: "Exploration Suit Mk4",
		112: "Jetpack Mk2",
		113: "Jetpack Mk3",
		114: "Jetpack Mk4",
		116: "MultiTool Mk2",
		117: "MultiTool Mk3",
		118: "MultiTool Mk4",
		392745: "Biomass Container",
		9550358: "Seeds",
		11691828: "Sleeping Bag",
	}

	def __init__(self, item_type: int):
		self.item_type = item_type

	def get_name(self):
		if self.item_type in self.names:
			return self.names[self.item_type]

		return "unknown item type {}".format(self.item_type)

