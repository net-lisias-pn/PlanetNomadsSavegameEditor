'''
Created on Aug 15, 2022

@author: lisias
'''
import os
import PlanetNomads

FILENAME = "~/Library/Application Support/unity.Craneballs.PlanetNomads/Saves/save_66.db"

def list_inventory(savegame):
	inventory = savegame.get_player_inventory()
	stacks = inventory.get_stacks()
	for slot in stacks:
		print("Slot {}: {} {}".format(slot, stacks[slot].get_count(), stacks[slot].get_item_name()))

def create_item(savegame, item_id, amount=1):
	inventory = savegame.get_player_inventory()
	if not inventory:
		print("Could not load inventory")
		return
	item = PlanetNomads.Item(item_id)

	if not inventory.add_stack(item, amount):
		print("Could not create resource. All slots full?")
		return
	print("Added {} to inventory".format(item.get_name()))
	inventory.save()

def trick_hotbar(savegame):
	update_hotbar1(savegame, 1);
	update_hotbar2(savegame, 2);
	update_hotbar3(savegame, 3);
	update_hotbar4(savegame, 4);
	update_hotbar5(savegame, 5);
	update_hotbar6(savegame, 6);
	update_hotbar7(savegame, 7);
	update_hotbar8(savegame, 8);
	update_hotbar9(savegame, 9);
	update_hotbar0(savegame, 0);

def list_hotbar(savegame):
	savegame.db.execute('select key,value from simple_storage where key like "hotBar_%" order by key;')
	r = savegame.db.fetchall()
	for i in r:
		for k in i.keys():
			print(k, i[k])

def update_hotbar(savegame, prefix, bar):
	l = list()
	fmt = "{:d}{:d}:E" # For Expendables (Items). Works only when present in the Inventory.
	fmt = "{:d}{:d}:B" # For blocks
	for i in range (1,10):
		l.append(fmt.format(prefix, i))
	l.append(fmt.format(prefix, 0))
	value = ";".join(l)
	savegame.db.execute(f'update simple_storage set value = "{value:s}" where key = "{bar:s}";')
	savegame.on_save()

def update_hotbar1(savegame, prefix):
	update_hotbar(savegame, prefix, "hotBar_building")

def update_hotbar2(savegame, prefix):
	update_hotbar(savegame, prefix, "hotBar_building1")

def update_hotbar3(savegame, prefix):
	update_hotbar(savegame, prefix, "hotBar_building2")

def update_hotbar4(savegame, prefix):
	update_hotbar(savegame, prefix, "hotBar_building3")

def update_hotbar5(savegame, prefix):
	update_hotbar(savegame, prefix, "hotBar_building4")

def update_hotbar6(savegame, prefix):
	update_hotbar(savegame, prefix, "hotBar_building5")

def update_hotbar7(savegame, prefix):
	update_hotbar(savegame, prefix, "hotBar_building6")

def update_hotbar8(savegame, prefix):
	update_hotbar(savegame, prefix, "hotBar_building7")

def update_hotbar9(savegame, prefix):
	update_hotbar(savegame, prefix, "hotBar_building8")

def update_hotbar0(savegame, prefix):
	update_hotbar(savegame, prefix, "hotBar_building9")

def main():
	savegame = PlanetNomads.Savegame()
	savegame.load(os.path.expanduser(FILENAME))
	print (savegame.get_name())
	list_inventory(savegame)

	trick_hotbar(savegame)
	list_hotbar(savegame);

#     for i in range(120, 150):
#         create_item(savegame, i)

	savegame.cleanup()
	return 0

if __name__ == '__main__':
	exit(main())
