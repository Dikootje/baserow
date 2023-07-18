from baserow.core.formula.registries import RuntimeFormulaFunction
from baserow.formula.types import BaseFormulaContext
from baserow.formula.types import FormulaArgs
from baserow.core.formula.argument_types import (
    NumberBaserowRuntimeFormulaArgumentType,
    TextBaserowRuntimeFormulaArgumentType,
)


class RuntimeConcat(RuntimeFormulaFunction):
    type = "concat"

    def execute(self, context: BaseFormulaContext, args: FormulaArgs):
        return "".join([str(a) for a in args])

    def validate_number_of_args(self, args):
        return len(args) >= 2


class RuntimeGet(RuntimeFormulaFunction):
    type = "get"
    args = [TextBaserowRuntimeFormulaArgumentType()]

    def execute(self, context: BaseFormulaContext, args: FormulaArgs):
        return context[args[0]]


class RuntimeAdd(RuntimeFormulaFunction):
    type = "add"
    args = [
        NumberBaserowRuntimeFormulaArgumentType(),
        NumberBaserowRuntimeFormulaArgumentType(),
    ]

    def execute(self, context: BaseFormulaContext, args: FormulaArgs):
        return args[0] + args[1]
