import pandas as pd


def list_to_str(input_list):
    return ",".join([str(item) for item in input_list])


class ExecutableExpr:
    def eval(self):
        raise NotImplementedError()


class AggregateExpr(ExecutableExpr):
    def __init__(
        self, aggregate_op=None, aggregate_modifier=None, function_call_body=None
    ):
        self.aggregate_op = aggregate_op
        self.aggregate_modifier = aggregate_modifier
        self.function_call_body = function_call_body

    def __str__(self):
        return f"AggregateExpr({self.aggregate_op}, {self.aggregate_modifier}, {list_to_str(self.function_call_body)})"

    def eval(self):
        pass


class AggregateModifier:
    def __init__(self, grouping=None, without=None):
        self.grouping = grouping
        self.without = without

    def __str__(self):
        return f"AggregateModifier({self.grouping}, {self.without})"


class BinaryExpression(ExecutableExpr):
    def __init__(self, op=None, left_expr=None, right_expr=None, bin_modifier=None):
        self.op = op
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.bin_modifier = bin_modifier

    def __str__(self):
        return f"BinaryExpression({self.op}, {self.left_expr}, {self.right_expr}, {self.bin_modifier})"

    def eval(self):
        pass


class BinaryExpr:
    def __init__(self, vector_matching=None, return_bool=False):
        self.vector_matching = vector_matching
        self.return_bool = return_bool

    def __str__(self):
        return f"BinaryExpr({self.vector_matching}, {self.return_bool})"


class VectorMatching:
    def __init__(self, card=None, matching_labels=None, on=False, include=None):
        self.card = card
        self.matching_labels = matching_labels
        self.on = on
        self.include = include

    def __str__(self):
        return f"VectorMatching({self.card}, {self.matching_labels}, {self.on}, {self.include})"


class Function(ExecutableExpr):
    def __init__(self, name=None, args=None):
        self.name = name
        self.args = args

    def __str__(self):
        return f"Function({self.name}, [{list_to_str(self.args)}])"

    def eval(self):
        pass


class MatrixSelector(ExecutableExpr):
    def __init__(self, vector_selector=None, _range=None, offset=0):
        self.vector_selector = vector_selector
        self.range = _range
        self.offset = offset

    def __str__(self):
        return f"MatrixSelector({self.vector_selector}, {self.range}, {self.offset})"

    def eval(self):
        pass


class SubqueryExpr(ExecutableExpr):
    def __init__(self, expr=None, _range=None, step=None, offset=0):
        self.expr = expr
        self.range = _range
        self.step = step
        self.offset = offset

    def __str__(self):
        return f"SubqueryExpr({self.expr}, {self.range}, {self.step}, {self.offset})"

    def eval(self):
        pass


class UnaryExpr(ExecutableExpr):
    def __init__(self, op=None, expr=None):
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"UnaryExpr({self.op}, {self.expr})"

    def eval(self):
        pass


class VectorSelector(ExecutableExpr):
    def __init__(self, name=None, label_matchers={}, offset=0):
        self.name = name
        self.label_matchers = label_matchers
        self.offset = offset

    def __str__(self):
        return f"VectorSelector({self.name}, {self.label_matchers}, {self.offset})"

    def eval(self):
        print("hey")


class SeriesDescription:
    def __init__(self, labels=None, values=None):
        self.labels = labels
        self.values = values

    def __str__(self):
        return f"SeriesDescription({self.labels}, {self.values})"


class SequenceValue:
    def __init__(self, value=None, omitted=False):
        self.value = value
        self.omitted = omitted

    def __str__(self):
        return f"SequenceValue({self.value}, {self.omitted})"


class TimeRange:
    def __init__(self, start_time=None, end_time=None):
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        return f"TimeRange({self.start_time}, {self.end_time})"
