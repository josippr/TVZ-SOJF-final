# SOJF seminarski

## Task 1:

`python task1.py --directory=path/to/dir`

- Skripta iterira kroz direktorij i analizira svaku datoteku.
- Koristi python-magic za prepoznavanje tipa datoteke.
- Računa MD5 i SHA256 hash vrijednosti.
- Generira JSON izvještaj s detaljima o datotekama.


## Task 2:

`python task2.py --volume=[DISK_VOLUME]`

- Skripta etektira ADS-ove u NTFS datotekama pomoću fsutil stream list.
- Extracta ADS-ove pomoću icat.
- Generira JSON izvještaj s pronađenim ADS-ovima i lokacijama izvađenih podataka.


## Task 3:

`python task3.py --directory=path/to/dir --export=json`

enum: --export=json/csv

- Skripta analizira datoteke u zadanom direktoriju, izračunava SHA256 hash i briše duplicirane datoteke.
- Generira izvještaj – Broji originalne i duplicirane datoteke.
- Podržava export u JSON ili CSV – Izvještaj se sprema u željenom formatu koristeći argument --export.

