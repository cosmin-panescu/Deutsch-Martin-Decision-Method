# Documentatie metoda Deutsch-Martin

**Instalare**
Inainte de a rula scriptul, instalati pachetele necesare folosind comanda:
`pip install numpy pandas openpyxl`

**Rulare script**
Executati scriptul folosind comanda:
`python script.py`

**Format pt. fisierele Excel/CSV**
Pentru fisierele Excel & CSV, prima coloana trebuie sa contina numele variantelor, iar primul rand trebuie sa contina numele criteriilor. Valorile din celelalte celule reprezinta valoarea fiecarei variante conform fiecarui criteriu.

**Descriere**
Acest script Python automatizeaza metoda Deutsch-Martin pentru luarea deciziilor. Metoda permite ordonarea si clasificarea variantelor decizionale pe baza mai multor criterii, utilizand un algoritm iterativ pentru calculul momentelor.

**Functionalitati**
Citirea din fisier:
-suport pentru fisiere Excel (.xlsx, .xls) si CSV
-detectarea automata a numarului de variante si criterii
-permite specificarea delimitatorului pentru fisierele CSV

Introducere manuala:
-permite utilizatorului sa introduca manual valorile pt. criterii si variante
-solicita utilizatorului nr. de variante si criterii dorit
