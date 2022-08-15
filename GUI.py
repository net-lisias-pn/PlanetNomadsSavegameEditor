#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, re
from math import sqrt

from tkinter import *
from tkinter import ttk, filedialog, messagebox, colorchooser
from tkinter.scrolledtext import ScrolledText
import _tkinter

from Feature import util
from Feature import Backup, Map3D, Migration
from PlanetNomads import Savegame

version = '1.4.0'

class GUI(Frame):
	current_file = None
	savegame = None
	locked_buttons = []

	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		parent.title("Planet Nomads Savegame Editor %s" % version)

		# Toolbar
		gui_toolbar_frame = ttk.Frame(parent, padding="5 5 5 5")
		gui_toolbar_frame.pack(fill="both", expand=True)

		gui_load_file_button = ttk.Button(gui_toolbar_frame, text="Select file", command=self.select_file)
		gui_load_file_button.grid(row=0, column=0, sticky=(E, W))

		gui_backup_button = ttk.Button(gui_toolbar_frame, text="Create backup", command=self.create_backup)
		gui_backup_button.grid(row=0, column=1, sticky=(E, W))
		self.locked_buttons.append(gui_backup_button)
		self.gui_restore_button = ttk.Button(gui_toolbar_frame, text="Restore backup", command=self.restore_backup)
		self.gui_restore_button.grid(row=0, column=2, sticky=(E, W))
		self.gui_restore_button.state(["disabled"])  # Restore button is unlocked separately

		gui_export_save_button = ttk.Button(gui_toolbar_frame, text="Export file", command=self.export_save)
		gui_export_save_button.grid(row=1, column=1, sticky=(E, W))
		self.locked_buttons.append(gui_export_save_button)

		gui_import_save_button = ttk.Button(gui_toolbar_frame, text="Import file", command=self.import_save)
		gui_import_save_button.grid(row=1, column=2, sticky=(E, W))

		# content
		gui_main_frame = ttk.Frame(parent, padding="5 5 5 5")
		gui_main_frame.grid_rowconfigure(0, weight=1)
		gui_main_frame.grid_columnconfigure(0, weight=1)
		gui_main_frame.pack(fill="both", expand=True)

		gui_tabs = ttk.Notebook(gui_main_frame)
		gui_tabs.grid(sticky=(N, E, S, W))

		# status
		gui_status_frame = ttk.Frame(parent, relief="sunken", padding="2 2 2 2")
		gui_status_frame.pack(fill="both", expand=True)
		self.gui_status = ScrolledText(gui_status_frame, state='disabled', width=40, height=5, wrap='none')
		self.gui_status.pack(expand=True, fill="both")

		# Tabs after status bar to enable message display
		gui_tabs.add(self.init_basic_buttons(gui_main_frame), text="Basic tools")
		gui_tabs.add(self.init_machine_buttons(gui_main_frame), text="Machine tools")
		gui_tabs.add(self.init_cheat_buttons(gui_main_frame), text="Cheats")
		gui_tabs.add(self.init_dev_buttons(gui_main_frame), text="Dev tools")

		for button in self.locked_buttons:
			button.state(["disabled"])

	def init_machine_buttons(self, gui_main_frame):
		frame = ttk.Frame(gui_main_frame)

		self.machine_select_options = ["Select machine"]
		self.gui_selected_machine_identifier = StringVar(self.parent)
		self.gui_selected_machine_identifier.set(self.machine_select_options[0])
		self.gui_selected_machine_identifier.trace('w', self.on_machine_selected)

		self.gui_machine_select = ttk.Combobox(frame, textvariable=self.gui_selected_machine_identifier,
											   values=self.machine_select_options, state='readonly')
		self.gui_machine_select.grid(sticky=(E, W))
		self.locked_buttons.append(self.gui_machine_select)

		# Teleport area
		teleport_tools = ttk.Frame(frame)
		teleport_tools.grid(sticky=(N, E, S, W))

		gui_push_machine_button = ttk.Button(teleport_tools, text="Teleport selected machine",
											 command=self.teleport_machine)
		gui_push_machine_button.grid(sticky=(E, W))
		self.locked_buttons.append(gui_push_machine_button)

		label = ttk.Label(teleport_tools, text=" to ")
		label.grid(row=0, column=1)

		self.gui_teleport_distance = IntVar(self.parent)
		self.gui_teleport_distance.set(20)
		self.gui_teleport_distance_button = ttk.Entry(teleport_tools, textvariable=self.gui_teleport_distance,
													  justify="center", width=5)
		self.gui_teleport_distance_button.grid(row=0, column=2)

		label = ttk.Label(teleport_tools, text=" meters over ")
		label.grid(row=0, column=3)

		options = ["current position"]
		self.gui_teleport_machine_target = StringVar(self.parent)
		self.gui_teleport_machine_target.set(options[0])
		self.gui_teleport_target_button = ttk.OptionMenu(teleport_tools, self.gui_teleport_machine_target, *options)
		self.gui_teleport_target_button.grid(row=0, column=4, sticky=(E, W))
		self.locked_buttons.append(self.gui_teleport_target_button)

		# Recolor area
		color_grid = ttk.Frame(frame)
		color_grid.grid(sticky=(N, E, S, W))
		gui_randomize_color = ttk.Button(color_grid, text="Randomize colors", command=self.randomize_machine_color)
		gui_randomize_color.grid(row=0, column=2, sticky=(E, W))
		self.locked_buttons.append(gui_randomize_color)
		gui_change_color = ttk.Button(color_grid, text="Paint all blocks", command=self.change_machine_color)
		gui_change_color.grid(row=0, sticky=(E, W))
		self.locked_buttons.append(gui_change_color)
		gui_change_color = ttk.Button(color_grid, text="Paint grey blocks", command=self.replace_machine_color)
		gui_change_color.grid(row=0, column=1, sticky=(E, W))
		self.locked_buttons.append(gui_change_color)

		return frame

	def update_machine_select(self, machines):
		self.machine_select_options = ["Select machine"]
		target = self.gui_teleport_target_button["menu"]
		target.delete(0, "end")
		target.add_command(label="current position")
		machine_list = []

		for m in machines:
			_type = m.get_type()
			name_id = m.get_name_or_id()
			if _type == "Construct" and m.get_name() == "":
				continue  # 300+ wrecks are just too much
			machine_list.append("{} {} [{}]".format(_type, name_id, m.identifier))
			target.add_command(label="{} {}".format(_type, name_id),
							   command=lambda value=m.identifier: self.gui_teleport_machine_target.set(value))
		machine_list.sort()
		self.machine_select_options.extend(machine_list)
		self.gui_machine_select["values"] = self.machine_select_options
		self.gui_selected_machine_identifier.set("Select machine")
		self.gui_teleport_machine_target.set("current position")

	def init_dev_buttons(self, gui_main_frame):
		gui_dev_tools_frame = ttk.Frame(gui_main_frame)

		gui_inventory_button = ttk.Button(gui_dev_tools_frame, text="List player inventory",
										  command=self.list_inventory)
		gui_inventory_button.grid(sticky=(E, W))
		self.locked_buttons.append(gui_inventory_button)

		gui_machines_button = ttk.Button(gui_dev_tools_frame, text="List machines", command=self.list_machines)
		gui_machines_button.grid(sticky=(E, W))
		self.locked_buttons.append(gui_machines_button)

		gui_teleport_northpole_button = ttk.Button(gui_dev_tools_frame,
												   text="Teleport player to north pole (death possible)",
												   command=self.teleport_northpole)
		gui_teleport_northpole_button.grid(sticky=(E, W))
		self.locked_buttons.append(gui_teleport_northpole_button)
		return gui_dev_tools_frame

	def init_basic_buttons(self, gui_main_frame):
		gui_basic_tools_frame = ttk.Frame(gui_main_frame)

		if Map3D.enable_map:
			gui_draw_map_button = ttk.Button(gui_basic_tools_frame, text="Draw map", command=self.draw_map)
			gui_draw_map_button.grid(sticky=(E, W))
			self.locked_buttons.append(gui_draw_map_button)
		else:
			self.update_statustext("Install numpy + matplotlib to enable the map!")

		gui_unlock_button = ttk.Button(gui_basic_tools_frame, text="Unlock all recipes", command=self.unlock_recipes)
		gui_unlock_button.grid(sticky=(E, W))
		self.locked_buttons.append(gui_unlock_button)

		gui_northbeacon_button = ttk.Button(gui_basic_tools_frame, text="Create north pole beacon",
											command=self.create_north_beacon)
		gui_northbeacon_button.grid(row=0, column=1, sticky=(E, W))
		self.locked_buttons.append(gui_northbeacon_button)

		gui_southbeacon_button = ttk.Button(gui_basic_tools_frame, text="Create GPS beacons",
											command=self.create_gps_beacons)
		gui_southbeacon_button.grid(row=1, column=1, sticky=(E, W))
		self.locked_buttons.append(gui_southbeacon_button)
		return gui_basic_tools_frame

	def get_selected_machine_id(self, warn=True):
		"""Return selected machine id or print status message"""
		machine_id = self.gui_selected_machine_identifier.get()
		if machine_id == "Select machine":
			if warn:
				self.update_statustext("Select a machine first")
			return
		x = re.search(r'\[(\d+)]$', machine_id)
		return int(x.group(1))

	def get_selected_machine(self, warn=True):
		machine_id = self.get_selected_machine_id(warn)
		if not machine_id:
			return
		for machine in self.savegame.machines:
			if machine.identifier == machine_id:
				return machine

	def on_machine_selected(self, *args):
		machine = self.get_selected_machine(False)
		if not machine:
			return
		machine_coords = machine.get_coordinates()
		player_coords = self.savegame.get_player_position()
		x = machine_coords[0] - player_coords[0]
		y = machine_coords[1] - player_coords[1]
		z = machine_coords[2] - player_coords[2]
		distance = sqrt(x**2 + y**2 + z**2)
		self.update_statustext("Selected machine %s, distance to player %.1f" % (machine.get_name_or_id(), distance))

	def teleport_machine(self):
		machine_id = self.get_selected_machine_id()
		if not machine_id:
			return
		target = self.gui_teleport_machine_target.get()
		if target == "current position":
			target_id = None
		else:
			target_id = int(target)

		try:
			distance = self.gui_teleport_distance.get()
		except _tkinter.TclError:
			self.update_statustext("Please use only numbers in the teleport distance")
			return

		target_machine = None
		active_machine = None
		for machine in self.savegame.machines:
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
			self.update_statustext("Something broke, did not find machine")
			return
		active_machine.teleport(distance, target_machine)
		self.update_statustext("Machine {} teleported".format(active_machine.get_name_or_id()))
		self.savegame.save()

	def init_cheat_buttons(self, gui_main_frame):
		gui_cheats_frame = ttk.Frame(gui_main_frame)
		gui_resource_menu = Menu(gui_cheats_frame, tearoff=0)
		gui_resource_menu.add_command(label="Aluminium", command=lambda: self.create_item(51))
		gui_resource_menu.add_command(label="Biomass Container", command=lambda: self.create_item(392745))
		gui_resource_menu.add_command(label="Carbon", command=lambda: self.create_item(49))
		gui_resource_menu.add_command(label="Cobalt", command=lambda: self.create_item(60))
		gui_resource_menu.add_command(label="Iron", command=lambda: self.create_item(56))
		gui_resource_menu.add_command(label="Silicium", command=lambda: self.create_item(52))
		gui_resource_menu.add_command(label="Silver", command=lambda: self.create_item(59))
		gui_resource_menu.add_command(label="Titanium", command=lambda: self.create_item(57))
		gui_resource_menu.add_command(label="Uranium", command=lambda: self.create_item(61))
		gui_resource_menu.add_command(label="Enriched Uranium", command=lambda: self.create_item(63))
		gui_resource_menubutton = ttk.Menubutton(gui_cheats_frame, text="Cheat: add stack of resource",
												 menu=gui_resource_menu)
		gui_resource_menubutton.grid(sticky=(E, W))
		self.locked_buttons.append(gui_resource_menubutton)

		gui_item_menu = Menu(gui_cheats_frame, tearoff=0)
		gui_item_menu.add_command(label="Basic Frame", command=lambda: self.create_item(69))
		gui_item_menu.add_command(label="Composite 1", command=lambda: self.create_item(78))
		gui_item_menu.add_command(label="Mechanical 1", command=lambda: self.create_item(76))
		gui_item_menu.add_command(label="Plating", command=lambda: self.create_item(67))
		gui_item_menu.add_command(label="Standard Electronics", command=lambda: self.create_item(73))
		gui_item_menubutton = ttk.Menubutton(gui_cheats_frame, text="Cheat: add stack of item", menu=gui_item_menu)
		gui_item_menubutton.grid(sticky=(E, W))
		self.locked_buttons.append(gui_item_menubutton)

		gui_unlock_button = ttk.Button(gui_cheats_frame, text="Cheat: give Mk4 equipment",
									   command=self.create_mk4_equipment)
		gui_unlock_button.grid(sticky=(E, W))
		self.locked_buttons.append(gui_unlock_button)
		return gui_cheats_frame

	def teleport_northpole(self):
		if self.savegame.teleport_player(0, self.savegame.get_planet_size() + 250, 0):
			self.update_statustext("Player teleported")

	def update_statustext(self, message: str):
		self.gui_status.config(state=NORMAL)
		self.gui_status.insert(END, message + "\n")
		self.gui_status.see(END)
		self.gui_status.config(state=DISABLED)

	def select_file(self):
		"""
		Show file select dialog
		:return: None
		"""
		opts = {"filetypes": [("PN save files", "*.db"), ("All files", "*.*")]}
		opts["initialdir"] = util.solve_savedir()
		filename = filedialog.askopenfilename(**opts)
		if not filename:
			return
		self.load_file(filename)

	def load_file(self, filename: Text):
		"""
		Load file
		:type filename: Filename with absolute path
		"""
		self.current_file = filename

		self.savegame = Savegame.Savegame()
		self.savegame.load(self.current_file)
		self.update_statustext("Loaded game '{}'".format(self.savegame.get_name()))

		# Enable some buttons once a file is loaded
		for button in self.locked_buttons:
			button.state(["!disabled"])

		if Backup.exists(filename):
			self.gui_restore_button.state(["!disabled"])
		else:
			self.gui_restore_button.state(["disabled"])

		self.update_machine_select(self.savegame.machines)

	def create_backup(self):
		if Backup.exists(self.current_file):
			if not messagebox.askokcancel("Overwrite existing backup?", "A backup already exists. Overwrite it?"):
				return
		try:
			Backup.create(self.current_file)
		except IOError:
			messagebox.showerror(message="Could not create backup file!")
		else:
			messagebox.showinfo("Backup created", "Backup was created")
			self.gui_restore_button.state(["!disabled"])

	def restore_backup(self):
		res = messagebox.askokcancel("Please confirm", "Are you sure you want to restore the backup?")
		if not res:
			return
		try:
			Backup.restore(self.current_file, self.savegame)
		except IOError:
			messagebox.showerror(message="Could not restore backup file!")
		else:
			messagebox.showinfo("Backup restore", "Backup was restored")

	def list_machines(self):
		for m in self.savegame.machines:
			print(m)

	def unlock_recipes(self):
		if self.savegame.unlock_recipes():
			self.update_statustext("All blocks unlocked")
		else:
			self.update_statustext("Nothing unlocked. Is this a survival save?")

	def create_north_beacon(self):
		self.savegame.create_north_pole_beacon()
		self.update_statustext("Beacon created with nav point C")

	def create_gps_beacons(self):
		self.savegame.create_gps_beacons()
		self.update_statustext("3 beacons created, north pole + 2x equator")

	def list_inventory(self):
		inventory = self.savegame.get_player_inventory()
		stacks = inventory.get_stacks()
		for slot in stacks:
			print("Slot {}: {} {}".format(slot, stacks[slot].get_count(), stacks[slot].get_item_name()))

	def create_item(self, item_id, amount=100):
		inventory = self.savegame.get_player_inventory()
		if not inventory:
			self.update_statustext("Could not load inventory")
			return
		item = Savegame.Item(item_id)

		if not inventory.add_stack(item, amount):
			messagebox.showerror(message="Could not create resource. All slots full?")
			return
		self.update_statustext("Added {} to inventory".format(item.get_name()))
		inventory.save()

	def create_mk4_equipment(self):
		self.create_item(118, 1)
		self.create_item(114, 1)
		self.create_item(110, 1)

	def draw_map(self):
		try:
			selected_machine_id = int(self.gui_selected_machine_identifier.get())
		except ValueError:
			selected_machine_id = 0
		Map3D.draw(self.savegame, selected_machine_id)

	def randomize_machine_color(self):
		machine = self.get_selected_machine()
		if not machine:
			return
		machine.randomize_color()
		self.update_statustext("Machine {} color changed".format(machine.get_name_or_id()))
		self.savegame.save()

	def change_machine_color(self):
		machine = self.get_selected_machine()
		if not machine:
			return
		col = colorchooser.askcolor()
		if not col[0]:
			return
		machine.set_color(col[0])
		self.update_statustext("Machine {} color changed".format(machine.get_name_or_id()))
		self.savegame.save()

	def replace_machine_color(self):
		machine = self.get_selected_machine()
		if not machine:
			return
		col = colorchooser.askcolor()
		if not col[0]:
			return
		# Default color is (180, 180, 180), left upper in PN color chooser
		machine.set_color(col[0], (180, 180, 180))
		self.update_statustext("Machine {} color changed".format(machine.get_name_or_id()))
		self.savegame.save()

	def export_save(self):
		zipname, zipdir = Migration.save_export(self.current_file)
		self.update_statustext("Exported current save to %s\n in %s" % (zipname, zipdir))

	def import_save(self):
		# Select import file
		opts = {"filetypes": [("PN export files", "*.pnsave.zip"), ("All files", "*.*")]}
		opts["initialdir"] = util.solve_savedir()
		importfilename = filedialog.askopenfilename(**opts)
		if not importfilename:
			return
		# See if the _main.db is in the same directory, or let user select correct directory
		importdir = os.path.dirname(importfilename)
		mainfile = os.path.join(importdir, "_main.db")
		if not os.path.exists(mainfile):
			mainfile = os.path.join(str(opts["initialdir"]), "_main.db")
		if not os.path.exists(mainfile):
			opts["filetypes"] = [("PN main database", "_main.db"), ("All files", ".*")]
			mainfile = filedialog.askopenfilename(**opts)
			if not mainfile:
				return
		if not os.path.exists(mainfile):
			self.update_statustext("Can't import without _main.db")
			return

		try:
			meta, next_id = Migration.save_import(mainfile, importfilename)
			self.update_statustext("Imported %s game '%s' as id %i" % (meta["type"], meta["name"], next_id))
		except RuntimeError:
			self.update_statustext("Could not load the exported file.\n Maybe the bzip2 extension is missing.")
		except OSError:
			self.update_statustext("Could not create the file")


if __name__ == "__main__":
	window = Tk()
	app = GUI(window)
	window.mainloop()
