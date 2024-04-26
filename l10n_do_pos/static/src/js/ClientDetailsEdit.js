odoo.define('point_of_sale.ClientDetailsEdit', function(require) {
    'use strict';

    const { _t } = require('web.core');
    const { getDataURLFromFile } = require('web.utils');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class ClientDetailsEdit extends PosComponent {
        constructor() {
            super(...arguments);
            this.loading = false;
            this.widget = {};
            this.intFields = ['country_id', 'state_id', 'property_product_pricelist'];
            const partner = this.props.partner || {};
            this.changes = {
                'country_id': partner.country_id && partner.country_id[0],
                'state_id': partner.state_id && partner.state_id[0],
                'l10n_do_dgii_tax_payer_type': partner.l10n_do_dgii_tax_payer_type || "non_payer",
                'vat': partner.vat
            };
            if (!partner.property_product_pricelist)
                this.changes['property_product_pricelist'] = this.env.pos.default_pricelist.id;
        }
        mounted() {
            this.env.bus.on('save-customer', this, this.saveChanges);
        }
        willUnmount() {
            this.env.bus.off('save-customer', this);
        }
        get partnerImageUrl() {
            const partner = this.props.partner;
            if (this.changes.image_1920) {
                return this.changes.image_1920;
            } else if (partner.id) {
                return `/web/image?model=res.partner&id=${partner.id}&field=image_128&write_date=${partner.write_date}&unique=1`;
            } else {
                return false;
            }
        }

        async hasInvoices(partnerId) {
            try {
                const response = await this.rpc({
                    route: '/check_invoices',
                    params: { partner_id: partnerId },
                });
                return response.has_invoices;
            } catch (error) {
                console.error(error);
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('An error occurred while checking invoices.'),
                });
                return false;
            }
        }

        /**
        * Save to field `changes` all input changes from the form fields.
        */
        captureChange(event) {
            const name = event.target.name;
            const value = event.target.value;

            this.changes[name] = value;

            if (name === 'vat') {
                this.widget.loading = true;
                this.checkVat(value).finally(() => {
                    this.widget.loading = false;
                });
            }
        }

        async checkVat(vatValue) {
            try {
                this.loading = true; // Activar indicador de carga

                const response = await this.rpc({
                    route: '/dgii/get_contribuyentes',
                    params: { vat: vatValue },
                });

                console.log("DGII Response:", response); // Imprimir la respuesta para depurar

                // Verificar el formato de la respuesta antes de continuar
                if (typeof response !== 'object' || response === null || response.error) {
                    await this.showPopup('ErrorPopup', {
                        title: this.env._t('Error'),
                        body: this.env._t(response && response.error ? response.error : 'Invalid response from DGII.'),
                    });
                    return;
                }

                if (response.warning) {
                    await this.showPopup('ErrorPopup', {
                        title: this.env._t('Warning'),
                        body: this.env._t(response.warning.message),
                    });
                } else if (response.name) {
                    this.changes['name'] = response.name;
                    console.log('Assigned name from DGII:', response.name);  // Registro de consola
                    this.render();
                }
            } catch (error) {
                console.error(error);
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Network Error'),
                    body: this.env._t('Unable to connect. Please check your network connection.'),
                });
            } finally {
                this.loading = false; // Desactivar indicador de carga al finalizar
            }
        }

        async saveChanges() {
            let processedChanges = {};
            const partner = this.props.partner || {};

            for (let [key, value] of Object.entries(this.changes)) {
                if (this.intFields.includes(key)) {
                    processedChanges[key] = parseInt(value, 10) || false;
                } else {
                    processedChanges[key] = value;
                }
            }

            // Comprobar si el contacto tiene facturas registradas y publicadas
            const hasInvoices = await this.hasInvoices(partner.id);

            if (hasInvoices) {
                return this.showPopup('ErrorPopup', {
                    title: this.env._t('Error'),
                    body: this.env._t('Cannot change the RNC for a contact with registered and published invoices.'),
                });
            }

            if ((!partner.name && !processedChanges.name) || processedChanges.name === '') {
                return this.showPopup('ErrorPopup', {
                    title: _t('A Customer Name Is Required'),
                });
            }

            // Antes de la validación
            console.log("Partner:", partner);
            console.log("Processed Changes:", processedChanges);
            const newTaxPayerType = processedChanges.l10n_do_dgii_tax_payer_type;
            const newVat = processedChanges.vat;
            console.log("newTaxPayerType:", newTaxPayerType);
            console.log("newVat:", newVat);

            // 1. Si l10n_do_dgii_tax_payer_type es diferente de 'non_payer', el vat es obligatorio
            if (newTaxPayerType !== 'non_payer' && newVat === '') {
                return this.showPopup('ErrorPopup', {
                    title: _t('VAT Required for Tax Payers'),
                    body: _t('A VAT number is required for tax payers.')
                });
            }

            // 2. Si l10n_do_dgii_tax_payer_type es igual a 'non_payer', el vat no es obligatorio
//            if (newTaxPayerType === 'non_payer' && newVat !== '') {
//                return this.showPopup('ErrorPopup', {
//                    title: _t('VAT Not Required for Non-Payers'),
//                    body: _t('VAT should not be present for non-payers.')
//                });
//            }

            // 3. Si ambos valores cambian, se valida primero l10n_do_dgii_tax_payer_type
            if (processedChanges.l10n_do_dgii_tax_payer_type && processedChanges.vat) {
                if (newTaxPayerType !== 'non_payer' && newVat === '') {
                    return this.showPopup('ErrorPopup', {
                        title: _t('VAT Required for Tax Payers'),
                        body: _t('A VAT number is required for tax payers.')
                    });
                }
            }

            // 4. Si l10n_do_dgii_tax_payer_type es igual a 'taxpayer', el vat es obligatorio
            if (newTaxPayerType === 'taxpayer' && newVat === '') {
                return this.showPopup('ErrorPopup', {
                    title: _t('VAT Required for Tax Payers'),
                    body: _t('A VAT number is required for tax payers.')
                });
            }

            processedChanges.id = partner.id || false;
            this.trigger('save-changes', { processedChanges });
        }

        async uploadImage(event) {
            const file = event.target.files[0];
            if (!file.type.match(/image.*/)) {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Unsupported File Format'),
                    body: this.env._t('Only web-compatible Image formats such as .png or .jpeg are supported.'),
                });
            } else {
                const imageUrl = await getDataURLFromFile(file);
                const loadedImage = await this._loadImage(imageUrl);
                if (loadedImage) {
                    const resizedImage = await this._resizeImage(loadedImage, 800, 600);
                    this.changes.image_1920 = resizedImage.toDataURL();
                    this.render();
                }
            }
        }

        _resizeImage(img, maxwidth, maxheight) {
            var canvas = document.createElement('canvas');
            var ctx = canvas.getContext('2d');
            var ratio = 1;

            if (img.width > maxwidth) {
                ratio = maxwidth / img.width;
            }
            if (img.height * ratio > maxheight) {
                ratio = maxheight / img.height;
            }
            var width = Math.floor(img.width * ratio);
            var height = Math.floor(img.height * ratio);

            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img, 0, 0, width, height);
            return canvas;
        }
        /**
         * Loading image is converted to a Promise to allow await when
         * loading an image. It resolves to the loaded image if succesful,
         * else, resolves to false.
         *
         * [Source](https://stackoverflow.com/questions/45788934/how-to-turn-this-callback-into-a-promise-using-async-await)
         */
        _loadImage(url) {
            return new Promise((resolve) => {
                const img = new Image();
                img.addEventListener('load', () => resolve(img));
                img.addEventListener('error', () => {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Loading Image Error'),
                        body: this.env._t('Encountered error when loading image. Please try again.')
                    });
                    resolve(false);
                });
                img.src = url;
            });
        }
    }
    ClientDetailsEdit.template = 'ClientDetailsEdit';

    Registries.Component.add(ClientDetailsEdit);

    return ClientDetailsEdit;
});