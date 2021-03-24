# Dodávky elektřiny 

Model elektrické rozvodné sítě je tvořen elektrárnami $0$, \dots $n_e-1$  a rozvodnami $n_e$, \dots, $n_e + n_r-1$. 
Tyto **přípojné body** jsou propojeny sítí čítající  $n_v$ vodičů. Jeden vodič vždy spojuje právě dva 
přípojné body a má definovaný maximální výkon, který jím může být přenášen (v obou směrech stejný). 
Žádné dvě elektrárny nejsou přímo propojeny a pro každou je znám její výkon. 
Elektrárny jsou napojeny libovolně na rozvodny. Rozvodny mohou být propojovány libovolně mezi sebou. 

Za účelem výstavby nového výrobního závodu bylo vytipováno $N$ míst. 
Pro každé místo $i=1,\dots ,N$ bylo navrženo $0 < k_i \le 3$ nezávislých elektrických přípojek napojených 
na přípojné body $r_{i,1}, \dots r_{i,k_i}$.
Navrhněte a implementujte algoritmus, který pro každou lokalitu určí maximální dostupný elektrický příkon.

## Popis vstupu
Na prvním řádku vstupu jsou tři přirozená čísla udávající: 
- počet elektráren $n_e$
- počet rozvoden $n_r$
- počet vodičů $n_v$

Na dalších $n_e$ řádcích jsou výkony elekráren. 

Na dalších $n_v$ řádcích je specifikace vodičů. 
Na jednom řádku jsou vždy tři přirozená čísla udávající postupně: 
- index prvního
- index druhého propojeného přípojného bodu 
- maximální přenášený výkon
Výkony elektráren a kapacity vodičů jsou přirozená čísla menší než 1000.

Následuje počet lokalit $N$ na samostatném řádku. Na každém z následujících $N$ řádcích 
je seznam přípojných bodů pro navržené elektrické přípojky (maximálně 3).
Na výstupu programu bude $N$ řádků, na každém maximální dostupný výkon pro odpovídající lokalitu.

Formulujte úlohu grafově jako úlohu tak, aby šla pro jednu lokalitu řešit jako problém sítě s jedním zdrojem a jedním cílem. 
Napište program pro nalezení optimálního toku sítí. Použijte Edmons-Karpův algoritmus (BFS pro hledání zlepšující cesty), nebo algoritmus s lepší složitostí.


## Příklad vstupu
```
2 3 4
4
4
0 4 6
1 4 5
4 2 4
4 3 7
3
2
3
2 3
```

## Očekávaný výstup
```
4
7
8
```
