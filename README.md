# MEDITRASH+++

## Výzva

Legislativa vyžaduje evidovat zdravotnický odpad ze strany lékařů.
Chceme vytvořit program na evidenci odpadu a na včasné, rychlé a snadné odesílání formulářů do systému  ISPOP. Cílem je snížit byrokratickou zátěž zdravotnického personálu v menších zdravotnických zařízeních. 

### Řešení

Naše řešení je multiplatformní aplikace, která klade důraz především na jednoduché a přehledné uživatelské prostředí a umožňuje Registraci/přihlášení zdravotnického zařízení a evidenci jejího odpadu. Po úspěšném přihlášení je jsou k dispozici tyto funkcionality:
- Zadání vyhozeného odpadu
- Odvezení jednotlivých typů odpadu s volbou odvozce
- Prohlížení historie vyhozeného odpadu
- Odstranění jednotlivých položek v historii odpadů
- Grafy se statistikami (aktuální odpad, celkový odpad, prostor do dosáhnutí zákonem daného limitu)
- Editace profilových informací
- Vytvoření ISPOP pdf souboru

### Návrh databázového schématu 

### Použité technologie

Programovací jazyk:

- Python

Knihovny:

 - Kivy, KivyMD - GUI
 - Pyodbc - připojení databáze
 - Matplotlib - grafy
 - FPDF - generování ISPOP

### Připojení k databázi

![image](https://github.com/JanPodavka/MediTrashplus/blob/main/Dokumentace/connection_to_dbs.png)

- Pro připojení k databázi používáme knihovnu Pyodbc, kdy při spuštění aplikace se vytvoří connection k naší databázi (zadáním IP, názvu databáze, jmena/hesla)
- Pokud se nepřipojí aplikace k databázi, tak se po 20 vteřinách ukončí a vypíši chybovou hlášku
- Poté jsme si předvytvořili cursor na dané připojení, ke kterému lze přistupovat (app.cursor) v jednotlivých screenech aplikace

### SQL Injection

![image](https://github.com/JanPodavka/MediTrashplus/blob/main/Dokumentace/protect_SQL_INJECTION.png)

- Aplikace řeší základní SQL Injection pomoci tzv.PreparedStatement, tedy je předvytvořeno query a následně se k němu připojují data v metodě cursor.execute(), která odešle naše query do databáze
