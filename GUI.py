#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
		This file is part of PlanetNomadsSavegameEditor /L
			© 2022-2024 LisiasT
			© 2017-2018 black silence

		PlanetNomadsSavegameEditor /L is licensed as follows:
				* GPL 2.0 : https://www.gnu.org/licenses/gpl-2.0.txt

		PlanetNomadsSavegameEditor /L is distributed in the hope that it will be useful,
		but WITHOUT ANY WARRANTY; without even the implied warranty of
		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

		You should have received a copy of the GNU General Public License 2.0
		along with PlanetNomadsSavegameEditor /L. If not, see <https://www.gnu.org/licenses/>.
'''
import os, traceback, re

import tkinter as tk
from tkinter import filedialog
from tkinter.simpledialog import Dialog
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import _tkinter

import PlanetNomads.SaveDirectory as PNSD
from Feature import Backup, Kickstarter, Map3D, Migration, Commands, Machine, Player, SuicidalMode

import PlanetNomads

version = '1.6.0'

class OpenGameDialog(Dialog):
	def __init__(self, parent):
		directory = PNSD.Directory()
		self.__current_games = sorted(directory, key=lambda k:k.modified_at, reverse=True)
		self.selected_game = None
		self.selected_game_file = None
		self.__listbox = None

		super().__init__(parent, "Select a savegame")

	def body(self, frame):
		self.geometry("640x300")
		list_items = tk.Variable(value=self.__current_games)
		self.__listbox = tk.Listbox(
			self,
			listvariable=list_items,
			selectmode=tk.SINGLE
		)
		self.__listbox.pack(expand=True, fill=tk.BOTH)
		self.__listbox.bind('<<ListboxSelect>>', self.items_selected)
		return frame

	def items_selected(self, event):
		selected_indices = self.__listbox.curselection()
		self.selected_game = self.__current_games[selected_indices[0]]
		self.selected_game_file = os.path.join(PNSD.util.solve_savedir(), "save_{}.db".format(self.selected_game.id))

	def ok_pressed(self):
		self.destroy()

	def cancel_pressed(self):
		self.selected_game = None
		self.selected_game_file = None
		self.destroy()

	def select_file(self):
		"""
		Show file select dialog
		:return: None
		"""
		opts = {"filetypes": [("PN save files", "*.db"), ("All files", "*.*")]}
		opts["initialdir"] = PNSD.util.solve_savedir()
		self.selected_game = None
		self.selected_game_file = filedialog.askopenfilename(**opts)
		if self.selected_game_file:
			self.destroy()

	def buttonbox(self):
		self.file_button = ttk.Button(self, text="Select by file…", command=self.select_file)
		self.file_button.pack(side="left")
		cancel_button = tk.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
		cancel_button.pack(side="right")
		self.ok_button = tk.Button(self, text='OK', width=5, command=self.ok_pressed)
		self.ok_button.pack(side="right")
		self.bind("<Return>", lambda event: self.ok_pressed())
		self.bind("<Escape>", lambda event: self.cancel_pressed())

class GUI(tk.Frame):
	current_file = None
	savegame = None
	locked_buttons = []
	__HOTBARS = {
			"HotBar 1" : "hotBar_building",
			"HotBar 2" : "hotBar_building1",
			"HotBar 3" : "hotBar_building2",
			"HotBar 4" : "hotBar_building3",
			"HotBar 5" : "hotBar_building4",
			"HotBar 6" : "hotBar_building5",
			"HotBar 7" : "hotBar_building6",
			"HotBar 8" : "hotBar_building7",
			"HotBar 9" : "hotBar_building8",
			"HotBar 0" : "hotBar_building9",
		}

	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		self.parent = parent
		parent.title("Planet Nomads Savegame Editor %s" % version)

		# Toolbar
		gui_toolbar_frame = ttk.Frame(parent, padding="5 5 5 5")
		gui_toolbar_frame.pack(fill="both", expand=False)

		gui_load_game_button = ttk.Button(gui_toolbar_frame, text="Select Game…", command=self.select_game)
		gui_load_game_button.grid(row=0, column=0, sticky=(tk.E, tk.W))

		gui_backup_button = ttk.Button(gui_toolbar_frame, text="Create backup", command=self.create_backup)
		gui_backup_button.grid(row=0, column=1, sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_backup_button)
		self.gui_restore_button = ttk.Button(gui_toolbar_frame, text="Restore backup", command=self.restore_backup)
		self.gui_restore_button.grid(row=0, column=2, sticky=(tk.E, tk.W))
		self.gui_restore_button.state(["disabled"])  # Restore button is unlocked separately

		gui_export_save_button = ttk.Button(gui_toolbar_frame, text="Export file…", command=self.export_save)
		gui_export_save_button.grid(row=1, column=1, sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_export_save_button)

		gui_import_save_button = ttk.Button(gui_toolbar_frame, text="Import file…", command=self.import_save)
		gui_import_save_button.grid(row=1, column=2, sticky=(tk.E, tk.W))

		# content
		gui_main_frame = ttk.Frame(parent, padding="5 5 5 5")
		gui_main_frame.grid_rowconfigure(0, weight=1)
		gui_main_frame.grid_columnconfigure(0, weight=1)
		gui_main_frame.pack(fill="both", expand=False)

		gui_tabs = ttk.Notebook(gui_main_frame)
		gui_tabs.grid(sticky=(tk.N, tk.E, tk.S, tk.W))

		# status
		gui_status_frame = ttk.Frame(parent, relief="sunken", padding="2 2 2 2")
		gui_status_frame.pack(fill="both", expand=True)
		self.gui_status = ScrolledText(gui_status_frame, state='disabled', width=40, height=5, wrap='none')
		self.gui_status.pack(expand=True, fill="both")

		# Tabs after status bar to enable message display
		gui_tabs.add(self.init_basic_buttons(gui_main_frame), text="Basic tools")
		gui_tabs.add(self.init_machine_buttons(gui_main_frame), text="Machine tools")
		gui_tabs.add(self.init_cheat_buttons(gui_main_frame), text="Cheats")
		gui_tabs.add(self.init_adv_buttons(gui_main_frame), text="Advanced tools")
		gui_tabs.add(self.init_dev_buttons(gui_main_frame), text="Development tools")

		for button in self.locked_buttons:
			button.state(["disabled"])

	def init_machine_buttons(self, gui_main_frame):
		frame = ttk.Frame(gui_main_frame)

		self.machine_select_options = ["Select machine"]
		self.gui_selected_machine_identifier = tk.StringVar(self.parent)
		self.gui_selected_machine_identifier.set(self.machine_select_options[0])
		self.gui_selected_machine_identifier.trace('w', self.on_machine_selected)

		self.gui_machine_select = ttk.Combobox(frame, textvariable=self.gui_selected_machine_identifier,
											values=self.machine_select_options, state='readonly')
		self.gui_machine_select.grid(sticky=(tk.E, tk.W))
		self.locked_buttons.append(self.gui_machine_select)

		# Teleport area
		teleport_tools = ttk.Frame(frame)
		teleport_tools.grid(sticky=(tk.N, tk.E, tk.S, tk.W))

		gui_push_machine_button = ttk.Button(teleport_tools, text="Teleport selected machine",
											command=self.teleport_machine)
		gui_push_machine_button.grid(sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_push_machine_button)

		label = ttk.Label(teleport_tools, text=" to ")
		label.grid(row=0, column=1)

		self.gui_teleport_distance = tk.IntVar(self.parent)
		self.gui_teleport_distance.set(20)
		self.gui_teleport_distance_button = ttk.Entry(teleport_tools, textvariable=self.gui_teleport_distance,
													justify="center", width=5)
		self.gui_teleport_distance_button.grid(row=0, column=2)

		label = ttk.Label(teleport_tools, text=" meters over ")
		label.grid(row=0, column=3)

		options = ["current position"]
		self.gui_teleport_machine_target = tk.StringVar(self.parent)
		self.gui_teleport_machine_target.set(options[0])
		self.gui_teleport_target_button = ttk.OptionMenu(teleport_tools, self.gui_teleport_machine_target, *options)
		self.gui_teleport_target_button.grid(row=0, column=4, sticky=(tk.E, tk.W))
		self.locked_buttons.append(self.gui_teleport_target_button)

		# Recolor area
		color_grid = ttk.Frame(frame)
		color_grid.grid(sticky=(tk.N, tk.E, tk.S, tk.W))
		gui_randomize_color = ttk.Button(color_grid, text="Randomize colors", command=self.randomize_machine_color)
		gui_randomize_color.grid(row=0, column=2, sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_randomize_color)
		gui_change_color = ttk.Button(color_grid, text="Paint all blocks", command=self.change_machine_color)
		gui_change_color.grid(row=0, sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_change_color)
		gui_change_color = ttk.Button(color_grid, text="Paint grey blocks", command=self.replace_machine_color)
		gui_change_color.grid(row=0, column=1, sticky=(tk.E, tk.W))
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

	def init_adv_buttons(self, gui_main_frame):
		gui_frame = ttk.Frame(gui_main_frame)

		gui_command_button = ttk.Button(gui_frame, text="Execute Commands on Beacons",
										command=self.execute_commands)
		gui_command_button.grid(sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_command_button)

		gui_suicidal_button = ttk.Button(gui_frame, text="Implement Suicidal Mode",
										command=self.suicidal_mode)
		gui_suicidal_button.grid(sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_suicidal_button)

		return gui_frame

	def init_dev_buttons(self, gui_main_frame):
		gui_dev_tools_frame = ttk.Frame(gui_main_frame)

		gui_inventory_button = ttk.Button(gui_dev_tools_frame, text="List player inventory",
										command=self.list_inventory)
		gui_inventory_button.grid(sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_inventory_button)

		gui_machines_button = ttk.Button(gui_dev_tools_frame, text="List machines", command=self.list_machines)
		gui_machines_button.grid(sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_machines_button)

		gui_teleport_northpole_button = ttk.Button(gui_dev_tools_frame,
												text="Teleport player to north pole (death possible)",
												command=self.teleport_northpole)
		gui_teleport_northpole_button.grid(sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_teleport_northpole_button)
		return gui_dev_tools_frame

	def init_basic_buttons(self, gui_main_frame):
		gui_basic_tools_frame = ttk.Frame(gui_main_frame)

		if Map3D.enable_map:
			gui_draw_map_button = ttk.Button(gui_basic_tools_frame, text="Draw map", command=self.draw_map)
			gui_draw_map_button.grid(sticky=(tk.E, tk.W))
			self.locked_buttons.append(gui_draw_map_button)
		else:
			self.update_statustext("Install numpy + matplotlib to enable the map!")

		gui_unlock_button = ttk.Button(gui_basic_tools_frame, text="Unlock all recipes", command=self.unlock_recipes)
		gui_unlock_button.grid(sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_unlock_button)

		gui_northbeacon_button = ttk.Button(gui_basic_tools_frame, text="Create north pole beacon",
											command=self.create_north_beacon)
		gui_northbeacon_button.grid(row=0, column=1, sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_northbeacon_button)

		gui_southbeacon_button = ttk.Button(gui_basic_tools_frame, text="Create GPS beacons",
											command=self.create_gps_beacons)
		gui_southbeacon_button.grid(row=1, column=1, sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_southbeacon_button)

		self.gui_kickstarters_A_button = ttk.Button(gui_basic_tools_frame, text="Kickstarters parts A on HotBar", command=self.hotbar_kickstarters_A)
		self.gui_kickstarters_A_button.grid(row=2, column=0, sticky=(tk.E, tk.W))

		self.gui_kickstarters_B_button = ttk.Button(gui_basic_tools_frame, text="Kickstarters parts B on HotBar", command=self.hotbar_kickstarters_B)
		self.gui_kickstarters_B_button.grid(row=2, column=1, sticky=(tk.E, tk.W))

		self.gui_kickstarters_C_button = ttk.Button(gui_basic_tools_frame, text="Kickstarters parts C on HotBar", command=self.hotbar_kickstarters_C)
		self.gui_kickstarters_C_button.grid(row=3, column=1, sticky=(tk.E, tk.W))

		self.hotbar_select_options = ["Select HotBar"]
		self.gui_selected_hotbar_identifier = tk.StringVar(self.parent)
		self.gui_selected_hotbar_identifier.set(self.hotbar_select_options[0])
		self.gui_selected_hotbar_identifier.trace('w', self.on_hotbar_selected)

		self.gui_hotbar_select = ttk.Combobox(gui_basic_tools_frame, textvariable=self.gui_selected_hotbar_identifier,
											values=self.hotbar_select_options, state='readonly')
		self.gui_hotbar_select.grid(row=2, column=2, sticky=(tk.E, tk.W))
		self.locked_buttons.append(self.gui_hotbar_select)
		self.hotbar_select_update();

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
		Machine.distance_from_player(self.update_statustext, self.savegame, machine)

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

		Machine.teleport(self.update_statustext, self.savegame, machine_id, target_id, distance)

	def init_cheat_buttons(self, gui_main_frame):
		gui_cheats_frame = ttk.Frame(gui_main_frame)
		gui_resource_menu = tk.Menu(gui_cheats_frame, tearoff=0)
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
		gui_resource_menubutton.grid(sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_resource_menubutton)

		gui_item_menu = tk.Menu(gui_cheats_frame, tearoff=0)
		gui_item_menu.add_command(label="Basic Frame", command=lambda: self.create_item(69))
		gui_item_menu.add_command(label="Composite 1", command=lambda: self.create_item(78))
		gui_item_menu.add_command(label="Mechanical 1", command=lambda: self.create_item(76))
		gui_item_menu.add_command(label="Plating", command=lambda: self.create_item(67))
		gui_item_menu.add_command(label="Standard Electronics", command=lambda: self.create_item(73))
		gui_item_menubutton = ttk.Menubutton(gui_cheats_frame, text="Cheat: add stack of item", menu=gui_item_menu)
		gui_item_menubutton.grid(sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_item_menubutton)

		gui_unlock_button = ttk.Button(gui_cheats_frame, text="Cheat: give Mk4 equipment",
									command=self.create_mk4_equipment)
		gui_unlock_button.grid(sticky=(tk.E, tk.W))
		self.locked_buttons.append(gui_unlock_button)
		return gui_cheats_frame

	def teleport_northpole(self):
		if self.savegame.teleport_player(0, self.savegame.get_planet_size() + 250, 0):
			self.update_statustext("Player teleported")

	def update_statustext(self, message: str):
		self.gui_status.config(state=tk.NORMAL)
		self.gui_status.insert(tk.END, message + "\n")
		self.gui_status.see(tk.END)
		self.gui_status.config(state=tk.DISABLED)

	def select_game(self):
		d = OpenGameDialog(self.parent)
		if not d.selected_game_file:
			return
		self.current_game = d.selected_game
		self.current_file = d.selected_game_file
		self.load_file(self.current_file)
		if self.current_game:
			self.update_statustext("Loaded game '{}'".format(self.current_game.name))
		else:
			self.update_statustext("Loaded game '{}' from file '{}'".format(self.savegame.get_name(), os.path.basename(self.current_file)))

	def load_file(self, filename: tk.Text):
		"""
		Load file
		:type filename: Filename with absolute path
		"""
		self.savegame = PlanetNomads.Savegame()
		self.savegame.load(self.current_file)

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
			if not tk.messagebox.askokcancel("Overwrite existing backup?", "A backup already exists. Overwrite it?"):
				return
		try:
			Backup.create(self.current_file)
		except IOError:
			tk.messagebox.showerror(message="Could not create backup file!")
		else:
			tk.messagebox.showinfo("Backup created", "Backup was created")
			self.gui_restore_button.state(["!disabled"])

	def restore_backup(self):
		res = tk.messagebox.askokcancel("Please confirm", "Are you sure you want to restore the backup?")
		if not res:
			return
		try:
			Backup.restore(self.current_file, self.savegame)
		except IOError:
			tk.messagebox.showerror(message="Could not restore backup file!")
		else:
			tk.messagebox.showinfo("Backup restore", "Backup was restored")

	def list_machines(self):
		for m in self.savegame.machines:
			print(m)

	def unlock_recipes(self):
		Player.unlock_recipes(self.update_statustext, self.savegame)

	def create_north_beacon(self):
		self.savegame.create_north_pole_beacon()
		self.update_statustext("Beacon created with nav point C")

	def create_gps_beacons(self):
		self.savegame.create_gps_beacons()
		self.update_statustext("3 beacons created, north pole + 2x equator")

	def list_inventory(self):
		Player.list_inventory(self.update_statustext, self.savegame)

	def create_item(self, item_id, amount=100):
		if not Player.create_item(self.update_statustext, self.savegame, item_id, amount):
			tk.messagebox.showerror(message="Could not create resource {}. All slots full?".format(item_id))

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
		Machine.randomize_color(self.update_statustext, self.savegame, machine)

	def change_machine_color(self):
		machine = self.get_selected_machine()
		if not machine:
			return
		col = tk.colorchooser.askcolor()
		if not col[0]:
			return

		Machine.change_color(self.update_statustext, self.savegame, machine, col[0])

	def replace_machine_color(self):
		machine = self.get_selected_machine()
		if not machine:
			return
		col = tk.colorchooser.askcolor()
		if not col[0]:
			return

		Machine.replace_color(self.update_statustext, self.savegame, machine, col[0])

	def export_save(self):
		Migration.save_export(self.update_statustext, self.current_file)

	def import_save(self):
		# Select import file
		opts = {"filetypes": [("PN export files", "*.pnsave.zip"), ("All files", "*.*")]}
		opts["initialdir"] = PNSD.util.solve_savedir()
		importfilename = tk.filedialog.askopenfilename(**opts)
		if not importfilename:
			return
		# See if the _main.db is in the same directory, or let user select correct directory
		importdir = os.path.dirname(importfilename)
		mainfile = os.path.join(importdir, "_main.db")
		if not os.path.exists(mainfile):
			mainfile = os.path.join(str(opts["initialdir"]), "_main.db")
		if not os.path.exists(mainfile):
			opts["filetypes"] = [("PN main database", "_main.db"), ("All files", ".*")]
			mainfile = tk.filedialog.askopenfilename(**opts)
			if not mainfile:
				return
		if not os.path.exists(mainfile):
			self.update_statustext("Can't import without _main.db")
			return

		Migration.save_import(self.update_statustext, mainfile, importfilename)

	def on_hotbar_selected(self, *args):
		selected = self.gui_selected_hotbar_identifier.get()
		state = "{}disabled".format("!" if "Select HotBar" != selected else "")
		self.gui_kickstarters_A_button.state([state])
		self.gui_kickstarters_B_button.state([state])
		self.gui_kickstarters_C_button.state([state])
		self.update_statustext("Selected {}.".format(selected))

	def hotbar_select_update(self):
		self.hotbar_select_options = ["Select HotBar"]
		_list = []

		for i in range(1, 10):
			_list.append("HotBar {}".format(i))
		_list.append("HotBar {}".format(0))
		self.hotbar_select_options.extend(_list)
		self.gui_hotbar_select["values"] = self.hotbar_select_options
		self.gui_selected_hotbar_identifier.set("Select HotBar")

	def hotbar_kickstarters_A(self):
		selected = self.gui_selected_hotbar_identifier.get()
		try:
			Kickstarter.set_kickstarters_1(self.savegame, GUI.__HOTBARS[selected])
			self.update_statustext("Kickstarters partset A applied to {}.".format(selected))
		except Exception:
			self.update_statustext("Could not apply the patch!")
			traceback.print_exc()

	def hotbar_kickstarters_B(self):
		selected = self.gui_selected_hotbar_identifier.get()
		try:
			Kickstarter.set_kickstarters_2(self.savegame, GUI.__HOTBARS[selected])
			self.update_statustext("Kickstarters partset B applied to {}.".format(selected))
		except Exception:
			self.update_statustext("Could not apply the patch!")
			traceback.print_exc()

	def hotbar_kickstarters_C(self):
		selected = self.gui_selected_hotbar_identifier.get()
		try:
			Kickstarter.set_kickstarters_3(self.savegame, GUI.__HOTBARS[selected])
			self.update_statustext("Kickstarters partset C applied to {}.".format(selected))
		except Exception:
			self.update_statustext("Could not apply the patch!")
			traceback.print_exc()

	def execute_commands(self):
		Commands.do_it(self.update_statustext, self.savegame)

	def suicidal_mode(self):
		if not SuicidalMode.check_requirements(self.update_statustext, self.savegame) :
			tk.messagebox.showerror(message="Could not implement Suicidal Mode on loaded savegame!\n\nCheck the status box for the reasons.")
			return
		SuicidalMode.implement(self.update_statustext, self.savegame)


if __name__ == "__main__":
	window = tk.Tk()
	app = GUI(window)
	window.mainloop()
