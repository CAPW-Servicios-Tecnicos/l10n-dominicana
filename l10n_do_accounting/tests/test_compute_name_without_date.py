from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestComputeNameWithoutDate(TransactionCase):

    def test_batch_with_dated_and_undated_moves(self):
        """Un lote con un asiento con fecha y otro sin fecha no debe fallar."""
        journal = self.env["account.journal"].search([("type", "=", "general")], limit=1)
        if not journal:
            self.skipTest("Hace falta un diario general")
        dated = self.env["account.move"].create({"journal_id": journal.id, "move_type": "entry"})
        undated = self.env["account.move"].new({"journal_id": journal.id, "move_type": "entry", "date": False})
        (dated | undated)._compute_name()
        self.assertTrue(dated.name)
        self.assertEqual(undated.name, "/")
