from sly import Lexer, Parser
import pandas as pd


class PromSqlLexer(Lexer):

    tokens = {
        NUMBER,
        STRING,
        ADD,
        SUB,
        MULT,
        DIV,
        MOD,
        POW,
        AND,
        OR,
        UNLESS,
        EQ,
        DEQ,
        NE,
        GT,
        LT,
        GE,
        LE,
        RE,
        NRE,
        BY,
        WITHOUT,
        ON,
        IGNORING,
        GROUP_LEFT,
        GROUP_RIGHT,
        OFFSET,
        BOOL,
        AGGREGATION_OPERATOR,
        FUNCTION,
        LEFT_BRACE,
        RIGHT_BRACE,
        LEFT_PAREN,
        RIGHT_PAREN,
        # LEFT_BRACKET,
        # RIGHT_BRACKET,
        COMMA,
        # COLON,
        TIME_RANGE,
        DURATION,
        METRIC_NAME,
        LABEL_NAME,
    }

    TIME_RANGE = r"\[\d+(s|m|h|d|w|y)\]|\[\d+(s|m|h|d|w|y):(\d+(s|m|h|d|w|y))?\]"

    DURATION = r"\d+(s|m|h|d|w|y)"

    NUMBER = r"\d+(\.\d+)?"

    STRING = r'\'([^\'\\]|\\.)*\'|"([^"\\]|\\.)*"'

    # Binary operators

    ADD = r"\+"
    SUB = r"-"
    MULT = r"\*"
    DIV = r"/"
    MOD = r"%"
    POW = r"\^"

    AND = r"and"
    OR = r"or"
    UNLESS = r"unless"

    # Comparison operators

    DEQ = r"=="
    NE = r"!="
    GE = r">="
    LE = r"<="
    RE = r"=~"
    NRE = r"!~"
    GT = r">"
    LT = r"<"
    EQ = r"="

    # Aggregation modifiers

    BY = r"by"
    WITHOUT = r"without"

    # Join modifiers

    ON = r"on"
    IGNORING = r"ignoring"
    GROUP_LEFT = r"group_left"
    GROUP_RIGHT = r"group_right"

    OFFSET = r"offset"

    BOOL = r"bool"

    FUNCTION = (
        r"absent_over_time|absent|abs|ceil"
        r"|changes|clamp_max|clamp_min|day_of_month"
        r"|day_of_week|days_in_month|delta|deriv"
        r"|exp|floor|histogram_quantile|holt_winters"
        r"|hour|idelta|increase|irate|label_join"
        r"|label_replace|ln|log2|log10|minute"
        r"|month|predict_linear|rate|resets"
        r"|round|scalar|sort|sort_desc|sqrt"
        r"|time|timestamp|vector|year|avg_over_time"
        r"|min_over_time|max_over_time|sum_over_time"
        r"|count_over_time|quantile_over_time"
        r"|stddev_over_time|stdvar_over_time"
    )

    AGGREGATION_OPERATOR = (
        r"sum|min|max|avg"
        r"|group|stddev|stdvar"
        r"|count_values|count"
        r"|bottomk|topk|quantile"
    )

    LEFT_BRACE = r"{"
    RIGHT_BRACE = r"}"

    LEFT_PAREN = r"\("
    RIGHT_PAREN = r"\)"

    # LEFT_BRACKET = r"\["
    # RIGHT_BRACKET = r"\]"

    METRIC_NAME = r"[a-zA-Z_:][a-zA-Z0-9_:]*"
    LABEL_NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"

    COMMA = r","
    # COLON = r":"

    ignore = " \t\n"

    def NUMBER(self, t):
        t.value = float(t.value)  # Convert to a numeric value
        return t

    def STRING(self, t):
        t.value = str(t.value)  # Convert to a numeric value
        return t

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)


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


