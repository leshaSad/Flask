import os

from flask import Flask, url_for, request, render_template
from data import db_session, jobs_api
from flask_restful import reqparse, abort, Api, Resource
from data.users import User
from data.jobs import Jobs
from data.users_resources import UsersListResource, UsersResource
from add_users import insert_users
from add_jobs import insert_jobs

db_sess = db_session.create_session()
db_session.global_init("db/mars_explorer.db")
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
answers = {
    'title': 'Анкета',
    'surname': 'Watny',
    'name': 'Mark',
    'education': 'выше среднего',
    'profession': 'штурман марсохода',
    'sex': 'male',
    'motivation': 'Всегда мечтал застрять на Марсе!',
    'ready': 'True'
}
planet = {
    'name': {
        'Меркурий': {
            '1': 'Меркурий — самая близкая к Солнцу планета Солнечной системы.',
            '2': 'На Меркурии нет атмосферы, пригодной для дыхания, и жидкой воды.',
            '3': 'Планета обладает слабым магнитным полем, составляющим около 1 % от земного.',
            '4': 'Поверхность Меркурия испещрена кратерами, свидетельствующими о его бурной истории.',
            '5': 'Несмотря на экстремальные температуры (от −180 °C до +430 °C), Меркурий поражает своей уникальной геологией.'
        },
        'Венера': {
            '1': 'Венера — вторая по удалённости от Солнца планета Солнечной системы, часто называемая «утренней» или «вечерней звездой».',
            '2': 'По размеру и массе Венера близка к Земле, из‑за чего её нередко называют «сестрой Земли».',
            '3': 'На Венере крайне плотная атмосфера, состоящая преимущественно из углекислого газа (CO2), что создаёт мощный парниковый эффект.',
            '4': 'Температура на поверхности Венеры достигает около 470 °C — это самая горячая планета в Солнечной системе.',
            '5': 'На Венере нет воды в жидком состоянии: вся влага давно испарилась из‑за экстремального нагрева.'
        },
        'Земля': {
            '1': 'Эта планета — наш общий дом, где каждый уголок наполнен удивительной жизнью.',
            '2': 'На ней существует невероятное разнообразие экосистем — от знойных пустынь до ледяных полярных шапок.',
            '3': 'Земля обладает уникальной биосферой, где миллионы видов организмов сосуществуют в хрупком равновесии.',
            '4': 'Её климат формирует разнообразные погодные явления — от нежных утренних туманов до мощных ураганов.',
            '5': 'На этой планете сохранились древние леса, кристально чистые озёра и величественные горные хребты.'
        },
        'Марс': {
            '1': 'Эта планета близка к Земле.',
            '2': 'На ней много необходимых ресурсов.',
            '3': 'На ней есть небольшое магнитное поле.',
            '4': 'Наконец, она просто красива!',
            '5': 'На ней есть вода и атмосфера'
        },
        'Юпитер': {
            '1': 'Юпитер — крупнейшая планета Солнечной системы, его масса более чем в два раза превышает суммарную массу всех остальных планет.',
            '2': 'На Юпитере нет твёрдой поверхности: он состоит преимущественно из водорода и гелия в газообразном и жидком состояниях.',
            '3': 'Планета обладает мощным магнитным полем, которое примерно в 20 000 раз сильнее земного.',
            '4': 'В атмосфере Юпитера наблюдаются гигантские штормы, самый известный из которых — Большое Красное Пятно, существующее уже несколько столетий.',
            '5': 'У Юпитера более 90 спутников, среди которых выделяются четыре крупных галилеевых спутника: Ио, Европа, Ганимед и Каллисто.'
        },
        'Сатурн': {
            '1': 'Сатурн — одна из самых узнаваемых планет Солнечной системы благодаря своим величественным кольцам, состоящим из миллиардов ледяных и каменных частиц.',
            '2': 'Эта планета значительно больше Земли: её экваториальный радиус превышает земной более чем в 9 раз.',
            '3': 'На Сатурне нет твёрдой поверхности — он относится к газовым гигантам и состоит преимущественно из водорода и гелия.',
            '4': 'У Сатурна более 140 известных спутников, самый крупный из которых — Титан, обладающий плотной атмосферой и метановыми озёрами.',
            '5': 'Магнитное поле Сатурна слабее земного, но всё же достаточно мощное, чтобы защищать планету от солнечного ветра.'
        },
        'Уран ': {
            '1': 'Уран — седьмая по удалённости от Солнца планета Солнечной системы.',
            '2': 'Эта планета вращается «лёжа на боку»: её ось наклонена примерно на 98 °С относительно плоскости орбиты.',
            '3': 'У Урана самая низкая температура среди планет Солнечной системы — до 224 °С.',
            '4': 'На Уране есть система колец, хотя они гораздо менее заметны, чем у Сатурна.',
            '5': 'У планеты 27 известных спутников, самый крупный из которых — Титания.'
        },
        'Нептун': {
            '1': 'Нептун — самая далёкая от Солнца планета Солнечной системы, расположенная на расстоянии около 4,5 млрд км от нашего светила.',
            '2': 'На Нептуне царит экстремальный холод: средняя температура атмосферы составляет около - 220 °С',
            '3': 'Эта планета обладает мощной атмосферой, где наблюдаются самые сильные ветры в Солнечной системе — их скорость может достигать 2100 км/ч.',
            '4': 'Нептун имеет систему колец, хотя они не такие заметные, как у Сатурна, и состоят преимущественно из пыли и ледяных частиц.',
            '5': 'У Нептуна известно 14 спутников, самый крупный из которых — Тритон, обладающий уникальной геологической активностью и азотными гейзерами.'
        }
    }
}


