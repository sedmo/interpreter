import re

def lex(text):
  i = 0
  d = []
  while i < len(text):
    if text[i] in " \n":
      i += 1
    elif text[i] in "+-*":  # Special characters
        d.append( ("Operator", text[i]) )
        i += 1
    elif text[i] in "();=":
        d.append( (text[i], "") )
        i += 1
    # identifier
    elif re.match("[_a-zA-Z]", text[i] ):
      prev = [ text[i] ]
      i += 1
      while re.match("[0-9a-zA-Z_]", text[i]):
        prev.append( text[i] )
        i += 1
      #once it stops matching, save it as identifier
      d.append( ("identifier", ''.join(prev) ) )
    # literal
    elif re.match("[0-9]", text[i] ):
      prev = [ text[i] ]
      i += 1
      while re.match("[1-9]", prev[0]) and text[i].isnumeric():
        prev.append( text[i] )
        i += 1
      d.append( ("literal", ''.join(prev) ) )
    else:
       raise Exception(
                "Error during tokenization process! Unrecognized character: '" + text[i] + "'.")
  return d

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
