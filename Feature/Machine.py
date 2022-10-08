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
import math

def distance_from_player(log, savegame, machine) -> float:
	machine_coords = machine.get_coordinates()
	player_coords = savegame.get_player_position()
	x = machine_coords[0] - player_coords[0]
	y = machine_coords[1] - player_coords[1]
	z = machine_coords[2] - player_coords[2]
	distance = math.sqrt(x**2 + y**2 + z**2)
	log("Selected machine %s, distance to player %.1f" % (machine.get_name_or_id(), distance))

def teleport(log, savegame, machine_id, target_id, distance):
	target_machine = None
	active_machine = None
	for machine in savegame.machines:
		if machine.identifier == machine_id:
			active_machine = machine
			if not target_id:
				target_machine = machine  # Relative to its current position
			if target_machine:
				break  # We found both or do not need a target
		if machine.identifier == target_id:
			target_machine = machine
			if active_machine:
				break  # We found both
	if not active_machine:
		log("Something broke, did not find machine")
		return
	active_machine.teleport(distance, target_machine)
	log("Machine {} teleported".format(active_machine.get_name_or_id()))
	savegame.save()

def replace_color(log, savegame, machine, col):
	# Default color is (180, 180, 180), left upper in PN color chooser
	machine.set_color(col[0], (180, 180, 180))
	log("Machine {} color changed".format(machine.get_name_or_id()))
	savegame.save()

def randomize_color(log, savegame, machine):
	machine.randomize_color()
	log("Machine {} color changed".format(machine.get_name_or_id()))
	savegame.save()

def change_color(log, savegame, machine, col):
	machine.set_color(col[0])
	log("Machine {} color changed".format(machine.get_name_or_id()))
	savegame.save()


