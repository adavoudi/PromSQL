#!/usr/bin/env python

from promsql import *
from lark.exceptions import UnexpectedEOF

if __name__ == "__main__":
    parser = PromSqlParser()
    transformer = PromSqlTransformer()
    while True:
        try:
            text = input("promsql > ")
            tree = parser.parse(text)
            print(transformer.transform(tree))
        except UnexpectedEOF as error:
            print(error)
