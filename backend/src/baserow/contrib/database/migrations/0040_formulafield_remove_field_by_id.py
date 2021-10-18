# Generated by Django 3.2.6 on 2021-09-15 13:11

from typing import Dict

from django.db import migrations, models
from django.db.models import F

from baserow.contrib.database.formula.parser.exceptions import (
    MaximumFormulaSizeError,
)
from baserow.contrib.database.formula.parser.generated.BaserowFormula import (
    BaserowFormula,
)
from baserow.contrib.database.formula.parser.generated.BaserowFormulaVisitor import (
    BaserowFormulaVisitor,
)
from baserow.contrib.database.formula.parser.parser import get_parse_tree_for_formula


# Copied from parser.py to ensure future changes to that file dont
# break this migration
def convert_string_literal_token_to_string(string_literal, is_single_q):
    literal_without_outer_quotes = string_literal[1:-1]
    quote = "'" if is_single_q else '"'
    return literal_without_outer_quotes.replace("\\" + quote, quote)


# Copied from parser.py to ensure future changes to that file dont
# break this migration
def convert_string_to_string_literal_token(string, is_single_q):
    quote = "'" if is_single_q else '"'
    escaped = string.replace(quote, "\\" + quote)
    return quote + escaped + quote


# Copied from update_field_names.py to ensure future changes to that file dont
# break this migration
# noinspection DuplicatedCode
class UpdateFieldNameFormulaVisitor(BaserowFormulaVisitor):
    def __init__(
        self,
        field_names_to_update: Dict[str, str],
        all_field_ids_to_name: Dict[int, str],
    ):
        self.field_names_to_update = field_names_to_update
        self.all_field_ids_to_name = all_field_ids_to_name

    def visitRoot(self, ctx: BaserowFormula.RootContext):
        return ctx.expr().accept(self)

    def visitStringLiteral(self, ctx: BaserowFormula.StringLiteralContext):
        return ctx.getText()

    def visitDecimalLiteral(self, ctx: BaserowFormula.DecimalLiteralContext):
        return ctx.getText()

    def visitBooleanLiteral(self, ctx: BaserowFormula.BooleanLiteralContext):
        return ctx.getText()

    def visitBrackets(self, ctx: BaserowFormula.BracketsContext):
        return ctx.expr().accept(self)

    def visitFunctionCall(self, ctx: BaserowFormula.FunctionCallContext):
        function_name = ctx.func_name().accept(self).lower()
        args = [expr.accept(self) for expr in (ctx.expr())]
        args_with_any_field_names_replaced = ",".join(args)
        return f"{function_name}({args_with_any_field_names_replaced})"

    def visitBinaryOp(self, ctx: BaserowFormula.BinaryOpContext):
        args = [expr.accept(self) for expr in (ctx.expr())]
        return args[0] + ctx.op.text + args[1]

    def visitFunc_name(self, ctx: BaserowFormula.Func_nameContext):
        return ctx.getText()

    def visitIdentifier(self, ctx: BaserowFormula.IdentifierContext):
        return ctx.getText()

    def visitIntegerLiteral(self, ctx: BaserowFormula.IntegerLiteralContext):
        return ctx.getText()

    def visitFieldReference(self, ctx: BaserowFormula.FieldReferenceContext):
        reference = ctx.field_reference()
        is_single_quote_ref = reference.SINGLEQ_STRING_LITERAL()
        field_name = convert_string_literal_token_to_string(
            reference.getText(), is_single_quote_ref
        )
        if field_name in self.field_names_to_update:
            new_name = self.field_names_to_update[field_name]
            escaped_new_name = convert_string_to_string_literal_token(
                new_name, is_single_quote_ref
            )
            return f"field({escaped_new_name})"
        else:
            return ctx.getText()

    def visitFieldByIdReference(self, ctx: BaserowFormula.FieldByIdReferenceContext):
        field_id = int(str(ctx.INTEGER_LITERAL()))
        if field_id not in self.all_field_ids_to_name:
            return f"field('unknown field {field_id}')"
        new_name = self.all_field_ids_to_name[field_id]
        escaped_new_name = convert_string_to_string_literal_token(new_name, True)
        return f"field({escaped_new_name})"

    def visitLeftWhitespaceOrComments(
        self, ctx: BaserowFormula.LeftWhitespaceOrCommentsContext
    ):
        updated_expr = ctx.expr().accept(self)
        return ctx.ws_or_comment().getText() + updated_expr

    def visitRightWhitespaceOrComments(
        self, ctx: BaserowFormula.RightWhitespaceOrCommentsContext
    ):
        updated_expr = ctx.expr().accept(self)
        return updated_expr + ctx.ws_or_comment().getText()


def update_field_names(
    formula: str,
    old_field_name_to_new_field_name: Dict[str, str],
    all_field_ids_to_names: Dict[int, str],
) -> str:
    try:
        tree = get_parse_tree_for_formula(formula)
        return UpdateFieldNameFormulaVisitor(
            old_field_name_to_new_field_name, all_field_ids_to_names
        ).visit(tree)
    except RecursionError:
        raise MaximumFormulaSizeError()


# noinspection PyPep8Naming
def forward(apps, schema_editor):
    FormulaField = apps.get_model("database", "FormulaField")

    for formula in FormulaField.objects.all():
        field_id_to_name = {}
        for field in formula.table.field_set.all():
            field_id_to_name[field.id] = field.name
        formula.old_formula_with_field_by_id = formula.formula
        formula.formula = update_field_names(formula.formula, {}, field_id_to_name)
        formula.save()


# noinspection PyPep8Naming
def reverse(apps, schema_editor):
    FormulaField = apps.get_model("database", "FormulaField")

    FormulaField.objects.filter(old_formula_with_field_by_id__isnull=False).update(
        formula=F("old_formula_with_field_by_id")
    )


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0039_formulafield"),
    ]

    operations = [
        migrations.AddField(
            model_name="formulafield",
            name="old_formula_with_field_by_id",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RunPython(forward, reverse),
    ]
