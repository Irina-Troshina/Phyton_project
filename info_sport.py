from flask import Flask, request, render_template
import sqlite3
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

# Определение формы для добавления спортсмена
class MyForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired()])
    gender = StringField('Пол')
    age = IntegerField('Возраст')
    country = StringField('Страна')
    sport = StringField('Спорт')
    
# Инициализация Flask приложения
app = Flask(__name__)

# Настройка соединения с базой данных (sqlite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///athletes.db'
db = SQLAlchemy(app)

# Модель спортсмена для SQLAlchemy
class Sportman(db.Model):
    __tablename__ = 'athletes'  # Указываем название таблицы

    # Определяем столбцы таблицы
    id = db.Column(db.Integer, primary_key=True)  # ID спортсмена (первичный ключ)
    name = db.Column(db.String(80))  # ФИО
    gender = db.Column(db.String(80))  # Пол
    age = db.Column(db.Integer)  # Возраст
    country = db.Column(db.String(80))  # Страна спортсмена
    sport = db.Column(db.String(80))  # Спорт
    
    # Конструктор для создания нового объекта Sportman
    def __init__(self, name, gender, age, country, sport):
        self.name = name
        self.gender = gender
        self.age = age
        self.country = country
        self.sport = sport
        
# Создание соединения с базой данных 
con = sqlite3.connect('./instance/athletes.db', check_same_thread=False)
# Создание курсора для выполнения SQL запросов  
cur = con.cursor()

# Маршрут для корневой страницы
@app.route("/")
def hello_world():
    return render_template('main.html')

# Маршрут для получения информации о спортсмене по ID
@app.route("/sport/<id>")
def sport_id(id):
    sport_id = Sportman.query.filter_by(id=id).all()
    print(sport_id)
    # Проверка, найден ли спортсмен
    if sport_id != []:
        return render_template('sport_id.html', sport_id = sport_id[0])
    else:
        return "Такого спортсмена нет"

# Маршрут для получения списка всех спортсменов
@app.route("/sports")
def sports():
    sports = Sportman.query.all()
    # Возвращение списка спортсменов
    return render_template('sports.html', sports = sports)

# Маршрут для отображения формы добавления спортсмена
@app.route("/sport_form",methods=['GET','POST'])
def sport_form():
    # Создание формы
    form = MyForm()
        # Проверка, была ли отправлена заполненная форма на сервер
    if form.validate_on_submit():
        # Извлекаем данные из формы
        name=form.data['name']
        gender=form.data['gender']
        age=form.data['age']
        country=form.data['country']
        sport=form.data['sport']
        #Создаем объект спортсмен
        new_sport = Sportman(name, gender, age, country, sport)
        #Добавляем в БД
        db.session.add(new_sport)
        #Фиксируем изменения
        db.session.commit()
        return 'Спортсмен добавлен!'
    # Возвращаем форму для отображения к заполнению
    return render_template('sport_add.html', form=form)
    
#Маршрут для добавления нового спортсмена
@app.route("/sport_add")
def sport_add():
    # Получение данных о фильме из параметров запроса
    name = request.args.get('name')
    gender = request.args.get('gender')
    age = request.args.get('age')
    country = request.args.get('country')
    sport = request.args.get('sport')
    # Формирование кортежа с данными о спортсмене
    sport_data = (name, gender, age, country, sport)
    # Выполнение SQL запроса для добавления спортсмена в базу данных
    cur.execute('INSERT INTO athletes (name, gender, age, country, sport) VALUES (?, ?, ?, ?, ?)', sport_data)
    # Сохранение изменений в базе данных
    con.commit()
    # Возвращение подтверждения о добавлении спортсмена
    return "name = {}; gender = {}; age = {}; country = {}; sport = {} ".format(name, gender, age, country, sport)    
    
# Запуск приложения, если оно выполняется как главный модуль
if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False # отключаем проверку  CSRF для WTForms
    # Запуск приложения в режиме отладки
    app.run()