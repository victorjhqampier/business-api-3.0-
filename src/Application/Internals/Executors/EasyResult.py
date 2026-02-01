from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Optional, TypeVar

from Application.Internals.Adapters.ValidationResultAdapter import ValidationResultAdapter

# ********************************************************************************************************          
# * Copyright © 2026 Arify Labs - All rights reserved.   
# * 
# * Info                  : EasyResult Class to standardize success and failure responses
# *
# * By                    : Victor Jhampier Caxi Maquera
# * Email/Mobile/Phone    : victorjhampier@gmail.com | 968991714
# *
# * Creation date         : 31/01/2026
# * 
# **********************************************************************************************************

T = TypeVar("T")
# Constante para evitar crear listas vacías repetidamente
_EMPTY_VALIDATIONS: list[ValidationResultAdapter] = []

@dataclass(frozen=True, slots=True)
class EasyResult(Generic[T]):
    is_success: bool
    status: int
    success_value: Optional[T] = None
    validation_values: list[ValidationResultAdapter] = field(default_factory=lambda: _EMPTY_VALIDATIONS)

    @classmethod
    def success(cls, success_value: T, status: int = 200) -> "EasyResult[T]":
        return cls(
            is_success=True,
            status=status,
            success_value=success_value,
            validation_values=_EMPTY_VALIDATIONS,
        )

    @classmethod
    def failure(cls, status: int, validation_values: list[ValidationResultAdapter]) -> "EasyResult[T]":
        return cls(
            is_success=False,
            status=status,
            success_value=None,
            validation_values=validation_values or _EMPTY_VALIDATIONS,
        )

    @classmethod
    def empty(cls) -> "EasyResult[T]":
        return cls(
            is_success=True,
            status=204,
            success_value=None,
            validation_values=_EMPTY_VALIDATIONS,
        )
    