grammar Krecik;	
	
s: proc_ahoj EOF;

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
    ;

/* wywołanie funkcji, zmiana położenia i orientacji */
instruction
	: 'XD'
    ;
/* if, for */



/* typy danych */

logicki_unary_operator
    : 'ne'
    ;

logicki_binary_operator
    : 'nebo' | 'oba' | 'je' | 'neje' | 'wetsi' | 'mensi'
    ;
/*    ||      &&      ==     !-       >         <       */

logicki
	: logicki_unary_operator SP logicki
	| '(' SP? logicki SP? ')' 
	| logicki SP? logicki_binary_operator SP? logicki
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

NEWLINE : [\r\n]+ -> skip;
SP: [ \t]+;
INT_VAL: [0-9]+;
DOUBLE_VAL: [0-9]+ '.' [0-9]+ ;
VARIABLE_VAL: [a-z_]+;
LOGIC_VAL: 'true' | 'false';
