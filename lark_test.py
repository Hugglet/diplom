from interpreter.lark_parser import parse_rcml


with open("examples/demo.rcml") as f:

    code = f.read()


ast = parse_rcml(code)


for node in ast:

    print(node)