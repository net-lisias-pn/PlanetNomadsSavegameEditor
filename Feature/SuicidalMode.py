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
import traceback
from Feature import Player

def check_requirements(log, savegame):
	if "Survival" != savegame.game_mode:
		log("Savegame is not Survival. Can't implement SuicidalMode")
		return False

	# Player can't be inside a vehicle, as everything will be destroyed!
	if Player.is_ridding_vehicle(log, savegame):
		log("Player shouldn't be inside a vehicle or chamber. Can't implement SuicidalMode")
		return False
	return True

def implement(log, savegame):
	try:
		savegame.db.execute("delete from detail_chunk")
		savegame.db.execute("delete from grass_modifications")
		savegame.db.execute("delete from terrain_modifications")
		savegame.db.execute("delete from terrain_harvest")
		log("Terrain and grass reset.")

		savegame.db.execute("delete from datalog")
		savegame.db.execute("update cns_active_nodes set nodes=''")
		savegame.db.execute("delete from cns_progress")
		savegame.db.execute("delete from cns_requests_data")
		log("Quests removed.")

		savegame.db.execute("delete from containers where id<>0")
		log("Clearing up all inventories.")

		savegame.db.execute("delete from blueprint_constructions")
		savegame.db.execute("delete from blueprint_grid")
		log("All Blueprints Machines removed.")

		savegame.db.execute("delete from machine")
		savegame.db.execute("delete from machine_rtree")
		savegame.db.execute("delete from machine_rtree_node")
		savegame.db.execute("delete from machine_rtree_parent")
		savegame.db.execute("delete from machine_rtree_rowid")
		log("All User Machines removed.")

		savegame.db.execute("delete from active_blocks")
		savegame.db.execute("delete from activeblocks_connector_bindable_input")
		savegame.db.execute("delete from activeblocks_connector_power")
		savegame.db.execute("delete from activeblocks_connector_pipe")
		savegame.db.execute("delete from activeblocks_connector_winch")
		log("All Active Blocks removed.")
	except:
		traceback.print_exc()
	finally:
		savegame.dbconnector.commit()

	savegame.unlock_recipes()
	Player.remove_inventory(log, savegame)
	Player.create_item(log, savegame, 90, 25)	# Purified Water
	Player.create_item(log, savegame, 92, 25)	# Nutrition Capsules
	Player.create_item(log, savegame, 95, 25)	# Bandages
	Player.create_item(log, savegame, 99, 5)	# Biohazard Treatment
	Player.create_item(log, savegame, 104, 5)	# ThermalR Injection
	Player.create_item(log, savegame, 11691828, 50)	# Sleeping Bags

	savegame.save()
	log("Suicidal mode implemented.")


