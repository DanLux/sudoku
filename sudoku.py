#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Daniel Alves'
__version__ = '1.0'

#-------------------------------------------------------------------------------


dimensions = 3

class Set:
    def __init__(self):
        self.forbidden = {}
        for symbol in Digit.symbols:
            self.forbidden[symbol] = False

    def forbid(self, digit):
        if digit.is_valid():
            if self.forbidden[digit.get_value()]:
                raise Exception
            else: self.forbidden[digit.get_value()] = True

    def allow(self, digit):
        self.forbidden[digit.get_value()] = False

    def verify(self, digit):
        return not self.forbidden[digit.get_value()]



class Table(Set):
    @staticmethod
    def get_index(position):
        row_index = Row.get_index(position)
        column_index = Column.get_index(position)
        return (row_index // dimensions) * dimensions - 1 + column_index // dimensions

class Row(Set):
    @staticmethod
    def get_index(position):
        return position // (dimensions ** 2)

class Column(Set):
    @staticmethod
    def get_index(position):
        return position % (dimensions ** 2)



class Digit:
    symbols = range(dimensions ** 2 + 1)
    position = {}
    for (index, symbol) in enumerate(symbols):
        position[symbol] = index

    def __init__(self, value):
        try:
            self.index = Digit.position[int(value)]
        except (KeyError, ValueError):
            self.index = 0

    def __repr__(self):
        if not self.is_valid():
            return '-'
        return str(self.get_value())

    def __cmp__(self, other):
        if self.index > other.index: return 1
        elif self.index < other.index: return -1
        else: return 0

    def get_value(self):
        return Digit.symbols[self.index]

    def next(self):
        if self.index + 1 < len(Digit.symbols):
            self.index += 1
            return True
        return False

    def reset(self):
        self.index = 0

    def is_valid(self):
        return 0 < self.index < len(Digit.symbols)



class Square:
    def __init__(self, value, table, row, column):
        self.digit = Digit(value)
        self.immutable = self.digit.is_valid()
        self.table = table
        self.row = row
        self.column = column
        if self.immutable:
            if not self.forbid():
                raise Exception('Invalid input file')

    def __repr__(self):
        if self.immutable:
            return '[' + repr(self.digit) + ']'
        else: return ' ' + repr(self.digit) + ' '

    def mark(self):
        if not self.immutable:
            self.allow()
            while self.digit.next():
                if self.verify_consistency():
                    self.forbid()
                    return True
        return False

    def allow(self):
        self.table.allow(self.digit)
        self.row.allow(self.digit)
        self.column.allow(self.digit)

    def forbid(self):
        try:
            self.table.forbid(self.digit)
            self.row.forbid(self.digit)
            self.column.forbid(self.digit)
            return True
        except:
            return False

    def verify_consistency(self):
        return self.table.verify(self.digit) and \
                    self.row.verify(self.digit) and \
                    self.column.verify(self.digit)

    def reset(self):
        if not self.immutable:
            self.digit.reset()


class Board:
    file_name = 'board.txt'

    def __init__(self):
        self.squares = []
        self.tables = [ Table() for table in range(dimensions ** 2) ]
        self.rows = [ Row() for row in range(dimensions ** 2) ]
        self.columns = [ Column() for column in range(dimensions ** 2) ]

        file_entry = open(Board.file_name)
        position = 0
        for line in file_entry.readlines():
            for symbol in line.split():
                table = self.tables[Table.get_index(position)]
                row = self.rows[Row.get_index(position)]
                column = self.columns[Column.get_index(position)]

                self.squares.append(Square(symbol, table, row, column))
                position += 1

        file_entry.close()
        if position != dimensions ** 4:
            raise Exception('Invalid input file: incorrect number of characters!')

    def __repr__(self):
        special_character = '.'
        row_counter = column_counter = 0
        output = '\n' + (4 * dimensions**2 + 1) * special_character + '\n' + special_character
        for square in self.squares:
            output += repr(square)
            if (column_counter + 1) % dimensions == 0:
                output += special_character
            else: output += ' '
            column_counter = (column_counter + 1) % dimensions ** 2
            if column_counter == 0:
                row_counter += 1
                if row_counter % dimensions == 0:
                    output += '\n' + (4 * dimensions**2 + 1) * special_character
                if row_counter < dimensions ** 2: output += '\n' + special_character
        output += '\n'
        return output


    def solve(self):
        square_index = 0
        proceed = True
        while 0 <= square_index < len(self.squares):
            square = self.squares[square_index]
            if not square.immutable:
                proceed = square.mark()

            if proceed:
                square_index += 1
            else:
                square.reset()
                square_index -= 1

        if square_index < 0:
            raise Exception('Inconsistent input file cannot be solved!')
        return self



if __name__ == '__main__':
    print(Board().solve())