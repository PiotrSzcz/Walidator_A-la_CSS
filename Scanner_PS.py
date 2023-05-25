import collections
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

class Scanner:

    def __init__(self, input):
        self.tokens = []
        self.current_token_number = 0
        for token in self.tokenize(input):
            self.tokens.append(token)

    def tokenize(self, input_string):
        keywords = {'EOF', '!IMPORTANT', 'NONE', 'BOLDER', 'SOLID', 'AVOID', "REM", "WHITE"}
        token_specification = [
            ('URL', r'url\([^)]*\)'),                  # URL
            ('HEX', r'\#[A-Fa-f]?\d+'),                # HEXADECIMAL NUMBERS
            ('PROC', r'\d+\%'),                        # PROCENTAGE
            ('STRING',  r'\"[^\"]*\"'),                # String
            ('ASSIGN',  r':'),                         # Assignment operator
            ('PIX',  r'\d+(\.\d*)?\s*px'),             # Integer or decimal pixel value
            ('NUMBER',  r'\d+(\.\d*)?'),               # Integer or decimal number
            ('END',     r';'),                         # Statement terminator
            ('OP',      r'[+*-]'),                     # Arithmetic operators
            ('RO', r'[<>]'),                           # Relational Operatos
            ('NEWLINE', r'\n'),                        # Line endings
            ('SEP', r','),                             # SEPERATOR
            ('COMMENT', r'\/\/.*'),                    # Comment
            ('SKIP',    r'[ ]'),                       # Skip over spaces
            ('TAB', r'[\t]'),                          # TABULATOr
            ('ID', r'[_#!\.]?[A-Za-z][A-Za-z0-9_-]*'),  # Identifiers
        ]
        tok_regex = '|'.join('(?P<%s>%s)' %
                             pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line_number = 1
        current_position = line_start = 0
        match = get_token(input_string)
        while match is not None:
            type = match.lastgroup
            if type == 'NEWLINE':
                line_start = current_position
                line_number += 1
            elif type != 'SKIP' and type != 'COMMENT':
                value = match.group(type)
                if type == 'ID' and value.upper() in keywords:
                    type = 'KEYWORD'
                if type == 'ID' and value[0] == '!'and value.upper() not in keywords:
                    raise RuntimeError(f'Error: keyword error in line {line_number} keyword "{value}" does not exist')
                yield Token(type, value, line_number, match.start()-line_start)
            current_position = match.end()
            match = get_token(input_string, current_position)
        if current_position != len(input_string):
            raise RuntimeError('Error: Unexpected character %r on line %d' %
                               (input_string[current_position], line_number))
        yield Token('EOF', '', line_number, current_position-line_start)

    def next_token(self):
        self.current_token_number += 1
        if self.current_token_number-1 < len(self.tokens):
            return self.tokens[self.current_token_number-1]
        else:
            raise RuntimeError('Error: No more tokens')