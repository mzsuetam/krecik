grammar Krecik;	
	
s: (SP? prikaz_def)* SP? proc_ahoj EOF;

prikaz_def
	:  'prikaz' SP variable SP? '(' SP? ( vartype (SP?',' SP? vartype)* )? SP?')' SP? body
	;

vartype 
	: cislo_var
	| logicki_var
	;
	
cislo_var
	: 'cislo' SP variable
	;

logicki_var
	:
	'logicki' SP variable
	;

proc_ahoj
    : 'prikaz' SP 'ahoj' SP? '(' SP? INT_VAL ',' SP? INT_VAL SP? ')' SP? body
    ;

body
    : '{' SP* (expr SP*)* '}'
    ;

expr
	: operation SP? ';'
	| instruction SP? body
	;

operation
	: declaration
	| definition
	| proc_call
	| 
    ;
/* brakuje:  operacje graficzne, zmiana położenia i orientacji */

proc_call
	: variable '(' ( SP? proc_arg (SP? ',' SP? proc_arg)* SP? )? ')'
	;

proc_arg
	: logicki
	| cislo
	;
	
if_instruction
    : 'kdyz' SP? '(' SP? logicki SP? ')' SP? 'pak'
    ;

for_instruction
	: 'opakujte' SP 'az' SP cislo
	; 
	
instruction
	: if_instruction
	| for_instruction
    ;
	

	
/* typy danych */

logicki_unary_operator
    : 'ne'
    ;

logicki_binary_operator
    : 'nebo' | 'oba' | 'je' | 'neje'
    ;
/*    	||      &&      ==     !-     */

logicki_comparison_operator
: 'wetsi' 
| 'mensi'
;

logicki
	: logicki_unary_operator SP logicki
	| '(' SP? logicki SP? ')' 
	| logicki SP? logicki_binary_operator SP? logicki
	| cislo SP logicki_comparison_operator SP cislo
	| logic 
	| variable 
	| variable 
	| logic 
	| variable
	| logic 
	;

cislo_unary_operator
    : '-'
    ;

cislo_binary_operator
    : '*' | '/'
    | '+' | '-'
    ;

cislo
	: '(' SP? cislo SP? ')' 
	| cislo SP? cislo_binary_operator SP? cislo
	| variable 
	| number 
	;

declaration
	: 'cislo' SP VARIABLE_VAL SP? '=' SP? cislo
	| 'logicki' SP VARIABLE_VAL SP? '=' SP? logicki
	;
	
definition
	: VARIABLE_VAL SP? '=' SP? cislo
	| VARIABLE_VAL SP? '=' SP? logicki
    ;


/* nazwy zmiennych w programie */

number : '-'? INT_VAL | DOUBLE_VAL;
variable: VARIABLE_VAL;
logic: LOGIC_VAL;


/* ZMIENNE LEKSERA */

COMMENT : '//' ~[\r\n]* -> skip;
NEWLINE : [\r\n]+ -> skip;
SP: [ \t]+;
DOUBLE_VAL: [0-9]+ '.' [0-9]+ ;
INT_VAL: [0-9]+;
LOGIC_VAL: 'true' | 'false';
VARIABLE_VAL: [a-z_]+;
