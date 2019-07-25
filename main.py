import Factories
from FileIO import FileIO
import Testing
import Rulebook
import ExtPropCalc

debug_cell = False
debug_json = False
debug_rules = True

print('Testing stage for Cell API\n')

Testing.cell_unit_test()
Testing.container_unit_test()
Testing.prop_calc_unit_test()

loc = [1, 1, 1]
dim = [2, 2, 2]

c = Factories.cellFactory(3, loc, dim, {'Density': 0.00787}, False)
cont = Factories.containerFactory("json_test_input.txt")

print('\n\n--- EXPERIMENTAL AREA ---\n')

if debug_cell:
    print('Cell data:')
    print('ID:\t\t\t', c.ID())
    print('Pos:\t\t', c.location())
    print('Dims:\t\t', c.dimensions())
    print('MinMax:\t\t', c.minmax())
    print('Volume:\t\t', c.volume())
    print('CoreProps:\t', c.coreProperties())
    print('ExtProps:\t', c.extProperties())
    print(c.vertices(), '\n')
    print(c.vertices(1), '\n')
    print(c.vertices([0, 2, 3]), '\n')
    print(c.edges(), '\n')
    print(c.faces(), '\n')

if debug_json:
    print('Input Data:\t\t\t', cont.dumpData())
    print('Nearest Data:\t\t', cont.getNearestData([-432432, -42343242, 4234324]))
    print('Enclosed Data:\t\t', cont.getEnclosedData([[4, 5], [4, 5], [4, 5]]))
    print('All Data:\t\t\t', cont.getData([[4, 5], [4, 5], [4, 5]]))
    print('Data fields:\t\t', cont.lengthOfData())

if debug_rules:
    dens = ExtPropCalc.cellDensity(c.dimensions(), 0.2, c.extProperties()['Density'])
    print('Nearest Data:\t\t', cont.getNearestData([-432432, -42343242, 4234324]))
    print(dens)
    tr = Rulebook.Density('Density')
    print(tr.getProp())
    print(tr.apply_min(cont.getNearestData([-432432, -42343242, 4234324]), dens))