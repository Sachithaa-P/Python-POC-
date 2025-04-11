class InvalidFileNameException(Exception):
    """Raised when the file name is invalid or empty."""
    pass

class RestrictedSQLCommandException(Exception):
    """Raised when the SQL query contains restricted commands."""
    pass

class DuplicateEntryException(Exception):
    """Raised when a duplicate entry is attempted to be inserted in a unique field."""
    pass

class DataTypeMismatchException(Exception):
    """Raised when inserted data does not match the expected column data type."""
    pass
