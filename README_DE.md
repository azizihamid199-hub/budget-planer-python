# Persönlicher Budget-Planer (Python & SQL)

[Switch to English version](README.md)

Konsolenanwendung in Python mit SQLite zum Erfassen von Einnahmen und Ausgaben.

## Funktionen
- Einnahmen und Ausgaben mit Kategorie und Zeitstempel erfassen
- Dauerhafte Speicherung in einer lokalen SQLite-Datenbank (`budget.db`)
- Kontostand berechnen, mit Warnung bei einem Minus
- Alle Transaktionen als Tabelle anzeigen
- Transaktionen ändern und löschen (CRUD)
- Eingabeprüfung: ungültige Beträge, leere Kategorien und unbekannte IDs führen nicht zum Absturz

## Technik
- Python 3 (nur Standardbibliothek)
- SQLite3 mit SQL (`CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `SUM`)
- Beträge werden als ganze Cent gespeichert, damit es keine Rundungsfehler gibt
- Datenbanklogik (`database.py`) und Benutzeroberfläche (`main.py`) sind getrennt
- Tests mit `unittest`

## Projektstruktur
| Datei | Aufgabe |
|---|---|
| `database.py` | Klasse `BudgetDatabase` mit allen SQL-Zugriffen |
| `main.py` | Konsolenmenü, Eingabeprüfung und Ausgabe |
| `tests/test_budget.py` | Tests für Datenbank und Eingabeprüfung |

## Starten
```bash
git clone https://github.com/azizihamid199-hub/budget-planer-python.git
cd budget-planer-python
python main.py
```

## Tests ausführen
```bash
python -m unittest discover -s tests
```

## Ideen zum Ausbauen
- Auswertung pro Kategorie oder Monat
- Export als CSV
- Grafische Oberfläche oder Web-Version
