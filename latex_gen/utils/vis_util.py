from .others_util import convert
import numpy as np

def is_outlier(points, thresh=3.5):
    """
    Returns a boolean array with True if points are outliers and False
    otherwise.

    Parameters:
    -----------
        points : An numobservations by numdimensions array of observations
        thresh : The modified z-score to use as a threshold. Observations with
            a modified z-score (based on the median absolute deviation) greater
            than this value will be classified as outliers.

    Returns:
    --------
        mask : A numobservations-length boolean array.

    References:
    ----------
        Boris Iglewicz and David Hoaglin (1993), "Volume 16: How to Detect and
        Handle Outliers", The ASQC Basic References in Quality Control:
        Statistical Techniques, Edward F. Mykytka, Ph.D., Editor.

        This function was taken from:
            https://stackoverflow.com/a/11886564
    """
    # Sanity check
    points = convert(points, np.asarray, np.ndarray)

    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh


def _filter_outliers(points, thresh=3.5):
    # Sanity check
    points = convert(points, np.asarray, np.ndarray)
    return points[~is_outlier(points, thresh)]


def filter_outliers(*points, thresh=3.5, mode="all"):
    """Function to filter outliers given a number of arrays.

    Parameters
    ----------
    *points : tuple
        `*args` that can contains multiple points of different arrays.
    thresh : type
        The modified z-score to use as a threshold. Observations with
        a modified z-score (based on the median absolute deviation) greater
        than this value will be classified as outliers.
    mode : 'all' or 'first' or 'last'
        `all`: each collection of datapoints will be filtered with its mask.
        `first`: only use mask of the first collection of points.
        `last`: only use mask of the last collection of points.

    Returns
    -------
    tuple
        A tuple containing all filtered ndarrays.

    """
    if mode == "all":
        return (_filter_outliers(point, thresh=thresh) for point in points)
    elif mode == "first":
        mask = is_outlier(points[0], thresh=thresh)
        return (point[~mask] for point in points)
    elif mode == "last":
        mask = is_outlier(points[-1], thresh=thresh)
        return (point[~mask] for point in points)
    else:
        raise ValueError("Invalid `mode` value. Expected: `all` or `first`"
                         " or `last`. Got {} instead".format(mode))
