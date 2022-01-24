from app import app
from flask import g, render_template, url_for, request, session, redirect, flash
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm, ReserveForm, DeliveryForm, BasketForm, PodBronForm, PodZakazForm
from app.DataBase import DataBase


# Подключение к СУБД через драйвер psycopg2
def connect_db():
    conn = psycopg2.connect(dbname="d7ahpk0rbq0pth",
                            user="aanagckfygyezv",
                            password="b68163b34754853746b81d41b1d727f52e7d86f4a4196fb346878c83f2647bed",
                            host="ec2-34-242-89-204.eu-west-1.compute.amazonaws.com")
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    db = get_db()
    global dbase
    dbase = DataBase(db)  # экземпляр DataBase


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


# маршрут главной страницы
@app.route('/')
def home():
    print(session)
    return render_template('home.html')


@app.route('/menu')
def menu():
    session.permanent = False
    session.modified = True
    db_menu = dbase.get_menu()
    menu_len = len(db_menu)
    img = dbase.loading_pic()
    print(db_menu[0][2])
    return render_template("menu.html", db_menu=db_menu, menu_len=menu_len, img=img)


@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()
    session.permanent = False
    session.modified = True

    if reg_form.validate_on_submit():

        _hashed_password = generate_password_hash(reg_form.password_regform.data)
        print(_hashed_password)

        account = dbase.get_account(reg_form.login_regform.data)

        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        else:
            dbase.add_account(reg_form.login_regform.data, _hashed_password, reg_form.fio_regform.data,
                              reg_form.phone_regform.data)
        flash('You have successfully registered!')
        return redirect(url_for('login'))
        # Show registration form with message (if any)
    return render_template('register.html', reg_form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.permanent = False
    login_form = LoginForm()

    if login_form.validate_on_submit():

        user = dbase.get_user(login_form.phone_loginform.data)
        sotrudnik = dbase.get_sotrudnik(login_form.phone_loginform.data)


        if user:
            password_rs = user['password']

            if check_password_hash(password_rs, login_form.password_loginform.data):
                session['loggedin'] = True
                session['id_user'] = user['id_user']
                session['phone'] = user['phone_user']
                session['role'] = "user"
                if sotrudnik:
                    session['role'] = "sotrudnik"
                    session['id_sotrudnik'] = sotrudnik['id_sotrudnik']
                return redirect(url_for('home'))
            else:
                flash('Incorrect phone or password')

        else:
            flash('Incorrect phone or password')

    return render_template('login.html', login_form=login_form), session


@app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    reserve_form = ReserveForm()
    if reserve_form.validate_on_submit():

        dbase.add_reserve(reserve_form.people_number_resform.data, reserve_form.date_resform.data,
                          reserve_form.time_resform.data, reserve_form.fio_resform.data,
                          reserve_form.phone_resform.data,
                          reserve_form.vish_resform.data)

        databron = f'{reserve_form.time_resform.data.hour}:{reserve_form.time_resform.data.minute // 10}' \
                   f'{reserve_form.time_resform.data.minute % 10}'
        return render_template('bron.html', reserve_form=reserve_form, databron=databron)
    else:
        flash('ужасное время')
    return render_template('reserve.html', reserve_form=reserve_form)


@app.route('/delivery', methods=['GET', 'POST'])
def delivery():
    delivery_form = DeliveryForm()


    if delivery_form.validate_on_submit():

        dbase.add_delivery(session['summ_price'], delivery_form.date_delform.data, delivery_form.adr_delform.data,
                           session['id_user'], delivery_form.fio_delform.data, delivery_form.time_delform.data,
                           delivery_form.phone_delform.data, delivery_form.people_number_delform.data,
                           delivery_form.vish_delform.data, delivery_form.payment_delform.data)

        databron = f'{delivery_form.time_delform.data.hour}:{delivery_form.time_delform.data.minute // 10}' \
                   f'{delivery_form.time_delform.data.minute % 10}'
        return render_template('zakaz.html', delivery_form=delivery_form, databron=databron)
        # if 'loggedin' in session:
    return render_template('delivery.html', delivery_form=delivery_form)
    # return redirect(url_for('login'))


@app.route('/basket', methods=['GET', 'POST'])
def basket():
    if 'loggedin' in session:
        basket_form = BasketForm()
        db_dish = dbase.get_dishes()
        db_dish_len = len(db_dish)
        basket_form.dish_basketform.choices = [db_dish[count][0] for count in range(db_dish_len)]

        db_kolich_dish = dbase.get_max_kolichdish()
        basket_form.kol_basketform.choices = [count+1 for count in range(db_kolich_dish[0][0])]

        info_basket = dbase.get_basket(session['id_user'])
        info_basket_len = len(info_basket)
        session['table_basket'] = []

        session['summ_price'] = 0

        for count in range(info_basket_len):
            atr_dish_for_table = dbase.get_dish_for_id(info_basket[count][0])
            price_for_dish = info_basket[count][1] * atr_dish_for_table[0][1]
            session['table_basket'] += [atr_dish_for_table[0][0], info_basket[count][1], price_for_dish]
            session['summ_price'] += price_for_dish

        table_basket_len = len(session['table_basket'])
        session['table_basket_len'] = table_basket_len

        if basket_form.validate_on_submit():
            if basket_form.submit_add_basketform.data:
                atr_dish = dbase.get_id_dish(basket_form.dish_basketform.data)
                if atr_dish[0][1] >= int(basket_form.kol_basketform.data):
                    dbase.add_basket(atr_dish[0][0], session['id_user'], basket_form.kol_basketform.data)
                else:
                    flash(f'Выберите меньшее количество блюд. Доступное количество блюд: {atr_dish[0][1]}')
                return redirect(url_for('basket'))

            elif basket_form.submit_basketform.data:
                dbase.delete_basket(session['id_user'])
                return redirect(url_for('basket'))

            elif basket_form.submit_next_basketform.data:
                return redirect(url_for('delivery'))

        return render_template('basket.html', basket_form=basket_form)

    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    return redirect(url_for('home'))


@app.route('/lk')
def lk():
    return render_template('lk.html')


@app.route('/podbron', methods=['GET', 'POST'])
def podbron():
    if session['role'] == "sotrudnik":
        podbron_form = PodBronForm()
        session.permanent = False
        session.modified = True
        db_podbron = dbase.get_podbron()
        podbron_len = len(db_podbron)
        if podbron_form.submit_add_podbronform.data:
            id = podbron_form.submit_id_podbronform.data
            info_podbron = dbase.get_info_podbron(id)
            dbase.add_podbron(info_podbron[0][0], info_podbron[0][1], info_podbron[0][2], info_podbron[0][3],
                              info_podbron[0][4], info_podbron[0][5], session['id_sotrudnik'], id)
            dbase.delete_info_podbron(id)
            return redirect(url_for('podbron'))
        return render_template('podbron.html', podbron_form=podbron_form, db_podbron=db_podbron,
                               podbron_len=podbron_len)
    else:
        return redirect(url_for('home'))


@app.route('/podzakaz', methods=['GET', 'POST'])
def podzakaz():
    if session['role'] == "sotrudnik":
        podzakaz_form = PodZakazForm()
        session.permanent = False
        session.modified = True
        db_podzakaz = dbase.get_podzakaz()
        podzakaz_len = len(db_podzakaz)
        if podzakaz_form.submit_add_podzakazform.data:
            id = podzakaz_form.submit_id_podzakazform.data
            info_podzakaz = dbase.get_info_podzakaz(id)
            dbase.add_podzakaz(info_podzakaz[0][0], info_podzakaz[0][1], info_podzakaz[0][2], info_podzakaz[0][3],
                               info_podzakaz[0][4], info_podzakaz[0][5], info_podzakaz[0][6], info_podzakaz[0][7],
                               info_podzakaz[0][8], info_podzakaz[0][9], session['id_sotrudnik'], id)
            dbase.delete_info_podzakaz(id)
            return redirect(url_for('podzakaz'))
        return render_template('podzakaz.html', podzakaz_form=podzakaz_form, db_podzakaz=db_podzakaz,
                           podzakaz_len=podzakaz_len)
    else:
        return redirect(url_for('home'))

@app.route('/zakazpod')
def zakazpod():
    if session['role'] == "sotrudnik":
        session.permanent = False
        session.modified = True
        db_zakazpod = dbase.get_zakazpod()
        zakazpod_len = len(db_zakazpod)
    return render_template('zakazpod.html', db_zakazpod=db_zakazpod, zakazpod_len=zakazpod_len)

@app.route('/bronpod')
def bronpod():
    if session['role'] == "sotrudnik":
        session.permanent = False
        session.modified = True
        db_bronpod = dbase.get_bronpod()
        bronpod_len = len(db_bronpod)
    return render_template('bronpod.html', db_bronpod=db_bronpod, bronpod_len=bronpod_len)