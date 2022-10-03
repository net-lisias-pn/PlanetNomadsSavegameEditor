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
from . import Attributes
Col = Attributes.Col
Pos = Attributes.Pos
Rot = Attributes.Rot

from . import Base
BaseBounds = Base.BaseBounds
BasePosition = Base.BasePosition
BaseRotation = Base.BaseRotation

from . import Blocks
ActiveBlock = Blocks.ActiveBlock
Block = Blocks.Block
Blocks = Blocks.Blocks

from . import Grids
Grid = Grids.Grid
SubGrid = Grids.SubGrid

from . import Savegame
DistancePhysicsFreezeData = Savegame.DistancePhysicsFreezeData
Container = Savegame.Container
Machine = Savegame.Machine
Stack = Savegame.Stack
Savegame = Savegame.Savegame

CLASSES = globals()

from . import Nodes
XmlNode = Nodes.XmlNode
MachineNode = Nodes.MachineNode
