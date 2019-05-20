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

def parser(tokens):
  # here we will add errors
  if "=" not in [x[0] for x in tokens] or "identifier" not in [x[0] for x in tokens]:
    raise Exception("Uninitialized variable")
  types = [x[0] for x in tokens]
  dict = {}
  for t in types:
    if t in dict:
      dict[t] += 1
    else:
      dict[t] = 1
  if dict["identifier"] != 1 or dict["="] < 1 or dict[";"] != 1:
    raise Exception("SyntaxErrorWarning")
  varTable = {}


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
