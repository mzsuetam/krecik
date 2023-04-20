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
	| instruction SP* body
	;

body_line
    : expression
	| declaration
	| assignment
    ;

expression
	: unary_operator SP* '(' SP* expression SP* ')'
	| product SP* ('+' | '-') SP* expression
	;

product
    : product SP* (('*' | '/') SP* product)*
    | '(' SP* expression SP* ')'
    | unary_operator SP* product
    | VARIABLE_NAME
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

loop_instruction
	: Opakujte SP Az SP expression
	;

instruction
	: conditional_instruction
	| loop_instruction
    ;


// ARITHMETIC AND LOGIC OPERATIONS
unary_operator
    : numeric_unary_operator
    | boolean_unary_operator
    ;

binary_operator
    : numeric_binary_operator
    | boolean_binary_operator
    | comparison_operator
    ;

numeric_unary_operator
    : '+'
    | '-'
    ;

numeric_binary_operator
    : '*'
    | '/'
    | '+'
    | '-'
    ;

boolean_unary_operator
    : Ne
    ;

boolean_binary_operator
    : Nebo
    | Oba
    | Je
    | Neje
    ;

comparison_operator
	: Wetsi
	| Mensi
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




