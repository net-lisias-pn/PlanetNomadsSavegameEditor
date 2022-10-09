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

__player_is_ridding_vehicle = None
def is_ridding_vehicle(log, savegame) -> bool:
	global __player_is_ridding_vehicle
	if None != __player_is_ridding_vehicle:
		return __player_is_ridding_vehicle

	savegame.db.execute("select value from simple_storage where key='playerVehicle'")
	try:
		value = savegame.db.fetchone()["value"]
		__player_is_ridding_vehicle = (-1 != value.find("True"))
	except TypeError:
		# Old games don't have advanced settings in simple storage
		# Assume the worst
		return True
	return __player_is_ridding_vehicle


def remove_inventory(log, savegame):
	savegame.db.execute("update containers set content='v:1,' where id=0")
	savegame.dbconnector.commit()

	inventory = savegame.get_player_inventory()
	if not inventory:
		log("Could not load inventory")
		return

	inventory.get_stacks().clear()
	inventory.save()
	log("Player's inventory was emptied.")
