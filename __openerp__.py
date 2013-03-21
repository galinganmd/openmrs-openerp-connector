{

    'name' : 'OpenMRS Connection module',
    'version' : '0.1',
    'author' : 'Jonathan D. Galingan',
    'category' : 'Generic Modules/Others',
    'complexity': "easy",
    'depends' : [],
    'description' : """

OpenERP-OpenMRS Demographics Synchronization

This module adds hooks to the write and create function of the
res.partner object to push data from the res_partner table of
OpenERP to the OpenMRS patient table.

If a push does not occur, the record will be marked for
synchronization and could be manually pushed in the button
on the form at the Configuration menu.

""",
    "website" : "",
    "init_xml" : [],
    "update_xml" : ["security/security.xml","openmrs_connect.xml", "data/config_data.xml", "security/ir.model.access.csv"],
    "active": False,
    "installable": True,
}
