import os
from pathlib import Path
from lark import Lark


class PromSqlParser(Lark):
    def __init__(self, **kwargs):
        current_dir = Path(__file__).parent.absolute()
        grammar = open(os.path.join(current_dir, "promsql.lark"), "r").read()
        kwargs["start"] = "start"
        kwargs["parser"] = "earley"
        super().__init__(grammar, **kwargs)

