from lark import Lark
from lark import Transformer

grammar = open("promsql.lark", "r").read()

class MyTransformer(Transformer):
    def number_literal(self, items):
        return "ALIREZA"
    def pair(self, key_value):
        k, v = key_value
        return k, v
    def dict(self, items):
        return dict(items)


parser = Lark(grammar, start="start")

text = '((- a ^ 2 * b + c) > 1) and d or e'
tree = parser.parse(text)
print(MyTransformer().transform(tree).pretty())

# print(TreeToJson().transform(tree))
