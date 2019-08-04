"""
Functions for calculating properties like density that are not contained in cell data directly.
Define functions here in order to implement new features.
Works in conjunction with the rules of Rulebook.py
"""

from functools import reduce
from Rulebook import PropRule


class CellDensity(PropRule):
    """Calculates the resulting density of the cell when void is subtracted from the outer wall.
    Air density is neglected."""

    prop = 'density'
    ### CHANGE DENSITY BACK TO MAT DENSITY
    resources = ('dimensions', 'wall_thickness', 'density')

    def __init__(self):
        super().__init__()

    @classmethod
    def calc(cls, ext_resources):
        """ext_resources: dimensions, wall_thickness, mat_density"""
        #dimensions = ext_resources['dimensions']
        #wall_thickness = ext_resources[1]
        #mat_density = ext_resources[2]
        innerHexa = [i - 2*ext_resources['wall_thickness'] for i in ext_resources['dimensions']]
        outerVolume = reduce(lambda res, i: res*i, ext_resources['dimensions'])
        innerVolume = reduce(lambda res, i: res*i, innerHexa)

        return {cls.prop: (outerVolume - innerVolume) / outerVolume * ext_resources['density']}


class MinMaxCoordinates(PropRule):
    """Calculates the min and max coordinates from cell location and dimensions.
    Min and Max can be calculated for any given dimensions."""

    prop = 'minmax'
    resources = ('location', 'dimensions')

    def __init__(self):
        super().__init__()

    @classmethod
    def calc(cls, *ext_resources):
        location = ext_resources[0]
        dimensions = ext_resources[1]
        if (type(location) is int or type(location) is float) and (type(dimensions) is int or type(dimensions) is float):
            min_location = location - dimensions / 2
            max_location = location + dimensions / 2
            minmax_coordinates = [min_location, max_location]
        else:
            minmax_coordinates = []
            for i in range(len(location)):
                min_location = location[i] - dimensions[i] / 2
                max_location = location[i] + dimensions[i] / 2
                minmax_coordinates.append([min_location, max_location])
        return minmax_coordinates