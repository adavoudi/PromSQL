#!/usr/bin/env python

from promsql.lexer import PromSqlLexer
from promsql.parser import PromSqlParser

if __name__ == "__main__":
    lexer = PromSqlLexer()
    parser = PromSqlParser()
    while True:
        try:
            text = input("promsql > ")
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break
