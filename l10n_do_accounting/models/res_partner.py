from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class Partner(models.Model):
    _inherit = "res.partner"

    def _get_l10n_do_dgii_payer_types_selection(self):
        """Return the list of payer types needed in invoices to classify accordingly to
        DGII requirements.
        """
        return [
            ("taxpayer", _("Fiscal Tax Payer")),
            ("non_payer", _("Non Tax Payer")),
            ("nonprofit", _("Nonprofit Organization")),
            ("special", _("Special from Tax Paying")),
            ("governmental", _("Governmental")),
            ("foreigner", _("Foreigner")),
        ]

    def _get_l10n_do_expense_type(self):
        """Return the list of expenses needed in invoices to classify accordingly to
        DGII requirements.
        """
        return [
            ("01", _("01 - Personal")),
            ("02", _("02 - Work, Supplies and Services")),
            ("03", _("03 - Leasing")),
            ("04", _("04 - Fixed Assets")),
            ("05", _("05 - Representation")),
            ("06", _("06 - Admitted Deductions")),
            ("07", _("07 - Financial Expenses")),
            ("08", _("08 - Extraordinary Expenses")),
            ("09", _("09 - Cost & Expenses part of Sales")),
            ("10", _("10 - Assets Acquisitions")),
            ("11", _("11 - Insurance Expenses")),
        ]

    l10n_do_dgii_tax_payer_type = fields.Selection(
        selection="_get_l10n_do_dgii_payer_types_selection",
        compute="_compute_l10n_do_dgii_payer_type",
        inverse="_inverse_l10n_do_dgii_tax_payer_type",
        string="Taxpayer Type",
        index=True,
        store=True,
    )

    l10n_do_expense_type = fields.Selection(
        selection="_get_l10n_do_expense_type",
        string="Cost & Expense Type",
        store=True,
    )

    country_id = fields.Many2one(
        default=lambda self: self._default_l10n_do_country_id()
    )

    @api.model
    def _default_l10n_do_country_id(self):
        """Set Dominican Republic as default country only when the company is Dominican.

        Important:
        A Many2one default must return an ID or False, not a recordset.
        Returning a recordset may break web_read/onchange in newer Odoo versions.
        """
        dominican_republic = self.env.ref("base.do", raise_if_not_found=False)

        if not dominican_republic:
            return False

        if self.env.company.country_id == dominican_republic:
            return dominican_republic.id

        return False

    def _check_l10n_do_fiscal_fields(self, vals):
        """Prevent changes to fiscal partner fields after fiscal documents are posted."""
        if not self:
            return

        fiscal_fields = [
            field
            for field in ["name", "vat", "country_id"]
            if field in vals
        ]

        if not fiscal_fields:
            return

        if self.env.user.has_group("l10n_do_accounting.group_l10n_do_edit_fiscal_partner"):
            return

        for partner in self:
            # Do not validate child contacts because their fiscal fields are readonly
            # and they depend on the commercial partner.
            if partner.parent_id:
                continue

            has_posted_fiscal_document = self.env["account.move"].sudo().search([
                ("l10n_latam_use_documents", "=", True),
                ("country_code", "=", "DO"),
                ("commercial_partner_id", "=", partner.id),
                ("state", "=", "posted"),
            ], limit=1)

            if has_posted_fiscal_document:
                raise AccessError(
                    _(
                        "You are not allowed to modify %s after partner "
                        "fiscal document issuing"
                    )
                    % (", ".join(self._fields[f].string for f in fiscal_fields))
                )

    def write(self, vals):
        self._check_l10n_do_fiscal_fields(vals)
        return super().write(vals)

    @api.depends("vat", "country_id", "name")
    def _compute_l10n_do_dgii_payer_type(self):
        """Compute the type of partner depending on soft decisions."""
        for partner in self:
            vat = partner.vat or partner.name or ""
            vat_len = len(vat)
            upper_name = partner.name.upper() if partner.name else ""
            is_dominican_partner = partner.country_code == "DO"

            if not is_dominican_partner:
                partner.l10n_do_dgii_tax_payer_type = "foreigner"
                continue

            if not vat.isdigit():
                partner.l10n_do_dgii_tax_payer_type = "non_payer"
                continue

            if vat_len == 11:
                partner.l10n_do_dgii_tax_payer_type = "non_payer"
            elif vat_len == 9:
                if "MINISTERIO" in upper_name and not vat.startswith("4"):
                    partner.l10n_do_dgii_tax_payer_type = "governmental"
                elif "ZONA FRANCA" in upper_name:
                    partner.l10n_do_dgii_tax_payer_type = "special"
                elif "IGLESIA" in upper_name or (
                        "MINISTERIO" in upper_name and vat.startswith("4")
                ):
                    partner.l10n_do_dgii_tax_payer_type = "special"
                elif not vat.startswith("4"):
                    partner.l10n_do_dgii_tax_payer_type = "taxpayer"
                else:
                    partner.l10n_do_dgii_tax_payer_type = "nonprofit"
            else:
                partner.l10n_do_dgii_tax_payer_type = "non_payer"

    def _inverse_l10n_do_dgii_tax_payer_type(self):
        """Allow manual edition of the computed taxpayer type."""
        for partner in self:
            partner.l10n_do_dgii_tax_payer_type = partner.l10n_do_dgii_tax_payer_type

    def _l10n_do_normalize_web_read_id(self, record_id):
        if isinstance(record_id, dict):
            record_id = record_id.get("id") or record_id.get("res_id") or record_id.get("origin")
            if isinstance(record_id, dict):
                record_id = record_id.get("id") or record_id.get("res_id")

        if hasattr(record_id, "origin"):
            origin = record_id.origin
            record_id = origin.id if hasattr(origin, "id") else origin

        return record_id

    def web_read(self, specification):
        raw_ids = list(getattr(self, "_ids", []))
        normalized_ids = []
        has_dirty_id = False

        for record_id in raw_ids:
            normalized_id = self._l10n_do_normalize_web_read_id(record_id)
            if normalized_id != record_id:
                has_dirty_id = True
            normalized_ids.append(normalized_id)

        if has_dirty_id:
            normalized_ids = [record_id for record_id in normalized_ids if record_id]
            return super(Partner, self.browse(normalized_ids)).web_read(specification)

        return super().web_read(specification)
