import abc
import os
import typing
from typing import Any, Callable, Generic, Optional, Type, TypeVar, get_args

from pydantic import BaseModel, Field, ValidationError
from pydantic.fields import ModelField, Undefined, UndefinedType
from pydantic.main import ModelMetaclass

T = TypeVar("T")
M = TypeVar("M", bound=BaseModel)


def UserConfigurable(
    default: T | UndefinedType = Undefined,
    *args,
    default_factory: Optional[Callable[[], T]] = None,
    from_env: Optional[str | Callable[[], T | None]] = None,
    description: str = "",
    **kwargs,
) -> T:
    # TODO: use this to auto-generate docs for the application configuration
    return Field(
        default,
        *args,
        default_factory=default_factory,
        from_env=from_env,
        description=description,
        **kwargs,
        user_configurable=True,
    )

# The SystemConfiguration class is a Pydantic base model that represents the system configuration.
class SystemConfiguration(BaseModel):
    def get_user_config(self) -> dict[str, Any]:
        """
        Returns a dictionary containing the user-configurable fields of the system configuration.
        """
        return _recurse_user_config_values(self)

    @classmethod
    def from_env(cls):
        """
        Initializes the config object from environment variables.

        Environment variables are mapped to UserConfigurable fields using the from_env
        attribute that can be passed to UserConfigurable.
        """

        def infer_field_value(field: ModelField):
            field_info = field.field_info
            default_value = (
                field.default
                if field.default not in (None, Undefined)
                else (field.default_factory() if field.default_factory else Undefined)
            )
            if from_env := field_info.extra.get("from_env"):
                val_from_env = (
                    os.getenv(from_env) if type(from_env) is str else from_env()
                )
                if val_from_env is not None:
                    return val_from_env
            return default_value

        return _recursive_init_model(cls, infer_field_value)

    class Config:
        extra = "forbid"
        use_enum_values = True
        validate_assignment = True


SC = TypeVar("SC", bound=SystemConfiguration)


class SystemSettings(BaseModel):
    """A base class for all system settings."""

    name: str
    description: str

    class Config:
        extra = "forbid"
        use_enum_values = True
        validate_assignment = True


S = TypeVar("S", bound=SystemSettings)


class Configurable(abc.ABC, Generic[S]):
    """A base class for all configurable objects."""

    prefix: str = ""
    default_settings: typing.ClassVar[S]

    @classmethod
    def get_user_config(cls) -> dict[str, Any]:
        """
        Returns a dictionary containing the user-configurable fields of the default settings.
        """
        return _recurse_user_config_values(cls.default_settings)

    @classmethod
    def build_agent_configuration(cls, overrides: dict = {}) -> S:
        """
        Process the configuration for this object.

        Args:
            overrides (dict, optional): A dictionary containing the overrides for the default settings. Defaults to {}.

        Returns:
            S: An instance of the class with the merged configuration.
        """
        base_config = _update_user_config_from_env(cls.default_settings)
        final_configuration = deep_update(base_config, overrides)

        return cls.default_settings.__class__.parse_obj(final_configuration)


def _update_user_config_from_env(instance: BaseModel) -> dict[str, Any]:
    """
    Update config fields of a Pydantic model instance from environment variables.

    Precedence:
    1. Non-default value already on the instance
    2. Value returned by `from_env()`
    3. Default value for the field

    Params:
        instance: The Pydantic model instance.

    Returns:
        The user config fields of the instance.
    """

    def infer_field_value(field: ModelField, value):
        field_info = field.field_info
        default_value = (
            field.default
            if field.default not in (None, Undefined)
            else (field.default_factory() if field.default_factory else Undefined)
        )
        if value == default_value and (from_env := field_info.extra.get("from_env")):
            val_from_env = os.getenv(from_env) if type(from_env) is str else from_env()
            if val_from_env is not None:
                return val_from_env
        return value

    def init_sub_config(model: Type[SC]) -> SC | None:
        try:
            return model.from_env()
        except ValidationError as e:
            # Gracefully handle missing fields
            if all(e["type"] == "value_error.missing" for e in e.errors()):
                return None
            raise

    return _recurse_user_config_fields(instance, infer_field_value, init_sub_config)


def _recursive_init_model(
    model: Type[M],
    infer_field_value: Callable[[ModelField], Any],
) -> M:
    """
    Recursively initialize the user configuration fields of a Pydantic model.

    Parameters:
        model: The Pydantic model type.
        infer_field_value: A callback function to infer the value of each field.
            Parameters:
                ModelField: The Pydantic ModelField object describing
