odoo.define('l10n_do_pos.PaymentScreen', function (require) {
    "use strict";

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    var { Gui } = require('point_of_sale.Gui');
    var core = require('web.core');
    var _t = core._t;
    const Dialog = require('web.Dialog');
const PaymentScreenCustom = PaymentScreen => class extends PaymentScreen {
        constructor() {
            super(...arguments);
            useListener('js_set_latam_document_type', this.click_set_latam_document_type);
            };

        click_set_latam_document_type() {

            var self = this;
            var current_order = self.env.pos.get_order();
            var client = self.env.pos.get_client();

            var ncf_types_data = self.env.pos.ncf_types_data.issued['non_payer'];
            if (client && client.l10n_do_dgii_tax_payer_type)
                ncf_types_data = self.env.pos.ncf_types_data.issued[client.l10n_do_dgii_tax_payer_type];

            var latam_document_type_list =
                _.map(self.env.pos.l10n_latam_document_types,
                    function (latam_document_type) {
                        if (latam_document_type.internal_type === 'invoice' &&
                            ncf_types_data.includes(latam_document_type.l10n_do_ncf_type)) {
                            return {
                                label: latam_document_type.name,
                                item: latam_document_type,
                            };
                        }
                        return false;
                    });

            this.showPopup('DocumentTypeSelectInfoPopup', { latam_document_type_list: latam_document_type_list, client: client, current_order: current_order, l10n_latam_document_type:self.env.pos.l10n_latam_document_type });
        }

    };
    Registries.Component.extend(PaymentScreen, PaymentScreenCustom);

    return PaymentScreen;
    });