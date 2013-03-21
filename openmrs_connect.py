import time
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from osv import fields, osv
from tools.translate import _
from connector import connect, connect_write, test_connect
import fcntl
import sys

class res_partner_custom(osv.osv):

    _name = "res.partner"
    _inherit = "res.partner"

    def get_whole_name(self, cr, uid, ids, field_name, arg, context):
        whole_name = {}
        for line in self.browse(cr, uid, ids ,context):
            if line.fname == False:
                fname = ''
            else:
                fname = ', ' + line.fname
            if line.mname == False:
                mname = ''
            else:
                mname = ' ' + line.mname
            whole_name[line.id] = str(line.name) + fname + mname
        return whole_name

    def _age(self, cr, uid, ids, name, arg, context={}):
        def compute_age_from_dates (patient_dob):
            now=datetime.now()
            if (patient_dob):
                dob=datetime.strptime(patient_dob,'%Y-%m-%d')
                delta=relativedelta (now, dob)
                years_months_days = str(delta.years) +"y "+ str(delta.months) +"m "+ str(delta.days)+"d"
            else:
                years_months_days = "No Birthdate!"

            return years_months_days
        result={}
        for patient_data in self.browse(cr, uid, ids, context=context):
                result[patient_data.id] = compute_age_from_dates (patient_data.birthdate)
        return result

    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['ref','name','fname','mname'], context=context)
        res = []
        for record in reads:
            if record['fname'] == False:
                fname = ''
            else:
                fname = ', ' + record['fname']
            if record['mname'] == False:
                mname = ''
            else:
                mname = ' ' + record['mname']
            if record['ref'] == False:
                ref = ''
            else:
                ref = "[" + record['ref'] + "] "
            name = ref + record['name'] + fname + mname
            res.append((record['id'], name))
        return res

    def copy(self, cr, uid, id, default=None, context=None):
        raise osv.except_osv(_('Restricted!!!'),_('Duplication could cause database desynchronization'))

    def create(self, cr, uid, vals, context={}):
        openmrs_object = self.pool.get('openmrs.connect')
        recId = openmrs_object.search(cr, uid, [], offset=0, limit=1, order=None, context=None, count=False)[0]
        username = openmrs_object.browse(cr, uid, recId, context={}).username
        ip_address = openmrs_object.browse(cr, uid, recId, context={}).ip_address
        port = openmrs_object.browse(cr, uid, recId, context={}).port
        password = openmrs_object.browse(cr, uid, recId, context={}).password
        database = openmrs_object.browse(cr, uid, recId, context={}).database
        identifier_type = openmrs_object.browse(cr, uid, recId, context={}).identifier_type

        res = super(res_partner_custom, self).create(cr, uid, vals)

        values = {}
        values['state'] = self.browse(cr, uid, res, context={}).address[0].state_id.name
        values['street'] = self.browse(cr, uid, res, context={}).address[0].street
        values['city'] = self.browse(cr, uid, res, context={}).address[0].city
        values['country'] = self.browse(cr, uid, res, context={}).address[0].country_id.name
        values['last'] = self.browse(cr, uid, res, context={}).name
        values['fname'] = self.browse(cr, uid, res, context={}).fname
        values['mname'] = self.browse(cr, uid, res, context={}).mname
        values['gender'] = self.browse(cr, uid, res, context={}).gender
        values['birthdate'] = self.browse(cr, uid, res, context={}).birthdate
        values['number'] = self.browse(cr, uid, res, context={}).ref
        values['mother'] = self.browse(cr, uid, res, context={}).mother.whole_name
        values['birthplace'] = self.browse(cr, uid, res, context={}).birthplace
        for item in values:
            if (values[item] is None) or (values[item] is False):
                values[item] = " "
        #raise osv.except_osv(_('Expecting an Agency Code'),_('IP adress is: %s' % values))
        try:
            id_openmrs = connect(ip_address, port, username, password, database, values, identifier_type)
            super(res_partner_custom, self).write(cr, uid, res, {'openmrs_number': id_openmrs}, context={})
            super(res_partner_custom, self).write(cr, uid, res, {'for_synchronization': False}, context={})
        except:
            super(res_partner_custom, self).write(cr, uid, res, {'for_synchronization': True}, context={})
        return res

    def write(self, cr, uid, ids, vals, context={}):
        res = super(res_partner_custom, self).write(cr, uid, ids, vals)
        openmrs_object = self.pool.get('openmrs.connect')
        recId = openmrs_object.search(cr, uid, [], offset=0, limit=1, order=None, context=None, count=False)[0]
        username = openmrs_object.browse(cr, uid, recId, context={}).username
        ip_address = openmrs_object.browse(cr, uid, recId, context={}).ip_address
        port = openmrs_object.browse(cr, uid, recId, context={}).port
        password = openmrs_object.browse(cr, uid, recId, context={}).password
        database = openmrs_object.browse(cr, uid, recId, context={}).database
        identifier_type = openmrs_object.browse(cr, uid, recId, context={}).identifier_type
        for rec in ids:
            values ={}
            values['state'] = self.browse(cr, uid, rec, context={}).address[0].state_id.name
            values['street'] = self.browse(cr, uid, rec, context={}).address[0].street
            values['city'] = self.browse(cr, uid, rec, context={}).address[0].city
            values['country'] = self.browse(cr, uid, rec, context={}).address[0].country_id.name
            values['last'] = self.browse(cr, uid, rec, context={}).name
            values['fname'] = self.browse(cr, uid, rec, context={}).fname
            values['mname'] = self.browse(cr, uid, rec, context={}).mname
            values['gender'] = self.browse(cr, uid, rec, context={}).gender
            values['birthdate'] = self.browse(cr, uid, rec, context={}).birthdate
            values['number'] = self.browse(cr, uid, rec, context={}).ref
            values['mother'] = self.browse(cr, uid, rec, context={}).mother.whole_name
            values['birthplace'] = self.browse(cr, uid, rec, context={}).birthplace
            patientid = self.browse(cr, uid, rec, context={}).openmrs_number
            #raise osv.except_osv(_('Expecting an Agency Code'),_('IP adress is: %s' % patientid))
            for item in values:
                if (values[item] is None) or (values[item] is False):
                    values[item] = " "
            #raise osv.except_osv(_('Expecting an Agency Code'),_('ids numbers: %s' % ids))
            if patientid != 0:
                try:
                    connect_write(ip_address, port, username, password, database, patientid, values, identifier_type)
                    super(res_partner_custom, self).write(cr, uid, rec, {'for_synchronization': False}, context={})
                except:
                    super(res_partner_custom, self).write(cr, uid, rec, {'for_synchronization': True}, context={})
            else:
                try:
                    id_openmrs = connect(ip_address, port, username, password, database, values, identifier_type)
                    super(res_partner_custom, self).write(cr, uid, rec, {'openmrs_number': id_openmrs}, context={})
                    super(res_partner_custom, self).write(cr, uid, rec, {'for_synchronization': False}, context={})

                except:
                    super(res_partner_custom, self).write(cr, uid, rec, {'for_synchronization': True}, context={})

        return True

    _columns = {
        'fname' : fields.char ('Firstname', size=50, required=True),
        'mname' : fields.char ('Middlename', size=50),
        'whole_name' : fields.function (get_whole_name, method=True, fnct_search=None, string="Name", type="char", size=150, store=True),
        'phone_no' : fields.char ('Phone No.', size=15),
        'gender' : fields.selection ([('Male','Male'), ('Female','Female')],'Gender'),
        'status' : fields.selection ([('Single','Single'), ('Married','Married'), ('Separated','Separated'), ('Divorced','Divorced'), ('Widowed','Widowed')],'Civil Status'),
        'birthdate' : fields.date ('Birthdate'),
        'age' : fields.function (_age, method=True, fnct_search=None, string="Age", type="char", size= 50,readonly=True),
        'birthplace' : fields.char ('Birthplace', size=100),
        'nationality' : fields.char ('Nationality', size=20),
        'religion' : fields.char ('Religion', size=20),
        'educ_attain' : fields.char ('Educ. Attain.', size=20),
        'occupation' : fields.char ('Occupation', size=20),
        'bus_name' : fields.char ('Name', size=100),
        'bus_address' : fields.char ('Address', size=200),
        'bus_phone_no' : fields.char ('Phone No.', size=15),
        'mother' : fields.many2one ('res.partner', 'Mother\'s Name', domain=[('customer', '=', 1)]),
        'mother_id' : fields.one2many ('res.partner', 'mother', 'Mother\'s Name'),
        'father' : fields.many2one ('res.partner', 'Father\'s Name', domain=[('customer', '=', 1)]),
        'father_id' : fields.one2many ('res.partner', 'father', 'Father\'s Name'),
        'spouse' : fields.many2one ('res.partner', 'Spouse\'s Name', domain=[('customer', '=', 1)]),
        'spouse_id' : fields.one2many ('res.partner', 'spouse', 'Spouse\'s Name'),
        'spouse_address' : fields.char ('Address', size=200),
        'spouse_empl' : fields.char ('Employer', size=100),
        'spouse_empl_address' : fields.char ('Address of Employer', size=200),
        'spouse_empl_phone_no' : fields.char ('Phone No. of Employer', size=15),
        'openmrs_number' : fields.integer('openmrs_number'),
        'for_synchronization' : fields.boolean ('For Synchronization'),

    }


    _defaults = {
        'birthdate': lambda * a: time.strftime('%Y-%m-%d'),
    }

