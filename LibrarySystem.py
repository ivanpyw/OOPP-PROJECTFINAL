from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators, PasswordField
from Symptom import Symptoms, ChestPain, AbdominalPain, Fever, Breathless
from warded import warded, A, B, C
from Users import Users
import firebase_admin
from firebase_admin import credentials, db
from StaffU import StaffU
from Create_request import CreateRequest
from descbill import Descbill
from datetime import datetime
from inpatientbill import inpatientbill
from inpatientbill import products
from inpatientbill import p
from medicinal import Medicinal
from appointment import Appointment
# from passlib.hash import sha256_crypt #need to pip install passlib on the command prompt
cred = credentials.Certificate('cred/stop-78245-firebase-adminsdk-jqcbt-d793e7c23d.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://stop-78245.firebaseio.com/'

})


root = db.reference()
app = Flask(__name__)

class AppointmentForm(Form):
    date = StringField('Date of appointment : ',[validators.DataRequired()], render_kw={"placeholder": "dd/mm/yyyy"})
    timee = SelectField('Time of appointment : ', [validators.DataRequired()],
                           choices=[('', 'Select'), ('0900', '0900'), ('0930', '0930'),
                                    ('1000', '1000'), ('1030', '1030'), ('1100', '1100'), ('1130', '1130')
                                    ,('1200', '1200'),('1230', '1230'), ('1300', '1300'), ('1330', '1330')
                                    , ('1400', '1400'), ('1430', '1430'), ('1500', '1500')],
                           default='')

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    form = AppointmentForm(request.form)
    if request.method == 'POST' and form.validate():
        #  def init(self, username, fullname, password, email):

        date = form.date.data
        timee = form.timee.data
        # password = sha256_crypt.encrypt(str(form.password.data)) #encryption

        ifUserExists = root.child('appt').order_by_child('date').equal_to(date).get()

        print(ifUserExists)

        for k, v in ifUserExists.items():
            print(k, v)

        else:

            user = Appointment(date, timee)
            user_db = root.child('appt')

            user_db.push(
                {
                    'date': user.get_date(),
                    'timee': user.get_timee(),
                }
            )

            flash('Appointment booked. Waiting for reply from doctor.', 'success')
            return redirect(url_for('appointment'))

    else:
        return render_template('appointment.html', form=form)

    return render_template('appointment.html', form=form)

@app.route('/aftappt')
def wat():
    wat = root.child('appt').get()
    list = []
    if wat == None:
        return render_template('aftappt.html')

    for pubid in wat:
        eachupdate = wat[pubid]

        appointment = Appointment(eachupdate['date'], eachupdate['timee'])
        appointment.set_pubid(pubid)
        print('ID : {}, Date: {}, Time: {}'.format(appointment.get_pubid, appointment.get_date, appointment.get_timee()))
        list.append(appointment)

    return render_template('aftappt.html', wat=list)

@app.route('/aftapp/<string:id>', methods=['POST'])
def viewappt(id):
    appointment_db = root.child('appt/' + id)
    appointment_db.delete()
    flash('Appointment cancelled.')

    return redirect(url_for('wat'))

class addbillForm(Form):
    nric = StringField('Patient NRIC', [validators.data_required()])

    productu = StringField('Item ID',[validators.data_required()])

    quantity = SelectField('Quantity',
                           choices=[("1",1),("2",2),("3",3)], default='1'
                           )
    #how do i retrieve nric data in selectfield value?

@app.route('/thenurseitem/<string:id>', methods=["POST"])
def thenurseitemform(id):
    item_db = root.child('productDesc/'+id)
    item_db.delete()
    flash('It is successfully deleted','success')

    return redirect(url_for('listnurseitem'))

@app.route('/thenurseitem')
def listnurseitem():

    nurseitem = root.child('productDesc').get()
    list = []
    if nurseitem ==None:
        return render_template('testingg.html')
    else:
        for pubid in nurseitem:
            eachupdate = nurseitem[pubid]
            bill = products(eachupdate['id'],eachupdate['product'], eachupdate['price'])
            bill.set_id(eachupdate['id'])
            print("ID: {}, Product: {}, Price:$ {}".format(bill.get_id(), bill.get_productName(),
                                                                     bill.get_unitPrice()))
        # print(bill.get_product())
            list.append(bill)
        return render_template('thenurseitem.html', nurseitem=list)

