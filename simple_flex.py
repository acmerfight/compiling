# coding=utf8

#给定如下的正则表达式 (a|b)((c|d)*)，请完成如下练习：
#（1）使用Thompson算法，将该正则表达式转换成非确定状态有限自动机（NFA）；
#（2）使用子集构造算法，将该上述的非确定有限状态自动机（NFA）转换成确定状态有限自动机（DFA）；
#（3）使用Hopcroft算法，对该DFA最小化。


SYMBOLS = {
    '(': 'LEFT_PAREN',
    ')': 'RIGHT_PAREN',
    '*': 'STAR',
    '|': 'ALT',
    '\x08': 'CONCAT',
    '+': 'PLUS',
    '?': 'QMARK',
}


class ReToNFA(object):

    def __init__(self):
        pass


class Token(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.lookahead = self.lexer.get_next_token()

    def parse(self):
        self.exp()
        return self.tokens

    def exp(self):
        self.term()
        if self.lookahead.name == "ALT":
            t = self.lookahead
            self.consume("ALT")
            self.exp()
            self.tokens.append(t)

    def term(self):
        self.factor()

    def factor(self):
        self.primary()
        if self.lookahead.name in {"STAR", "PLUS", "QMARK"}:
            self.tokens.append(self.lookahead)
            self.consume(self.lookahead.name)

    def primary(self):
        if self.lookahead.name == "LEFT_PAREN":
            self.exp()
            self.consume("RIGHT_PAREN")
        elif self.lookahead.name == "CHAR":
            self.tokens.append(self.lookahead)
            self.consume("CHAR")

    def consume(self, name):
        self.lookahead = self.lexer.get_next_token()



class Lexer(object):
    def __init__(self, regex_pattern):
        self.regex_pattern = regex_pattern
        self.length = len(regex_pattern)
        self.current_pos = 0

    def get_next_token(self):
        if self.current_pos < self.length:
            char = self.regex_pattern[self.current_pos]
            self.current_pos += 1
            token = Token(SYMBOLS.get(char, "CHAR"), char)
            return token
        else:
            return Token("NONE", '')
