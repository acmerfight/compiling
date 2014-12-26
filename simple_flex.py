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

    def __str__(self):
        return self.name + ":" + self.value


class State(object):
    def __init__(self, name):
        self.epsilon = []
        self.transitions = {}
        self.name = name
        self.is_end = False


class NFA(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        end.is_end = True

    def add_state(self, state, state_set):
        if state in state_set:
            return
        state_set.add(state)
        for eps in state.epsilon:
            self.add_state(eps, state_set)

    def match(self, s):
        pass


class Handler(object):
    def __init__(self):
        self.state_count = 0

    def create_state(self):
        self.state_count += 1
        return State('s' + str(self.state_count))

    def handle_char(self, token, nfa_stack):
        state_start = self.create_state()
        state_end = self.create_state()
        state_start.transitions[token.value] = state_end
        nfa_stack.append(NFA(state_start, state_end))

    def handle_concat(self, token, nfa_stack):
        pre_nfa = nfa_stack.pop()
        more_pre_nfa = nfa_stack.pop()
        more_pre_nfa.is_end = False
        more_pre_nfa.end.epsilon.append(pre_nfa.start)
        nfa_stack.append(NFA(more_pre_nfa.start, pre_nfa.end))

    def handle_alt(self, token, nfa_stack):
        pre_nfa = nfa_stack.pop()
        more_pre_nfa = nfa_stack.pop()
        s0 = self.create_state()
        s0.epsilon = [more_pre_nfa.start, pre_nfa.start]
        s3 = self.create_state()
        more_pre_nfa.end.epsilon.append(s3)
        pre_nfa.end.epsilon.append(s3)
        more_pre_nfa.is_end = False
        pre_nfa.is_end = False
        nfa = NFA(s0, s3)
        nfa_stack.append(nfa)

    def handle_rep(self, token, nfa_stack):
        pre_nfa = nfa_stack.pop()
        s0 = self.create_state()
        s1 = self.create_state()
        s0.epsilon = [pre_nfa.start]
        if token.name == "STAR":
            s0.epsilon.append(s1)
        pre_nfa.end.epsilon.extend([s1, pre_nfa.start])
        pre_nfa.end.is_end = False
        nfa = NFA(s0, s1)
        nfa_stack.append(nfa)

    def handle_qmark(self, token, nfa_stack):
        pre_token = nfa_stack.pop()
        pre_token.start.epsilon.append(pre_token.end)
        nfa_stack.append(pre_token)


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
        if self.lookahead.value not in ")|":
            self.term()
            self.tokens.append(Token("CONCAT", "\0x08"))

    def factor(self):
        self.primary()
        if self.lookahead.name in {"STAR", "PLUS", "QMARK"}:
            self.tokens.append(self.lookahead)
            self.consume(self.lookahead.name)

    def primary(self):
        if self.lookahead.name == "LEFT_PAREN":
            self.consume("LEFT_PAREN")
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

lexer = Lexer("a*b")
parser = Parser(lexer)
tokens = parser.parse()
