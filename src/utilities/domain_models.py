class GridGeometry2D:
    def __init__(self, rows: int, cols: int, dx: float, dy: float):
        if rows < 0 or cols < 0:
            raise ValueError("Rows and columns must be non-negative.")
        if dx <= 0 or dy <= 0:
            raise ValueError("dx and dy must be positive.")
        
        self.rows = rows
        self.cols = cols
        self.dx = dx
        self.dy = dy

    def total_area(self) -> float:
        """Calculates the total area of the grid."""
        return self.rows * self.cols * self.dx * self.dy

    def perimeter(self) -> float:
        """Calculates the perimeter of the grid."""
        return 2 * (self.rows * self.dx + self.cols * self.dy)

    def diagonal_length(self) -> float:
        """Calculates the diagonal length of the grid."""
        return ((self.rows * self.dx) ** 2 + (self.cols * self.dy) ** 2) ** 0.5

    def scale(self, factor: float):
        """Scales the grid dimensions by a given factor."""
        if factor <= 0:
            raise ValueError("Scale factor must be positive.")
        self.dx *= factor
        self.dy *= factor

    def to_dict(self) -> dict:
        """Serializes the object to a dictionary."""
        return {"rows": self.rows, "cols": self.cols, "dx": self.dx, "dy": self.dy}

    @classmethod
    def from_dict(cls, data: dict):
        """Deserializes the object from a dictionary."""
        return cls(data['rows'], data['cols'], data['dx'], data['dy'])

    def __eq__(self, other) -> bool:
        """Checks equality between two GridGeometry2D objects."""
        if not isinstance(other, GridGeometry2D):
            return NotImplemented
        return (self.rows == other.rows and self.cols == other.cols and 
                self.dx == other.dx and self.dy == other.dy)

    def __str__(self) -> str:
        return (f"GridGeometry2D(rows={self.rows}, cols={self.cols}, "
                f"dx={self.dx}, dy={self.dy})")

    def __repr__(self) -> str:
        return self.__str__()


class Unit:
    """
    The unit class is used to represent the units for data values.
    """
    def __init__(self, name: str):
        if not name:
            raise ValueError("Unit name cannot be empty.")
        self.name = name

    def __eq__(self, other) -> bool:
        """Checks equality between two Unit objects."""
        if not isinstance(other, Unit):
            return NotImplemented
        return self.name == other.name

    def __str__(self) -> str:
        return f"Unit(name={self.name})"

    def __repr__(self) -> str:
        return self.__str__()
