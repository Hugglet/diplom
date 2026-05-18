from lark import Lark

from interpreter.transformer import RCMLTransformer


with open("grammar/rcml.lark") as f:

    grammar = f.read()


parser = Lark(
    grammar,
    parser="lalr"
)


transformer = RCMLTransformer()


def parse_rcml(code):

    tree = parser.parse(code)

    ast = transformer.transform(tree)

    return ast