res_partner_custom ()

class openmrs_connection(osv.osv):

    def create(self, cr, uid, vals, context={}):
        recIds = self.search(cr, uid, [], offset=0, limit=None, order=None, context=None, count=False)
        #raise osv.except_osv(_('Error:'),_('Cannot create more than one connection res = %s' % res))
        if len(recIds) >= 1:
            raise osv.except_osv(_('Error:'),_('Cannot create more than one connection'))
        else:
            res = super(openmrs_connection, self).create(cr, uid, vals)
            return res

    def test_sync(self, cr, uid, context={}, *args):
        recId = self.search(cr, uid, [], offset=0, limit=1, order=None, context=None, count=False)[0]
        openmrs_object = self.pool.get('openmrs.connect')
        username = openmrs_object.browse(cr, uid, recId, context={}).username
        ip_address = openmrs_object.browse(cr, uid, recId, context={}).ip_address
        port = openmrs_object.browse(cr, uid, recId, context={}).port
        password = openmrs_object.browse(cr, uid, recId, context={}).password
        database = openmrs_object.browse(cr, uid, recId, context={}).database
        try:
            test_connect(ip_address, port, username, password, database)
            message = 'accepted'
        except:
            message = 'failed'

        raise osv.except_osv(_('Connection Status:'),_('Connection %s' % message))

    def synchronize(self, cr, uid, *args):
        syncIds = self.pool.get('res.partner').search(cr, uid, [('for_synchronization', '=', True)], offset=0, limit=None, order=None, context=None, count=False)
        self.pool.get('res.partner').write(cr, uid, syncIds, {}, context={})
        raise osv.except_osv(_('Synchronization:'),_('Complete'))


    _name = "openmrs.connect"
    _columns = {
        'ip_address' : fields.char ('ip_address', size=50, help='IP address of your OpenMRS mysql server' ),
        'port' : fields.char ('port', size=50, help='port of your OpenMRS mysql server'),
        'username' : fields.char ('username', size=50, help='Username of your OpenMRS mysql server'),
        'password' :fields.char ('password', size=50, help='Password of your OpenMRS mysql server'),
        'database' :fields.char ('database', size=50, help='Database of OpenMRS in your mysql server'),
        'identifier_type' : fields.integer('identifier_type', help='ID of the identifier type \n Ex. 2 for Old OpenMRS Identifier'),
    }

openmrs_connection()

