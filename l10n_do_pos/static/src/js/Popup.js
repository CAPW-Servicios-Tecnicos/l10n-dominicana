//odoo.define('l10n_do_pos.DocumentTypeSelectInfoPopup', function(require) {
//    'use strict';
//
//    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
//    const Registries = require('point_of_sale.Registries');
//    const { posbus } = require('point_of_sale.utils')
//
//
//
//    class DocumentTypeSelectInfoPopup extends AbstractAwaitablePopup {
//        constructor() {
//            super(...arguments);
//            console.log(arguments)
//        }
//        async willStart() {
//            const order = this.env.pos.get_order();
//
//        }
//        change_doc_type_order(ev){
//
//            let doc_id = ev.target.value;
//            const current_order = this.env.pos.get_order()
//
//            let latam_doc_type =  this.env.pos.l10n_latam_document_types.filter(d => {
//                if(d.id == doc_id)
//                    current_order.set_latam_document_type(d);
//            })
//
//        }
//
//    }
//
//    DocumentTypeSelectInfoPopup.template = 'DocumentTypeSelectInfoPopup';
//    Registries.Component.add(DocumentTypeSelectInfoPopup);
//});
odoo.define('l10n_do_pos.DocumentTypeSelectInfoPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    class DocumentTypeSelectInfoPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
        }

        change_doc_type_order(ev) {
            let doc_id = parseInt(ev.target.value);
            const current_order = this.env.pos.get_order();
            const latam_doc_type = this.env.pos.l10n_latam_document_types.find(d => d.id === doc_id);

            if (latam_doc_type) {
                current_order.set_latam_document_type(latam_doc_type);
            } else {
                console.error('Document type not found for ID:', doc_id);
            }
        }
    }

    DocumentTypeSelectInfoPopup.template = 'DocumentTypeSelectInfoPopup';
    Registries.Component.add(DocumentTypeSelectInfoPopup);
});

