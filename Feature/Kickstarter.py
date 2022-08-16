'''
Created on Aug 16, 2022

@author: lisias
'''

__KICKSTARTER_PARTS = [
		147, 148, 149, 150, 151, 152, 153, 154, 155, 156,
		157, 158, 159, 161, 162, 163, 164, 165, 166, 169,
		172, 175, 176, 177,	181
	]

def set_kickstarters_1(savegame, selected_hotbar):
	partlist = __KICKSTARTER_PARTS[:10]
	__update_hotbar(savegame, selected_hotbar, partlist)

def set_kickstarters_2(savegame, selected_hotbar):
	partlist = __KICKSTARTER_PARTS[10:20]
	__update_hotbar(savegame, selected_hotbar, partlist)

def set_kickstarters_3(savegame, selected_hotbar):
	partlist = __KICKSTARTER_PARTS[20:]
	__update_hotbar(savegame, selected_hotbar, partlist)

def __update_hotbar(savegame, selected_hotbar, partlist):
	l = list()
	fmt = "{:d}:B" # For blocks
	for i in partlist:
		l.append(fmt.format(i))
	l.append(fmt.format(i))
	value = ";".join(l)
	savegame.db.execute(f'update simple_storage set value = "{value:s}" where key = "{selected_hotbar:s}";')
	savegame.on_save()
