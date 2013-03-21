import MySQLdb
import time
MySQLdb.paramstyle
from datetime import datetime
import fcntl
import time
import sys

def connect(ip_address, port1, username, password, database, values, identifier_type):
    port1 = int(port1)
    connMRS = MySQLdb.connect (host = ip_address,
        port=port1,
        user=username,
        passwd = password,
        db=database)
    # Map ids values of OpenERP to OpenMRS table

    caseno = values['number']
    gender = values['gender']
    if gender == 'Male':
        gender = 'M'
    elif gender == 'Female':
        gender = 'F'
    else:
        gender = 'F'
    bdate = values['birthdate']
    crdate = datetime.today().strftime('%Y-%m-%d')
    st = values['street']
    city = values['city']
    state = values['state']
    fname = values['fname']
    mname = values['mname']
    lname = values['last']
    sufname = ""
    brgy = "NA"
    town ="NA"
    bplace = values['birthplace']
    mothrname = values['mother']
    for item in values:
        if (values[item] is None) or (values[item] is False):
            values[item] = "_"

    #insert on person table
    cursoromrs1 = connMRS.cursor()
    inspersonstmnt = """INSERT INTO person(gender,birthdate,birthdate_estimated,dead,\
                  creator,date_created,voided,\
                  uuid) \
                  VALUES(%s, %s,'0','0', '1',%s,'0', uuid())"""
    cursoromrs1.execute(inspersonstmnt, (gender, bdate, crdate))
    patientid = int(cursoromrs1.lastrowid)
    cursoromrs1.execute("commit")
    cursoromrs1.close()

    #get uuid from person table insert and alias as uuid1
    cursoromrs1a = connMRS.cursor()
    uuidStmnt1 = 'SELECT uuid FROM person WHERE person_id = %s' % patientid
    cursoromrs1a.execute(uuidStmnt1)
    uuidResult1 = cursoromrs1a.fetchall()
    uuid1 = uuidResult1[0][0]
    cursoromrs1a.close()

    #insert into patient table
    cursoromrs2 = connMRS.cursor()
    inspatientstmnt = """INSERT INTO patient (patient_id,creator,date_created) \
    VALUES(%s,1,%s)"""
    cursoromrs2.execute(inspatientstmnt, (patientid, crdate))
    cursoromrs2.execute("commit")
    cursoromrs2.close()

    #insert into patient_identifier table
    #cursoromrs3 = connMRS.cursor()
    #inspatientidentstmnt = """INSERT INTO patient_identifier (patient_id, \
    #identifier,identifier_type,preferred , location_id, creator, date_created,uuid) \
    #VALUES( %s, %s ,2, 1, 1, 1, %s , uuid())"""
    #cursoromrs3.execute(inspatientidentstmnt, (patientid, currmaxpinomrs, crdate))
    #cursoromrs3.execute("commit")
    #cursoromrs3.close()

    #insert into patient_identifier table
    cursoromrs4 = connMRS.cursor()
    inscasestmnt = """INSERT INTO patient_identifier (patient_id, \
    identifier,identifier_type,preferred , location_id, creator, date_created,uuid) \
    VALUES( %s, %s , %s, 1, 1, 1, %s , uuid())"""
    cursoromrs4.execute(inscasestmnt, (patientid, caseno, identifier_type, crdate))
    cursoromrs4.execute("commit")
    cursoromrs4.close()

    #insert into person_address table
    cursoromrs5 = connMRS.cursor()
    inspersonaddstmnt = """INSERT INTO person_address (person_id, preferred, \
    address1, city_village, state_province, creator, date_created, uuid) \
    VALUES (%s, 1, %s, %s, %s, 1, %s, uuid())"""
    cursoromrs5.execute(inspersonaddstmnt, (patientid,  st, brgy, town, crdate))
    cursoromrs5.execute("commit")
    # print"person_id %s" % (patientid)
    cursoromrs5.close()

    #insert into person_name table
    cursoromrs6 = connMRS.cursor()
    inspersonnamestmnt = """INSERT INTO person_name (preferred,person_id,given_name, \
    middle_name,family_name,family_name_suffix,creator,date_created,uuid) \
    VALUES(1,%s,%s,%s,%s,%s,1,%s,uuid())"""
    cursoromrs6.execute(inspersonnamestmnt, (patientid,  fname, mname, lname, sufname, crdate))
    cursoromrs6.execute("commit")
    cursoromrs6.close()

    #insert birthplace into person_attribute table
    cursoromrs7 = connMRS.cursor()
    inspersonbplace = """INSERT INTO person_attribute(person_id, value, person_attribute_type_id, \
    creator, date_created, voided, uuid)  VALUES (%s, %s, %s, %s, %s, %s, uuid())"""
    cursoromrs7.execute(inspersonbplace, (patientid, bplace, 2, 1, crdate, 0))
    cursoromrs7.close()

    #insert mother name into person_attribute table
    cursoromrs8 = connMRS.cursor()
    inspersonmoname = """INSERT INTO person_attribute(person_id, value, person_attribute_type_id, \
    creator, date_created, voided, uuid)  VALUES (%s, %s, %s, %s, %s, %s, uuid())"""
    cursoromrs8.execute(inspersonmoname, (patientid, mothrname, 4, 1, crdate, 0))
    cursoromrs8.execute("commit")
    # print"person_id %s" % (patientid)
    cursoromrs8.close()

    return patientid

