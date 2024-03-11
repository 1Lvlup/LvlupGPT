"""The singleton metaclass for ensuring only one instance of a class."""
import abc


class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.

    This metaclass implements the Singleton design pattern, which guarantees that only one
    instance of a class is created, and provides a global point of access to that instance.

    Attributes:
        _instances (dict): A dictionary that stores the created instances of each class.

    Methods:
        __call__(cls, *args, **kwargs):
            Call method for the singleton metaclass.

            This method checks if an instance of the class has already been created. If not,
            it creates a new instance and stores it in the `_instances` dictionary.

            Args:
                cls (type): The class to create an instance of.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                The created instance of the class.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
