# Constant values

DEFAULT_CONFIGS = {
    "DB": "postgresql://admin:quest@localhost:8812",
    "LOOK_BEHIND_DURATION": 60 * 60,  # seconds (1 hour)
    "TABLE_NAME": "{metric_name}",
    "VALUE_COLUMN": "value",
    "TIMESTAMP_COLUMN": lambda params: "timestamp",
    # Columns to use as tag; can be a list of str, a regex or a function of params
    # if None, we will use all columns other than value_column and timestamp_column
    # as tags
    "TAG_COLUMNS": None,
}


CUSTOM_CONFIGS = []
# Sample Custom Configs
# CUSTOM_CONFIGS = [
#     # custom configs
#     # they will be checked in the defined order
#     {
#         # It can be a regex; in this case, we will check it against the metric_name
#         "check": r"[a-b]",
#         "configs": {
#             # can be partial configs
#             "DB_URL": "postgresql://admin:quest@localhost:8812"
#         },
#     },
#     {
#         # It can also be a function which takes params and return a boolean value.
#         # In this case, we will evaluate the function and use the configs if it returns True
#         "check": lambda params: True,
#         "configs": {
#             # can be partial configs
#             "TABLE_NAME": "{metric_name}",
#         },
#     },
# ]
