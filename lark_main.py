from lark import Lark
from lark import Transformer
from nodes import *

grammar = open("promsql.lark", "r").read()


def get_vector_name(metric_name, label_matchers):
    if "__name__" in label_matchers:
        metric_name = metric_name or label_matchers["__name__"]["value"]
        del label_matchers["__name__"]
    return metric_name, label_matchers


def duration_literal_to_seconds(duration_literal: str) -> int:
    """Converts duration literal string to number of seconds

    Args:
        duration_literal (str): input string

    Raises:
        InvalidParameterError: when the unit is not one of `s|m|h|d|w`

    Returns:
        int: number of seconds
    """
    num = int(duration_literal[:-1])
    unit = duration_literal[-1]
    if unit == "s":
        seconds = num
    elif unit == "m":
        seconds = num * 60
    elif unit == "h":
        seconds = num * 60 * 60
    elif unit == "d":
        seconds = num * 60 * 60 * 24
    elif unit == "w":
        seconds = num * 60 * 60 * 24 * 7
    return seconds


class MyTransformer(Transformer):
    def start(self, items):
        if len(items) == 0:
            return "no expression found in input"
        return items[0]

    def expr(self, items):
        return items[0]

    def aggregate_expr(self, items):
        result = AggregateExpr(items[0])
        if len(items) == 3:
            if isinstance(items[1], AggregateModifier):
                result.aggregate_modifier = items[1]
                result.function_call_body = items[2]
            else:
                result.aggregate_modifier = items[2]
                result.function_call_body = items[1]
        else:
            result.function_call_body = items[1]
        return result

    def aggregate_modifier(self, items):
        result = AggregateModifier(grouping=items[1])
        if items[0] == "without":
            result.without = True
        else:
            result.without = False
        return result

    def binary_expr(self, items):
        result = BinaryExpression(
            op=items[1], left_expr=items[0], right_expr=items[3], bin_modifier=items[2]
        )
        return result

    def bin_modifier(self, items):
        return items[0]

    def bool_modifier(self, items):
        result = BinaryExpr(vector_matching=VectorMatching(card="OneToOne"))
        if len(items) == 1:
            result.return_bool = True
        return result

    def on_or_ignoring(self, items):
        result = items[0]
        result.vector_matching.matching_labels = items[2]
        if items[1] == "on":
            result.vector_matching.on = True
        return result

    def group_modifiers(self, items):
        result = items[0]
        if len(items) == 3:
            result.vector_matching.include = items[2]
            if items[1] == "group_right":
                result.vector_matching.card = "OneToMany"
            else:
                result.vector_matching.card = "ManyToOne"
        return result

    def grouping_labels(self, items):
        if len(items) == 2:
            return []
        else:
            return items[1]

    def grouping_label_list(self, items):
        result = items[0]
        if len(items) == 3:
            result.append(items[2])
        else:
            result = [result]
        return result

    def grouping_label(self, items):
        return items[0]

    def function_call(self, items):
        # TODO: Check if the function exists
        result = Function(name=str(items[0]), args=items[1])
        return result

    def function_call_body(self, items):
        if len(items) == 3:
            return items[1]
        return []

    def function_call_args(self, items):
        result = items[0]
        if len(items) == 3:
            result.append(items[2])
        elif len(items) == 1:
            result = [result]
        return result

    def paren_expr(self, items):
        return items[1]

    def offset_expr(self, items):
        result = items[0]
        result.offset = items[2]
        return result

    def matrix_selector(self, items):
        result = MatrixSelector(vector_selector=items[0], _range=items[2])
        return result

    def subquery_expr(self, items):
        result = SubqueryExpr(expr=items[0], _range=items[2], step=items[4])
        return result

    def unary_expr(self, items):
        result = UnaryExpr(op=items[0], expr=items[1])
        return result

    def vector_selector(self, items):
        if len(items) == 2:
            result = items[1]
            metric_name, label_matchers = get_vector_name(
                items[0], result.label_matchers
            )
            result.name = metric_name
            result.label_matchers = label_matchers
        elif isinstance(items[0], dict):
            result = items[0]
            metric_name, label_matchers = get_vector_name(None, result.label_matchers)
            if metric_name is None:
                raise Exception("Metric name is None!")
            result.name = metric_name
            result.label_matchers = label_matchers
        else:
            result = VectorSelector(name=items[0])
        return result

    def label_matchers(self, items):
        result = VectorSelector()
        if len(items) >= 3:
            result.label_matchers = items[1]
        return result

    def label_match_list(self, items):
        result = items[0]
        if len(items) == 3:
            result.update(items[2])
        return result

    def label_matcher(self, items):
        return {str(items[0]): {"value": str(items[2]), "op": str(items[1])}}

    def metric(self, items):
        if len(items) == 2:
            result = items[1]
            result.update({"__name__": items[0]})
        else:
            result = items[0]
        metric_name, label_matchers = get_vector_name(None, result)
        if metric_name is None:
            raise Exception("Metric name is None!")
        result = VectorSelector(name=metric_name, label_matchers=label_matchers)
        return result

    def metric_identifier(self, items):
        return str(items[0])

    def label_set(self, items):
        if len(items) >= 3:
            return items[1]
        return {}

    def label_set_list(self, items):
        result = items[0]
        if len(items) == 3:
            result.update(items[2])
        return result

    def label_set_item(self, items):
        return {str(items[0]):{"value": str(items[2]), "op": "="}}

    def series_description(self, items):
        return SeriesDescription(labels=items[0], values=items[1])

    def series_values(self, items):
        if len(items) == 0:
            return []
        result = items[0]
        if len(items) == 3:
            result.append(items[2])
        return result

    def series_item(self, items):
        if len(items) == 1 and items[0] == "_":
            return SequenceValue(omitted=True)
        if len(items) == 3 and items[0] == "_":
            result = []
            for _ in range(items[2]):
                result.append(SequenceValue(omitted=True))
        elif len(items) == 0:
            result = [SequenceValue(value=items[0])]
        elif len(items) == 3:
            result = []
            for _ in range(items[2]):
                result.append(SequenceValue(value=items[0]))
        else:
            result = []
            value = items[0]
            for _ in range(items[3]):
                result.append(SequenceValue(value=value))
                value += items[1]
        return result

    def series_value(self, items):
        # TODO: Should convert binary string to number here
        return items[0]

    def aggregate_op(self, items):
        return items[0]

    def maybe_label(self, items):
        return str(items[0])

    def unary_op(self, items):
        return items[0]

    def match_op(self, items):
        return items[0]

    def number_literal(self, items):
        return float(items[0])

    def number(self, items):
        return float(items[0])

    def signed_number(self, items):
        if items[0] == "-":
            return -1 * items[1]
        return items[1]

    def uint(self, items):
        return int(items[0])

    def duration(self, items):
        return duration_literal_to_seconds(str(items[0]))

    def string_literal(self, items):
        return items[0][1:-1]

    def maybe_duration(self, items):
        if len(items) == 0:
            return 0
        return items[0]

    def maybe_grouping_labels(self, items):
        if len(items) == 0:
            return None
        return items[0]


parser = Lark(grammar, start="start", parser="earley")

text = "container_cpu_usage_seconds_total * on(pod) group_left(node) kube_pod_info"

tree = parser.parse(text)
print(MyTransformer().transform(tree))

# print(TreeToJson().transform(tree))
