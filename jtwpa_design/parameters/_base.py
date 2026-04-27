"""Shared Pydantic base model for repository parameter schemas."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class ParameterModel(BaseModel):
    """Immutable, strict base model for repository parameter objects.

    These models act as the schema layer for layout and simulation workflows:

    - ``model_copy(update=...)`` for small notebook / sweep edits
    - ``model_dump()`` for serialization
    - ``to_kwargs()`` for passing top-level parameters into GDSFactory cells

    ``to_kwargs()`` is intentionally shallow so nested parameter models stay as
    model objects instead of being recursively converted into dictionaries.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    def to_kwargs(self) -> dict[str, Any]:
        """Return a shallow field mapping suitable for function kwargs."""

        return {field_name: getattr(self, field_name) for field_name in self.__class__.model_fields}
