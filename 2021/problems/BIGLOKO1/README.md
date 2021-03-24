# Problém Železnice 

Železniční společnost VELKÁ MAŠINA plánuje propojit železnicí $n$ měst, mezi nimiž zatím nikde železnice nevede. Byla vypracována studie, 
ve které byla naceněna výstavba železnice mezi vybranými dvojicemi měst. 
Pro některé dvojice měst bylo vypracováno více variant, celkem bylo uvažováno $m$ různých spojení mezi dvojicemi měst. 
Studie také určila míru spoločenské a ekologické vhodnosti a oznámkovala je 1-5. 
Společnost VELKÁ MAŠINA potřebuje program, který pro zadané výsledky studie navrhne železniční síť, která propojí všechna města
a zároveň bude mít nejmenší součet známek. V případě více takových síťí bude vybrána síť nejlevnější.
Formulujte úlohu jako grafový problém hledání minimální kostry a navrhněte a implementujte algoritmus pro jeho řešení s časovou složitostí $O(m \log n)$ nebo lepší.

Vstupní textový soubor má:
- na prvním řádku čísla $n$ a $m$
- na dalších $m$ řádcích jsou vždy data jedné varianty, tj. čtyři čísla:
    - první dvě udávají indexy koncových měst úseku, tedy jsou to čísla z množiny $\{0,\dots,n-1\}$
    - další číslo udává cenu vybudování úseku, opět celé číslo 
    - poslední číslo udává známku množiny ${1,2,3,4,5}$, pět je nejhorší 

Výstup má $n-1$ řádků s indexy použitých variant železničních úseků (číslovaných od $0$ do $m-1$).
Jejich pořadí je dáno následovně:

1. Uvažujte výslednou kostru jako zakořeněný strom v městě $0$. 
   *Představte si že kostra je z korálků (vrcholy) a provázků stejné délky (hrany) a pověsíte jí za město $0$.*
2. Pro každé další město $j$ existuje v tomto zakořeněném stromu jediný předek $\pi[j]$. Od každého korálku vede nahoru jediný provázek.
3. Na pozici $j-1$ výstupu bude index ($0$ až $m-1$) varianty použité pro spojení z $j$ do předka $\pi[j]$, tj. index hrany $(j, \pi[j])$.




## Příklad vstupu:
```
4 7
0 1 20  5
0 1 40  2
1 2 5   3
1 3 11  2
1 3 20  1
0 2 42  2 
2 3 30  4
```



## Očekávaný výstup:
```
1
5
4
```