def connect_write(ip_address, port1, username, password, database, patientid, values, identifier_type):
    port1 = int(port1)
    connMRS = MySQLdb.connect (host = ip_address,
        port=port1,
        user=username,
        passwd = password,
        db=database)
    # Map ids values of OpenERP to OpenMRS table

    caseno = values['number']
    gender = values['gender']
    if gender == 'Male':
        gender = 'M'
    elif gender == 'Female':
        gender = 'F'
    else:
        gender = 'F'
    bdate = values['birthdate']
    crdate = datetime.today().strftime('%Y-%m-%d')
    st = values['street']
    city = values['city']
    state = values['state']
    fname = values['fname']
    mname = values['mname']
    lname = values['last']
    sufname = ""
    brgy = "NA"
    town ="NA"
    bplace = values['birthplace']
    mothrname = values['mother']


    #update person table
    cursoromrs1 = connMRS.cursor()
    inspersonstmnt = """UPDATE person SET gender = %s, birthdate = %s where person_id = %s """
    cursoromrs1.execute(inspersonstmnt, (gender, bdate, patientid))
    cursoromrs1.execute("commit")
    cursoromrs1.close()


    #update patient_identifier table
    cursoromrs4 = connMRS.cursor()
    inscasestmnt = """UPDATE patient_identifier SET identifier = %s where patient_id = %s  and identifier_type = %s """
    cursoromrs4.execute(inscasestmnt, (caseno, patientid, identifier_type))
    cursoromrs4.execute("commit")
    cursoromrs4.close()

    #update person_address table
    cursoromrs5 = connMRS.cursor()
    inspersonaddstmnt = """UPDATE person_address SET address1 = %s, \
    city_village = %s , state_province = %s  WHERE person_id = %s"""
    cursoromrs5.execute(inspersonaddstmnt, (st, brgy, town, patientid))
    cursoromrs5.execute("commit")
    cursoromrs5.close()

    #insert into person_name table
    cursoromrs6 = connMRS.cursor()
    inspersonnamestmnt = """UPDATE person_name SET given_name = %s, \
    middle_name =%s ,family_name = %s WHERE preferred = 1 and person_id = %s"""
    cursoromrs6.execute(inspersonnamestmnt, (fname, mname, lname, patientid))
    cursoromrs6.execute("commit")
    cursoromrs6.close()

    #update birthplace in person_attribute table
    cursoromrs7 = connMRS.cursor()
    inspersonbplace = """UPDATE person_attribute SET value = %s  \
    WHERE person_attribute_type_id = 2 and person_id = %s"""
    cursoromrs7.execute(inspersonbplace, (bplace, patientid))
    cursoromrs7.execute("commit")
    cursoromrs7.close()

    #update mother name in person_attribute table
    cursoromrs8 = connMRS.cursor()
    inspersonmother = """UPDATE person_attribute SET value = %s  \
    WHERE person_attribute_type_id = 4 and person_id = %s"""
    cursoromrs8.execute(inspersonmother, (mothrname, patientid))
    cursoromrs8.execute("commit")
    cursoromrs8.close()

def test_connect(ip_address, port1, username, password, database):
    port1 = int(port1)
    connMRS = MySQLdb.connect (host = ip_address,
        port=port1,
        user=username,
        passwd = password,
        db=database)

    mrstest = connMRS.cursor()
    mrstest.execute('select person_id from person limit 1')
    result = mrstest.fetchall()
    mrstest.close

    return result
