# Rozvrh 

Řešte zjednodušený problém sestavování rozvrhu. Jsou dány:

- množina studentů $S=\{0,\dots, n_S - 1\}$, 
- množina předmětů $P=\{0,\dots, n_P - 1\}$,
- množina učitelů  $U=\{0,\dots, n_U - 1\}$, 
- množina výukových bloků $B=\{0,\dots, n_B - 1\}$. 

Každý student $i\in S$ má definovánu množinu zapsaných předmětů $p_i \subset P$. 
Každý předmět $j\in P$ má definovaného učitele $u_j \in U$. Předpokládáme neomezenou zásobu učeben.
Cílem je přiřadit předmětům vyučovací bloky tak, aby předměty které mají průnik studentů nebo učitelů
neměly stejný blok.

Úkoly:

1. Formulujte úlohu jako problém barvení grafu. Co jsou vrcholy, hrany, barvy?
2. Vyberte si jeden z heuristických barvících algoritmů a popište jeho průběh při aplikaci na tento konkrétní problém.
3. Zvojený algoritmus implementujte.


Vstupem je textový soubor. Na prvním řádku jsou čísla $n_S$, $n_P$, $n_U$, $n_B$.
Na dalších $n_S$ řádcích je pro každého studenta $i$ seznam čísel jeho předmětů $p_i$. 
Na dalších $n_P$ řádcích je pro každý předmět $j$ číslo jeho učitele $u_j$.
Výstup programu má $n_P$ řádků na řádku $j$ je pro předmět $j$ číslo jeho bloku. 
Bloky jsou očíslovány tak, aby při ponechání pouze řádků s prvním výskytem bloku
tvořily uspořádanou posloupnost.

## Příklad vstupu
```
6 6 3 3
0 1 3
0 1 5
0 4 3
0 4 5
2 1 3
2 4 5
0
0
1
1
2
2
```

## Očekávaný výstup
```
0
1
0
2
1
2
```

