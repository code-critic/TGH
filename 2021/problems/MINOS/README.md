# Bludiště

Krétský král Mínos plánuje stavět bludiště pro nevlastního krvelačného syna [Minotaura](https://cs.wikipedia.org/wiki/M%C3%ADnotaurus). 
Bludiště má mít pouze jedno patro, bude kutáno v podzemí z jediného vchodu, chodby bludiště
budou pravoúhlé s celočíselnými délkami. Král chce, aby v bludišti existovala mezi každou dvojicí křižovatek právě jedna cesta.
Při kopání je však skála různě tvrdá (tvrdost $0$ až $2^{16}$) a stavitel chce aby se dělníci co nejméně nadřeli, přitom tvrdost skály je známá jen na stěnách již 
vykopaných chodeb. Chceme tedy bludiště, které má celkovou tvrdost vykopané horniny co nejmenší a pokud takových existuje více, 
chceme aby se při vynášení vykopané horniny urazila co nejmenší vzdélenost (součet vzdáleností všech křižovatek od vstupu).

Napište program na generování bludiště na čtvercové síti $n \times m$ bodů. Chodby mohou vést pouze po hranách čtvercové sítě. 
Kopání bludiště probíhá vždy pouze po jedné hraně a v okamžiku dosažení jejího koncového vrcholu se ohodnotí tvrdost dosud 
neohodnocených hran, které z něj vycházejí a to v pořadí (východ-0, západ-1, sever-2, jih-3). Tvrdost $\alpha_i$ se generujte náhodně pomocí
kongruenčního generátoru:

$$
    \alpha_{i+1} =  \alpha_i * 1664525 + 1013904223  \text{ mod } M
$$

hodnota $\alpha_0$, která je součástí vstupu, se použije pro ohodnocení první hrany. 
Hodnota $M$ je $2^{16}$. Vstup do bludiště uvažujte vždy v levém horním rohu z levé strany.

Vstupem programu je jeden řádek se třemi celými čisly $n$, $m$, $\alpha_0$.
Výstupem bude pro každou křižovatku (bod sítě) kód typu křižovatky. Z jedné křižovatky existuje (1) nebo neexistuje (0) chodba 
do každého ze čtyř směrů (východ-0, západ-1, sever-2, jih-3), kód křižovatky je tedy 4-bitové číslo s uvedeným významem jednotlivých bitů. 
Jedna křižovatka je tedy jedna cifra v 16-kové soustavě (např. křižovatka sever, západ jih je reprezentována cifrou $2+4+8=14=E$). 
Bludiště vypište na $n$ řádků po $m$ znacích.

## Vstup
```
3 3 3000
```

## Řešení

Výsledné bludiště, zaokrouhlené ceny hran v tisících:
```
X -  3 - X -  1 - X
|                  
56       64       65
|         
X - 59 - X - 17 - X
                  |
61       58       46
                  |
X - 31 - X -  7 - X
```

## Výstup
```
932
53A
136
```
