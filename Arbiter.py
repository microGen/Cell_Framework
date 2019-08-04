from numpy import inf
from math import sqrt
from statistics import mean, median
from ExtPropCalc import MinMaxCoordinates

class Arbiter:
    def __init__(self, data_container, *args):
        self.__data_container = data_container
        pass

    ####################################################################################################################


    def applyRules(self, cell, rules, priorities, calc):
        """Applies the passed rules to cell and returns a boolean.
        cell: Cell to be tested against rules.
        rules: A list of rule classes.
        priorities: A list of priorities, in which order the rules are being applied. Must be the same length as rules.
        *calc: Functions for calculating properties that are not contained in cell data directly.

        Return Values: True - Cell is within set properties. False - Cell exceeds properties
        """

        cell_minmax = MinMaxCoordinates.calc(cell.properties('location'), cell.properties('dimensions'))
        grid_data = self.__data_container.getGridPoints(cell_minmax)

        rule_results = []
        for i in range(len(rules)):
            rule_resource = rules[i].getResources()

            prop_max = -inf
            for grid_point in grid_data:
                print('Grid point data: ', grid_point[rule_resource])
                prop_max = max(-inf, grid_point[rule_resource])

            if calc[i] != 0:
                pcalc_resources = calc[i].getResources()
                resource_list = []
                for r in pcalc_resources:
                    resource_list.append(cell.properties(r))
                pcalc_result = pcalc.calc(resource_list)
                rule_results.append(rules[i].apply(pcalc_result, prop_max))
            else:
                print('Cell props:', cell.properties(rule_resource))
                print('Grid data:', prop_max)
                rule_results.append(rules[i].apply(cell.properties(rule_resource), prop_max))
        print("Rule results: ", rule_results)
        return rule_results

    def applyRules2(self, cell, rules, priorities, prop_options, calc):

        # Handles choice of options for extraction of grid point properties.
        # Supported options are min, max, arithmetic mean (amn), median (med)
        def calc_prop_opt(properties, option):
            def prop_min(props):
                return min(props)
            def prop_max(props):
                return max(props)
            def prop_amn(props):
                return mean(props)
            def prop_med(props):
                return median(props)
            option_list = {'min': prop_min, 'max': prop_max, 'amn': prop_amn, 'med': prop_med}
            func = option_list.get(option)
            return func(properties)

        cell_minmax = MinMaxCoordinates.calc(cell.properties('location'), cell.properties('dimensions'))
        grid_points = self.__data_container.getGridPoints(cell_minmax)

        rule_results = []

        for i in range(len(rules)):
            # Grid points should only get resource lists from rules as they must already contain the data that the rule
            # compares the cell to.
            rule_resources = rules[i].getResources()

            # Choose how to get resource data from cell. If property calculator exists for rule, the resource list is
            # generated by calling its resource getter method. The cell's properties are passed to the calculator, which
            # generates the final property to be compared with grid data. Otherwise, cell properties are pulled by
            # calling the rule's getter.
            if calc[i] != 0:
                calc_resources = calc[i].getResources()
                cell_properties = {cr: cell.properties(cr) for cr in calc_resources}
                cell_resources = calc[i].calc(cell_properties)
            else:
                calc_resources = rule_resources
                cell_resources = {cr: cell.properties(cr) for cr in calc_resources}

            # Get property list from the grid and extract the min / max / mean / median value from list
            grid_resource_list = []
            for grid_point in grid_points:
                grid_resource = {rr: grid_point[rr] for rr in rule_resources}
                grid_resource_list.append(grid_resource)

            grid_resources = {}
            for resource in rule_resources:
                grid_data = [gr[resource] for gr in grid_resource_list]
                grid_resources.update({resource: calc_prop_opt(grid_data, prop_options[i])})

            print('cell resources: ', cell_resources, ', grid resources: ', grid_resources)
            rule_results.append(rules[i].apply(grid_resources, cell_resources))

        print("Rule results: ", rule_results)
        return rule_results


    ####################################################################################################################

    def splitCell(self, axis, cell):
        pass
