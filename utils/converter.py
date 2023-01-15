import numpy as np


HEART_RATE = 6371.009 * 1000    # Earth radius in meters


def degrees2meters(degrees: float):
    """Calculate the approximate meters to which a certain variation of degrees
    on Earth is equivalent. The planet is assumed to be a perfect sphere of
    radius 6371.009 km.

    Arguments
    ---------
    degrees: float
        The variation of degrees to be converted.

    Returns
    -------
    meters: float
        The equivalent variation of meters.
    """
    return 2 * np.pi * HEART_RATE * degrees / 360


def meters2degrees(meters: float):
    """Calculate the approximate degrees to which a certain variation of meters
    on Earth is equivalent. The planet is assumed to be a perfect sphere of
    radius 6371.009 km.

    Arguments
    ---------
    meters: float
        The variation of meters to be converted.

    Returns
    -------
    degrees: float
        The equivalent variation of degrees.
    """
    return 360 * meters / (2 * np.pi * HEART_RATE)
