"""
This module contains the functions to find carpooling opportunities.

The main function is calculate_carpooling, which receives a list of trips
and returns a list of carpooling opportunities.

A documented version of this module can be found at: study.ipynb
"""
import numpy as np
import pandas as pd

from datetime import datetime as dt, date
from scipy.spatial import cKDTree
from shapely import wkt
from utils.converter import meters2degrees


MAX_NEIGHBORS_DISTANCE = 5000   # in meters
MAX_TIME_DIFFERENCE = 120       # in minutes
MAX_NEIGHBORS_DEGREES = meters2degrees(MAX_NEIGHBORS_DISTANCE)


def calculate_carpooling(trips):
    """Calculate carpooling opportunities.

    Arguments
    ---------
    trips: list
        List of lists following the format:
        [
            [
                id (int),
                region (string),
                origin_x (int),
                origin_y (int),
                destination_x (int),
                destination_y (int),
                datetime (string),
                datasource (string)
            ],
            ...
        ]

    Returns
    -------
    carpooling: tuple of FrozenSets-
        List of carpooling opportunities following the format:
        (
            {trip1_id: int, trip2_id: int, ...},
            ...
        )
    """
    trips = make_dataframe(trips)
    trips = ckdnearest(trips, 'origin')
    trips = ckdnearest(trips, 'destination')
    trips = cotemporals(trips, 'datetime')
    trips['similar_trips'] = trips.apply(get_similar_trips, axis=1)
    similar_trips = trips.dropna()
    result = similar_trips.similar_trips.unique()
    result = fix_ids(result, trips)
    return result


def make_dataframe(trips: list):
    """Make a dataframe from a list of trips.
    """
    columns = [
        'id', 'region', 'origin_x', 'origin_y',
        'destination_x', 'destination_y',
        'datetime', 'datasource'
    ]
    trips = pd.DataFrame(trips, columns=columns)
    trips['datetime'] = trips['datetime'].apply(
        lambda x: dt.combine(date.today(), x.time())
    )
    trips.drop(['datasource'], axis=1, inplace=True)
    return trips

# Based on https://gis.stackexchange.com/questions/222315/finding-nearest-point-in-other-geodataframe-using-geopandas


def ckdnearest(
    df: pd.DataFrame,
    column: str,
    distance: float = MAX_NEIGHBORS_DEGREES
):
    """Find points that are less than the indicated distance from each point in
    the indicated column.

    Argument
    ---------
    df: pd.DataFrame
        A pandas DataFrame with at least two columns of
        coordinates
    column: str
        The columns prefix of the df used for search the nearest points. The df
        must have two columns named {column}_x and {column}_y, both of them
        must be float.
    distance: float (optional)
        The maximum distance a point can be to be considered a neighbor. The
        default value is MAX_NEIGHBORS_DEGREES.

    Returns
    -------
    df_nearest: pd.DataFrame
        A pandas DataFrame with the same columns as the input df, plus a column
        with the nearest points named {column}_neighbors.
    """
    x_column, y_column = f'{column}_x', f'{column}_y'
    coords = np.array(list(zip(df[x_column], df[y_column])))
    btree = cKDTree(coords)
    # Find the nearest points
    idx = btree.query_ball_tree(btree, r=distance)
    for i, neighbors in enumerate(idx, start=0):
        neighbors.remove(i)
    df_nearest = pd.concat(
        [
            df,
            pd.Series(idx, name=f'{column}_neighbors')
        ],
        axis=1)
    return df_nearest


def cotemporals(df: pd.DataFrame, column: str, time: int = MAX_TIME_DIFFERENCE):
    """Find points that are less than the indicated time difference from each
    point in the indicated column.

    Argument
    ---------
    df: pd.DataFrame
        A pandas DataFrame with at least one column of datetimes.
    column: str
        The column of the df used for search the cotemporal trips. Elements in
        this columns must be datetime.datetime.
    time: int (optional)
        The maximum time difference a point can be to be considered a neighbor.
        The default value is MAX_TIME_DIFFERENCE.

    Returns
    -------
    df_nearest: pd.DataFrame
        A pandas DataFrame with the same columns as the input df, plus a column
        with the nearest points named {column}_neighbors.
    """
    delta = pd.Timedelta(time, unit='m')

    def get_neighbors(x):
        return df[
            (
                (
                    (df[column] >= x[column]) &
                    (df[column] <= x[column] + delta)
                ) | (
                    (df[column] <= x[column]) &
                    (df[column] >= x[column] - delta)
                )
            ) & (df.index != x.name)
        ].index.to_list()
    df_nearest = pd.concat(
        [
            df,
            pd.Series(
                df.apply(get_neighbors, axis=1),
                name=f'{column}_neighbors'
            )
        ],
        axis=1
    )
    return df_nearest


def get_similar_trips(trip):
    """Get similar trips to the indicated trip. Similar trips are trips that
    have the same origin and destination coordinates and are cotemporals.
    """
    origin_neighbors = set(trip.origin_neighbors)
    destination_neighbors = set(trip.destination_neighbors)
    time_neighbors = set(trip.datetime_neighbors)
    similar_trips = origin_neighbors & destination_neighbors & time_neighbors
    frozen_similar_trips = frozenset(similar_trips.union({trip.name}))
    return frozen_similar_trips if similar_trips else np.nan


def fix_ids(result: list, df: pd.DataFrame):
    """Fix the ids of the trips in the list. The ids are the ids of the
    original trips, not the ids of the trips in the dataframe.
    """
    def fix_group(group): return frozenset(df.loc[group].id)
    return tuple(map(fix_group, result))