@app.route('/promotion')
def promotion():
    adds_list = ['Человечество вырастает из детства.', 'Человечеству мала одна планета.',
                 'Мы сделаем обитаемыми безжизненные пока планеты.', 'И начнем с Марса!', 'Присоединяйся!']
    return '</br>'.join(adds_list)


@app.route('/image_mars')
def image_mars():
    return """<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <title>Привет, Марс!</title>
                      </head>
                      <body>
                        <h1>Жди нас, Марс!</h1>
                        <img src="/static/images/MARS.png"/>
                        <figcaption>Вот она какая, красная планета</figcaption>
                      </body>
                    </html>"""


@app.route('/promotion_image', methods=['GET', 'POST'])
def promotion_image():
    return f"""<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        <link rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                    crossorigin="anonymous">
                        <title>Привет, Марс!</title>
                      </head>
                      <body>
                        <h1>Жди нас, Марс!</h1>
                        <img src="/static/images/MARS.png"/>
                        <div class="alert alert-primary" role="alert">
                      Человечество вырастает из детства.
                        </div>
                        <div class="alert alert-success" role="alert">
                      Человечеству мала одна планета.
                        </div>
                        <div class="alert alert-secondary" role="alert">
                      Мы сделаем обитаемыми безжизненные пока планеты.
                        </div>
                        <div class="alert alert-warning" role="alert">
                      И начнем с Марса!
                        </div>
                        <div class="alert alert-danger" role="alert">
                      Присоединяйся!
                        </div>
                      </body>
                    </html>"""


@app.route('/astronaut_selection', methods=['GET', 'POST'])
def astronaut_selection():
    if request.method == 'GET':
        return f'''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                crossorigin="anonymous">
                                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                                <title>Отбор астронавтов</title>
                              </head>
                              <body>
                              <center>
                                <h1>Анкета претедента </h1>
                                <h4>на участие в миссии</h4>
                              </center>
                                <div>
                                    <form class="login_form" method="post" enctype="multipart/form-data">
                                        <input type="text" class="form-control" id="surname" aria-describedby="surnameHelp" placeholder="Введите фамилию" name="surname">
                                        <input type="text" class="form-control" id="name" aria-describedby="nameHelp" placeholder="Введите имя" name="name">
                                        <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">
                                        <div class="form-group">
                                            <label for="classSelect">Какое у вас образование</label>
                                            <select class="form-control" id="classSelect" name="class">
                                              <option>Начальное</option>
                                              <option>Среднее</option>
                                              <option>Профессиональное</option>
                                            </select>
                                         </div>
                                         <div class="form-group">
                                            <label for="form-check">Какие у вас есть профессии?</label>
                                            <div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        инженер-исследователь
                                      </label>
                                    </div>
                                    <div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        пилот
                                      </label>
                                    </div>
                                    <div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        строитель
                                      </label>
                                    </div>
                                    <div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        экзобиолог
                                      </label>
                                    </div>
                                    <div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        врач
                                      </label>
                                    </div>
                                    <div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        инженер по терраформированию
                                      </label>
                                    </div>
                                    <div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        климатолог
                                      </label>
                                    </div>
                                    <div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        специалист по радиационной защите
                                      </label>
                                    </div>
                                    <div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        астрогеолог
                                      </label>
                                    </div><div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        гляциолог
                                      </label>
                                    </div><div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        инженер жизнеобеспечения
                                      </label>
                                    </div><div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        метеоролог
                                      </label>
                                    </div><div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        оператор марсохода
                                      </label>
                                    </div><div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        киберинженер
                                      </label>
                                    </div><div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        штурман
                                      </label>
                                    </div><div class="form-check">
                                      <input class="form-check-input" type="checkbox" value="" id="flexCheckChecked" >
                                      <label class="form-check-label" for="flexCheckChecked">
                                        пилот дронов
                                      </label>
                                        </div>
                                        <div class="form-group">
                                            <label for="form-check">Укажите пол</label>
                                            <div class="form-check">
                                              <input class="form-check-input" type="radio" name="sex" id="sex_male" value="male" checked>
                                              <label class="form-check-label" for="sex_male">Мужской</label>
                                            </div>
                                            <div class="form-check">
                                              <input class="form-check-input" type="radio" name="sex" id="sex_female" value="female">
                                              <label class="form-check-label" for="sex_female">Женский</label>
                                            </div>
                                        </div>
                                        <div class="form-group">
                                            <label for="about">Почему вы хотите принять участие в миссии?</label>
                                            <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                        </div>
                                        <div class="form-group">
                                            <label for="photo">Приложите фотографию</label>
                                            <input type="file" class="form-control-file" id="photo" name="file">
                                        </div>

                                        <div class="form-group form-check">
                                            <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                            <label class="form-check-label" for="acceptRules">Готов остаться на Марсе?</label>
                                        </div>
                                        <button type="submit" class="btn btn-primary">Отправить</button>
                                    </form>
                                </div>
                              </body>
                            </html>'''
    elif request.method == 'POST':
        print(request.form['surname'], '')
        print(request.form['name'], '')
        print(request.form['email'], '')
        print(request.form['class'], '')
        print(', '.join(request.form.getlist('profession')))
        print(request.form['sex'], '')
        print(request.form['about'], '')
        f = request.files['file']
        print(f.read())
        print(request.form['accept'], '')

        return "Форма отправлена"