class PromSqlParser(Parser):
    debugfile = "parser.out"
    # Get the token list from the lexer (required)
    tokens = PromSqlLexer.tokens
    start = "vectorOperation"

    # precedence = (
    #     ("left", OR),
    #     ("left", AND, UNLESS),
    #     ("left", LE, GE, LT, NE, DEQ, NRE, GT, EQ),
    #     ("left", ADD, SUB),
    #     ("left", MULT, DIV, MOD),
    #     ("right", POW),
    # )

    @_("unaryOp vectorOperation")
    def vectorOperation(self, p):
        unaryop = p[0]
        unaryop.expr = p[1]
        return unaryop

    @_("vectorOperation compareOp vectorOperation")
    @_("vectorOperation arithmeticOp vectorOperation")
    @_("vectorOperation andUnlessOp vectorOperation")
    @_("vectorOperation orOp vectorOperation")
    def vectorOperation(self, p):
        binop = p[1]
        binop.left_expr = p[0]
        binop.right_expr = p[2]
        return binop

    @_("vector")
    def vectorOperation(self, p):
        return p[0]

    # Operators

    @_("ADD")
    @_("SUB")
    def unaryOp(self, p):
        return UnaryOp(op=p[0])

    @_("POW grouping")
    @_("MULT grouping")
    @_("DIV grouping")
    @_("MOD grouping")
    @_("ADD grouping")
    @_("SUB grouping")
    def arithmeticOp(self, p):
        binop = p[1]
        binop.op = p[0]
        return binop

    @_("POW")
    @_("MULT")
    @_("DIV")
    @_("MOD")
    @_("ADD")
    @_("SUB")
    def arithmeticOp(self, p):
        return BinOp(op=p[0])

    @_("DEQ BOOL grouping")
    @_("NE BOOL grouping")
    @_("GT BOOL grouping")
    @_("LT BOOL grouping")
    @_("GE BOOL grouping")
    @_("LE BOOL grouping")
    def compareOp(self, p):
        binop = p[2]
        binop.op = p[0]
        binop.has_bool = True
        return binop

    @_("DEQ grouping")
    @_("NE grouping")
    @_("GT grouping")
    @_("LT grouping")
    @_("GE grouping")
    @_("LE grouping")
    def compareOp(self, p):
        binop = p[1]
        binop.op = p[0]
        return binop
    
    @_("DEQ BOOL")
    @_("NE BOOL")
    @_("GT BOOL")
    @_("LT BOOL")
    @_("GE BOOL")
    @_("LE BOOL")
    def compareOp(self, p):
        return BinOp(op=p[0], has_bool=True)

    @_("DEQ")
    @_("NE")
    @_("GT")
    @_("LT")
    @_("GE")
    @_("LE")
    def compareOp(self, p):
        return BinOp(op=p[0])

    @_("AND grouping")
    @_("UNLESS grouping")
    def andUnlessOp(self, p):
        binop = p[1]
        binop.op = p[0]
        return binop

    @_("AND")
    @_("UNLESS")
    def andUnlessOp(self, p):
        return BinOp(op=p[0])

    @_("OR grouping")
    def orOp(self, p):
        binop = p[1]
        binop.op = p[0]
        return binop

    @_("OR")
    def orOp(self, p):
        return BinOp(op=p[0])

    @_("function")
    @_("aggregation")
    @_("instantSelector")
    @_("matrixSelector")
    @_("offset")
    @_("literal")
    @_("parens")
    def vector(self, p):
        return p[0]

    @_("LEFT_PAREN vectorOperation RIGHT_PAREN")
    def parens(self, p):
        return p[1]

    # Selectors

    @_("METRIC_NAME LEFT_BRACE labelMatcherList RIGHT_BRACE")
    def instantSelector(self, p):
        return Metric(p[0], tags=p.labelMatcherList)

    @_("METRIC_NAME LEFT_BRACE RIGHT_BRACE")
    @_("METRIC_NAME")
    def instantSelector(self, p):
        return Metric(p[0])

    @_("LEFT_BRACE labelMatcherList RIGHT_BRACE")
    def instantSelector(self, p):
        return Metric(tags=p.labelMatcherList)

    @_("labelName EQ STRING")
    @_("labelName NE STRING")
    @_("labelName RE STRING")
    @_("labelName NRE STRING")
    def labelMatcher(self, p):
        return Tag(name=p[0], op=p[1], value=p[2])

    @_("labelMatcher COMMA labelMatcherList")
    def labelMatcherList(self, p):
        tag_list = p[2]
        tag_list.tags.append(p[0])
        return tag_list

    @_("labelMatcher")
    def labelMatcherList(self, p):
        return TagList([p[0]])

    @_("instantSelector TIME_RANGE")
    def matrixSelector(self, p):
        metric = p[0]
        metric.time_range = TimeRange(*p[1].split(":"))
        return metric

    @_("instantSelector OFFSET DURATION")
    @_("matrixSelector OFFSET DURATION")
    def offset(self, p):
        metric = p[0]
        metric.offset = p[2]
        return metric

    # @_("LEFT_BRACKET DURATION COLON DURATION RIGHT_BRACKET")
    # def time_range(self, p):
    #     return TimeRange(p[1], p[3])

    # @_("LEFT_BRACKET DURATION COLON RIGHT_BRACKET")
    # def time_range(self, p):
    #     return TimeRange(p[1])

    # @_("LEFT_BRACKET DURATION RIGHT_BRACKET")
    # def time_range(self, p):
    #     return TimeRange(p[1])

    # Functions

    @_("FUNCTION parameterList")
    def function(self, p):
        return Function(p[0], p[1])

    @_("literal")
    @_("vectorOperation")
    def parameter(self, p):
        return Parameter(value=p[0])

    @_("parameter COMMA parameterList2")
    def parameterList2(self, p):
        return [p[0]] + p[2]

    @_("parameter")
    def parameterList2(self, p):
        return [p[0]]

    @_("LEFT_PAREN parameterList2 RIGHT_PAREN")
    def parameterList(self, p):
        return ParameterList(p[1])

    # Aggregations

    @_("AGGREGATION_OPERATOR parameterList")
    def aggregation(self, p):
        return AggOp(name=p[0], params=p[1])

    @_("AGGREGATION_OPERATOR BY labelNameList parameterList")
    @_("AGGREGATION_OPERATOR WITHOUT labelNameList parameterList")
    def aggregation(self, p):
        params = ParameterList(p[3].parameters[:-1])
        expr = p[3].parameters[-1].value
        return AggOp(
            name=p[0],
            filter_method=p[1],
            label_name_list=p[2],
            params=params,
            expr=expr,
        )
        return AggOp(name=p[0], filter_method=p[1], label_name_list=p[2], params=p[3])

    @_("AGGREGATION_OPERATOR parameterList BY labelNameList")
    @_("AGGREGATION_OPERATOR parameterList WITHOUT labelNameList")
    def aggregation(self, p):
        params = ParameterList(p[1].parameters[:-1])
        expr = p[1].parameters[-1].value
        return AggOp(
            name=p[0],
            filter_method=p[2],
            label_name_list=p[3],
            params=params,
            expr=expr,
        )

    @_("on groupLeft")
    @_("on groupRight")
    @_("ignoring groupLeft")
    @_("ignoring groupRight")
    def grouping(self, p):
        return BinOp(
            filter_method=p[0][0],
            filter_label_list=p[0][1],
            group_side=p[1][0],
            group_label_list=p[1][1],
        )

    @_("on")
    @_("ignoring")
    def grouping(self, p):
        return BinOp(filter_method=p[0][0], filter_label_list=p[0][1])

    @_("ON labelNameList")
    def on(self, p):
        return "ON", p[1]

    @_("IGNORING labelNameList")
    def ignoring(self, p):
        return "IGNORING", p[1]

    @_("GROUP_LEFT labelNameList")
    def groupLeft(self, p):
        return "GROUP_LEFT", p[1]

    @_("GROUP_RIGHT labelNameList")
    def groupRight(self, p):
        return "GROUP_RIGHT", p[1]

    # Label names

    @_("keyword")
    @_("METRIC_NAME")
    @_("LABEL_NAME")
    def labelName(self, p):
        return p[0]

    @_("labelName COMMA labelNameList2")
    def labelNameList2(self, p):
        return [p.labelName] + p.labelNameList2

    @_("labelName")
    def labelNameList2(self, p):
        return [p[0]]

    @_("LEFT_PAREN labelNameList2 RIGHT_PAREN")
    def labelNameList(self, p):
        return p.labelNameList2

    @_("AND")
    @_("OR")
    @_("UNLESS")
    @_("BY")
    @_("WITHOUT")
    @_("ON")
    @_("IGNORING")
    @_("GROUP_LEFT")
    @_("GROUP_RIGHT")
    @_("OFFSET")
    @_("BOOL")
    @_("AGGREGATION_OPERATOR")
    @_("FUNCTION")
    def keyword(self, p):
        return p[0]

    @_("NUMBER")
    @_("STRING")
    def literal(self, p):
        return p[0]


if __name__ == "__main__":
    lexer = PromSqlLexer()
    parser = PromSqlParser()
    query = """
    max without (revision) 
    (
        kube_statefulset_status_current_revision{job="kube-state-metrics"}
            unless
        kube_statefulset_status_update_revision{job="kube-state-metrics"}
    )
    *
    (
        kube_statefulset_replicas{job="kube-state-metrics"}
            !=
        kube_statefulset_status_replicas_updated{job="kube-state-metrics"}
    )
    """
    while True:
        try:
            text = input("calc > ")
            result = parser.parse(lexer.tokenize(query))
            print(result)
            # for tok in lexer.tokenize(text):
            # print("type=%r, value=%r" % (tok.type, tok.value))
        except EOFError:
            break