grammar Krecik;


// PRIMARY EXPRESSION AND MAIN FUNCTION
s
	: (SP? function_declaration)* SP? ahoj_declaration EOF
	;

ahoj_declaration
    : Prikaz SP 'ahoj' SP? '(' SP? NUMERIC_VAL ',' SP? NUMERIC_VAL SP? ')' SP? body
    ;


// FUNCTIONS
function_declaration
	:  Prikaz SP VARIABLE_NAME SP? '(' SP? declaration_arg_list SP? ')' SP? body
	;

declaration_arg_list
    : declaration_arg SP? ',' SP? declaration_arg_list
    | declaration_arg
    ;

declaration_arg
	: var_type SP VARIABLE_NAME
	;

body
    : '{' SP* (expr SP?)* '}'
    ;

expr
	: operation SP? ';'
	| instruction SP? body
	;

operation
	: declaration
	| assignment
	| draw_operation
	| function_call
    ;

draw_operation
	: Stetec SP brush_option
	| 'dopredu' SP? '(' SP? numeric_value SP? ')'
	| 'dozpet' SP? '(' SP? numeric_value SP? ')'
	| 'doleva' SP? '(' SP? numeric_value SP? ')'
	| 'doprava' SP? '(' SP? numeric_value SP? ')'
	| 'vlevo' SP? '(' SP? numeric_value SP? ')'
	| 'vpravo' SP? '(' SP? numeric_value SP? ')'
	;

brush_option
	: Krecik
	| Netoperek
	| Naopak
	;

function_call
	: VARIABLE_NAME '(' function_arg_list ')'
	;

function_arg_list
    : function_arg SP? ',' SP? function_arg_list
    | function_arg
    ;

function_arg
	: boolean_value
	| numeric_value
	;


// CONDITIONAL INSTRUCTIONS AND LOOPS
if_instruction
    : Kdyz SP? '(' SP? boolean_value SP? ')' SP? Pak
    ;

for_instruction
	: Opakujte SP Az SP numeric_value
	;

instruction
	: if_instruction
	| for_instruction
    ;


// ARITHMETIC AND LOGIC OPERATIONS
numeric_unary_operator
    : '-'
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
	: Cislo SP VARIABLE_NAME SP? '=' SP? numeric_value
	| Logicki SP VARIABLE_NAME SP? '=' SP? boolean_value
	;

numeric_value
	: '(' SP? numeric_value SP? ')'
	| numeric_value SP? numeric_binary_operator SP? numeric_value
	| VARIABLE_NAME
	| numeric_unary_operator? NUMERIC_VAL
	;

boolean_value
	: boolean_unary_operator SP boolean_value
	| '(' SP? boolean_value SP? ')'
	| boolean_value SP? boolean_binary_operator SP? boolean_value
	| numeric_value SP comparison_operator SP numeric_value
	| LOGIC_VAL
	| VARIABLE_NAME
	;

assignment
	: VARIABLE_NAME SP? '=' SP? var_value
    ;

var_value
    : numeric_value
    | boolean_value
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
Stetec: 'stetec';
Krecik: 'krecik';
Netoperek: 'netoperek';
Naopak: 'naopak';

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
