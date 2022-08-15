'''
Created on Aug 15, 2022

@author: lisias
'''
import shutil, os, re
import zipfile, sqlite3, json

def save_export(current_file:str) -> tuple():
	zipdir = os.path.dirname(current_file)
	save_id = re.search(r"_(\d+)\.db$", current_file).group(1)

	# Load _main.db for meta data
	dbconnector = sqlite3.connect(os.path.join(zipdir, "_main.db"))
	maindb = dbconnector.cursor()
	maindb.row_factory = sqlite3.Row
	maindb.execute("select * from saves where id = ?", (save_id,))
	row = maindb.fetchone()
	metadata = {}
	for k in row.keys():
		metadata[k] = row[k]
	del (metadata["id"], metadata["thumbnail"])

	# Generate a safe name from the saved game title
	zipname = "{}.pnsave.zip".format(re.sub(r"[^a-zA-Z0-9._-]+", "-", metadata["name"]))
	fullname = os.path.join(zipdir, zipname)

	# Open zip file and write save and meta. Try to compress it
	try:
		myzip = zipfile.ZipFile(fullname, "w", zipfile.ZIP_BZIP2)
	except RuntimeError:
		myzip = zipfile.ZipFile(fullname, "w")
	stripped_name = "save_00.db"
	myzip.write(current_file, arcname=stripped_name)
	myzip.writestr("meta.json", json.dumps(metadata))
	myzip.close()
	return zipname, zipdir

def save_import(mainfile:str, importfilename:str) -> tuple:
	# See if the _main.db is in the same directory, or let user select correct directory
	# Load _main.db
	dbconnector = sqlite3.connect(mainfile)
	maindb = dbconnector.cursor()
	maindb.execute("select max(id) from saves")
	next_id = maindb.fetchone()[0] + 1

	# Load zip
	with zipfile.ZipFile(importfilename) as myzip:
		myzip.extract("save_00.db")
		# TODO detect correct file name scheme from existing saves
		shutil.move("save_00.db", os.path.join(os.path.dirname(mainfile), "save_%i.db" % next_id))
		metajson = myzip.read("meta.json")
		meta = json.loads(metajson)
		maindb.execute(
			"insert into saves (type, id_master_autosave, name, created, modified, base_seed_string, "
			"world_name) values (:type, -1, :name, :created, :modified, :base_seed_string, :world_name)",
			meta)
		dbconnector.commit()
	return meta, next_id
