import datetime
from typing import List
import pandas as pd

from .constants import TIME_COL, VAL_COL, DEFAULT_INTERVAL


def find_tags(df: pd.DataFrame) -> List[str]:
    tags = set(df.columns) - set([VAL_COL, TIME_COL])
    return list(tags)


def resample(
    df: pd.DataFrame,
    interval: int = DEFAULT_INTERVAL,
    agg_type: str = "mean",
    start_datetime: datetime.datetime = None,
    end_datetime: datetime.datetime = None,
) -> pd.DataFrame:
    df = df.set_index(TIME_COL)
    if start_datetime is not None and start_datetime not in df.index:
        df.loc[start_datetime] = None
    if end_datetime is not None and end_datetime not in df.index:
        df.loc[end_datetime] = None

    df_resampled = df.groupby(find_tags(df))[VAL_COL].resample(f"{interval}S").agg(agg_type)
    interpolated = df_resampled.interpolate(method="linear")
    out_df = interpolated.reset_index()
    return out_df

