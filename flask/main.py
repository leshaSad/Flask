import json

from flask import Flask, url_for, render_template, redirect,request

from forms.loginform import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/<title>')
@app.route('/index/<title>')
def index(title):
    param = {}
    param['title'] = title
    return render_template('base.html', **param)


@app.route('/odd_even')
def odd_even():
    print('jfjjf')
    return render_template('odd_even.html', number=8)


@app.route('/success')
def success():
    return 'OK'


@app.route('/news')
def news():
    with open("news.json", "rt", encoding="utf8") as f:
        news_list = json.loads(f.read())
    print(news_list)
    return render_template('news.html', news=news_list)


@app.route('/promotion')
def promotion():
    rec = ['Человечество вырастает из детства.', 'Человечеству мала одна планета.',
           'Мы сделаем обитаемыми безжизненные пока планеты.', 'И начнем с Марса!',
           'Присоединяйся!']
    return '</br>'.join(rec)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/image_mars')
def image():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                    <title>Привет, Марс!</title>
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1>
                    <img src="{url_for('static', filename='img/mars.jpg')}"
                        class="img-fluid"
                        alt="здесь должна была быть картинка, но не нашлась"
                        width=400>
                    <div>Вот она какая, красная планета.</dif>
                  </body>
                </html>
    
    
           '''


@app.route('/sample_page')
def return_sample_page():
    return f"""<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}" />
                    <title>Привет, Яндекс!</title>
                  </head>
                  <body>
                    <h1>Первая HTML-страница</h1>
                  </body>
                </html>"""


@app.route('/bootstrap_sample')
def bootstrap():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                    crossorigin="anonymous">
                    <title>Привет, Яндекс!</title>
                  </head>
                  <body>
                    <h1>Привет, Яндекс!</h1>
                    <div class="alert alert-primary" role="alert">
                      А мы тут компонентами Bootstrap балуемся
                    </div>
                  </body>
                </html>'''


@app.route('/promotion_image')
def promotion_image():
    return f'''<!doctype html>
                <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                    <link rel="stylesheet"
                    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                    integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                    crossorigin="anonymous">
                    <title>Колонизация</title>
                </head>
                <body>
                <h1>Жди нас, Марс!</h1>
                <img src="{url_for('static', filename='img/mars.jpg')}"
                                        class="img-fluid"
                                        alt="здесь должна была быть картинка, но не нашлась"
                                        width=400>
                <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}"/>
                <div class="--bs-secondary-color">
                    <h4>Человечество вырастает из детства.</h4>
                </div>
                </body>
                </html>'''


i = 0


@app.route('/i')
def show_i():
    global i
    i += 1
    return str(i)


@app.route('/greeting/<username>')
def greeting(username):
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                   <link rel="stylesheet"
                   href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css"
                   integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1"
                   crossorigin="anonymous">
                    <title>Привет, {username}</title>
                  </head>
                  <body>
                    <h1>Привет, {username}!</h1>
                  </body>
                </html>'''

@app.route('/astronaut_selection', methods=['POST', 'GET'])
def form_sample():
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
                            <title>Пример формы</title>
                          </head>
                          <body>
                          <center>
                            <h1>Анкета претендента</h1>
                            <h4>на участие в миссии</h4>
                        </center>
                            <div>
                                <form class="login_form" method="post">
                                    <input type="surname" class="form-control" id="surname" aria-describedby="emailHelp" placeholder="Введите фамилию" name="surname">
                                    <input type="name" class="form-control" id="name" placeholder="Введите имя" name="name">
                                    <input type="email" class="form-control" id="email" aria-describedby="emailHelp" placeholder="Введите адрес почты" name="email">

                                    <div class="form-group">
                                        <label for="classSelect">Какое у Вас образование?</label>
                                        <select class="form-control" id="classSelect" name="class">
                                          <option>дошкольное</option>
                                          <option>начальное общее</option>
                                          <option>основное общее</option>
                                          <option>среднее общее </option>
                                          <option>высшее</option>
                                        </select>
                                     </div>
                                    <div class="form-group">
                                        <label for="about">Какие у Вас есть профессии?</label>
                                    </div>
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
                                    <div class="form-group">
                                        <label for="form-check">Укажите пол</label>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="male" value="male" checked>
                                          <label class="form-check-label" for="male">
                                            Мужской
                                          </label>
                                        </div>
                                        <div class="form-check">
                                          <input class="form-check-input" type="radio" name="sex" id="female" value="female">
                                          <label class="form-check-label" for="female">
                                            Женский
                                          </label>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label for="about">Почему Вы хотите принять участие в миссии?</label>
                                        <textarea class="form-control" id="about" rows="3" name="about"></textarea>
                                    </div>
                                    <div class="form-group">
                                        <label for="photo">Приложите фотографию</label>
                                        <input type="file" class="form-control-file" id="photo" name="file">
                                    </div>
                                    <div class="form-group form-check">
                                        <input type="checkbox" class="form-check-input" id="acceptRules" name="accept">
                                        <label class="form-check-label" for="acceptRules">Готовы остаться на Марсе?</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary">Отправить</button>
                                </form>
                            </div>
                          </body>
                        </html>'''
    elif request.method == 'POST':
        print(request.form['surname'])
        print(request.form['name'])
        print(request.form['email'])
        print(request.form['class'])
        print(request.form['file'])
        print(request.form['about'])
        print(request.form['accept'])
        print(request.form['sex'])
        return "Форма отправлена"



if __name__ == '__main__':
    app.run(port=8082, host='127.0.0.1')
