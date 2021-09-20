parser grammar BaserowFormula;

options { tokenVocab=BaserowFormulaLexer; }

root
    : expr EOF
    ;

expr
    :
    SINGLEQ_STRING_LITERAL # StringLiteral
    | DOUBLEQ_STRING_LITERAL #  StringLiteral
    | INTEGER_LITERAL # IntegerLiteral
    | OPEN_PAREN expr CLOSE_PAREN # Brackets
    | expr op=(PLUS | MINUS | SLASH | EQUAL) expr # BinaryOp
    | FIELD OPEN_PAREN field_reference CLOSE_PAREN # FieldReference
    | FIELDBYID OPEN_PAREN INTEGER_LITERAL CLOSE_PAREN # FieldByIdReference
    | func_name OPEN_PAREN (expr (COMMA expr)*)? CLOSE_PAREN # FunctionCall
    ;

func_name
    : identifier
    ;

field_reference
    : SINGLEQ_STRING_LITERAL
    | DOUBLEQ_STRING_LITERAL
    ;

identifier
    : IDENTIFIER
    | IDENTIFIER_UNICODE
    ;
