from sly import Parser
from .lexer import PromSqlLexer


class PromSqlParser(Parser):
    # Get the token list from the lexer (required)
    tokens = PromSqlLexer.tokens
    start = "vectorOperation"

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

