import enum
import re
from typing import Any, Dict, List, Literal, Optional, Union  # Importing necessary types

import jsonschema
from pydantic import BaseModel
from textwrap import indent  # Importing indent for formatting strings


class JSONSchema(BaseModel):
    """
    A class representing a JSON Schema object.
    This class is used to define and validate JSON schemas.
    """
    class Type(str, enum.Enum):
        """
        An enum representing the different types of JSON schema.
        """
        STRING = "string"
        ARRAY = "array"
        OBJECT = "object"
        NUMBER = "number"
        INTEGER = "integer"
        BOOLEAN = "boolean"

    description: Optional[str] = None  # Optional field for describing the schema
    type: Optional[Type] = None  # Optional field for specifying the schema type
    enum: Optional[List[Union[str, int, float, bool]]] = None  # Optional field for specifying allowed values
    required: bool = False  # Optional field for specifying if the schema is required
    items: Optional["JSONSchema"] = None  # Field for specifying the schema for array items
    properties: Optional[Dict[str, "JSONSchema"]] = None  # Field for specifying the schema for object properties
    minimum: Optional[Union[int, float]] = None  # Optional field for specifying the minimum allowed value
    maximum: Optional[Union[int, float]] = None  # Optional field for specifying the maximum allowed value
    min_items: Optional[int] = None  # Optional field for specifying the minimum number of items in an array
    max_items: Optional[int] = None  # Optional field for specifying the maximum number of items in an array

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the JSONSchema object to a dictionary.

        Returns:
            A dictionary representation of the JSONSchema object.
        """
        schema: Dict[str, Any] = {
            "type": self.type.value if self.type else None,
            "description": self.description,
        }
        # Code for handling array schema
        if self.type == "array":
            if self.items:
                schema["items"] = self.items.to_dict()
            schema["minItems"] = self.min_items
            schema["maxItems"] = self.max_items
        # Code for handling object schema
        elif self.type == "object":
            if self.properties:
                schema["properties"] = {
                    name: prop.to_dict() for name, prop in self.properties.items()
                }
                schema["required"] = [
                    name for name, prop in self.properties.items() if prop.required
                ]
        # Code for handling enum schema
        elif self.enum:
            schema["enum"] = self.enum
        else:
            schema["minimum"] = self.minimum
            schema["maximum"] = self.maximum

        schema = {k: v for k, v in schema.items() if v is not None}

        return schema

    @classmethod
    def from_dict(cls, schema: Dict[str, Any]) -> "JSONSchema":
        """
        Creates a JSONSchema object from a dictionary.

        Args:
            schema (Dict[str, Any]): A dictionary representation of a JSONSchema object.

        Returns:
            A JSONSchema object.
        """
        return JSONSchema(
            description=schema.get("description"),
            type=schema["type"],
            enum=schema["enum"] if "enum" in schema else None,
            items=JSONSchema.from_dict(schema["items"]) if "items" in schema else None,
            properties=JSONSchema.parse_properties(schema)
            if schema["type"] == "object"
            else None,
            minimum=schema.get("minimum"),
            maximum=schema.get("maximum"),
            min_items=schema.get("minItems"),
            max_items=schema.get("maxItems"),
        )

    @staticmethod
    def parse_properties(schema_node: Dict[str, Any]) -> Dict[str, "JSONSchema"]:
        """
        Parses the properties of a JSONSchema object.

        Args:
            schema_node (Dict[str, Any]): A dictionary representation of a JSONSchema object.

        Returns:
            A dictionary of property names and corresponding JSONSchema objects.
        """
        properties = (
            {k: JSONSchema.from_dict(v) for k, v in schema_node["properties"].items()}
            if "properties" in schema_node
            else {}
        )
        if "required" in schema_node:
            for k, v in properties.items():
                v.required = k in schema_node["required"]
        return properties

    def validate_object(
        self, object: object, logger: Any
    ) -> tuple[Literal[True], None] | tuple[Literal[False], List[jsonschema.ValidationError]]:
        """
        Validates a dictionary object against the JSONSchema.

        Args:
            object (object): A dictionary object to validate.
            logger (Any): A logger object for logging validation errors.

        Returns:
            A tuple of a boolean and a list of validation errors.
            The boolean is True if the object is valid, False otherwise.
            The list of validation errors is None if the object is valid.
        """
        validator = jsonschema.Draft7Validator(self.to_dict())

        if errors := sorted(validator.iter_errors(object), key=lambda e: e.path):
            return False, errors

        return True, None

    def to_typescript_object_interface(self, interface_name: str = "") -> str:
        """
        Converts the JSONSchema object to a TypeScript interface.

        Args:
            interface_name (str, optional): The name of the interface. Defaults to "".

        Returns:
            A string representation of the TypeScript interface.
        """
        if self.type != JSONSchema.Type.OBJECT:
            raise NotImplementedError("
