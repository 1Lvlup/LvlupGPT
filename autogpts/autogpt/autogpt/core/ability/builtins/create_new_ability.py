import logging
from dataclasses import dataclass
from typing import Any, ClassVar, List, Literal, Optional

import json_schema
from autogpt.core.ability.base import Ability, AbilityConfiguration, AbilityResult
from autogpt.core.plugin.simple import PluginLocation, PluginStorageFormat

logger = logging.getLogger(__name__)


class CreateNewAbility(Ability):
    default_configuration: AbilityConfiguration = AbilityConfiguration(
        location=PluginLocation(
            storage_format=PluginStorageFormat.INSTALLED_PACKAGE,
            storage_route="autogpt.core.ability.builtins.CreateNewAbility",
        ),
    )

    @dataclass
    class Configuration(AbilityConfiguration):
        ability_name: str
        description: str
        arguments: List[dict[str, Any]]
        required_arguments: List[str]
        package_requirements: List[str]
        code: str

    description: ClassVar[str] = "Create a new ability by writing python code."

    parameters: ClassVar[dict[str, json_schema.JSONSchema]] = {
        "ability_name": json_schema.JSONSchema(
            description="A meaningful and concise name for the new ability.",
            type=json_schema.JSONSchema.Type.STRING,
            required=True,
        ),
        "description": json_schema.JSONSchema(
            description=(
                "A detailed description of the ability and its uses, "
                "including any limitations."
            ),
            type=json_schema.JSONSchema.Type.STRING,
            required=True,
        ),
        "arguments": json_schema.JSONSchema(
            description="A list of arguments that the ability will accept.",
            type=json_schema.JSONSchema.Type.ARRAY,
            items=json_schema.JSONSchema(
                type=json_schema.JSONSchema.Type.OBJECT,
                properties={
                    "name": json_schema.JSONSchema(
                        description="The name of the argument.",
                        type=json_schema.JSONSchema.Type.STRING,
                    ),
                    "type": json_schema.JSONSchema(
                        description=(
                            "The type of the argument. "
                            "Must be a standard json schema type."
                        ),
                        type=json_schema.JSONSchema.Type.STRING,
                    ),
                    "description": json_schema.JSONSchema(
                        description=(
                            "A detailed description of the argument and its uses."
                        ),
                        type=json_schema.JSONSchema.Type.STRING,
                    ),
                },
            ),
        ),
        "required_arguments": json_schema.JSONSchema(
            description="A list of the names of the arguments that are required.",
            type=json_schema.JSONSchema.Type.ARRAY,
            items=json_schema.JSONSchema(
                description="The names of the arguments that are required.",
                type=json_schema.JSONSchema.Type.STRING,
            ),
        ),
        "package_requirements": json_schema.JSONSchema(
            description=(
                "A list of the names of the Python packages that are required to "
                "execute the ability."
            ),
            type=json_schema.JSONSchema.Type.ARRAY,
            items=json_schema.JSONSchema(
                description=(
                    "The name of the Python package that is required to execute the ability."
                ),
                type=json_schema.JSONSchema.Type.STRING,
            ),
        ),
        "code": json_schema.JSONSchema(
            description=(
                "The Python code that will be executed when the ability is called."
            ),
            type=json_schema.JSONSchema.Type.STRING,
            required=True,
        ),
    }

    def __init__(
        self,
        logger: logging.Logger,
        configuration: Configuration,
    ):
        self._logger = logger
        self._configuration = configuration

    async def __call__(
        self,
        ability_name: str,
        description: str,
        arguments: List[dict[str, Any]],
        required_arguments: List[str],
        package_requirements: List[str],
        code: str,
    ) -> AbilityResult:
        raise NotImplementedError