@app.route('/choice/<planet_name>')
def choice_planet(planet_name):
    # Проверяем, существует ли такая планета
    if planet_name not in planet['name']:
        return f'''
                <!DOCTYPE html>
                <html>
                <head><title>Ошибка</title><meta charset="utf-8"></head>
                <body>
                    <h1>❌ Планета { planet_name } не найдена!</h1>
                    <a href="/">Вернуться на главную</a>
                </body>
                </html>
            '''

    # Получаем данные о планете если она есть
    planet_facts = planet['name'][planet_name]
    fist_fact = planet_facts['1']
    del planet_facts['1']
    return render_template('choice.html', p=planet_facts, planet=planet_name, f_p=fist_fact)

@app.route('/results/<nickname>/<int:level>/<float:rating>')
def result(nickname, level, rating):
    return f"""<!doctype html>
                    <html lang="en">
                      <head>
                        <meta charset="utf-8">
                        <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                        <link rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                    crossorigin="anonymous">
                        <title>Результаты</title>
                      </head>
                      <body>
                        <h1>Результаты отбора</h1>
                        <h2>Претендента на участие в миссии {nickname}:</h2>
                        <div class="alert alert-primary" role="alert">
                      Поздравляем ваш рейтинг после {level} этапа отбора
                        </div>
                        <h3>составляет {rating}!</h3>
                        <div class="alert alert-success" role="alert">
                      Желаем удачи!
                        </div> 
                      </body>
                    </html>"""


@app.route('/load_photo', methods=['GET', 'POST'])
def load_photo():
    if request.method == 'GET':
        if not os.path.exists('static/uploads'):
            os.makedirs('static/uploads')
        return f'''<!doctype html>
                            <html lang="en">
                              <head>
                                <meta charset="utf-8">
                                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                                <link rel="stylesheet"
                                href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                                integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                                crossorigin="anonymous">
                                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                                <title>Отбор астронавтов</title>
                              </head>
                              <body>
                              <center>
                                <h1>Загрузка фотографии</h1>
                                <h2>Для участия в миссии</h2>
                              </center>
                                <div>
                                    <form class="login_form" method="post" enctype="multipart/form-data">
                                        <div class="form-group">
                                            <label for="photo">Приложите фотографию</label>
                                            <input type="file" class="form-control-file" id="photo" name="file">
                                        </div>
                                        <img src="/static/uploads/photo.jpg" style="max-width: 300px; height: auto;">
                                        </br>
                                        <button type="submit" class="btn btn-primary">Отправить</button>
                                    </form>
                                </div>
                              </body>
                            </html>'''
    elif request.method == 'POST':
        f = request.files['file']
        f.save('static/uploads/photo.jpg')
        return "Форма отправлена"


@app.route('/carousel')
def carousel():
    return render_template('carousel.html')


@app.route('/')
@app.route('/index')
def index():
    jobs = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    names = {}
    for user in users:
        names[user.id] = f'{user.surname} {user.name}'
    param = {}
    param['title'] = 'main'
    return render_template('index.html', jobs=jobs, names=names, **param)


@app.route('/training/<prof>')
def training(prof):
    param = {}
    param['profession'] = prof
    return render_template('prof.html', **param)


@app.route('/list_prof/<listing>')
def spisok(listing):
    param = {}
    param['how'] = listing
    return render_template('prof_listing.html', **param)


@app.route('/answer')
@app.route('/auto_answer')
def answer():
    return render_template('auto_answer.html', **answers)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        print(request.form['id_astronaut'], '')
        print(request.form['password_astronaut'], '')
        print(request.form['id_captain'], '')
        print(request.form['password_captain'], '')

        return "Доступ разрешен"


@app.route('/distribution')
def distribution():
    return render_template('distrib.html')


@app.route('/table/<gender>/<int:age>')
def table(gender, age):
    param = {}
    param['gender'] = gender
    param['age'] = age
    return render_template('table.html', **param)


if __name__ == '__main__':
    app.register_blueprint(jobs_api.blueprint)
    api.add_resource(UsersListResource, '/api/v2/users')
    api.add_resource(UsersResource, '/api/v2/users/<int:news_id>')
    app.run(port=8082, host='127.0.0.1')
