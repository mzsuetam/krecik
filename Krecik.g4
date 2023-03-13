grammar Krecik;	
	
s: proc_ahoj EOF;

proc_ahoj: 'prikaz' SP 'ahoj' SP* '(' SP* INT_VAL ',' SP* INT_VAL SP* ')' SP* body;

body: '{' SP* expr SP* '}';

expr: cislo | logicki;

/*
expr: (operacja|instrukcja) SP*

operacja: 
// deklaracja, podstawianie, wywołanie funkcji
// zmiana położenia i orientacji

instrukcja:
// if, for, 
*/

logicki_unary_operator
    : 'ne'
    ;

logicki_binary_operator
    : 'nebo' | 'oba' | 'je' | 'neje' | 'wetsi' | 'mensi'
    ;

logicki
	: logicki_unary_operator SP logicki
	| '(' SP* logicki SP*')' 
	| logicki SP logicki_binary_operator SP logicki
	| variable 
	| logic 
	;

cislo_unary_operator
    : '-'
    ;

cislo_binary_operator
    : '*' | '/'
    : '+' | '-'
    ;

cislo
	: '(' SP* cislo SP* ')' 
	| cislo SP cislo_binary_operator SP cislo
	| variable 
	| number 
	;
    
/* znienne w programie */

number : '-'? INT_VAL | DOUBLE_VAL;

variable: variable_VAL;

logic: LOGIC_VAL;

/* ZMIENNE LEKSERA */

NEWLINE : [\r\n]+ -> skip;
SP: [ ]+;
INT_VAL: [0-9]+;
DOUBLE_VAL   : [0-9]+ '.' [0-9]+ ;
BOOL_VAL : 'true' | 'false';
variable_VAL : [a-zA-Z_]+;
LOGIC_VAL : 'true' | 'false'
