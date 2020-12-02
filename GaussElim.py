from numpy import array
from copy import deepcopy
from fractions import Fraction

equation = array([
    [Fraction(2), Fraction(2), Fraction(0), Fraction(1)],
    [Fraction(3), Fraction(0), Fraction(3), Fraction(1)],
    [Fraction(0), Fraction(4), Fraction(4), Fraction(1)],
])


class InvalidGrid(Exception):

    def __init__(self, error="Unsolvable grid"):
        super().__init__(error)


class GaussElimination(object):

    def __init__(self, grid=array([])):
        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0])
        if not self.valid_grid():
            raise InvalidGrid()

    def valid_grid(self):

        def sum_line(line):
            return sum([abs(num) for num in line])

        def check_line(line, length):
            return sum_line(line) != 0 and len(line) == length

        check_columns = all([check_line(column, self.columns) for column in self.grid])
        check_rows = all([check_line(row, self.rows) for row in self.grid.T])
        check_size = self.rows+1 == self.columns

        return check_rows and check_columns and check_size

    def solve(self):
        # Implement fraction class when less lazy
        grid = self.grid.astype(Fraction)

        for row_num, row in enumerate(grid):
            diag_lead = row[row_num]

            if diag_lead == 0:
                temp = deepcopy(grid[row_num])
                grid[row_num] = grid[row_num+1]
                grid[row_num+1] = temp

                return self.solver(grid)
                return self.solve(grid)

            for r_num, r in enumerate(grid[row_num+1:]):
                d_lead = r[row_num] / diag_lead
                if d_lead == 0:
                    continue
                r -= row*d_lead

        for r_num, row in enumerate(grid):
            diag_lead = row[row_num]
            grid[r_num] = [value/diag_lead if diag_lead != 0 else value for value in row]

        self.grid = grid
        return self

    def __str__(self):
        letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + list("abcdefghijklmnopqrstuvwxyz")
        index = letters[:self.columns-1] + ["=="]
        output = "\t-|-\t".join(index) + "\n"
        for row in self.grid:
            row = list(map(lambda x: str(Fraction(x)), row))  # neatening the -0's
            output += "\t-|- \t".join(row) + "\n"
        return output


grid = GaussElimination(equation)

if __name__ == '__main__':
    print(grid.solve())
