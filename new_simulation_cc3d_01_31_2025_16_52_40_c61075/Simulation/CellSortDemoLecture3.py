
from cc3d import CompuCellSetup
        

from CellSortDemoLecture3Steppables import CellSortDemoLecture3Steppable

CompuCellSetup.register_steppable(steppable=CellSortDemoLecture3Steppable(frequency=1))


CompuCellSetup.run()
