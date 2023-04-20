grammar Krecik;


// PRIMARY EXPRESSION AND MAIN FUNCTION
primary_expression
	: SP* functions_declarations_list SP* EOF
	;

functions_declarations_list
    : function_declaration SP* functions_declarations_list
    | function_declaration
    ;


// FUNCTIONS
function_declaration
	:  return_var_type SP VARIABLE_NAME SP* '(' SP* declaration_arg_list? SP* ')' SP* body
	;

declaration_arg_list
    : declaration SP* ',' SP* declaration_arg_list
    | declaration
    ;

body
    : '{' SP* body_items_list? SP* vratit? SP* body_items_list? SP*'}'
    ;

body_items_list
    : body_item SP* body_items_list
    | body_item
    ;

body_item
	: body_line SP* ';'
	| conditional_instruction SP* body SP* (Jiny SP* body SP*)?
	| loop_instruction SP* body
	;

body_line
    : expression
	| declaration
	| assignment
    ;

expression
    :   secondary_operator SP* expression                   # expressionUnaryOperator
    |   expression SP* primary_operator SP* expression      # expressionPrimaryOperator
    |   expression SP* secondary_operator SP* expression    # expressionSecondaryOperator
    |   expression SP* comparison_operator SP* expression   # expressionComparisonOperator
    |   expression SP* Oba SP* expression                   # expressionLogicalAndOperator
    |   expression SP* Nebo SP* expression                  # expressionLogicalOrOperator
    |   '(' SP* expression SP* ')'                          # parenthesisedExpression
    |   atom                                                # atomExpression
    ;

primary_operator
    : ( '*' | '/' )
    ;

secondary_operator
    : ( '+' | '-' | Ne)
    ;

comparison_operator
    :  ( Mensi | Wetsi | Je | Neje )
    ;

atom
    : VARIABLE_NAME
    | literal
    | function_call
    ;

function_call
	: VARIABLE_NAME '(' SP* expressions_list? SP* ')'
	;

expressions_list
    : expression SP* ',' SP* expressions_list
    | expression
    ;

vratit
    : Vratit (SP expression)? SP* ';'
    ;


// CONDITIONAL INSTRUCTIONS AND LOOPS
conditional_instruction
    : Kdyz SP? '(' SP* expression SP* ')' SP* Pak
    ;

else_instruction
    : Jiny
    ;

loop_instruction
	: Opakujte SP Az SP expression
	;

// VARIABLES AND TYPES
return_var_type
    : Cislo
    | Cely
    | Logicki
    | Nedostatek
    ;

var_type
    : Cislo
    | Cely
    | Logicki
    ;

declaration
	: var_type SP VARIABLE_NAME
	;

literal
    : BOOLEAN_VAL
    | FLOAT_VAL
    | INT_VAL
    ;

assignment
    : variable SP? '=' SP? expression
    ;

variable
    : declaration
    | VARIABLE_NAME
    ;


// KEYWORDS AND OTHER LEXER VARIABLES
Cislo: 'cislo';
Cely: 'cely';
Logicki: 'logicki';
Ne: 'ne';
Nebo: 'nebo';
Oba: 'oba';
Je: 'je';
Neje: 'neje';
Wetsi: 'wetsi';
Mensi: 'mensi';
Kdyz: 'kdyz';
Pak: 'pak';
Jiny: 'jiny';
Opakujte: 'opakujte';
Az: 'az';
Vratit: 'vratit';
Nedostatek: 'nedostatek';

SP
    : [ ]
    ;

SPACES
    : [ ]+ -> type(SP)
    ;

TAB
    : '\t' -> type(SP)
    ;

NEWLINE
    : [\r\n]+ -> skip
    ;

LINECOMMENT
    : '//' ~[\r\n]* -> skip
    ;

BLOCKCOMMENT
    : '/*' .*? '*/' -> skip
    ;

BOOLEAN_VAL
    : 'true'
    | 'false'
    ;

FLOAT_VAL  // accepts: 10.11 and 10 and 10. and .01
    :  INT_VAL '.' [0-9]*
    | '0'? '.' [0-9]+
    ;

INT_VAL
    : '0'
    | [1-9][0-9]*
    ;

VARIABLE_NAME
    : [a-z_]+
    ;




