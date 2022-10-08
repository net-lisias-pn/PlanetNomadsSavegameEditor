'''
Created on Oct 8, 2022

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
import PlanetNomads

def unlock_recipes(log, savegame):
	if savegame.unlock_recipes():
		log("All blocks unlocked")
	else:
		log("Nothing unlocked. Is this a survival save?")

def list_inventory(log, savegame):
	inventory = savegame.get_player_inventory()
	stacks = inventory.get_stacks()
	for slot in stacks:
		log("Slot {}: {} {}".format(slot, stacks[slot].get_count(), stacks[slot].get_item_name()))

def create_item(log, savegame, item_id, amount=100):
	inventory = savegame.get_player_inventory()
	if not inventory:
		log("Could not load inventory")
		return

	item = PlanetNomads.Item(item_id)

	if not inventory.add_stack(item, amount):
		return False

	log("Added {} to inventory".format(item.get_name()))
	inventory.save()
	return True

def remove_inventory(log, savegame):
	pass
