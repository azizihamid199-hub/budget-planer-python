# Personal Budget Planner (Python & SQL)

[Zur deutschen Version](README_DE.md)

A command line application in Python with SQLite for tracking income and expenses.

## Features
- Add income and expenses with a category and timestamp
- Persistent storage in a local SQLite database (`budget.db`)
- Balance calculation with a warning when the balance is negative
- List all transactions as a table
- Edit and delete transactions (CRUD)
- Input validation: invalid amounts, empty categories and unknown IDs do not crash the program

## Tech
- Python 3 (standard library only)
- SQLite3 with SQL (`CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `SUM`)
- Amounts are stored as whole cents to avoid rounding errors
- Database logic (`database.py`) is separated from the user interface (`main.py`)
- Tests with `unittest`

## Project structure
| File | Purpose |
|---|---|
| `database.py` | `BudgetDatabase` class with all SQL access |
| `main.py` | Console menu, input validation and output |
| `tests/test_budget.py` | Tests for the database and input validation |

## Run
```bash
git clone https://github.com/azizihamid199-hub/budget-planer-python.git
cd budget-planer-python
python main.py
```

## Run the tests
```bash
python -m unittest discover -s tests
```

## Ideas for improvement
- Report per category or month
- CSV export
- Graphical or web interface
