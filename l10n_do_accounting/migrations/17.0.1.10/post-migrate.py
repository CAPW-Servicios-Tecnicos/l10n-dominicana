import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """El grupo de campos fiscales de contactos ya no implica Contabilidad /
    Administrador. Como el registro es noupdate, hay que quitar el vinculo a mano.

    Los usuarios que ya recibieron Administrador por este grupo lo conservan:
    no se puede distinguir de una asignacion directa, asi que solo se listan
    en el log para revisarlos manualmente.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    fiscal_group = env.ref(
        "l10n_do_accounting.group_l10n_do_edit_fiscal_partner",
        raise_if_not_found=False,
    )
    manager_group = env.ref("account.group_account_manager", raise_if_not_found=False)
    if not fiscal_group or not manager_group:
        return

    fiscal_group.implied_ids = [(3, manager_group.id)]

    users = fiscal_group.users.filtered(
        lambda u: manager_group in u.groups_id
        and u.id not in (SUPERUSER_ID, env.ref("base.user_admin").id)
    )
    if users:
        _logger.warning(
            "Usuarios con 'Puede modificar campos fiscales de contactos' que "
            "tienen Contabilidad / Administrador; revisar si lo necesitan: %s",
            ", ".join(f"{u.login} (id {u.id})" for u in users),
        )
