"""Konsolenmenü des Budget-Planers. Die Datenbanklogik steht in database.py."""
import re

from database import AUSGABE, EINNAHME, BudgetDatabase


def parse_betrag(text):
    """Wandelt Eingaben wie '12,50' oder '12.5' in Cent um (hier: 1250).

    Wirft ValueError bei ungültigen Eingaben (Text, null, negativ, mehr als 2 Nachkommastellen).
    """
    text = text.strip().replace(",", ".")
    if not re.fullmatch(r"\d+(\.\d{1,2})?", text):
        raise ValueError("Bitte einen Betrag wie 12,50 eingeben (nur Zahlen, max. 2 Nachkommastellen).")
    euro, _, rest = text.partition(".")
    cent = int(euro) * 100 + int(rest.ljust(2, "0") or 0)
    if cent <= 0:
        raise ValueError("Der Betrag muss größer als 0 sein.")
    return cent


def format_euro(cent):
    vorzeichen = "-" if cent < 0 else ""
    euro, rest = divmod(abs(cent), 100)
    return f"{vorzeichen}{euro:,}".replace(",", ".") + f",{rest:02d} €"


def lese_betrag():
    while True:
        try:
            return parse_betrag(input("Betrag in €: "))
        except ValueError as fehler:
            print(f"Fehler: {fehler}")


def lese_kategorie():
    while True:
        kategorie = input("Kategorie (z. B. Gehalt, Miete, Essen): ").strip()
        if kategorie:
            return kategorie
        print("Fehler: Die Kategorie darf nicht leer sein.")


def lese_id():
    try:
        return int(input("ID der Transaktion: ").strip())
    except ValueError:
        print("Fehler: Bitte eine Zahl eingeben.")
        return None


def transaktion_hinzufuegen(db, typ):
    kategorie = lese_kategorie()
    betrag = lese_betrag()
    db.add_transaction(typ, kategorie, betrag)
    print(f"Gespeichert: {'Einnahme' if typ == EINNAHME else 'Ausgabe'} {format_euro(betrag)} ({kategorie}).")
    zeige_saldo(db)


def zeige_transaktionen(db):
    zeilen = db.get_all()
    if not zeilen:
        print("Noch keine Transaktionen vorhanden.")
        return
    print(f"\n{'ID':>3} | {'Datum':<16} | {'Art':<9} | {'Kategorie':<18} | {'Betrag':>12}")
    print("-" * 70)
    for z in zeilen:
        art = "Einnahme" if z["type"] == EINNAHME else "Ausgabe"
        vorzeichen = 1 if z["type"] == EINNAHME else -1
        print(f"{z['id']:>3} | {z['created_at']:<16} | {art:<9} | {z['category']:<18} | "
              f"{format_euro(vorzeichen * z['amount_cent']):>12}")


def zeige_saldo(db):
    saldo = db.get_balance_cent()
    print(f"Kontostand: {format_euro(saldo)}")
    if saldo < 0:
        print("Achtung: Du bist im Minus!")


def transaktion_aendern(db):
    id_ = lese_id()
    if id_ is None:
        return
    kategorie = lese_kategorie()
    betrag = lese_betrag()
    print("Geändert." if db.update_transaction(id_, kategorie, betrag) else "Fehler: ID nicht gefunden.")


def transaktion_loeschen(db):
    id_ = lese_id()
    if id_ is None:
        return
    print("Gelöscht." if db.delete_transaction(id_) else "Fehler: ID nicht gefunden.")


MENUE = """
=== Budget-Planer ===
1) Einnahme hinzufügen
2) Ausgabe hinzufügen
3) Alle Transaktionen anzeigen
4) Kontostand anzeigen
5) Transaktion ändern
6) Transaktion löschen
0) Beenden"""


def main():
    db = BudgetDatabase("budget.db")
    try:
        while True:
            print(MENUE)
            wahl = input("Auswahl: ").strip()
            if wahl == "1":
                transaktion_hinzufuegen(db, EINNAHME)
            elif wahl == "2":
                transaktion_hinzufuegen(db, AUSGABE)
            elif wahl == "3":
                zeige_transaktionen(db)
            elif wahl == "4":
                zeige_saldo(db)
            elif wahl == "5":
                transaktion_aendern(db)
            elif wahl == "6":
                transaktion_loeschen(db)
            elif wahl == "0":
                print("Tschüss!")
                break
            else:
                print("Ungültige Auswahl.")
    except (KeyboardInterrupt, EOFError):
        print("\nProgramm beendet.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
