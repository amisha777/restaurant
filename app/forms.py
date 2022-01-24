from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, DateTimeField, \
    RadioField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    phone_loginform = StringField("Phone", validators=[DataRequired()])
    password_loginform = PasswordField("Password", validators=[DataRequired()])
    remember_loginform = BooleanField("Remember me", default=False)
    submit_loginform = SubmitField("Sign in")


class RegisterForm(FlaskForm):
    login_regform = StringField("Login", validators=[DataRequired()])
    password_regform = PasswordField("Password", validators=[DataRequired()])
    fio_regform = StringField("FIO", validators=[DataRequired()])
    phone_regform = StringField("Phone", validators=[DataRequired()])
    submit_regform = SubmitField("Register")


class ReserveForm(FlaskForm):
    date_resform = DateField("Дата", validators=[DataRequired()])
    time_resform = DateTimeField("Время", format='%H:%M', validators=[DataRequired()])
    fio_resform = StringField("ФИО", validators=[DataRequired()])
    phone_resform = StringField("Номер телефона", validators=[DataRequired()])
    vish_resform = StringField("Пожелания", validators=[DataRequired()])
    submit_resform = SubmitField("Забронировать")
    people_number_resform = SelectField("Количество человек", choices=[1, 2, 3, 4, 5, 6])


class DeliveryForm(FlaskForm):
    fio_delform = StringField("Кому доставить", validators=[DataRequired()])
    phone_delform = StringField("Номер телефона", validators=[DataRequired()])
    adr_delform = StringField("Куда доставить", validators=[DataRequired()])
    date_delform = DateField("Дата", validators=[DataRequired()])
    time_delform = DateTimeField("Время", format='%H:%M', validators=[DataRequired()])
    people_number_delform = SelectField("Количество персон", choices=[1, 2, 3, 4, 5, 6])
    payment_delform = RadioField("Оплата", choices=[('Наличными', 'Наличными'), ('Картой курьеру', 'Картой курьеру')])
    vish_delform = StringField("Комметарии", validators=[DataRequired()])
    submit_delform = SubmitField("Оформить доставку")


class BasketForm(FlaskForm):
    dish_basketform = SelectField("Выберите блюдо", choices=[])
    kol_basketform = SelectField("Укажите количество порций", choices=[])
    submit_basketform = SubmitField("Очистить корзину")
    submit_next_basketform = SubmitField("Продолжить")
    submit_add_basketform = SubmitField("Добавить")


class PodBronForm(FlaskForm):
    submit_id_podbronform = HiddenField()
    submit_add_podbronform = SubmitField("Подтвердить")


class PodZakazForm(FlaskForm):
    submit_id_podzakazform = HiddenField()
    submit_add_podzakazform = SubmitField("Подтвердить")