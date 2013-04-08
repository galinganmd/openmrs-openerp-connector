openmrs-openerp-connector
=========================

This module adds hooks to the write and create function of the res.partner object to push data from the res_partner table of OpenERP to the OpenMRS patient table.

If a push does not occur, the record will be marked for synchronization and could be manually pushed in the button on the form at the Configuration menu.

The module uses the Philippine General Hospital module for Patient Enrollment created by Mr. Edwin Gonzales and Mr. Jaynar Santos and has been modified to incorporate the hooks on the Write and Create function.

Instructions on usage:

The module uses the python-mysqldb which is not commonly installed in Ubuntu distributions. On Ubuntu 12.04, the following installs the python-mysqldb module.

sudo apt-get install python-mysqldb

Installation then follows the same process of any other module in OpenERP. Upon cloning the repository to your computer, just copy the folder to the addons folder of OpenERP.

On Ubuntu 12.04: /usr/lib/pymodules/python2.7/openerp/addons/

Search for the module in the OpenERP client under the category "Extra" and install it. A new menu with the modified Philippine General Hospital Patient Enrollment Form appears. Each entry to this form pushes data directly to your OpenMRS installation once configured correctly.

The Configuration menu represents the MySQL database of your current OpenMRS implementation which comprises the IP address, port, username, password, database name and identifier_type that you want your OpenERP implementation to synchronize with in OpenMRS.
