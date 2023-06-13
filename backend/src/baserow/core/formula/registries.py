from baserow.core.formula.runtime_formula_types import (
    RuntimeAdd,
    RuntimeConcat,
    RuntimeGet,
)
from baserow.formula.parser.exceptions import FormulaFunctionTypeDoesNotExist
from abc import ABC, abstractmethod
from typing import Any, List, TypeVar

from baserow.core.formula.data_ledger import DataLedger
from baserow.core.registry import Instance, Registry


class BaserowRuntimeFormulaFunctionRegistry(Registry):
    name = "formula_runtime_function"
    does_not_exist_exception_class = FormulaFunctionTypeDoesNotExist


formula_runtime_function_registry = BaserowRuntimeFormulaFunctionRegistry()


def register_runtime_formula_function_types():
    formula_runtime_function_registry.register(RuntimeConcat())
    formula_runtime_function_registry.register(RuntimeGet())
    formula_runtime_function_registry.register(RuntimeAdd())


class DataProviderType(
    Instance,
    ABC,
):
    """
    A data provider is responsible to collect the data from the application context and
    use them to expose data for formula resolver.

    The application context depends on the application. For instance, the application
    context for the application builder is the request and the current service. For the
    workflow automation tool, it's the current node.
    """

    @abstractmethod
    def get_context(self, **kwargs) -> Any:
        """
        Extract data from the application context. This data can then be use by the
        data provider to fulfill a data query from the formula.

        :param kwargs: application context parameters.
        :return: Any value that can be used lateron by the data provider.
        """

    @abstractmethod
    def get_data_chunk(self, data_ledger: DataLedger, path: List[str]):
        """
        Returns data designated by the path parameter. Usually use some of the
        context created by the get_context method and stored in the data ledger.
        """


DataProviderTypeSubClass = TypeVar("DataProviderTypeSubClass", bound=DataProviderType)


class DataProviderTypeRegistry(
    Registry[DataProviderTypeSubClass],
):
    """
    Contains all registered data provider types.
    """

    name = "data_provider"
