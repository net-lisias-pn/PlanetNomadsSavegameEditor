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

class Item:
	names = {
		3: "Pistol *MIA*",

		8: "SMG *MIA*",

		11: "Rifle *MIA*",

		30: "Shotgun *MIA*",
		31: "Pulse Defense Rifle",
		32: "Plasma Launcher *MIA*",
		33: "Battery",

		49: "Carbon",

		51: "Aluminium",
		52: "Silicon",

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
		79: "Composite Parts Mk2",
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

		99: "Biohazard Treatment",
		100: "Adrenaline Injection",

		102: "Weapon Battery",

		104: "ThermalR Injection",

		107: "Exploration Suit Mk1",
		108: "Exploration Suit Mk2",
		109: "Exploration Suit Mk3",
		110: "Exploration Suit Mk4",
		111: "Jetpack Mk1",
		112: "Jetpack Mk2",
		113: "Jetpack Mk3",
		114: "Jetpack Mk4",
		115: "Multitool Mk1",
		116: "MultiTool Mk2",
		117: "MultiTool Mk3",
		118: "MultiTool Mk4",

		392745:   "Biomass Container",
		8058188:  "Dried Meat",
		9550358:  "Seeds",
		11691828: "Sleeping Bag",
		15928778: "Oxygen Tank",
		25268490: "Extraterrestrial Power Cell",
		27509316: "Mission Manual Datapad",
		50589143: "Scanner",
		64230464: "Mover Tool",
		65103317: "Crystal Override Matrix",
		65103378: "Pure Crystal",
		66837776: "Polycrystal Chassis",
	}

	def __init__(self, item_type: int):
		self.item_type = item_type

	def get_name(self):
		if self.item_type in self.names:
			return self.names[self.item_type]

		return "unknown item type {}".format(self.item_type)

