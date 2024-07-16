# interfaces.py

from typing import Dict, List, Tuple, Union
import numpy as np
from domain_models import GridGeometry2D, Unit
import sys
import warnings

class IDataRequest:
    def __init__(self):
        self._identifiers: Dict[str, object] = {}
        self._parameters: List[str] = []
        self._levels: Tuple[str, ...] = ()

    @property
    def datatype(self) -> str:
        """The datatype name and key to which factory will be used."""
        raise NotImplementedError

    def add_identifier(self, identifier: str, value: object) -> None:
        """An identifier the factory can use to determine which data to return."""
        self._identifiers[identifier] = value

    def set_parameters(self, *params: str) -> None:
        """Parameters passed to the data access component."""
        self._parameters = list(params)

    def set_levels(self, *levels: str) -> None:
        """Levels of the requested data."""
        self._levels = levels

    def get_datatype(self) -> str:
        """Return the datatype for this request."""
        return self.datatype

    def get_identifiers(self) -> Dict[str, object]:
        """Returns a dictionary containing all identifier-value pairs."""
        return self._identifiers

    def get_parameters(self) -> List[str]:
        """Returns a list of parameters passed to this request."""
        return self._parameters

    def get_levels(self) -> Tuple[str, ...]:
        """Returns a list of levels requested for this data access."""
        return self._levels


class IGridData:
    """
    Base interface for grid-based environmental and geographic data.
    """
    def get_grid_geometry(self) -> GridGeometry2D:
        """Returns the grid geometry representing row, column dimensions and cell size."""
        raise NotImplementedError

    @property
    def unit(self) -> Union[Unit, None]:
        """Returns the unit for the data values, or None if no unit is available."""
        raise NotImplementedError

    def get_parameter(self) -> str:
        """Returns the parameter name associated with this grid."""
        raise NotImplementedError

    def get_raw_data(self) -> np.ndarray:
        """Returns a numpy array containing the raw data for this grid."""
        raise NotImplementedError

    def populate_data(self, destination: 'DataDestination', unit_conversion_callback=None) -> None:
        """Populates the raw data to a specific data destination and optionally converts it to a specified unit."""
        raw_data = self.get_raw_data()
        converted_data = unit_conversion_callback(raw_data) if unit_conversion_callback else raw_data
        destination.wrap_raw_data(converted_data)


class IData(IGridData):
    """
    Interface for environmental and geographic data that can be requested through `IDataRequest`.
    """
    @property
    def datatype(self) -> str:
        """Returns the datatype of this grid, e.g., 'Float32' or 'Int16'."""
        raise NotImplementedError


class DataDestination:
    """
    Base interface for data destinations used to populate raw grid data into memory.
    """
    def __init__(self):
        pass

    def wrap_raw_data(self, raw_data: np.ndarray) -> np.ndarray:
        """Wraps the raw grid data into a native format for this application."""
        raise NotImplementedError

    @property
    def datatype(self) -> str:
        """Returns the native datatype of data stored in this destination."""
        raise NotImplementedError

