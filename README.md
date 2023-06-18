# Język Krecik

## Autorzy

- Mateusz Mazur
- Patryk Knapek 
- Piotr Karaś
- Tomasz Kawiak

## Założenia ogólne:

- Język proceduralny
- Interpreter plików .krecik pisany w języku Python
- W języku piszemy skrypt poruszania się krecika po planszy.
- Na planszy oprócz krecika znajdują
się inne obiekty: kamen (kamień), kopecek (kopiec), rajce (pomidorek),
muchomurka (muchomorek). Krecik może podnosić i przenosić niektóre z
tych przedmiotów.
- Krecik ma ekwipunek o wielkości 1.
- Z powyższymi obiektami będziemy mogli wchodzić w interakcje opisane poniżej.

## Spis tokenów i gramatyka

Spis tokenów i gramatyka znajdują się w [src/antlr/Krecik.g4](https://github.com/mzsuetam/krecik/blob/master/src/antlr/Krecik.g4)

## Stosowany generator parserów

ANTLR 4

## Sposób użycia:

1. Należy sklonować repozytorium z [githuba](https://github.com/mzsuetam/krecik) projektu.
2. W głównym folderze projektu należy uruchomić ‘pip install -r requirements.txt’, aby pobrać wymagane biblioteki.
3. Plik prezentacyjny włączamy poleceniem `src/driver.py --allow-prints true --display window`
4. Dowolny plik `.krecik` włączamy poleceniem `src/driver.py example_programs/foos.krecik`

## Opis języka:

---

### Zmienne:

- Zmienne typowane statycznie
- Zasięg obowiązywania zmiennych: do klamr
- Zmienne int (cely), float (cislo) i boolean (logicki)
- Deklaracja: cely n = 4;
- Przypisanie: n = n + 2 * foo();

### Operacje arytmetyczne i logiczne:

---

Operacje na zmiennych cislo i cely:

- +
- -
- *
- /
- ()
- operacje arytmetyczne zwracają typ cislo lub cely

Operacje na zmiennych logicki:

- wetsi >
- mensi <
- je ==
- neje !=
- nebo ||
- oba &&
- ne ~
- ()
- operacje logiczne zwracają typ logicki

### Funkcje:

---

<zwracany_typ> nazwa_funkcji(<typ_zmiennej> <nazwa_zmiennej>, … ) {}

nazwa funkcji musi być unikalna w skali pliku

wywołanie: <nazwa_funkcji>(<nazwa_zmiennej>, … )

wywołanie funkcji jest operacją

możliwe jest wywoływanie rekurencyjne

argumenty są przekazywane poprzez wartość

zwracany_typ - typy zmiennych oraz dodatkowo *nedostatek* (void)

Słowo kluczowe *vratit* (return)

### Funkcje wbudowane

```c
do_predu(Cely n) - przesunięcie krecika do przodu o n pól
v_pravo() - obrót krecika w prawo
v_zad() - obrót krecika do tyłu
v_levo() - obrót krecika w lewo
wzit() - weź do ekwipunku
poloz() - odłóż z ekwipunku
vykop() - wykop kopiec
pohrbit() - zakop kopiec
skryt() - wejdź do kopca
vstavej() - wyjdź z kopca
zda_trava() - czy krecik jest na trawie
zda_trava_pred() - czy krecik stoi przed trawą
zda_kamen() - czy krecik jest na kamieniu
zda_kamen_pred() - czy krecik stoi przed kamieniem
zda_kopecek() - czy krecik jest na kopcu
zda_kopecek_pred() - czy krecik jest przed kopcem
zda_rajce() - czy krecik jest na pomidorku
zda_rajce_pred() - czy krecik jest przed pomidorkiem
zda_muchomur() - czy krecik jest na muchomorku
zda_muchomur_pred() - czy krecik jest przed muchomorkiem
zda_drzi_rajce() - czy krecik trzyma w ekwipunku pomidorka
zda_drzi_muchomur() - czy krecik trzyma w ekwipunku muchomorka
pockejte(Cislo f) - poczekaj o f sekund
print(<variable>) - wypisz wartość zmiennej (tylko dla flagi-allow-prints true)
```

## Przykład programu:

```c
cely foo(cely a){
    kdyz ( a mensi 1 ) {
        print(-100);
        kdyz ( true){
            kdyz (true){
                vratit a;

            }
        }
    }
    a = a-1;
    print(a);
    cely b = foo(a);
    print(a);
    vratit b;
}

nedostatek ahoj() {
	print(-1);
  cely a = foo(5);
  print(-1);
  print(a);

	cely a = (3*3+3*3) * - ( 1 ) * -1;
    logicki l = ne(true);
	cislo b = 3.14;
	cely c = (3+6)*(3+6)+7;
    cely d = -2;
	do_predu(a*5-c-d);
	pockejte(6. - b);
	v_levo();
    v_pravo();
    v_pravo();
    v_levo();
	pockejte(2.+2.*2.);
    kdyz(l)
    {
       do_predu(2);
       kdyz(18 mensi 88 nebo 18 wetsi -2)
       {
           do_predu(2);
           pockejte(3.);
       }
       jiny
       {
           do_predu(1);
           pockejte(3.);
       }
    }
    jiny {
        do_predu(1);
        pockejte(2.);
        kdyz(true nebo true oba false)
        {
            do_predu(1);
            pockejte(2.);
        }
    }
    vratit;
}
```
