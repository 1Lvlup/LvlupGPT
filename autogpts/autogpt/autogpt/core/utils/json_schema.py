import enum
import re
from typing import Any, Dict, List, Literal, Optional, Union

import jsonschema
from pydantic import BaseModel
from textwrap import indent


class JSONSchema(BaseModel):
    class Type(str, enum.Enum):
        STRING = "string"
        ARRAY = "array"
        OBJECT = "object"
        NUMBER = "number"
        INTEGER = "integer"
        BOOLEAN = "boolean"

    description: Optional[str] = None
    type: Optional[Type] = None
    enum: Optional[List[Union[str, int, float, bool]]] = None
    required: bool = False
    items: Optional["JSONSchema"] = None
    properties: Optional[Dict[str, "JSONSchema"]] = None
    minimum: Optional[Union[int, float]] = None
    maximum: Optional[Union[int, float]] = None
    min_items: Optional[int] = None
    max_items: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        schema: Dict[str, Any] = {
            "type": self.type.value if self.type else None,
            "description": self.description,
        }
        if self.type == "array":
            if self.items:
                schema["items"] = self.items.to_dict()
            schema["minItems"] = self.min_items
            schema["maxItems"] = self.max_items
        elif self.type == "object":
            if self.properties:
                schema["properties"] = {
                    name: prop.to_dict() for name, prop in self.properties.items()
                }
                schema["required"] = [
                    name for name, prop in self.properties.items() if prop.required
                ]
        elif self.enum:
            schema["enum"] = self.enum
        else:
            schema["minimum"] = self.minimum
            schema["maximum"] = self.maximum

        schema = {k: v for k, v in schema.items() if v is not None}

        return schema

    @classmethod
    def from_dict(cls, schema: Dict[str, Any]) -> "JSONSchema":
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

        Params:
            object: The dictionary object to validate.
            schema (JSONSchema): The JSONSchema to validate against.

        Returns:
            tuple: A tuple where the first element is a boolean indicating whether the
                object is valid or not, and the second element is a list of errors found
                in the object, or None if the object is valid.
        """
        validator = jsonschema.Draft7Validator(self.to_dict())

        if errors := sorted(validator.iter_errors(object), key=lambda e: e.path):
            return False, errors

        return True, None

    def to_typescript_object_interface(self, interface_name: str = "") -> str:
        if self.type != JSONSchema.Type.OBJECT:
            raise NotImplementedError("Only `object` schemas are supported")

        if self.properties:
            attributes: list[str] = []
            for name, property in self.properties.items():
                if property.description:
                    attributes.append(f"// {property.description}")
                attributes.append(f"{name}: {property.typescript_type};")
            attributes_string = "\n".join(attributes)
        else:
            attributes_string = "[key: string]: any"

        return (
            f"interface {interface_name} " if interface_name else ""
        ) + f"{{\n{indent(attributes_string, '  ')}\n}}"

    @property
    def typescript_type(self) -> str:
        if self.type == JSONSchema.Type.BOOLEAN:
            return "boolean"
        elif self.type in {JSONSchema.Type.INTEGER, JSONSchema.Type.NUMBER}:
            return "number"
        elif self.type == JSONSchema.Type.STRING:
            return "string"
        elif self.type == JSONSchema.Type.ARRAY:
            return f"Array<{self.items.typescript_type}>" if self.items else "Array"
        elif self.type == JSONSchema.Type.OBJECT:
            if not self.properties:
                return "Record<string, any>"
            return self.to_typescript_object_interface()
        elif self.enum:
            return " | ".join(repr(v) for v in self.enum)
        else:
            raise NotImplementedError(
                f"JSONSchema.typescript_type does not support Type.{self.type.name} yet"
            )
