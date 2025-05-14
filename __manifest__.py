{
    "name": "Comision en punto de venta",
    "summary": """
            Asignar comisiones al punto de venta""",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "DerinDickson",
    "depends": ["point_of_sale"],
    "data": [
        "data/commission_sequence.xml",
        "security/ir.model.access.csv",
        "views/commission_type_views.xml",
        "views/commission_views.xml",
        "views/menuitem_data.xml",
        "views/pos_commission_views.xml",
        "views/pos_order_views.xml",
        "views/res_partner_views.xml"
    ],
    'installable': True,
    'auto_install': False,
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_comission_sale/static/src/app/models.js",
            "pos_comission_sale/static/src/app/screens/product_screen/control_buttons/select_agent_button/select_agent_button.js",
            "pos_comission_sale/static/src/app/screens/product_screen/control_buttons/select_agent_button/select_agent_button.xml",
            "pos_comission_sale/static/src/app/screens/product_screen/orderline.xml",
            "pos_comission_sale/static/src/app/screens/product_screen/orderline.scss",
        ],
    },
    'license': 'LGPL-3',
}
