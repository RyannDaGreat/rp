#ALL CREDIT GOES TO https://gist.github.com/julian-klode/1e278ce6dd9be1a83b715c8729baf912
#!/usr/bin/python3
# Copyright (C) 2010 Julian Andres Klode <jak@jak-linux.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Sudoku Game.
A simple Sudoku game that uses backtracking for solving and creating
Sudokos."""


import curses
import random
import time


class Block(object):
    """Store a single 3x3 block in the complete field."""

    def __init__(self):
        self._block = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __setitem__(self, point, value):
        """Set the value, check that value is not already in the block."""
        # n == -n, as n < 0 means user generated abs(n).
        if abs(self._block[point[1] + 3 * point[0]]) == abs(value):
            self._block[point[1] + 3 * point[0]] = value
            return
        if value != 0 and (value in self._block or -value in self._block):
            raise ValueError("Block already contains %d" % value)
        self._block[point[1] + 3 * point[0]] = value

    def __getitem__(self, point):
        """Return the value at the given point."""
        return self._block[point[1] + 3 * point[0]]


class Sudoku(object):

    def __init__(self):
        self._field = [Block() for i in range(9)]
        # Cached values used in solve() and populate()
        self._values = list(range(1, 10))
        self._points = [(x, y) for y in range(9) for x in range(9)]

    def clear(self):
        """Reset the game to empty."""
        for b in self._field:
            b._block = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def candidates(self, point):
        """Return all candidates at the point (x, y)."""
        candidates = set()
        previous = self[point]
        for i in self._values:
            try:
                self[point] = i
            except ValueError:
                pass
            else:
                candidates.add(i)
        self[point] = previous
        return candidates

    def populate(self, n=36):
        """Populate ca. n fields of the Sudoku.
        Clear the Sudoku, run the solver using random values and
        remove as many values as possible.
        """
        # Randomize the list of points and values
        random.shuffle(self._points)
        random.shuffle(self._values)
        self.clear()
        self.solve()

        for point in self._points:
            if self[point] == 0:
                continue
            val = self[point]
            for v in self.candidates(point):
                if v == val:
                    continue
                self[point] = v
                if self.solve(True):
                    self[point] = val
                    break
            else:
                if (81 - sum(b._block.count(0) for b in self._field) < n):
                    self[point] = val
                    break
                self[point] = 0

        for point in self._points:
            self[point] *= -1

    def __str__(self):
        """Represent the Sudoku as a string (for debugging purposes)."""
        s = ""
        for y in range(9):
            for x in range(9):
                s += '%d ' % self[x, y]
                if (x + 1) % 3 == 0:
                    s += " "
            s += "\n"
            if (y + 1) % 3 == 0:
                s += "\n"
        return s.strip()

    def __getitem__(self, p):
        pb = (p[0] // 3, p[1] // 3)
        block = self._field[pb[1] + 3 * pb[0]]

        return block[p[0] % 3, p[1] % 3]

    def __setitem__(self, p, val):
        if self[p] < 0 and val >= 0:
            raise ValueError("Value at point %s is pre-defined" % str(p))
        if val != 0:
            for i in range(9):
                if i != p[1] and abs(self[p[0], i]) == abs(val):
                    raise ValueError("Already in column: %d" % val)
                if i != p[0] and abs(self[i, p[1]]) == abs(val):
                    raise ValueError("Already in row: %d" % val)

        pb = (p[0] // 3, p[1] // 3)
        block = self._field[pb[1] + 3 * pb[0]]

        block[p[0] % 3, p[1] % 3] = val

    def is_solved(self):
        return all(0 not in self._field[i]._block for i in range(0, 9))

    def solve(self, reset=False):
        """Solve the Sudoku.
        If 'reset' is True, just check whether the sudoku can be solved,
        after return the sudoku will be identical to before the call.
        """
        if self.is_solved():
            return True

        field = None
        for x in range(9):
            if field is not None:
                break
            for y in range(9):
                if self[x, y] == 0:
                    field = (x, y)
                    break

        if field is None:
            return True

        for new in self._values:
            try:
                self[field] = new
            except ValueError:
                continue
            else:
                if self.solve(reset):
                    if reset:
                        self[field] = 0
                    return True
                else:
                    self[field] = 0


class CursesUI(object):
    """Command-line 'curses' interface."""

    def __init__(self):
        self._screen = curses.initscr()
        self._sudoku = Sudoku()

        # Draw the borders
        self._screen.vline(0, 4 * 3 - 2, curses.ACS_VLINE, 2 * 9 - 1)
        self._screen.vline(0, 4 * 6 - 2, curses.ACS_VLINE, 2 * 9 - 1)
        self._screen.hline(2 * 3 - 1, 0, curses.ACS_HLINE, 4 * 9 - 3)
        self._screen.hline(2 * 6 - 1, 0, curses.ACS_HLINE, 4 * 9 - 3)
        self._screen.addch(2 * 3 - 1, 4 * 3 - 2, curses.ACS_PLUS)
        self._screen.addch(2 * 3 - 1, 4 * 6 - 2, curses.ACS_PLUS)
        self._screen.addch(2 * 6 - 1, 4 * 3 - 2, curses.ACS_PLUS)
        self._screen.addch(2 * 6 - 1, 4 * 6 - 2, curses.ACS_PLUS)
        self._draw_sudoku()
        curses.noecho()
        curses.cbreak()
        self._screen.keypad(1)

    def __enter__(self, *a):
        return self

    def __exit__(self, *a):
        curses.nocbreak()
        self._screen.keypad(0)
        curses.echo()
        curses.endwin()

    def _draw_sudoku(self):
        for y in range(0, 9):
            for x in range(0, 9):
                value = self._sudoku[x, y]
                attr = curses.A_BOLD if value < 0 else 0
                # Mark cells with only one possible solution.
                #if len(self._sudoku.candidates((x,y))) == 1:
                #    attr  |= curses.A_UNDERLINE
                self._screen.addch(2 * y, 4 * x, ord('0') + abs(value), attr)

    def _print_string(self, string):
        self._screen.move(20, 0)
        self._screen.deleteln()
        self._screen.addstr(string)

    def _help(self):
        self._print_string("Commands: (q)uit, (p)opulate, (P)opulate, "
                           "(r)eset, (c)andidates, (s)olve")

    def main(self):
        x = 0
        y = 0
        self._help()
        while True:
            self._screen.move(y, x)
            try:
                c = chr(self._screen.getch())
            except:
                c = ':'
            if c == ':':
                self._print_string(":")
                curses.echo()
                #self._screen.move(20, 0)
                c = self._screen.getstr()
                curses.noecho()
            if c == 'q':
                break  # Exit the while()
            elif c == 'h':
                self._help()
            elif c in ('p', 'P'):
                if c == 'P':
                    self._print_string("Enter number of fields: ")
                    curses.echo()
                    n = int(self._screen.getstr())
                    curses.noecho()
                else:
                    n = 36
                start = time.time()
                self._sudoku.populate(n)
                end = time.time()
                self._draw_sudoku()
                self._print_string("Populated with %d fields in %.3f seconds"
                                   % (n, end - start))
            elif c == 's':
                if not self._sudoku.solve():
                    self._print_string("Could not solve sudoku")
                self._draw_sudoku()
            elif c == 'r':
                self._sudoku = Sudoku()
                self._draw_sudoku()
            elif c == 'c':
                point = (x // 4, y // 2)
                self._print_string("Candidates for %s are: %s" %
                                   (point, self._sudoku.candidates(point)))
            elif c == chr(curses.KEY_LEFT):
                x -= x >= 4 and 4 or 0
            elif c == chr(curses.KEY_RIGHT):
                x += x + 4 < 4 * 9 and 4 or 0
            elif c == chr(curses.KEY_UP):
                y -= y >= 2 and 2 or 0
            elif c == chr(curses.KEY_DOWN):
                y += y + 2 < 2 * 9 and 2 or 0
            elif c in "0123456789":
                try:
                    self._sudoku[x // 4, y // 2] = ord(c) - ord('0')
                    self._screen.addch(y, x, c)
                    # If single-candidate cells should be highlighted, use the
                    # following instead of self._screen.addch():
                    #self._draw_sudoku()
                except Exception as e:
                    self._print_string(str(e))
                else:
                    if self._sudoku.is_solved():
                        self._print_string("Solved")
                    else:
                        self._print_string("")
            else:
                self._print_string("Error: Invalid command '%s'" % c)


if True or __name__ == '__main__':
    with CursesUI() as ui:
        ui.main()
        assert False,'Sudoku game over'
