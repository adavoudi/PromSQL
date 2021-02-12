"""All AST nodes"""


class RangeVector:
    """
    Range vector literals work like instant vector literals, except that they select a range 
    of samples back from the current instant. Syntactically, a time duration is appended in 
    square brackets ([]) at the end of a vector selector to specify how far back in time values 
    should be fetched for each resulting range vector element.
    """
    def __init__(self, name=None, time_range=None, tags=None, offset=None):
        self.name = name
        self.time_range = time_range
        self.tags = tags
        self.offset = offset

    def __str__(self):
        return f"RangeVector: {self.name}, tags: {self.tags}, time_range: {self.time_range}, offset: {self.offset}"


class InstantVector:
    """
    Instant vector selectors allow the selection of a set of time series and a single sample value 
    for each at a given timestamp (instant): in the simplest form, only a metric name is specified. 
    This results in an instant vector containing elements for all time series that have this metric name.
    """
    def __init__(self, name=None, tags=None):
        self.name = name
        self.tags = tags

    def __str__(self):
        return f"InstantVector: {self.name}, tags: {self.tags}"


class Scalar:
    """
    Scalar float values can be written as literal integer or floating-point numbers
    """
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return f"Scalar: {self.value}"


class String:
    """
    Strings may be specified as literals in single quotes, double quotes or backticks.
    """
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return f"String: {self.value}"


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
    def __init__(self, op=None, expr=None):
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"UnaryOp: {self.op}, expr: {self.expr}"


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
