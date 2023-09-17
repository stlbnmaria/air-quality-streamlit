from typing_extensions import Final
from typing import Tuple

_DEFAULT_ZOOM_LEVEL: Final = 12
_ZOOM_LEVELS: Final = [
    360,
    180,
    90,
    45,
    22.5,
    11.25,
    5.625,
    2.813,
    1.406,
    0.703,
    0.352,
    0.176,
    0.088,
    0.044,
    0.022,
    0.011,
    0.005,
    0.003,
    0.001,
    0.0005,
    0.00025,
]


def _get_zoom_level(distance: float) -> int:
    """Get the zoom level for a given distance in degrees.
    Function from https://github.com/streamlit/streamlit/blob/develop/lib/streamlit/elements/map.py#L443

    See https://wiki.openstreetmap.org/wiki/Zoom_levels for reference.

    Parameters
    ----------
    distance : float
        How many degrees of longitude should fit in the map.

    Returns
    -------
    int
        The zoom level, from 0 to 20.

    """
    for i in range(len(_ZOOM_LEVELS) - 1):
        if _ZOOM_LEVELS[i + 1] < distance <= _ZOOM_LEVELS[i]:
            return i

    # For small number of points the default zoom level will be used.
    return _DEFAULT_ZOOM_LEVEL


def _get_viewport_details(
    data: str, lat_col_name: str, lon_col_name: str, zoom: float = None
) -> Tuple[float]:
    """Auto-set viewport when not fully specified by user.

    Function from https://github.com/streamlit/streamlit/blob/develop/lib/streamlit/elements/map.py#L443
    """
    min_lat = data[lat_col_name].min()
    max_lat = data[lat_col_name].max()
    min_lon = data[lon_col_name].min()
    max_lon = data[lon_col_name].max()
    center_lat = (max_lat + min_lat) / 2.0
    center_lon = (max_lon + min_lon) / 2.0
    range_lon = abs(max_lon - min_lon)
    range_lat = abs(max_lat - min_lat)

    if zoom is None:
        if range_lon > range_lat:
            longitude_distance = range_lon
        else:
            longitude_distance = range_lat
        zoom = _get_zoom_level(longitude_distance)

    return zoom, center_lat, center_lon
