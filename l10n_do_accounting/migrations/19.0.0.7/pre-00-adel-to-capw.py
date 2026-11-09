"""Convert Adel data before CAPW initializes account.move and fiscal sequences.

shellfish_features depends on this module, so its own pre-migration is too
late for the conversion. Load only its migration script, not its addon package:
importing the package here would register dependent models before CAPW.
"""
import logging
from pathlib import Path
import runpy

from odoo.modules.module import get_module_path

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return
    cr.execute(
        """
        SELECT 1 FROM ir_module_module
         WHERE name IN ('dgii_reports', 'l10n_latam_invoice')
           AND state IN ('installed', 'to upgrade', 'to remove')
        UNION ALL
        SELECT 1 FROM information_schema.columns
         WHERE table_schema = current_schema()
           AND table_name = 'account_fiscal_sequence'
           AND column_name = 'fiscal_type_id'
        LIMIT 1
        """
    )
    if not cr.fetchone():
        _logger.info("Adel -> CAPW: no legacy localization to convert.")
        return

    module_path = get_module_path("shellfish_features", display_warning=False)
    if not module_path:
        raise RuntimeError(
            "Adel -> CAPW requires the shellfish_features conversion script "
            "before l10n_do_accounting can be upgraded."
        )
    script = Path(module_path) / "migrations" / "19.0.1.1.0" / "pre-migrate.py"
    namespace = runpy.run_path(str(script))
    if namespace.get("EARLY_ADEL_CONVERSION_API") != 1:
        raise RuntimeError(
            "shellfish_features must include the early Adel conversion guard. "
            "Deploy the matching submodule commits together."
        )
    _logger.info("Adel -> CAPW: converting before CAPW model initialization.")
    namespace["prepare_adel_conversion"](cr, version)
    _logger.info("Adel -> CAPW: early conversion completed.")