class ProductForm(Form):

    product = StringField('Product', [validators.Length(min=1, max=100), validators.DataRequired()])
    price = StringField('Price', [validators.Length(min=1, max=100), validators.DataRequired()])
    id = StringField('Product ID', [validators.Length(max=5), validators.DataRequired()])


@app.route('/medicine', methods=['GET', 'POST'])
def med():
    form = ProductForm(request.form)
    if request.method == 'POST' and form.validate():
            #  def init(self, username, fullname, password, email):

        product = form.product.data
        price = form.price.data
        id = form.id.data
            # password = sha256_crypt.encrypt(str(form.password.data)) #encryption

        ifUserExists = root.child('productDesc').order_by_child('product').equal_to(product).get()

        print(ifUserExists)

        for k, v in ifUserExists.items():
            print(k, v)

        else:

            user = Medicinal(product, price, id)
            user_db = root.child('productDesc')

            user_db.push(
                {
                    'product': user.get_product(),
                    'price': user.get_price(),
                    'id':user.get_id(),
                }
            )

            flash('Medicine added.', 'success')
            return redirect(url_for('med'))

    else:
        return render_template('medicine.html', form=form)

    return render_template('medicine.html', form=form)



@app.route('/medicine2')
def total():

    total = root.child('productDesc').get()
    list = []
    if total == None:
        return render_template('medicine2.html')

    for pubid in total:
        eachupdate = total[pubid]

        med = Medicinal(eachupdate['id'], eachupdate['product'], eachupdate['price'])
        med.set_pubid(pubid)
        print('ID : {}, ID: {}, Product: {}', 'Price : {}'.format(med.get_pubid, med.get_id, med.get_product(), med.get_price ))
        list.append(med)

    return render_template('medicine2.html', total=list)


@app.route('/medicine2/<string:id>', methods=['POST'])
def viewtotalitems(id):
    med_db = root.child('productDesc/' + id)
    med_db.delete()
    flash('Item Removed.', 'success')

    return redirect(url_for('total'))

@app.route('/bill', methods=['POST','GET'])
def bill():
    form = addbillForm(request.form)
    if request.method == 'POST' and form.validate():
        nric = form.nric.data
        # price = form.price.data
        productu = form.productu.data
        quantity = form.quantity.data
        ifItemsExists = root.child('messages').order_by_child('nric').equal_to(nric).get()
        for k, v in ifItemsExists.items():
            print(ifItemsExists.items())
            # print(session['nric'])
            print(k, v)
        items = products(nric, productu, quantity)
        items_db = root.child('patientbill')

        items_db.push(
            {
                'nric': items.get_id(),
                'product': items.get_productName(),
                'quantity': items.get_unitPrice()
            }
        )
        flash('Submit Successful.', 'success')
        return redirect(url_for('listnurseitem'))
    else:
        return render_template('bill.html', form=form)
    return render_template('bill.html', form=form)
    # listofp = root.child('productDesc').get()
    # list = []
    # for pubid in listofp:
    #     eachupdate = listofp[pubid]
    #     if eachupdate['nric'] == session['nric']:
    #         bill = Descbill(eachupdate['product'], eachupdate['quantity'], eachupdate['price'])
    #         bill.set_pubid(pubid)
    #         print("ID: {}, Product: {}, Quantity: {}, Price:$ {}".format(bill.get_pubid(), bill.get_product(),bill.get_quantity(), bill.get_price()))
    #         # print(bill.get_product())
    #         list.append(bill)
    # return render_template('bill.html', listofp=list)
@app.route('/viewItems', methods=['GET', 'POST'])
def staffitem():
    list = []
    ifItemsExists = root.child('patientbill').order_by_child('nric').equal_to(session['nric']).get()

    # if root.child('patientbill').order_by_child('nric') == session['nric']:

        # for pubid in ifItemsExists:
    for k, v in ifItemsExists.items():

        bill = products(v['nric'], v['product'],v['quantity'])
        bill.set_id(v['nric'])
        print("ID: {}, Product: {}, Quantity: {}".format(bill.get_id(), bill.get_productName(),
                                                                     bill.get_unitPrice()))
        # print(bill.get_product())
        list.append(bill)
    return render_template('viewItems.html', ifItemsExists=list)

