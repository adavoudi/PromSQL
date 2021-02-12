from sly import Lexer


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

