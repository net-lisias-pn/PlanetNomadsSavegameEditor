#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
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
import os, datetime
import atexit

import sqlite3

from PlanetNomads.SaveDirectory import util

class Entry:
	def __init__(self, row):
		self.id = int(row["id"])
		self.type = row["type"]
		self.master_autosave_id = int(row["id_master_autosave"])
		self.name = row["name"]
		self.created_at = datetime.datetime.fromtimestamp(int(row["created"]))
		self.modified_at = datetime.datetime.fromtimestamp(int(row["modified"]))
		self.base_seed_string = row["base_seed_string"]
		self.world_name = row["world_name"]
		self.thumbnail = bytes(row["thumbnail"])

	def __hash__(self):
		return self.id

	def __eq__(self, other):
		if isinstance(other, Entry):
			return self.id == other.id
		return NotImplemented

	def __ne__(self, other):
		if isinstance(other, Entry):
			return self.id != other.id
		return NotImplemented

	def __lt__(self, other):
		if isinstance(other, Entry):
			return self.id < other.id
		return NotImplemented

	def __gt__(self, other):
		if isinstance(other, Entry):
			return self.id > other.id
		return NotImplemented

	def __le__(self, other):
		if isinstance(other, Entry):
			return self.id <= other.id
		return NotImplemented

	def __ge__(self, other):
		if isinstance(other, Entry):
			return self.id >= other.id
		return NotImplemented

	def __repr__(self):
		return "Entry(id:{id:}, world:{world_name:}, type:{type:}, name:{name:})".format(**self.__dict__)

	def __str__(self):
		return "Savegame '{name}' in World '{world_name}' saved at {modified_at}".format(**self.__dict__)

class Directory:
	def __init__(self):
		self.loaded = False
		self.dbconnector = None
		self.db = None
		self.directory_path = os.path.join(util.solve_savedir(), "_main.db")
		print(self.directory_path)
		atexit.register(self.cleanup)
		self.__init_internal()
		self.reset()

	def __init_internal(self):
		self.__directory = list()
		self.__by_id = dict();
		self.__by_name = dict();

	def __del__(self):
		self.cleanup()

	def cleanup(self):
		self.__init_internal()
		if self.db:
			self.db.close()
			self.db = None

	def reset(self):
		self.dbconnector = sqlite3.connect(self.directory_path)
		self.db = self.dbconnector.cursor()
		self.db.row_factory = sqlite3.Row
		self.__init_internal()
		self.__load_directory()
		self.loaded = True

	def __load_directory(self):
		self.db.execute("select * from saves")
		for row in self.db.fetchall():
			e = Entry(row)
			self.__directory.append(e)
			self.__by_id[e.id] = e
			self.__by_name[e.name] = e.name

	def __getitem__(self, key):
		if isinstance(key, int): return self.__by_id[key]
		if isinstance(key, str): return self.__by_name[key]
		raise IndexError("{} with type {} is not a valid key".format(key, type(key)))

	def __iter__(self):
		return _DirectoryIterator(self)

	def __contains__(self, key):
		if isinstance(key, int): return key in self.__by_id
		if isinstance(key, str): return key in self.__by_name
		raise IndexError("{} with type {} is not a valid key".format(key, type(key)))

	def __len__(self):
		return len(self.__directory)

	def get(self, i:int) -> Entry:
		return self.__directory[i]

class _DirectoryIterator:
	def __init__(self, target:Directory):
		self.target = target
		self.i = 0

	def __next__(self):
		if self.i < len(self.target):
			r = self.target.get(self.i)
			self.i += 1
			return r
		raise StopIteration

