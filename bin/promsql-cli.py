#!/usr/bin/env python

from promsql.lexer import PromSqlLexer
from promsql.parser import PromSqlParser


class Metric:
    def __init__(self, name=None, time_range=None, tags=None, offset=None):
        self.name = name
        self.time_range = time_range
        self.tags = tags

    def __str__(self):
        return f"Metric: {self.name}, tags: {self.tags}, time_range: {self.time_range}"


class Tag:
    def __init__(self, name=None, op=None, value=None):
        self.name = name
        self.op = op
        self.value = value

    def __str__(self):
        return f"Tag: {self.name} {self.op} {self.value}"


class TagList:
    def __init__(self, tags=None):
        self.tags = tags

    def __str__(self):
        return ", ".join([str(item) for item in self.tags])


class TimeRange:
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

    def __str__(self):
        return f"TimeRange: {self.start}, {self.end}"


class Function:
    def __init__(self, name=None, params=None):
        self.name = name
        self.params = params

    def __str__(self):
        return f"Function: {self.name}, params: {self.params}"


class AggOp:
    def __init__(
        self,
        name=None,
        filter_method=None,
        label_name_list=None,
        params=None,
        expr=None,
    ):
        self.name = name
        self.filter_method = filter_method
        self.label_name_list = label_name_list
        self.params = params
        self.expr = expr

    def __str__(self):
        return f"AggOp: {self.name}, filter_method: {self.filter_method}, label_name_list: {self.label_name_list}, expr: {self.expr}, params: {self.params}"


class BinOp:
    def __init__(
        self,
        op=None,
        left_expr=None,
        right_expr=None,
        filter_method=None,
        group_side=None,
        filter_label_list=None,
        group_label_list=None,
        has_bool=None,
    ):
        self.op = op
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.filter_method = filter_method
        self.group_side = group_side
        self.filter_label_list = filter_label_list
        self.group_label_list = group_label_list
        self.has_bool = has_bool

    def __str__(self):
        return f"BinOp: {self.op}, left: ({self.left_expr}), right: ({self.right_expr}), filter_method: {self.filter_method}, group_side: {self.group_side}, filter_label_list: {self.filter_label_list}, group_label_list: {self.group_label_list}, has_bool: {self.has_bool}"


class UnaryOp:
    def __init__(self, op: None, expr: None):
        self.op = op
        self.expr = expr


class Parameter:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return f"param: {self.value}"


class ParameterList:
    def __init__(self, parameters=None):
        self.parameters = parameters

    def __str__(self):
        return ", ".join([str(item) for item in self.parameters])


if __name__ == "__main__":
    lexer = PromSqlLexer()
    parser = PromSqlParser()
    while True:
        try:
            text = input("calc > ")
            result = parser.parse(lexer.tokenize(text))
            print(result)
            # for tok in lexer.tokenize(text):
            # print("type=%r, value=%r" % (tok.type, tok.value))
        except EOFError:
            break
