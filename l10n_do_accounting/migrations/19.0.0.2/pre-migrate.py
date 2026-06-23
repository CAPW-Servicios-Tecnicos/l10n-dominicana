# -*- coding: utf-8 -*-
"""Pre-migración BOAT-MAX 16 -> 19.

Corre ANTES del _auto_init de l10n_do_accounting (que crea el índice único de
NCF) y antes de la carga de vistas de res.partner. Deja la BD lista para que el
upgrade de odoo.sh no falle. Idempotente (seguro re-ejecutar).

Hace, en una sola pasada y por SQL (saltando constrains de ORM):
  1) Deduplica los NCF de compras (marca los sobrantes con sufijo /DUP-<id> y los
     respalda en z_ncf_dup_backup) para que el índice único se pueda crear.
  2) Desactiva las vistas de los módulos sin código (Elytek/faltantes) que
     referencian campos inexistentes.
  3) Neutraliza a no-op las vistas HEREDADAS de pak_pier (arch 16.0 viejo); el
     -u de cada módulo las repuebla con su arch 19.0.
"""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return  # solo en upgrade real, no en instalación nueva

    # ---- 1) Deduplicar NCF de compras (manual=TRUE) ----
    cr.execute("""
        CREATE TABLE IF NOT EXISTS z_ncf_dup_backup (
            snapshot_at timestamp DEFAULT now(), move_id integer, name varchar,
            state varchar, ncf_original varchar, commercial_partner_id integer,
            company_id integer, amount_total numeric)
    """)
    cr.execute("""
        WITH grp AS (
          SELECT id, l10n_do_fiscal_number AS ncf, commercial_partner_id AS partner,
                 company_id, state, amount_total, name,
                 row_number() OVER (PARTITION BY l10n_do_fiscal_number, commercial_partner_id, company_id
                                    ORDER BY (state='posted') DESC, id ASC) AS rn,
                 count(*)     OVER (PARTITION BY l10n_do_fiscal_number, commercial_partner_id, company_id) AS cnt
          FROM account_move
          WHERE l10n_latam_document_type_id IS NOT NULL
            AND move_type IN ('in_invoice','in_refund')
            AND l10n_latam_manual_document_number IS TRUE
            AND l10n_do_fiscal_number IS NOT NULL AND l10n_do_fiscal_number <> ''
            AND l10n_do_fiscal_number NOT LIKE '%/DUP-%'
        )
        SELECT id, ncf, partner, company_id, state, amount_total, name
        FROM grp WHERE cnt > 1 AND rn > 1
    """)
    losers = cr.fetchall()
    if losers:
        cr.executemany(
            "INSERT INTO z_ncf_dup_backup "
            "(move_id,name,state,ncf_original,commercial_partner_id,company_id,amount_total) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)",
            [(r[0], r[6], r[4], r[1], r[2], r[3], r[5]) for r in losers],
        )
        cr.execute(
            "UPDATE account_move "
            "SET l10n_do_fiscal_number = l10n_do_fiscal_number || '/DUP-' || id::text "
            "WHERE id IN %s", (tuple(r[0] for r in losers),))
        _logger.info("BOATMAX pre-migrate: %s NCF duplicados marcados /DUP", len(losers))

    # ---- 2) Desactivar vistas de módulos sin código ----
    cr.execute("""
        UPDATE ir_ui_view SET active = false
        WHERE id IN (SELECT res_id FROM ir_model_data WHERE model='ir.ui.view'
                     AND module IN ('pak_elytek_base','pak_elytek_ncf_management',
                                    'pak_elytek_rnc_management','pak_inputs_outputs',
                                    'odoo_direct_print','pak_pier_simulate_contracts_invoice'))
    """)
    _logger.info("BOATMAX pre-migrate: vistas de módulos sin código desactivadas (%s)", cr.rowcount)

    # ---- 3) Neutralizar vistas heredadas pak_pier (el -u las repuebla) ----
    cr.execute("""
        UPDATE ir_ui_view SET arch_db = '{"en_US": "<data/>"}'::jsonb
        WHERE inherit_id IS NOT NULL
          AND id IN (SELECT res_id FROM ir_model_data WHERE model='ir.ui.view'
                     AND module IN ('pak_pier_base','pak_pier_boat_management',
                                    'pak_pier_service_invoices','pak_pier_penalties_managment',
                                    'pak_pier_contract_management','pak_pier_invoice_to_visitors',
                                    'pak_pier_late_payment','pak_pier_report_payments',
                                    'pak_pier_payment_extend'))
    """)
    _logger.info("BOATMAX pre-migrate: vistas heredadas pak_pier neutralizadas (%s)", cr.rowcount)
