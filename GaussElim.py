from numpy import array, flip
from copy import deepcopy
from fractions import Fraction
from functools import reduce

variables = array([
    [Fraction(2), Fraction(2), Fraction(1)],
    [Fraction(3), Fraction(0), Fraction(3)],
    [Fraction(2), Fraction(4), Fraction(4)],
])
values = array([
    [Fraction(1)],
    [Fraction(1)],
    [Fraction(1)],
])


class InvalidGrid(Exception):

    def __init__(self, error="Unsolvable grid"):
        super().__init__(error)


class GaussElimination(object):

    def __init__(self, variables, values):
        self.variables = variables
        self.values = values
        self.check_grid()

    def check_grid(self):
        var_dim = self.variables.shape
        if not var_dim[0] == var_dim[1]:
            raise InvalidGrid("Invalid amount of variables given")

        val_dim = self.values.shape
        if not var_dim[0] == val_dim[0]:
            raise InvalidGrid("Number of variables is not the same as answers given")

        def valid_line(num_array):
            return 0 not in reduce(lambda x, y: abs(x)+abs(y), num_array)

        if not (valid_line(self.variables) and valid_line(self.variables.T)):
            raise InvalidGrid

    def simplify_variables(self, clean_grid=True):
        for r_num, row in enumerate(self.variables):
            diag_value = row[r_num]
            if diag_value == 0:
                print("fuck")
                temp = deepcopy(self.variables[r_num])
                self.variables[r_num] = self.variables[r_num+1]
                self.variables[r_num+1] = temp
                return self.simplify_variables()
            row_index = r_num+1
            for r in self.variables[row_index:]:
                d_lead = r[r_num] / diag_value
                r -= row * d_lead
                self.values[row_index] -= self.values[r_num] * d_lead
                row_index += 1

        return self

    def clean_grid(self):
        for r_num, r in enumerate(self.variables):
            diag_lead = self.variables[r_num][r_num]
            r /= diag_lead
            self.values[r_num] /= diag_lead

    def solve_system(self):
        def quick_flip():
            self.variables = flip(self.variables)
            self.values = flip(self.values)

        self.simplify_variables()
        quick_flip()
        self.simplify_variables()
        quick_flip()

        self.clean_grid()

        return self

    def __str__(self):
        letters = list("XYZABCDEFGHIJKLMNOPQRSTUVW")
        length = self.variables.shape[0]
        output = "\t".join(letters[:length]) + "\n"
        self.variables = self.variables.astype(Fraction)
        self.values = self.values.astype(Fraction)
        for row, val in zip(self.variables, self.values):
            for var in row:
                output += str(var) + "\t"
            output += "=\t" + str(val[0])+"\n"
        return output


if __name__ == '__main__':
    grid = GaussElimination(variables, values)
    print(grid.solve_system())
