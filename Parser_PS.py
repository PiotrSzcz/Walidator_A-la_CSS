class Parser:

    def __init__(self, scanner):
        self.next_token = scanner.next_token
        self.token = self.next_token()

    def take_token(self, token_type):
        if self.token.type != token_type:
            self.error(f"Unexpected token: {self.token.type}")
        if token_type != 'EOF':
            self.token = self.next_token()

    def error(self, msg):
        raise RuntimeError(f'Parser error in line {self.token.line}: {msg}')

    def start(self):
        if self.token.type == 'ID' or self.token.value == 'EOF':
            self.program()
            self.take_token('EOF')
        else:
            self.error("Epsilon not allowed")

    def program(self):
        if self.token.type == 'ID':
            self.statement()
            self.program()
        else:
            pass

    def statement(self):
        if self.token.type == 'ID':
            self.take_token('ID')
            if self.token.type == 'TAB':
                self.create()
            elif self.token.type == 'ASSIGN':
                self.assignWithCreation()
            elif self.token.type == 'OP' or self.token.type == 'RO':
                self.operation()
            elif self.token.type == 'ID':
                self.statement()
            elif self.token.type == 'SEP':
                self.take_token('SEP')
            else:
                self.error("Epsilon not allowed")
        else:
            self.error("Epsilon not allowed")

    def assignWithCreation(self):
        self.take_token('ASSIGN')
        self.take_token('ID')
        if self.token.type == 'TAB':
            self.take_token('TAB')
            self.assign_stmt()
        print("assignWithCreation OK")

    def assign_stmt(self):
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('ASSIGN')
            self.value()
            if self.token.type == 'END':
                self.take_token('END')
                print("assign_stmt OK")

        elif self.token.type == 'ASSIGN':
            self.take_token('ASSIGN')
            self.value()
            self.take_token('END')
            print("assign_stmt OK")
        else:
            self.error("Epsilon not allowed")
        if self.token.type == 'TAB':
            self.take_token('TAB')
            self.assign_stmt()

    def create(self):
        if self.token.type == 'TAB':
            self.take_token("TAB")
            self.assign_stmt()
            print("create Ok")
        else:
            self.error("create error")

    def operation(self):
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token(str(self.token.type))
            self.take_token('ID')
            print("operation OK")
        elif self.token.value == '*':
            self.take_token('OP')
            self.take_token(str(self.token.type))
            if self.token.type == 'ID':
                self.take_token('ID')
                print("operation OK")
            elif self.token.type == 'OP':
                self.take_token('OP')
                print("operation OK")
            else:
                self.error("operation error")
        elif self.token.type == 'OP' or self.token.type == 'RO':
            self.take_token(str(self.token.type))
            self.take_token('ID')
            print("operation OK")
        else:
            self.error("Epsilon not allowed")
        if self.token.type == 'SEP':
            self.take_token('SEP')
            self.operation()
        if self.token.type == 'TAB':
            self.take_token('TAB')
            self.assign_stmt()

    def value(self):
        if self.token.type == 'NUMBER':
            self.take_token('NUMBER')
        elif self.token.type == 'PROC':
            self.take_token('PROC')
        elif self.token.type == 'URL':
            self.take_token('URL')
        elif self.token.type == 'HEX':
            self.take_token('HEX')
        elif self.token.type == 'STRING':
            self.take_token('STRING')
        elif self.token.type == 'PIX':
            self.take_token('PIX')
        elif self.token.type == 'KEYWORD':
            self.take_token('KEYWORD')
        else:
            self.error("Epsilon not allowed")

        if self.token.type == 'ID':
            return
        if self.token.type != 'END':
            self.value()
