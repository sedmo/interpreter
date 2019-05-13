import re

class PeekableStream:
    def __init__(self, iterator):
        self.iterator = iter(iterator)
        self._fill()

    def _fill(self):
        try:
            self.next = next(self.iterator)
        except StopIteration:
            self.next = None

    def move_next(self):
        ret = self.next
        self._fill()
        return ret


def lex(chars_iter):
    chars = PeekableStream(chars_iter)
    while chars.next is not None:
        c = chars.move_next()
        if c in " \n":  # Ignore white space
            pass
        elif c in "+-*":  # Special characters
            yield ("Operator", c)

        elif c in "();=":
            yield (c, "")

        elif re.match("[1-9]", c):
            yield ("NonZeroDigit", c)

        elif re.match("[0-9]", c):
            yield ("Digit", c)

        elif re.match("[a-zA-Z_]", c):
            yield ("Letter", c)

        else:
            raise Exception(
                "Error during tokenization process! Unrecognized character: '" + c + "'.")


class Parser:

    def __init__(self, tokens, stop_at):
        self.tokens = tokens
        self.stop_at = stop_at

    def next_expression(self, prev):
        self.fail_if_at_end(";")
        typ, value = self.tokens.next
        if typ in self.stop_at:
            return prev
        self.tokens.move_next()
        if typ in ("NonZeroDigit", "Digit", "Letter") and prev is None:
            return self.next_expression((typ, value))
        elif typ == "Operator":
            nxt = self.next_expression(None)
            return self.next_expression(("Operator", value, prev, nxt))
        elif typ == "(":
            args = self.multiple_expressions(",", ")")
            return self.next_expression(("Exp", prev, args))
        elif typ == "=":
            if prev[0] != "Identifier":
                raise Exception(
                    "You can't assign to anything except an identifier.")
            nxt = self.next_expression(None)
            return self.next_expression(("Assignment", prev, nxt))
        else:
            raise Exception("Unexpected token: " + str((typ, value)))

    def multiple_expressions(self, sep, end):
        ret = []
        self.fail_if_at_end(end)
        typ = self.tokens.next[0]
        if typ == end:
            self.tokens.move_next()
        else:
            arg_parser = Parser(self.tokens, (sep, end))
            while typ != end:
                p = arg_parser.next_expression(None)
                if p is not None:
                    ret.append(p)
                typ = self.tokens.next[0]
                self.tokens.move_next()
                self.fail_if_at_end(end)
        return ret

    def fail_if_at_end(self, expected):
        if self.tokens.next is None:
            raise Exception("Hit end of file - expected '%s'." % expected)


def parse(tokens):
    # determine if it is an assignment
    parser = Parser(tokens, ";")
    while parser.tokens.next is not None:
        p = parser.next_expression(None)
        if p is not None:
            yield p
        parser.tokens.move_next()


def main():
    while True:
        try:
            text = input('steph_preter> ')
        except EOFError:
            break
        tokens = lex(text)
        p = parse(tokens)
        print(p)
        # interpreter = Interpreter(text)
        # result = interpreter.expr()
        # print(result)


if __name__ == '__main__':
    main()
