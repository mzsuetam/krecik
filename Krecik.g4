grammar Krecik;


// PRIMARY EXPRESSION AND MAIN FUNCTION
s
	: functions_declarations_list? SP? ahoj_declaration SP? functions_declarations_list? SP? EOF
	;

functions_declarations_list
    : function_declaration SP? functions_declarations_list
    | function_declaration
    ;

ahoj_declaration
    : Prikaz SP 'ahoj' SP? '()' SP? body
    ;


// FUNCTIONS
function_declaration
	:  Prikaz SP VARIABLE_NAME SP? '(' SP? declaration_arg_list? SP? ')' SP? body
	;

declaration_arg_list
    : declaration SP? ',' SP? declaration_arg_list
    | declaration
    ;

body
    : '{' SP? body_items_list? SP? '}'
    ;

body_items_list
    : body_item SP? body_items_list
    | body_item
    ;

body_item
	: body_line SP? ';'
	| instruction SP? body
	;

body_line
    : expression
	| declaration
	| assignment
    ;

expression
	: '(' SP? expression SP? ')'
	| unary_operator SP? expression
	| expression SP? binary_operator SP? expression
	| function_call
	| VARIABLE_NAME
	| literal
	;

function_call
	: VARIABLE_NAME '(' SP? expressions_list? SP? ')'
	;

expressions_list
    : expression SP? ',' SP? expressions_list
    | expression
    ;


// CONDITIONAL INSTRUCTIONS AND LOOPS
conditional_instruction
    : Kdyz SP? '(' SP? expression SP? ')' SP? Pak
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
var_type
    : Cislo
    | Logicki
    ;

declaration
	: var_type SP VARIABLE_NAME
	;

literal
    : LOGIC_VAL
    | NUMERIC_VAL
    ;

assignment
    : declaration SP? '=' SP? expression
	| VARIABLE_NAME SP? '=' SP? expression
    ;


// KEYWORDS AND OTHER LEXER VARIABLES
Cislo: 'cislo';
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
Prikaz: 'prikaz';

SP
    : [ ]+
    ;

TAB
    : '\t' -> skip
    ;

NEWLINE
    : [\r\n]+ -> skip
    ;

COMMENT
    : '//' ~[\r\n]* -> skip
    ;

VARIABLE_NAME
    : [a-z_]+
    ;

NUMERIC_VAL
    : DOUBLE_VAL
    | INT_VAL
    ;

DOUBLE_VAL
    : [0-9]+ '.' [0-9]+ ;

INT_VAL // used only for main function
    : [0-9]+
    ;

LOGIC_VAL
    : 'true'
    | 'false'
    ;