class StaffLogin(Form):
    staffid = StringField('Staff id', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    type = RadioField('Type', choices=[('tDoctor', 'Doctor'), ('tNurse', 'Nurse')], default='tDoctor')

@app.route('/stafflogin', methods=['GET', 'POST'])
def stafflogin():
    form = StaffLogin(request.form)
    if request.method == 'POST' and form.validate():
        staffid = form.staffid.data
        password = form.password.data
        type = form.type.data
        navbarstaff = False

        ifUserExists = root.child('users').order_by_child('staffid').equal_to(staffid).get()
        # print(root.child('messages').order_by_child('staffid').equal_to(staffid).get())
        print(password)
        for k, v in ifUserExists.items():
            print(k, v)

            print(v['staffid'])
            print(v['password'])


            if staffid == v['staffid'] and  password == v['password'] and type == v['type']:
                session['logged_in'] = True
                session['staffid'] = staffid
                session['navbarstaff']= True
                # session['password'] = password
                return redirect(url_for('aftstafflog'))
            else:
                error = 'Invalid login'
                flash(error, 'danger')
                return render_template('StaffLog.html', form=form)
    else:
        return render_template('StaffLog.html', form=form)
    return render_template('StaffLog.html',form=form)

@app.route('/aftstaffLog')
def aftstafflog():
    return render_template('aftstafflog.html')
class Staffreg(Form):
    staffid = StringField('Staffid',validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    type = RadioField('Type', choices=[('tDoctor', 'Doctor'), ('tNurse', 'Nurse')], default='tDoctor')

@app.route('/staffreg', methods=['POST', 'GET'])
def register():
    form = Staffreg(request.form)
    if request.method == 'POST' and form.validate():
        #  def __init__(self, username, fullname, password, email):

        staffid = form.staffid.data

        password = form.password.data
        # password = sha256_crypt.encrypt(str(form.password.data)) #encryption
        type = form.type.data

        ifUserExists = root.child('users').order_by_child('staffid').equal_to(staffid).get()

        print(ifUserExists)

        for k, v in ifUserExists.items():
            print(k, v)

        if len(ifUserExists) > 0:
            flash('User exist.', 'danger')
        else:

            user = StaffU(staffid, password, type)
            user_db = root.child('users')


            user_db.push(
                {
                    'staffid': user.get_staffid(),
                    'password': user.get_password(),
                    'type': user.get_type()
                }
            )

            flash('Registraion Successfully.', 'success')
            return redirect(url_for('stafflogin'))

    else:
        return render_template('staffreg.html', form=form)


@app.route('/afterLog')
def afterLog():
    return render_template('afterLog.html')

class RegisterUserForm(Form):
    nric = StringField('Nric', validators=[validators.DataRequired()])
    fullname = StringField('Full Name', validators=[validators.DataRequired()])
    gender = RadioField('Gender', choices=[('tMale', 'Male'), ('tFemale', 'Female')], default='tMale')
    dob = StringField('Date Of Birth(dd/MM/YYYY)',validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[validators.DataRequired()])
    # email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    form = RegisterUserForm(request.form)
    if request.method == 'POST' and form.validate():
        #  def __init__(self, username, fullname, password, email):

        # username = form.username.data
        nric = form.nric.data
        fullname = form.fullname.data
        gender = form.gender.data
        password = form.password.data
        # password = sha256_crypt.encrypt(str(form.password.data)) #encryption
        # email = form.email.data
        dob = form.dob.data

        ifUserExists = root.child('patientacc').order_by_child('username').equal_to(nric).get()

        print(ifUserExists)

        for k, v in ifUserExists.items():
            print(k, v)

        if len(ifUserExists) > 0:
            flash('User exist.', 'danger')
        else:

            user = Users(nric, fullname, dob, gender, password)
            user_db = root.child('messages')


            user_db.push(
                {
                    'nric': user.get_nric(),
                    'fullname': user.get_fullname(),
                    'dob': user.get_dob(),
                    'gender': user.get_gender(),
                    'password': user.get_password(),


                }
            )

            flash('Registraion Successfully.', 'success')
            return redirect(url_for('login'))

    else:
        return render_template('Register.html', form=form)

class Request(Form):
    drinks=SelectField('Drinks',
                              choices=[('', 'Select'), ('Warm Water', 'Warm Water'),
                                       ('Cold Water', 'Cold Water'),
                                       ('Milo', 'Milo'), ('Green Tea', 'Green Tea')], default='')

    food=SelectField('Food',
                              choices=[('', 'Select'), ('Chicken Porridge', 'Chicken Porridge'),
                                       ('Vegetarian Rice', 'Vegetarian Rice'),
                                       ('Steamed Bun', 'Steamed Bun')], default='')

    assistance=SelectField('Assistance',
                              choices=[( '', 'Select'), ('Bathing Service', "Bathing Service"),
                                       ('Toilet Assistance', 'Toilet Assistance'),
                                       ('Outdoor Personal Assistant', 'Outdoor Personal Assistant')], default='')

    emergency=SelectField('Emergency',
                                    choices=[('','Select'),('PAIN', 'Im in great pain'), ('Urgent Leave Required', "Urgent reason to leave the hospital")], default='')


    other=StringField('Other', default='')



@app.route('/request_help', methods=['GET', 'POST'])
def requesthelppage():
    form = Request(request.form)

    if request.method == 'POST' and form.validate():

        status= 1
        NRIC = session['nric']
        DatePublished = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        drinks = form.drinks.data
        food = form.food.data
        assistance = form.assistance.data
        other = form.other.data
        emergency= form.emergency.data
        # password = sha256_crypt.encrypt(str(form.password.data)) #encryption

        # ifUserExists = root.child('request').order_by_child('NRIC').equal_to(NRIC).get()
        #
        # print(ifUserExists)
        #
        # # for k, v in ifUserExists.items():
        # #     print(ifUserExists.items())
        # #     print(k, v)
        # #     print(session['nric'])

        user = CreateRequest(drinks, food, assistance, other, DatePublished, NRIC, status, emergency)
        user_db = root.child('request/')

        user_db.push(
            {
                'emergency': user.get_emergency(),
                'status': user.get_status(),
                'NRIC': user.get_NRIC(),
                'DatePublished': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'drinks': user.get_drinks(),
                'food': user.get_food(),
                'assistance': user.get_assistance(),
                'other': user.get_other(),
            }
        )

        flash('Request Sent.', 'success')
        return redirect(url_for('home'))

    else:
        return render_template('Request_help.html', form=form)

    return render_template('Request_help.html', form=form)


@app.route('/request_help/<string:id>', methods=['GET', 'POST'])
def updaterequestpage(id):
    form = Request(request.form)

    if request.method == 'POST' and form.validate():

        status= 1
        NRIC = session['nric']
        DatePublished = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        drinks = form.drinks.data
        food = form.food.data
        assistance = form.assistance.data
        other = form.other.data
        emergency= form.emergency.data
        # password = sha256_crypt.encrypt(str(form.password.data)) #encryption

        # ifUserExists = root.child('request').order_by_child('NRIC').equal_to(NRIC).get()
        #
        # print(ifUserExists)
        #
        # # for k, v in ifUserExists.items():
        # #     print(ifUserExists.items())
        # #     print(k, v)
        # #     print(session['nric'])

        user = CreateRequest(drinks, food, assistance, other, DatePublished, NRIC, status, emergency)
        user_db = root.child('request/'+ id)

        user_db.set(
            {
                'emergency': user.get_emergency(),
                'status': user.get_status(),
                'NRIC': user.get_NRIC(),
                'DatePublished': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'drinks': user.get_drinks(),
                'food': user.get_food(),
                'assistance': user.get_assistance(),
                'other': user.get_other(),
            }
        )

        flash('Request Sent.', 'success')
        return render_template('Request_help.html', form=form)
    return redirect(url_for('home'))





@app.route('/')
def default():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/viewsymptoms', methods = ['GET','POST'])
#nat
def viewsymptoms():
    listofsymptoms = root.child('symptom').get()
    list = []

    for pubid in listofsymptoms:
        storesymptoms = listofsymptoms[pubid]

        if storesymptoms['symptom'] == 'scp':
            chestpain = ChestPain(storesymptoms['symptom'], storesymptoms['travelled'], storesymptoms['allergy'],
                                  storesymptoms['specific_allergy'], storesymptoms['pain_rate'], storesymptoms['nric'])
            chestpain.set_pubid(pubid)
            list.append(chestpain)
            print(list)

        elif storesymptoms['symptom'] == 'sap':
            abdopain = AbdominalPain(storesymptoms['symptom'], storesymptoms['travelled'], storesymptoms['allergy'],
                                     storesymptoms['specific_allergy'], storesymptoms['pain_rate'], storesymptoms['nric'])
            abdopain.set_pubid(pubid)
            list.append(abdopain)
            print(list)


        elif storesymptoms['symptom'] == 'sfr':
            fever = AbdominalPain(storesymptoms['symptom'], storesymptoms['travelled'], storesymptoms['allergy'],
                                  storesymptoms['specific_allergy'], storesymptoms['other_symptoms'], storesymptoms['nric'])
            fever.set_pubid(pubid)
            list.append(fever)
            print(list)


        elif storesymptoms['symptom'] == 'sbr':
            breath = Breathless(storesymptoms['symptom'], storesymptoms['travelled'], storesymptoms['allergy'],
                                storesymptoms['specific_allergy'], storesymptoms['history_of_asthma'],storesymptoms['nric'])
            breath.set_pubid(pubid)
            list.append(breath)
            print (list)


    return render_template('view_all_publications.html', listofsymptoms = list)

@app.route('/wardpatients', methods = ['GET','POST'])
#nat
def wardpatients():
    listofpatients = root.child('ward').get()
    list = []

    for pubid in listofpatients:
        storepatients = listofpatients[pubid]

        if storepatients['ward'] == 'A':
            a = A(storepatients['name'], storepatients['ward'], storepatients['number'], storepatients['a room'],
                                  storepatients['nric'])
            a.set_pubid(pubid)
            list.append(a)
            print(list)


        elif storepatients['ward'] == 'B':
            b = B(storepatients['name'], storepatients['ward'], storepatients['number'], storepatients['b room'],
                                  storepatients['nric'])
            b.set_pubid(pubid)
            list.append(b)
            print(list)


        elif storepatients['ward'] == 'C':
            c = C(storepatients['name'], storepatients['ward'], storepatients['number'], storepatients['c room'],
                  storepatients['nric'])
            c.set_pubid(pubid)
            list.append(c)
            print(list)

    return render_template('viewwardpatients.html', listofpatients = list)

@app.route('/viewreceipt')
def viewreceipt():
    return render_template('viewreceipt.html')


# @app.route('/viewpublications')
# def viewpublications():
#     publications = root.child('publications').get()
#     list = [] #create a list to store all the publication objects
#     print(publications)
#     for pubid in publications:
#
#         eachpublication = publications[pubid]
#
#         if eachpublication['type'] == 'smag':
#             magazine = Magazine(eachpublication['title'], eachpublication['publisher'], eachpublication['status'], eachpublication['created_by'], eachpublication['category'], eachpublication['type'], eachpublication['frequency'])
#             magazine.set_pubid(pubid)
#             print(magazine.get_pubid())
#             list.append(magazine)
#         else:
#             book = Book(eachpublication['title'], eachpublication['publisher'], eachpublication['status'], eachpublication['created_by'], eachpublication['category'], eachpublication['type'], eachpublication['synopsis'], eachpublication['author'], eachpublication['isbn'])
#             book.set_pubid(pubid)
#             list.append(book)
#
#     return render_template('view_all_publications.html', publications = list)

class RequiredIf(object):

    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)


@app.route('/viewrequest/<string:id>', methods=['POST'])
def viewrequestform(id):
    user_db = root.child('request/'+ id)
    user_db.delete()
    flash('Request Deleted', 'success')

    return redirect(url_for('listofrequest'))

@app.route('/current_request/<string:id>', methods=['POST'])
def deleterequestform(id):
    user_db = root.child('request/'+ id)
    user_db.delete()
    flash('Request Deleted', 'success')

    return redirect(url_for('specificrequest'))

@app.route("/current_request")
def specificrequest():
    listofcurrent = root.child('request').get()
    list = []
    if listofcurrent == None:
        flash('no current requests made by this user', 'success')
        return render_template('home.html')
    else:
        for pubid in listofcurrent:
            eachupdate = listofcurrent[pubid]
            if eachupdate["NRIC"]== session['nric']:
                currentrequest = CreateRequest(eachupdate['drinks'], eachupdate['food'], eachupdate['assistance'],
                                             eachupdate['other'], eachupdate['DatePublished'], eachupdate['NRIC'],
                                             eachupdate['status'], eachupdate['emergency'])
                currentrequest.set_pubid(pubid)
                print(currentrequest.get_pubid())
                list.append(currentrequest)
                print(list)
            else:
                pass
    return render_template('currentrequest.html', listofcurrent=list)

@app.route('/viewrequest')
def listofrequest():
    listofrequest = root.child('request').get()
    list = []
    if listofrequest== None:
        flash('There are no requests for now', 'success')
        return render_template('viewrequestempty.html')
    else:
        for pubid in listofrequest:
            eachupdate = listofrequest[pubid]
            storerequest = CreateRequest( eachupdate['drinks'], eachupdate['food'], eachupdate['assistance'], eachupdate['other'], eachupdate['DatePublished'], eachupdate['NRIC'], eachupdate['status'], eachupdate['emergency'])
            storerequest.set_pubid(pubid)
            print(storerequest.get_pubid())
            list.append(storerequest)
            print(list)
        return render_template('viewrequest.html', listofrequest=list)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        nric = form.nric.data
        password = form.password.data
        navbarpatient = False

        ifUserExists = root.child('messages').order_by_child('nric').equal_to(nric).get()

        for k, v in ifUserExists.items():
            print(k, v)
            # print(sha256_crypt.encrypt(password))
            print(v['nric'])
            print(v['password'])

            # if username == v['username'] and sha256_crypt.verify(password, v['password']):
            if nric == v['nric'] and  password == v['password']:
                session['logged_in'] = True
                session['nric'] = nric
                session['navbarpatient']= True
                print(nric)
                # session['password'] = password
                return redirect(url_for('afterLog'))
            else:
                error = 'Invalid login'
                flash(error, 'danger')
                return render_template('Login.html', form=form)
    else:
        return render_template('Login.html', form=form)
    return render_template('Login.html',form=form)



@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

class LoginForm(Form):
    nric = StringField('Nric', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

class SymptomsForm(Form):
    #nat
    travel = SelectField('Have you have travelled to Middle East or West Africa in the last 2 - 3 weeks?',[validators.DataRequired()],
                        choices = [('', 'Select'), ('Y', 'Yes'), ('N', 'No')], default='')

    symptype = RadioField('Symptoms', choices=[('scp', 'Chest Pain'), ('sap', 'Abdominal Pain'),
                                           ('sfr', 'Fever'), ('sbr', 'Breathless')],
                                            default='scp')

    allergies = SelectField('Do you have any medication allergies?',[validators.DataRequired()],
                        choices = [('', 'Select'), ('Y', 'Yes'), ('N', 'No')], default='')

    sallergies = StringField('If yes, specify your medication allergies', [
                            validators.Length(min=1, max=100), RequiredIf(allergies='Y')])

    othersymptoms = SelectField('Other symptoms', [RequiredIf(symptype='sfr')],
                         choices=[('', 'Select'), ('U', 'Difficulty Urinating'),
                                  ('V', 'Persistent Vomiting'), ('H', 'Severe Headache'),
                                  ('N', 'None')], default='')

    rate = SelectField('Rate your pain', [RequiredIf(symptype='scp' or 'sap')],
                           choices=[('', 'Select'), ('1', '1'), ('2', '2'), ('3', '3'),
                                    ('4', '4'), ('5', '5'), ('6', '6'),
                                    ('7', '7'), ('8', '8'), ('9', '9'),
                                    ('10', '10')], default='')

    hist = SelectField('Do you have history of Asthma?', [RequiredIf(symptype='sbr')],
                            choices=[('', 'Select'), ('Y', 'Yes'), ('N', 'No')], default='')

class AdmissionForm(Form):
    name = StringField('Full Name (as in NRIC)', validators=[validators.DataRequired()])
    number = StringField('Contact Number', validators=[validators.DataRequired()])
    ward = RadioField('Ward Class', choices=[('A', 'A'),
                                             ('B', 'B'), ('C', 'C')],
                      validators=[validators.DataRequired()], default='A')

    aroom = SelectField('Ward Room', [RequiredIf(symptype='A')], choices=[('', 'Select'), ('A1', 'A1'),
                                             ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'),
                                             ('A5', 'A5'),('A6', 'A6'),('A7', 'A7'),
                                               ('A8', 'A8'),('A9', 'A9'),('A10', 'A10')], default='')

    broom = SelectField('Ward Rooms', [RequiredIf(symptype='B')], choices=[('', 'Select'), ('B1', 'B1'),
                                             ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'),
                                             ('B5', 'B5'),('B6', 'B6'),('B7', 'B7'),
                                               ('B8', 'B8'),('B9', 'B9'),('B10', 'B10')], default='')

    croom = SelectField('Ward Room', [RequiredIf(symptype='C')],  choices=[('', 'Select'), ('C', 'C1'),
                                             ('C2', 'C2'), ('C3', 'C3'), ('C4', 'C4'),
                                             ('C5', 'C5'),('C6', 'C6'),('C7', 'C7'),
                                               ('C8', 'C8'),('C9', 'C9'),('C10', 'C10')], default='')


@app.route('/newsymptoms', methods=['GET', 'POST'])
#nat
def new():
    form = SymptomsForm(request.form)
    print(request.method)
    if request.method == 'POST' and form.validate():
        # session['nric'] = request.form['nric']

        print(form.symptype.data)

        if  form.symptype.data == 'scp':
            nric = session['nric']
            type = form.symptype.data
            travel = form.travel.data
            allergies = form.allergies.data
            specify = form.sallergies.data
            rate = form.rate.data

            # ifUserExists = root.child('symptom').order_by_child('symptom').equal_to(type).get()
            #
            # print(ifUserExists)
            #
            # for k, v in ifUserExists.items():
            #     print(ifUserExists.items())
            #     print(k, v)
            #     print(session['nric'])
            #
            # user = Symptoms(t, NRIC)
            # user_db = root.child('request/')

            chp = ChestPain(travel, allergies, specify, type, rate, nric)

            #create the magazine object
            chp_db = root.child('symptom')

            chp_db.push({
                    'nric': chp.get_nric(),
                    'symptom': chp.get_type(),
                    'travelled': chp.get_travel(),
                    'allergy': chp.get_allergies(),
                    'specific_allergy': chp.get_specify(),
                    'pain_rate': chp.get_painrate()
            })

            # if allergies == 'Y':
            #     flash('Please enter your allergy') vv mmm

            if int(rate) < 5:
                flash('If you have a non-emergency condition, like flu, please visit Polyclinic or your General Practitioner. You will get treated sooner. Do take note that we prioritise emergency cases. Thank You.', 'success')

            else:
                flash('You have registered successfully.', 'success')

        elif  form.symptype.data == 'sap':
            nric = session['nric']
            type = form.symptype.data
            travel = form.travel.data
            allergies = form.allergies.data
            rate= form.rate.data
            specify = form.sallergies.data

            abdop = AbdominalPain(travel, allergies, specify, type, rate, nric)

            #create the magazine object
            abdop_db = root.child('symptom')
            abdop_db.push({
                    'nric': abdop.get_nric(),
                    'symptom': abdop.get_type(),
                    'travelled': abdop.get_travel(),
                    'allergy': abdop.get_allergies(),
                    'specific_allergy': abdop.get_specify(),
                    'pain_rate': abdop.get_painrate()
            })

            if int(rate) < 5:
                print(nric, type, travel, allergies, rate, specify)
                flash('If you have a non-emergency condition, like flu, please visit Polyclinic or your General Practitioner. You will get treated sooner. Do take note that we prioritise emergency cases. Thank You.', 'success')

            else:
                flash('You have registered successfully.', 'success')


        elif form.symptype.data == 'sfr':
            nric = session['nric']
            type = form.symptype.data
            travel = form.travel.data
            allergies = form.allergies.data
            specify = form.sallergies.data
            osymps = form.othersymptoms.data

            fvr = Fever(travel, allergies, specify, type, osymps, nric)

            fvr_db = root.child('symptom')
            fvr_db.push({
                'nric': fvr.get_nric(),
                'symptom': fvr.get_type(),
                'travelled': fvr.get_travel(),
                'allergy': fvr.get_allergies(),
                'specific_allergy': fvr.get_specify(),
                'other_symptoms': fvr.get_osymps()
            })
            if osymps == 'N':
                print(nric, type, travel, allergies, osymps, specify)

                flash('You have registered successfully. Find a staff to get your temperature taken', 'success')

            else:
                flash('You have registered successfully. Find a staff to get your temperature taken', 'success')

        elif form.symptype.data == 'sbr':
            nric = session['nric']
            type = form.symptype.data
            travel = form.travel.data
            allergies = form.allergies.data
            history= form.hist.data
            specify = form.sallergies.data

            # ifUserExists = root.child('symptom').order_by_child('symptom').equal_to(type).get()

            brth = Breathless(travel, allergies, specify, type, history, nric)

            brth_db = root.child('symptom')
            brth_db.push({
                'nric': brth.get_nric(),
                'symptom': brth.get_type(),
                'travelled': brth.get_travel(),
                'allergy': brth.get_allergies(),
                'specific_allergy': brth.get_specify(),
                'history_of_asthma': brth.get_history()
            })
            print(nric, type, travel, allergies, history, specify)

            flash('You have registered sucessfully.', 'success')
        return redirect(url_for('afterLog'))

    return render_template('create_publication.html', form=form)



@app.route('/wardadmission', methods=['GET', 'POST'])
#nat
def wardadmission():
    form = AdmissionForm(request.form)
    print(request.method)
    if request.method == 'POST' and form.validate():


        if form.ward.data == 'A':
            nric = session['nric']
            name = form.name.data
            ward = form.ward.data
            number = form.number.data
            aroom = form.aroom.data

            ifUserExists = root.child('ward').order_by_child('nric').equal_to(nric).get()

            for k, v in ifUserExists.items():
                print(k, v)
                # print(sha256_crypt.encrypt(password))
                print(v['nric'])
                # print(v['password'])

            arm = A(name, number, ward, aroom, nric)
            arm_db = root.child('ward')

            arm_db.push(
                {
                    'nric': arm.get_nric(),
                    'name': arm.get_name(),
                    'number': arm.get_number(),
                    'ward': arm.get_ward(),
                    'a room': arm.get_aroom()
                }
            )

            flash('Admission Success.', 'success')
            print(name, nric, number, ward, aroom)

        elif form.ward.data == 'B':
            nric = session['nric']
            name = form.name.data
            ward = form.ward.data
            number = form.number.data
            broom = form.broom.data

            brm = B(name, number, ward, broom, nric)
            brm_db = root.child('ward')

            brm_db.push(
                {
                    'nric': brm.get_nric(),
                    'name': brm.get_name(),
                    'number': brm.get_number(),
                    'ward': brm.get_ward(),
                    'b room': brm.get_broom()
                }
            )

            flash('Admission Success.', 'success')
            print(name, nric, number, ward, broom)



        elif form.ward.data == 'C':
            nric = session['nric']
            name = form.name.data
            ward = form.ward.data
            number = form.number.data
            croom = form.croom.data


            crm = C(name, number, ward, croom, nric)
            crm_db = root.child('ward')

            crm_db.push(
                {
                    'nric': crm.get_nric(),
                    'name': crm.get_name(),
                    'number': crm.get_number(),
                    'ward': crm.get_ward(),
                    'c room': crm.get_croom()
                }
            )

            flash('Admission Success.', 'success')
            print(name, nric, number, ward, croom)
        return redirect(url_for('afterLog'))


    return render_template('wardadmission.html', form=form)










# @app.route('/viewrequest/<string:id>/', methods=['GET', 'POST'])
# def update_request(id):
#     if request.method == "POST":
#         if request.form["taken"] == "Interested?":
#             status = "Taken"
#             ride = root.child("listofridesp/" + id)
#             ride.set({
#                 "Starting position": from_where,
#                 "Destination": to_where,
#                 "date": date,
#                 "sessionemail": "sessionemail",
#                 "time": time,
#                 "usertype": userid,
#                 "schedule": schedule,
#                 "status": "Taken"})
#             return redirect(url_for("listofridesD"))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()
