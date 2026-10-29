import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import AUSGABE, EINNAHME, BudgetDatabase  # noqa: E402
from main import format_euro, parse_betrag  # noqa: E402


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.db = BudgetDatabase(":memory:")

    def tearDown(self):
        self.db.close()

    def test_leere_datenbank_hat_saldo_null(self):
        self.assertEqual(self.db.get_balance_cent(), 0)

    def test_saldo_aus_einnahmen_und_ausgaben(self):
        self.db.add_transaction(EINNAHME, "Gehalt", 200000)
        self.db.add_transaction(AUSGABE, "Miete", 75000)
        self.db.add_transaction(AUSGABE, "Essen", 1250)
        self.assertEqual(self.db.get_balance_cent(), 123750)

    def test_negativer_saldo(self):
        self.db.add_transaction(AUSGABE, "Auto", 5000)
        self.assertLess(self.db.get_balance_cent(), 0)

    def test_aendern_und_loeschen(self):
        id_ = self.db.add_transaction(AUSGABE, "Essen", 1000)
        self.assertTrue(self.db.update_transaction(id_, "Restaurant", 2500))
        self.assertEqual(self.db.get_all()[0]["category"], "Restaurant")
        self.assertTrue(self.db.delete_transaction(id_))
        self.assertEqual(self.db.get_all(), [])

    def test_unbekannte_id(self):
        self.assertFalse(self.db.update_transaction(99, "x", 100))
        self.assertFalse(self.db.delete_transaction(99))

    def test_ungueltiger_typ(self):
        with self.assertRaises(ValueError):
            self.db.add_transaction("geschenk", "x", 100)


class EingabeTests(unittest.TestCase):
    def test_gueltige_betraege(self):
        self.assertEqual(parse_betrag("12,50"), 1250)
        self.assertEqual(parse_betrag("12.5"), 1250)
        self.assertEqual(parse_betrag("7"), 700)

    def test_ungueltige_betraege(self):
        for text in ["abc", "", "-5", "0", "1,234", "1e3"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    parse_betrag(text)

    def test_format(self):
        self.assertEqual(format_euro(123456), "1.234,56 €")
        self.assertEqual(format_euro(-500), "-5,00 €")


if __name__ == "__main__":
    unittest.main()
