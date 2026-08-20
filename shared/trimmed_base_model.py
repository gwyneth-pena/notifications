from pydantic import BaseModel, model_validator
from typing import Any, ClassVar

class TrimmedBaseModel(BaseModel):
    NO_TRIM: ClassVar[set[str]] = {"password"}

    @model_validator(mode="before")
    @classmethod
    def trim_strings(cls, values: Any) -> Any:
        return cls._trim_recursive(values)

    @classmethod
    def _trim_recursive(cls, value: Any, key_name: str = None) -> Any:
        if isinstance(value, str):
            if key_name and key_name.lower() in cls.NO_TRIM:
                return value
            return value.strip()

        if isinstance(value, dict):
            return {
                k: cls._trim_recursive(v,k)
                for k, v in value.items()
            }

        if isinstance(value, list):
            return [cls._trim_recursive(v) for v in value]

        if isinstance(value, tuple):
            return tuple(cls._trim_recursive(v) for v in value)

        return value
