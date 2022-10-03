# PlanetNomadsSavegameEditor :: Change Log

* 2022-1002: 1.5.0 (Lisias) for PN >= 1.0.7.2
	+ Refactoring
		- Each feature is now on its own Module.
	+ Workaround for an Axes3d idiosyncrasy on modern Python.
	+ Restoring MacOS support on dialogs.
	+ Updated Blocks and Expendables definitions
	+ Unlocking the new Recipes from recent PN versions
	+ Allowing access to the Kickstarts parts by hacking them into the Hotbars.
	+ Adding "Commands" to be executed by the tool:
		- `restore_grass`
		- `resgore_terrain`
		- `restore_all`
* 2019-0510: 1.4.0 (black silence) for PN >= 1.0.0
	+ Updated load/save to work with zipfiles created by PN 1.0.0
* 2018-0429: 1.3.1 (black silence)
	+ Added glass cockpit to vehicle detection
	+ After selecting machines, show the distance to the player character to help identify what you selected
* 2018-0202: 1.3.0 (black silence)
	+ Export saved games to a file. The file is bzip2 compressed if possible.
	+ Import saved games from a file
* 2018-0131: 1.2.0 (black silence)
	+ Recolor your constructions easily
	+ Better machine select
* 2017-1113: 1.1.0 (black silence)
	+ Named machines are now displayed in the machine select even if they are not vehicles (cockpit) or bases (generator)
	+ Teleport distance can be customized
	+ Teleport target location can be selected
* 2017-0705: No precise dates known, using first commit as place holder.
	+ v1.0.4
		- read planet size from game settings
		- pushing machines updated to work with PN 0.7.10
	+ v1.0.3
		- map now displays the selected machine separately
	+ v1.0.2
		- updated to work with PN 0.7.8
		- added map drawing
	+ v1.0.1
		- replaced status bar with scrolling log area
		- better initial directory for file open dialog
		- better machine selector
		- minor UI changes
	+ v1.0.0
		- first public release
		- recipe unlocking
		- vehicle teleporter
		- navigation beacons
