from typing import Dict, List, Tuple, Union
import numpy as np
import data_request

class GridGeometry2D:
    """
    The grid geometry class is used to represent the 2D grid dimensions
and cell size.
    """
    def __init__(self, rows: int, cols: int, dx: float, dy: float):
        self.rows = rows
        self.cols = cols
        self.dx = dx
        self.dy = dy

class Unit:
    """
    The unit class is used to represent the units for data values.
    """
    def __init__(self, name: str):
        self.name = name

class IGridData(IGridDataMixin):
    """
    Base interface for grid-based environmental and geographic data.
    """
    def get_grid_geometry(self) -> GridGeometry2D:
        """Returns the grid geometry representing row, column dimensions
and cell size."""

    @property
    def unit(self) -> Union[Unit, None]:
        """Returns the unit for the data values, or None if no unit is
available."""

    def get_parameter(self) -> str:
        """Returns the parameter name associated with this grid."""

    # Methods to populate raw data in different ways based on user preference.
    def get_raw_data(self) -> np.ndarray:
        """Returns a numpy array containing the raw data for this grid."""

    def populate_data(self, destination: DataDestination) -> None:
        """Populates the raw data to a specific data destination based on
user preference."""

    def populate_data(self, destination: DataDestination, unit: Unit =None) -> None:
        """Populates the raw data to a specific data destination and
converts it to a specified unit if provided."""

class IData(IGridData):
    """
    Interface for environmental and geographic data that can be requested
through `IDataRequest`.
    """

    @property
    def datatype(self) -> str:
        """Returns the datatype of this grid, e.g., 'Float32' or
'Int16'."""

class DataDestination:
    """
    Base interface for data destinations used to populate raw grid data
into memory.
    """
    def __init__(self):
        pass

    # Methods to convert raw data into native data type and structure ofthe user application.
    def wrap_raw_data(self, raw_data: np.ndarray) -> np.ndarray:
        """Wraps the raw grid data into a native format for this
application."""

    @property
    def datatype(self) -> str:
        """Returns the native datatype of data stored in this
destination."""