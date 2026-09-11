# -*- coding: utf-8 -*-
"""Post-migración: preservación del NCF histórico tras el reemplazo de la
localización DO de Adel por la de CAPW/iterativo.

Corre DESPUÉS de que el módulo nuevo actualizó el esquema (ya existe la columna
`l10n_do_fiscal_number`) y cargó sus datos (los tipos de documento ya están
actualizados en sitio, con los mismos ids, por lo que `l10n_latam_document_type_id`
de cada factura sigue siendo válido).

En el módulo nuevo `l10n_latam_document_number` es COMPUTADO desde
`l10n_do_fiscal_number`. Como Adel guardaba el NCF directamente en
`l10n_latam_document_number`, aquí:
  1. Repoblamos `l10n_do_fiscal_number` (la nueva fuente de verdad) desde el
     respaldo hecho en pre-migrate, y reafirmamos `l10n_latam_document_number`.
  2. Marcamos `l10n_latam_manual_document_number` para que el sistema trate esos
     NCF como preexistentes y no intente re-secuenciarlos.
  3. Recomputamos los campos derivados (`l10n_latam_document_number`,
     `l10n_do_sequence_prefix`, `l10n_do_sequence_number`).
"""
import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return

    # Guardas: el respaldo y la columna nueva deben existir.
    cr.execute("SELECT to_regclass('public.l10n_do_migr_move_ncf_bak')")
    if not cr.fetchone()[0]:
        _logger.warning(
            "Post-migración: no existe l10n_do_migr_move_ncf_bak; se omite el "
            "repoblado de NCF (¿corrió el pre-migrate?)"
        )
        return

    cr.execute(
        """
        SELECT 1 FROM information_schema.columns
         WHERE table_name = 'account_move'
           AND column_name = 'l10n_do_fiscal_number'
        """
    )
    if not cr.fetchone():
        _logger.error(
            "Post-migración: falta la columna account_move.l10n_do_fiscal_number; "
            "el módulo nuevo no se cargó bien. Abortando repoblado de NCF."
        )
        return

    # 1) Repoblar la fuente de verdad + reafirmar el número visible ------------
    cr.execute(
        """
        UPDATE account_move m
           SET l10n_do_fiscal_number = b.ncf,
               l10n_latam_document_number = b.ncf,
               l10n_latam_manual_document_number = TRUE
          FROM l10n_do_migr_move_ncf_bak b
         WHERE m.id = b.move_id
           AND b.ncf IS NOT NULL
           AND b.ncf <> ''
        """
    )
    restored = cr.rowcount
    _logger.info("Post-migración: NCF repoblado en %s facturas", restored)

    # 2) Recomputar campos derivados desde l10n_do_fiscal_number ---------------
    cr.execute("SELECT move_id FROM l10n_do_migr_move_ncf_bak")
    move_ids = [r[0] for r in cr.fetchall()]

    env = api.Environment(cr, SUPERUSER_ID, {})
    moves = env["account.move"].browse(move_ids).exists()
    if moves:
        moves.modified(["l10n_do_fiscal_number"])
        env.flush_all()
        _logger.info(
            "Post-migración: recomputados campos fiscales de %s facturas",
            len(moves),
        )

    # 3) Fix de xmlid de grupos de impuestos -----------------------------------
    #    La localización busca `account.<cid>_tax_group_itbis` / `_tax_group_isr`
    #    vía env.ref() (p.ej. al renderizar la factura), pero la base heredada de
    #    Adel los tiene como `_group_itbis` / `_group_isr`. Sin esto la impresión
    #    de facturas falla con "External ID not found". Idempotente y no
    #    destructivo (agrega el xmlid nuevo apuntando al mismo registro).
    cr.execute(
        """
        INSERT INTO ir_model_data (module, name, model, res_id, noupdate,
                                   create_date, write_date)
        SELECT 'account', replace(d.name, '_group_', '_tax_group_'),
               d.model, d.res_id, true, now(), now()
          FROM ir_model_data d
         WHERE d.module = 'account'
           AND d.model  = 'account.tax.group'
           AND d.name ~ '^[0-9]+_group_(itbis|isr)$'
           AND NOT EXISTS (
                SELECT 1 FROM ir_model_data x
                 WHERE x.module = 'account'
                   AND x.name   = replace(d.name, '_group_', '_tax_group_')
           )
        """
    )
    if cr.rowcount:
        _logger.info(
            "Post-migración: %s xmlid(s) de grupo de impuestos remapeado(s) "
            "(_group_ -> _tax_group_)", cr.rowcount
        )

    # Nota: las tablas de respaldo (l10n_do_migr_move_ncf_bak,
    # l10n_do_migr_fiscal_sequence_bak) se conservan a propósito para auditoría.
    # Se pueden eliminar manualmente una vez validada la migración.
