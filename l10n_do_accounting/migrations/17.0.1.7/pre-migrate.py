# -*- coding: utf-8 -*-
"""Pre-migración: reemplazo de la localización DO de Adel Networks por la de
CAPW/iterativo dentro del MISMO nombre técnico `l10n_do_accounting`.

Corre ANTES de que Odoo actualice el esquema y cargue el XML/CSV nuevo. Deja la
base en un estado desde el cual el módulo nuevo puede cargar sin romper y sin
perder el NCF histórico. El repoblado del NCF se hace en post-migrate.py.

Qué hace:
  1. Respalda `account_fiscal_sequence` (modelo Adel que Odoo eliminará).
  2. Respalda el NCF histórico (`l10n_latam_document_number` + tipo) por factura.
     En el módulo nuevo `l10n_latam_document_number` pasa a ser COMPUTADO desde
     `l10n_do_fiscal_number`; sin este respaldo el recompute borraría el NCF.
  3. Protege los tipos de documento Adel que el CSV nuevo NO trae (p.ej.
     `non_fiscal`) para que el _process_end no intente borrarlos (evita choques
     con el FK RESTRICT de account_fiscal_sequence).
  4. Elimina las vistas Adel huérfanas que referencian campos ya inexistentes
     (p.ej. `account.move.tax_line_ids`) y romperían la validación de vistas.
"""
import logging

_logger = logging.getLogger(__name__)

# Módulos de la localización vieja (Adel) que comparten nombre técnico con la
# nueva y cuyas vistas huérfanas hay que eliminar.
OLD_MODULES = ("l10n_do_accounting", "l10n_do_pos")

# Módulo ADHOC que la localización nueva reemplaza por el oficial
# `l10n_latam_invoice_document`. Sin código en la rama 19.0, queda "to upgrade"
# y sus vistas rompen la validación de account.move. Se limpia y se neutraliza.
ADHOC_MODULE = "l10n_latam_invoice"

# Todos los módulos cuyas vistas huérfanas se eliminan.
VIEW_CLEANUP_MODULES = OLD_MODULES + (ADHOC_MODULE,)

# xmlids de tipos de documento que provee el CSV de la localización NUEVA
# (l10n_do_accounting/data/l10n_latam.document.type.csv). Los tipos Adel con
# estos mismos xmlids se actualizan en sitio; el resto se "desadopta" para que
# sobreviva al cleanup.
NEW_DOCTYPE_XMLIDS = (
    "ncf_fiscal_client", "ncf_consumer_supplier", "ncf_debit_note_client",
    "ncf_credit_note_client", "ncf_informal_supplier", "ncf_unique_client",
    "ncf_minor_supplier", "ncf_special_client", "ncf_gov_client",
    "ncf_export_client", "ncf_exterior_supplier", "non_fiscal_import_supplier",
    "ecf_fiscal_client", "ecf_consumer_supplier", "ecf_debit_note_client",
    "ecf_credit_note_client", "ecf_informal_supplier", "ecf_minor_supplier",
    "ecf_special_client", "ecf_gov_client", "ecf_export_client",
    "ecf_exterior_supplier",
)


def migrate(cr, version):
    if not version:
        return  # instalación limpia: nada que migrar

    # 1) Respaldo de las secuencias fiscales Adel -------------------------------
    cr.execute("SELECT to_regclass('public.account_fiscal_sequence')")
    if cr.fetchone()[0]:
        cr.execute(
            "CREATE TABLE IF NOT EXISTS l10n_do_migr_fiscal_sequence_bak AS "
            "TABLE account_fiscal_sequence"
        )
        _logger.info("Pre-migración: respaldo de account_fiscal_sequence")

    # 2) Respaldo del NCF histórico por factura --------------------------------
    #    Antes de que el campo pase a computado. Se usa en post-migrate.
    cr.execute("DROP TABLE IF EXISTS l10n_do_migr_move_ncf_bak")
    cr.execute(
        """
        CREATE TABLE l10n_do_migr_move_ncf_bak AS
        SELECT id AS move_id,
               l10n_latam_document_number AS ncf,
               l10n_latam_document_type_id AS type_id
          FROM account_move
         WHERE l10n_latam_document_number IS NOT NULL
           AND l10n_latam_document_number <> ''
        """
    )
    cr.execute("SELECT count(*) FROM l10n_do_migr_move_ncf_bak")
    _logger.info(
        "Pre-migración: respaldados %s NCF históricos", cr.fetchone()[0]
    )

    # 3) Proteger los tipos de documento Adel que el CSV nuevo no trae ----------
    cr.execute(
        """
        DELETE FROM ir_model_data
         WHERE module = 'l10n_do_accounting'
           AND model = 'l10n_latam.document.type'
           AND name NOT IN %s
        """,
        (NEW_DOCTYPE_XMLIDS,),
    )
    if cr.rowcount:
        _logger.info(
            "Pre-migración: %s tipo(s) de documento Adel desadoptado(s) para "
            "que sobrevivan al cleanup", cr.rowcount
        )

    # 4) Eliminar vistas huérfanas (Adel + ADHOC) ------------------------------
    #    Referencian campos/modelos ya inexistentes (p.ej. tax_line_ids) y
    #    romperían la validación del árbol de account.move.
    cr.execute(
        """
        SELECT res_id FROM ir_model_data
         WHERE model = 'ir.ui.view' AND module IN %s
        """,
        (VIEW_CLEANUP_MODULES,),
    )
    view_ids = tuple(r[0] for r in cr.fetchall())
    if view_ids:
        _logger.info(
            "Pre-migración: eliminando %s vistas huérfanas (Adel/ADHOC)",
            len(view_ids),
        )
        cr.execute("DELETE FROM ir_ui_view WHERE id IN %s", (view_ids,))
    cr.execute(
        "DELETE FROM ir_model_data WHERE model = 'ir.ui.view' AND module IN %s",
        (VIEW_CLEANUP_MODULES,),
    )

    # 5) Neutralizar el módulo ADHOC l10n_latam_invoice ------------------------
    #    No tiene código en la rama 19.0 (se reemplaza por el oficial
    #    l10n_latam_invoice_document). Se marca como desinstalado para que deje
    #    de quedar "to upgrade" y no bloquee la carga. Los campos que aportaba
    #    (l10n_latam_document_number/type_id) los provee el módulo oficial, así
    #    que las columnas quedan válidas.
    cr.execute(
        "UPDATE ir_module_module SET state = 'uninstalled' "
        "WHERE name = %s AND state != 'uninstalled'",
        (ADHOC_MODULE,),
    )
    if cr.rowcount:
        _logger.info(
            "Pre-migración: módulo ADHOC %s marcado como desinstalado",
            ADHOC_MODULE,
        )
