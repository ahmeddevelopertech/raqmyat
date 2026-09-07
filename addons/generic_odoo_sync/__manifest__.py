{
    "name": "Generic Odoo Two Way Sync",
    "version": "1.0",
    "category": "Tools",
    "auther": "Eng/Mohamed Ramah Elgary",
    "summary": "Dynamic Two-Way Sync between Odoo systems",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/sync_config_views.xml",
        "views/sync_log_views.xml",
        "views/menu.xml",
        # "data/sync_cron.xml",
    ],
    "installable": True,
    "application": True,
}
