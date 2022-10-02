'''
Created on Oct 2, 2022

@author: lisias
'''

def get_commands(savegame) -> list:
	r = list()
	for m in savegame.machines:
		blocks = m.active_block_data
		for b in blocks.keys():
			block = blocks[b]
			if '56' != block.root.attrib['Type_ID'] : continue
			if block.name.startswith("COMMAND:"):
				tag, cmd, parm = block.name.split(" ")
				r.append((m, b, cmd, parm))
	return r

def execute_commands(savegame, commands) -> list:
	r = list()
	for command in commands:
		machine = command[0]
		block = command[1]
		cmd = command[2]
		parm = float(command[3])

		if cmd.lower() == "restore_all":
			try:
				__remove_transformations(savegame, 'grass', machine.get_coordinates(), parm)
				__remove_transformations(savegame, 'terrain', machine.get_coordinates(), parm)
				r.append((machine, block))
			except Exception as e:
				print(str(e))
			continue
		if cmd.lower() == "restore_terrain":
			try:
				__remove_transformations(savegame, 'terrain', machine.get_coordinates(), parm)
				r.append((machine, block))
			except Exception as e:
				print(str(e))
			continue
		if cmd.lower() == "restore_grass":
			try:
				__remove_transformations(savegame, 'grass', machine.get_coordinates(), parm)
				r.append((machine, block))
			except Exception as e:
				print(str(e))
			continue
	return r

def cleanup_commands(savegame, command_holders:list):
	for h in command_holders:
		machine = h[0]
		block = h[1]
		machine.active_block_ids.remove(block)
		del machine.active_block_data[block]

		savegame.db.execute("delete from active_blocks where id=?", (block,))
		if 0 == len(machine.active_block_data):
			savegame.db.execute("delete from machine_rtree_rowid where rowid=?", (machine.identifier,))
			savegame.db.execute("delete from machine_rtree where id=?", (machine.identifier,))
			savegame.db.execute("delete from machine where id=?", (machine.identifier,))
		savegame.dbconnector.commit()
	pass

def __remove_transformations(savegame, kind:str, coord:tuple, radius:float):
	table = "{:s}_modifications".format(kind)

	x_min = coord[0] - radius
	x_max = coord[0] + radius
	y_min = coord[1] - radius
	y_max = coord[1] + radius
	z_min = coord[2] - radius
	z_max = coord[2] + radius

	savegame.db.execute("select idChunk, p_x, p_y, p_z, radius from {:s}".format(table))
	rows = savegame.db.fetchall()

	victims = set()
	for row in rows:
		idChunk = row['idChunk']
		p_x = row['p_x']
		p_y = row['p_y']
		p_z = row['p_z']
		r = row['radius']

		if (x_min <= p_x <= x_max) and \
			(y_min <= p_y <= y_max) and \
			(z_min <= p_z <= z_max) :
			victims.add((idChunk,p_x,p_y,p_z))

	for v in victims:
		savegame.db.execute("delete from {:s} where idChunk=? and p_x=? and p_y=? and p_z=?".format(table), v)
	savegame.dbconnector.commit()

