/** @odoo-module */
import { Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {
    setup() {
        super.setup(...arguments);
        this.agent = null;
        this.commision_value = null;
    },
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            agent: this.get_agent(),
            commision_value: this.get_commision_value(),
        };
    },
    set_agent(agent) {
        this.agent = agent;
    },
    get_agent() {
        return this.agent;
    },
    set_commision_value(commision_value) {
        this.commision_value = commision_value;
    },
    get_commision_value() {
        return this.commision_value;
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        return {
            ...json,
            agent_id: this.agent ? this.agent.id : false,
            commision_value_id: this.commision_value ? this.commision_value.id : false,
        };
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.agent = json.agent ? {
            id: json.agent.id,
            name: json.agent.name,
        } : null;

        this.commision_value = json.commision_value ? {
            id: json.commision_value.id,
            name: json.commision_value.name,
        } : null;
    },
    clone() {
        const orderline = super.clone();
        orderline.agent = this.agent;
        orderline.commision_value = this.commision_value;
        return orderline;
    },
});