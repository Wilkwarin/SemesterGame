# SemesterGame

Tento repozitár obsahuje hru, ktorá bola vytvorená ako praktická časť skúšky z predmetu **Objektové technológie**.

**Téma vybraná zo zoznamu poskytnutého vyučujúcim:** Farba ako herná mechanika.

---

## 1. Úvod

### 1.1 Inšpirácia

**Zuma**  
Klasická arkádová hra, v ktorej hráč ovláda kamennú žabu strieľajúcu farebné guličky. Cieľom hry je zničiť reťaz guličiek, ktoré sa pohybujú po kľukatej dráhe, skôr než sa dostanú na koniec trasy. Pre zničenie guličiek je potrebné vytvárať skupiny troch alebo viacerých guličiek rovnakej farby, ktoré po zásahu zmiznú.

<img src="https://github.com/Wilkwarin/SemesterGame/blob/main/readme_zuma.jpg" max-width="600" />

### 1.2 Herný zážitok

Cieľom hry je zničiť pohybujúcu sa reťaz guličiek, než dosiahne výstupný bod. Táto hra kombinuje prvky **platformovej hry** a **logickej hry**.

### 1.3 Vývojový softvér

- **Pygame 2.6.1**: Zvolený programovací jazyk.  
- **PyCharm 2024.3.1.1**: Vybrané IDE.  
- **Tiled 1.11.0**: Grafický nástroj na tvorbu levelov.

---

## 2. Koncept

### 2.1 Prehľad hry

Hráč ovláda postavu, ktorá môže skákať po platformách, teleportovať sa na jednosmerných teleportoch a brať farebné balóniky na špeciálnych bodoch. Ak sa reťaz balónikov dostane do výstupného bodu, hra je prehratá.

### 2.2 Interpretácia témy

Farba slúži na uľahčenie pohybu postavy po mape (teleporty na vstupe a výstupe majú rovnakú farbu) a na ničenie pohybujúcej sa reťaze farebných balónikov.

### 2.3 Základné mechaniky

- **Interakcia s farbou**:  
  Postava nesúca balónik môže skočiť medzi dve alebo viac balónikov rovnakej farby; táto skupina zmizne. Ak postava skočí vedľa jedneho balónika rovnakej farby a jedneho ineho, tento iný balónik zmení svoju farbu na farbu balónika postavy.

- **Pohyb**:  
  Postava môže skákať po platformách, padať z nich a používať teleporty.

### 2.4 Návrh tried

- **Hero**: Obsahuje vlastnosti postavy, logiku pohybu po mape, používania teleportov, zbierania balónikov a interakcie s reťazou balónikov.
- **MovingObject**: Trieda pre pohybujúce sa balóniky, obsahuje algoritmus ich pohybu po obrazovke a kontrolu, či dosiahli výstupný bod.
- **Ball**: Trieda pre zobrazenie balónika, ktorý nesie postava.

Hlavný herný cyklus sa nachádza v súbore `main.py`.

---

## 3. Grafika

### 3.1 Interpretácia témy

Keďže témou hry je farba, boli vybrané assety, ktoré obsahujú viaceré farebné varianty rovnakých objektov.

<img src="https://github.com/Wilkwarin/SemesterGame/blob/main/readme_level_objects.png" width="600" />

### 3.2 Dizajn

Použité assety:  
- [Cute Platformer Sisters](https://opengameart.org/content/cute-platformer-sisters) od používateľa [Master484](https://opengameart.org/users/master484).

Niektoré assety slúžia ako súčasť hernej logiky, iné slúžia na estetické vylepšenie hry.

---

## 4. Zvuk

### 4.1 Hudba

Štýl hudby ladí s vizuálnym dizajnom hry.  
Zdroj: [Pixabay - 8-bit Music](https://pixabay.com/ru/music/8-bit-music-on-245249/).

---

## 5. Herný zážitok

### 5.1 Používateľské rozhranie

Po zničení všetkých balónikov alebo po tom, čo balóniky dosiahnu výstupný bod, má hráč možnosť reštartovať hru.

### 5.2 Ovládanie

- **Šípky vľavo/vpravo/hore**: Pohyb postavy po mape.  
- **Šípka dole**: Výber balónika na špeciálnom bode.


---
Autor projektu: Mariia Shorokhova
