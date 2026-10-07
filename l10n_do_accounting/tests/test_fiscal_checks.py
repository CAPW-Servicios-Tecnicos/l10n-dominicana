# -*- coding: utf-8 -*-
"""QR del e-CF, contingencia y RNC obligatorio del comprador."""
from datetime import date, datetime
from unittest import mock

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

COMPANY_RNC = "101010101"   # RNC sintético con dígito verificador válido
CLIENT_RNC = "131000002"


@tagged("post_install", "-at_install")
class TestFiscalChecks(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.company.write({"vat": COMPANY_RNC, "l10n_do_require_buyer_vat": True,
                           "l10n_do_consumer_vat_threshold": 250000.0})
        cls.Move = cls.env["account.move"]
        cls.partner = cls.env["res.partner"].create({"name": "Cliente prueba fiscal", "vat": CLIENT_RNC})
        cls.partner_no_vat = cls.env["res.partner"].create({"name": "Consumidor final prueba"})
        # contribuyente SIN RNC cargado (un cliente sin RNC queda 'non_payer', que la regla exime)
        cls.partner_taxpayer_no_vat = cls.env["res.partner"].create(
            {"name": "Contribuyente sin RNC", "l10n_do_dgii_tax_payer_type": "taxpayer"})

    def _doc(self, prefix):
        doc = self.env["l10n_latam.document.type"].search(
            [("doc_code_prefix", "=", prefix), ("country_id.code", "=", "DO")], limit=1)
        if not doc:
            self.skipTest("Tipo de documento %s no disponible" % prefix)
        return doc

    def _ecf(self, prefix="E31", total=1500.0, partner=None, **kw):
        vals = {
            "move_type": "out_invoice", "company_id": self.company.id,
            "partner_id": (partner or self.partner).id,
            "l10n_latam_document_type_id": self._doc(prefix).id,
            "l10n_do_fiscal_number": "%s0000000001" % prefix, "invoice_date": date(2026, 9, 10),
            "l10n_do_ecf_sign_date": datetime(2026, 9, 10, 14, 30, 5),
            "l10n_do_ecf_security_code": "AbC123", "amount_total_signed": total,
        }
        vals.update(kw)
        return self.Move.new(vals)

    # ------------------------------------------------------------------ QR
    def test_stamp_url_format_matches_production(self):
        url = self._ecf()._l10n_do_build_stamp_url("TesteCF", 1500.0)
        self.assertEqual(
            url,
            "https://ecf.dgii.gov.do/TesteCF/consultatimbre?rncemisor=%s&rnccomprador=%s&encf=E310000000001"
            "&fechaemision=10-09-2026&montototal=1500&fechafirma=10-09-2026+14:30:05"
            "&codigoseguridad=AbC123" % (COMPANY_RNC, CLIENT_RNC))

    def test_stamp_security_code_special_characters_are_encoded(self):
        url = self._ecf(l10n_do_ecf_security_code="OnX+KN")._l10n_do_build_stamp_url("ecf", 6000.0)
        self.assertTrue(url.endswith("&codigoseguridad=OnX%2BKN"))
        self.assertIn("&montototal=6000&", url)

    def test_stamp_url_never_writes_false(self):
        self.company.vat = False
        url = self._ecf(partner=self.partner_no_vat)._l10n_do_build_stamp_url("TesteCF", 1500.0)
        self.assertNotIn("False", url)
        self.assertIn("rncemisor=&", url)
        self.assertIn("rnccomprador=&", url)

    def test_stamp_url_consumer_summary_below_threshold(self):
        url = self._ecf("E32", total=1500.0, partner=self.partner_no_vat)._l10n_do_build_stamp_url("ecf", 1500.0)
        self.assertTrue(url.startswith("https://fc.dgii.gov.do/ecf/consultatimbreFC?rncemisor="))
        self.assertNotIn("fechafirma", url)
        self.assertNotIn("rnccomprador", url)
        big = self._ecf("E32", total=300000.0)._l10n_do_build_stamp_url("ecf", 300000.0)
        self.assertTrue(big.startswith("https://ecf.dgii.gov.do/"))     # desde el umbral es e-CF completo

    def test_stamp_threshold_is_configurable(self):
        self.company.l10n_do_consumer_vat_threshold = 1000.0
        url = self._ecf("E32", total=1500.0)._l10n_do_build_stamp_url("ecf", 1500.0)
        self.assertTrue(url.startswith("https://ecf.dgii.gov.do/"))

    # --------------------------------------------------------- contingencia
    def test_contingency_only_for_companies_that_issued_ecf(self):
        Move = type(self.Move)
        draft = self.Move.new({"company_id": self.company.id, "state": "draft"})
        self.company.l10n_do_ecf_issuer = False
        with mock.patch.object(Move, "_read_group", return_value=[(self.company, 3)]):
            draft._compute_company_in_contingency()
            self.assertTrue(draft.l10n_do_company_in_contingency)
        # otra compañía con e-CF no debe contagiar a esta
        other = self.env["res.company"].new({"name": "Otra"})
        with mock.patch.object(Move, "_read_group", return_value=[(other, 5)]):
            draft._compute_company_in_contingency()
            self.assertFalse(draft.l10n_do_company_in_contingency)
        # compañía marcada como emisora: no hay contingencia
        self.company.l10n_do_ecf_issuer = True
        with mock.patch.object(Move, "_read_group", return_value=[(self.company, 3)]):
            draft._compute_company_in_contingency()
            self.assertFalse(draft.l10n_do_company_in_contingency)

    def test_contingency_compute_does_not_write(self):
        Move = type(self.Move)
        draft = self.Move.new({"company_id": self.company.id, "state": "draft"})
        with mock.patch.object(Move, "_read_group", return_value=[]), \
                mock.patch.object(Move, "write") as write:
            draft._compute_company_in_contingency()
        write.assert_not_called()

    # --------------------------------------------------- RNC del comprador
    def _sale(self, prefix, untaxed=0.0, total=0.0, partner=None):
        journal = self.env["account.journal"].search(
            [("type", "=", "sale"), ("company_id", "=", self.company.id),
             ("l10n_latam_use_documents", "=", True)], limit=1)
        if not journal:
            self.skipTest("No hay diario de ventas fiscal en la base de pruebas")
        return self.Move.new({
            "move_type": "out_invoice", "company_id": self.company.id, "journal_id": journal.id,
            "partner_id": (partner or self.partner_no_vat).id,
            "l10n_latam_document_type_id": self._doc(prefix).id,
            "amount_untaxed_signed": untaxed, "amount_total_signed": total or untaxed})

    def test_vat_required_document_types(self):
        self.assertTrue(self._sale("B01", 1000.0, partner=self.partner_taxpayer_no_vat)._l10n_do_buyer_vat_required())
        self.assertFalse(self._sale("B01", 1000.0, partner=self.partner)._l10n_do_buyer_vat_required())
        # un cliente 'non_payer' sin RNC no se bloquea (no puede recibir crédito fiscal)
        self.assertFalse(self._sale("B01", 1000.0)._l10n_do_buyer_vat_required())

    def test_consumer_invoice_requires_vat_from_threshold(self):
        self.assertFalse(self._sale("B02", untaxed=249999.99)._l10n_do_buyer_vat_required())
        self.assertTrue(self._sale("B02", untaxed=250000.0)._l10n_do_buyer_vat_required())
        # B02 se compara sin ITBIS; e-CF 32 con el total
        self.assertFalse(self._sale("B02", untaxed=200000.0, total=250000.0)._l10n_do_buyer_vat_required())
        self.assertTrue(self._sale("E32", untaxed=200000.0, total=250000.0)._l10n_do_buyer_vat_required())

    def test_buyer_vat_check_is_configurable(self):
        move = self._sale("B01", 1000.0, partner=self.partner_taxpayer_no_vat)
        with self.assertRaises(ValidationError):
            move._l10n_do_check_buyer_vat()
        self.company.l10n_do_require_buyer_vat = False
        move._l10n_do_check_buyer_vat()                      # ya no exige

    def test_settings_have_help(self):
        fields = self.env["res.company"]._fields
        self.assertTrue(fields["l10n_do_require_buyer_vat"].help)
        self.assertTrue(fields["l10n_do_consumer_vat_threshold"].help)
