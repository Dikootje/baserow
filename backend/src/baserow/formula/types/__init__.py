from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Dict, List

ReturnType = TypeVar("ReturnType", bound=Any)


class BaseDataLedger(Generic[ReturnType], ABC):
    @abstractmethod
    def __getitem__(self, key: str) -> ReturnType:
        ...


RuntimeFormulaContext = Dict
RuntimeFormulaArg = any
RuntimeFormulaArgs = List
