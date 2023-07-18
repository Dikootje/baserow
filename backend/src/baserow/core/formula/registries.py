from abc import ABC, abstractmethod
from typing import Any, List, Optional, TypeVar

from baserow.core.formula.data_ledger import DataLedger
from baserow.formula.types import FunctionCollection
from baserow.core.registry import Instance, Registry
from baserow.formula.parser.exceptions import (
    FormulaFunctionTypeDoesNotExist,
    InvalidFormulaArgumentType,
    InvalidNumberOfArguments,
)
from baserow.formula.types import (
    BaseFormulaContext,
)
from baserow.formula.types import (
    FormulaArg,
    FormulaArgs,
)
from baserow.core.formula.argument_types import BaserowRuntimeFormulaArgumentType


class RuntimeFormulaFunction(ABC, Instance):
    @classmethod
    @property
    @abstractmethod
    def type(cls) -> str:
        """
        Should be a unique lowercase string used to identify this type.
        """

        pass

    @property
    def args(self) -> Optional[List[BaserowRuntimeFormulaArgumentType]]:
        """
        Should define the arguments the function has. If null then we don't know what
        arguments the function has any anything is accepted.

        :return: The arguments configuration that is expected by the execute function
        """

        return None

    @property
    def num_args(self):
        """
        Should define the number of arguments expected byt he execute function.

        :return: The number of arguments that are expected
        """

        return None if self.args is None else len(self.args)

    @abstractmethod
    def execute(self, context: BaseFormulaContext, args: FormulaArgs) -> Any:
        """
        This is the main function that will produce a result for the defined formula

        :return: Result of executing the formula
        """

        pass

    def validate_args(self, args: FormulaArgs):
        """
        This function can be called to validate all arguments given to the formula

        :param args: The arguments provided to the formula
        :raises InvalidNumberOfArguments: If the number of arguments is invalid
        :raises InvalidFormulaArgumentType: If any of the arguments have a wrong type
        """

        if not self.validate_number_of_args(args):
            raise InvalidNumberOfArguments(self, args)
        invalid_arg = self.validate_type_of_args(args)
        if invalid_arg:
            raise InvalidFormulaArgumentType(self, invalid_arg)

    def validate_number_of_args(self, args: FormulaArgs) -> bool:
        """
        This function validates that the number of args is correct.

        :param args: The args passed to the execute function
        :return: If the number of arguments is correct
        """

        return self.num_args is None or len(args) <= self.num_args

    def validate_type_of_args(self, args: FormulaArgs) -> Optional[FormulaArg]:
        """
        This function validates that the type of all args is correct.
        If a type is incorrect it will return that arg.

        :param args: The args that are being checked
        :return: The arg that has the wrong type, if any
        """

        if self.args is None:
            return None

        return next(
            (
                arg
                for arg, index in zip(args, range(len(args)))
                if not self.args[index].test(arg)
            ),
            None,
        )

    def parse_args(self, args: FormulaArgs) -> FormulaArgs:
        """
        This function parses the arguments before they get handed over to the execute
        function. This allows us to cast any args that might be of the wrong type to
        the correct type or transform the data in any other way we wish to.

        :param args: The args that are being parsed
        """

        if self.args is None:
            return args

        return [
            self.args[index].parse(arg) for arg, index in zip(args, range(len(args)))
        ]


class BaserowRuntimeFormulaFunctionRegistry(
    Registry[RuntimeFormulaFunction], FunctionCollection
):
    name = "formula_runtime_function"
    does_not_exist_exception_class = FormulaFunctionTypeDoesNotExist


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


formula_runtime_function_registry = BaserowRuntimeFormulaFunctionRegistry()
