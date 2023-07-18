from typing import Any

from baserow.formula.parser.exceptions import (
    BaserowFormulaException,
    BaserowFormulaSyntaxError,
    MaximumFormulaSizeError,
)
from baserow.formula.parser.generated.BaserowFormula import BaserowFormula
from baserow.formula.parser.generated.BaserowFormulaVisitor import BaserowFormulaVisitor
from baserow.formula.types import BaseFormulaContext, FunctionCollection

__all__ = [
    BaserowFormulaException,
    MaximumFormulaSizeError,
    BaserowFormulaVisitor,
    BaserowFormula,
    BaserowFormulaSyntaxError,
]


from baserow.formula.parser.parser import get_parse_tree_for_formula
from baserow.formula.parser.python_executor import BaserowPythonExecutor


def resolve_formula(
    formula: str, functions: FunctionCollection, data_ledger: BaseFormulaContext
) -> Any:
    """
    Helper to resolve a formula given the data_ledger.

    :param formula: the formula itself.
    :param data_ledger: A dict like object that contains the data that can be accessed
        in from the formulas.
    :return: the formula result.
    """

    tree = get_parse_tree_for_formula(formula)
    return BaserowPythonExecutor(functions, data_ledger).visit(tree)
