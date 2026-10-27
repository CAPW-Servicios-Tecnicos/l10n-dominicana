from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestFiscalPartnerGroup(TransactionCase):

    def test_group_does_not_grant_accounting_access(self):
        """El permiso de campos fiscales no debe dar acceso a menus contables."""
        fiscal_group = self.env.ref("l10n_do_accounting.group_l10n_do_edit_fiscal_partner")
        user = self.env["res.users"].create({
            "name": "Fiscal Partner Editor",
            "login": "fiscal_partner_editor",
            "groups_id": [(6, 0, [self.env.ref("base.group_user").id, fiscal_group.id])],
        })
        self.assertTrue(user.has_group("l10n_do_accounting.group_l10n_do_edit_fiscal_partner"))
        self.assertFalse(user.has_group("account.group_account_manager"))
        self.assertFalse(user.has_group("account.group_account_invoice"))
