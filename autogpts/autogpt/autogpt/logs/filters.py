import logging  # Importing the logging module for logging purposes


class BelowLevelFilter(logging.Filter):
    """Filter for logging levels below a certain threshold.

    This class is a custom filter for the logging module that only allows
    log records with a level number greater than the specified threshold.
    """

    def __init__(self, below_level: int):
        """
        Initialize the BelowLevelFilter instance.

        :param below_level: The logging level below which records will be filtered out.
        """
        super().__init__()  # Call the parent class constructor
        self.below_level = below_level  # Set the threshold level

    def filter(self, record: logging.LogRecord):
        """
        Determine if the log record should be logged or filtered out.

        :param record: The log record to be filtered.
        :return: True if the record's level is above the threshold, False otherwise.
        """
        return record.levelno < self.below_level  # Return True if the level is above the threshold
