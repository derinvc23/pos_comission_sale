/** @odoo-module */

import {Component} from "@odoo/owl";
import {ProductScreen} from "@point_of_sale/app/screens/product_screen/product_screen";
import {ErrorPopup} from "@point_of_sale/app/errors/popups/error_popup";
import {SelectionPopup} from "@point_of_sale/app/utils/input_popups/selection_popup";
import {usePos} from "@point_of_sale/app/store/pos_hook";
import {useService} from "@web/core/utils/hooks";
import {_t} from "@web/core/l10n/translation";

export class SelectAgentButton extends Component {
    static template = "point_of_sale.SelectAgentButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
        this.dialog = useService("dialog");
        this.orm = useService("orm");
    }

    async selectAgent() {
        const order = this.pos.get_order();
        const selectedLine = order.get_selected_orderline();

        if (!selectedLine) {
            await this.popup.add(ErrorPopup, {
                title: _t('Ninguna linea Seleccionada'),
                body: _t('Porfavor seleccione una linea para asignar un agente'),
            });
            return;
        }

        // Obtener la lista de agentes
        const agents = await this.orm.call(
            'res.partner',
            'search_read',
            [[['is_agent', '=', true]], ['id', 'name']],
        );

        var {confirmed, payload: selectedAgent} = await this.popup.add(SelectionPopup, {
            title: _t('Seleccionar Agente'),
            list: agents.map(agent => ({
                id: agent.id,
                label: agent.name,
                item: agent,
            })),
        });

        // Obtener la lista de agentes
        const commision_type = await this.orm.call(
            'pos.commission.type',
            'search_read',
            [[['active', '=', true]], ['id', 'name', 'value']],
        );


        /*if (confirmed) {
            selectedLine.set_agent({
                id: selectedAgent.id,
                name: selectedAgent.name,
                commission_percentage: selectedAgent.commission_percentage,
            });
        }*/
        if (confirmed) {
            selectedLine.set_agent({
                id: selectedAgent.id,
                name: selectedAgent.name,
            });
        }

        var {confirmed, payload: selectedCommision} = await this.popup.add(SelectionPopup, {
            title: _t('Porcentaje'),
            list: commision_type.map(comm => ({
                id: comm.id,
                label: selectedAgent.name + ',' + comm.name,
                item: comm,
            })),
        });
        if (confirmed) {
            selectedLine.set_commision_value({
                id: selectedCommision.id,
                name: selectedCommision.name,
            });
        }
    }
}

ProductScreen.addControlButton({
    component: SelectAgentButton,
});