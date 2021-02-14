#!/usr/bin/env python

from promsql import *

if __name__ == "__main__":
    parser = PromSqlParser()
    transformer = PromSqlTransformer()
    while True:
        try:
            text = input("promsql > ")
            tree = parser.parse(text)
            print(transformer.transform(tree))
        except EOFError:
            break
