"""Base models."""

import json
from pathlib import Path
from typing import Self

import yaml
from pydantic import (
    BaseModel,
    ConfigDict,
)


class StrictBaseModel(BaseModel):
    """Basemodel used to ensure no extra fields tolerance."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    @classmethod
    def from_json(cls, text: str) -> Self:
        """Load model from JSON."""
        return cls.model_validate_json(text)

    @classmethod
    def from_yaml(cls, text: str) -> Self:
        """Load model from YAML."""
        return cls.model_validate(yaml.safe_load(text))

    @classmethod
    def from_json_file(cls, path: str) -> Self:
        """Load model from JSON file."""
        with Path(path).open(encoding="utf-8") as f:
            return cls.model_validate(json.load(f))

    @classmethod
    def from_yaml_file(cls, path: str) -> Self:
        """Load model from YAML file."""
        with Path(path).open(encoding="utf-8") as f:
            return cls.model_validate(yaml.safe_load(f))

    def to_yaml(self, exclude_defaults: bool = True) -> str:
        """Export model to YAML."""
        return yaml.safe_dump(
            self.model_dump(
                mode="json",
                exclude_defaults=exclude_defaults,
            ),
            sort_keys=False,
        )

    def to_yaml_file(self, path: str, exclude_defaults: bool = True) -> None:
        """Export model to YAML file."""
        with Path(path).open("w", encoding="utf-8") as f:
            f.write(self.to_yaml(exclude_defaults=exclude_defaults))


class TolerantBaseModel(StrictBaseModel):
    """Basemodel with extra fields tolerance."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)
