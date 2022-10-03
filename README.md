# PlanetNomadsSavegameEditor /L

PNSE is a save game editor for the game Planet Nomads by Craneballs.

This is Lisias's fork.


## Disclaimer:

- I am not a developer of Planet Nomads.
	- I'm not the original author of PlanetNomadsSavegameEditor neither. :)
- Planet Nomads is property of Craneballs, their copyright and stuff. See https://www.planet-nomads.com/
- The original PlanetNomadsSavegameEditor is authored by black-silence.
- Use the backup button regularly, PNSE is mangling the savegames without any real knowledge about how PN works internally. It's possible that something can go down trough the tubes eventually due something I could not foresee.


## Requirements:

- Python 3.5 or later
- optional: numpy and matplotlib


## Usage:

- run GUI.py
- either exit Planet Nomads or at least go to the main menu
- select a saved game
- make a backup
- click one of the buttons
- load the game in Planet Nomads

### Advanced Usage:

- Map: drag to rotate. Can be used to locate player and vehicles on the planet. Most of the construct will be crash sites.
- GPS beacons: creates 3 beacons, one at the north pole and two on the equator. They form an equilateral triangle that could be used to check your position on the planet.
- Machine Tools: In Planet Nomads, use the "Rename Block" feature to give a useful name to your machines. This name will show in the machine select instead of the numeric ID.
    - Teleporting: You can teleport your machine around. Please note that machines are not rotated, if you teleport something from the north pole to the south pole it will be upside down.
- Cheats: you're only cheating yourself if you use this too often. 
- Advanced Tools: stuff to help **you** on Planed Nomads.
- Dev Tools: stuff to help **me** with PNSE.

### Advanced Tools

#### Execute Command on Beacons

PNSE now supports "Commands" to allow you to customize (or uncustomize) your game.

To do so, you build a Beacon on the place you want to alter and name it `COMMAND: <cmd> <parm>`. It must be **exactly** the string `COMMAND:` followed by a space, followed by a command, followed by a space, followed by a parameter (those type depends do the command). `<cmd>` is case insensitive.

If you place the Beacon directly on the ground, creating a new "Machine" (with a single block) on your game, then the coordinates of the Beacon will be used as parameter by the commands.

If you place the Beacon on a existing "Machine" (any kind of construction, including vehicles and bases), then the coordinate of the "Machine" will be used instead.

**This is very important** as on larger constructions, the coordinates that will be used **will differ** from the place where you "welded" the Beacon!

Once a command is executed, the Beacon is removed from the game. If the "Machine" holding the Beacon has only one block (the Beacon itself), then the "Machine" is removed from the game too. No resources is recovered, think on it as an Environment Tax. :)

The following Commands are currently implemented:

##### `restore_grass <radius:float>`

This command will remove from the game any grass "modifications" (as the game calls every bit of grass you removed from the World) those center is inside a cube those center is the coordinate of the "Machine" and the sides are twice the "radius". The radius of the "modification" is ignored.

Any grass you had removed will be placed back inside the cube - **including** inside your constructions!

##### `restore_terrain <radius:float>`

This command will remove from the game any terrain "modifications" (as the game calls every hole you dug on the World) those center is inside a cube those center is the coordinate of the "Machine" and the sides are twice the "radius". The radius of the "modification" is ignored.

Any hole you had dug will be restored inside the cube - **including** inside your constructions! This can be very messy! ;) 

##### `restore_all <radius:float>`

A shortcut to execute both the commands above at the same time.

### Examples

You will find some use cases explained [here](./Docs/use-cases).


## Installation

WORK IN PROGRESS!

### License

* PlanetNomadsSavegameEditor /L is double licensed as follows:
	+ [GPL 2.0](https://www.gnu.org/licenses/gpl-2.0.txt). See [here](./LICENSE.GPL-2_0)
		+ You are free to:
			- Use : unpack and use the material in any computer or device
			- Redistribute : redistribute the original package in any medium
			- Adapt : Reuse, modify or incorporate source code into your works (and redistribute it!) 
		+ Under the following terms:
			- You retain any copyright notices
			- You recognise and respect any trademarks
			- You don't impersonate the authors, neither redistribute a derivative that could be misrepresented as theirs.
			- You credit the author and republish the copyright notices on your works where the code is used.
			- You relicense (and fully comply) your works using GPL 2.0
				- Please note that upgrading the license to GPLv3 **IS NOT ALLOWED** for this work, as the author **DID NOT** added the "or (at your option) any later version" on the license. 	
			- You don't mix your work with GPL incompatible works.

See [NOTICE](./NOTICE) for further copyright and trademarks notices.


## UPSTREAM

* [black-silence](https://github.com/black-silence/) **ROOT**
	+ [GitHub](https://github.com/black-silence/PlanetNomadsSavegameEditor)
