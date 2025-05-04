import os
from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.games import Games
from forms.enters import LoginForm
from forms.user import RegisterForm
from forms.games import GamesForm
from flask_login import LoginManager, login_user, logout_user, current_user
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join("static", "IMG")
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
def index():
    return redirect('/register')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect("/games")
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            balance=0,
            role='Пользователь'
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect("/login")
    return render_template('registration.html', title='Регистрация', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/games")
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            login_user(user)
            return redirect("/games")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Главная', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logut():
    logout_user()
    return redirect('/register')


def main():
    db_session.global_init("db/base.db")
    db_sess = db_session.create_session()


@app.route("/games", methods=['GET', 'POST'])
def games():
    if not current_user.is_authenticated:
        return redirect("/register")
    images = {}
    db_sess = db_session.create_session()
    role = current_user.role
    games = db_sess.query(Games)

    for game in games:
        img = os.path.join(app.config["UPLOAD_FOLDER"], 'Default.jpg')
        if game.img:
            if os.path.isfile(os.path.join(app.config["UPLOAD_FOLDER"], game.img)):
                img = os.path.join(app.config["UPLOAD_FOLDER"], game.img)
        images[game.id] = img
    return render_template("games.html", games=games, user_role=role, images=images)


@app.route("/create_game", methods=['GET', 'POST'])
def create_game():
    if not current_user.is_authenticated:
        return redirect("/register")
    form = GamesForm()
    if form.validate_on_submit():
        if form.photo.data:
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        db_sess = db_session.create_session()
        games = Games(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            genre=str(form.genres.data),
            author_id=current_user.id,
            img=filename)
        db_sess.add(games)
        db_sess.commit()
        return redirect("/games")
    return render_template('create_game.html', title='Создание игры', form=form)


@app.route('/edit_games/<int:id>', methods=['GET', 'POST'])
def edit_games(id):
    if not current_user.is_authenticated:
        return redirect("/register")
    form = GamesForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        games = db_sess.query(Games).filter(Games.id == id,
                                            Games.author_id == current_user.id
                                            ).first()
        if games:
            form.name.data = games.name
            form.description.data = games.description
            form.price.data = games.price
            if games.img:
                form.photo.data = os.path.join(app.config['UPLOAD_FOLDER'], games.img)
        else:
            os.abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        games = db_sess.query(Games).filter(Games.id == id,
                                          Games.author_id == current_user.id
                                          ).first()
        if games:
            if form.photo.data:
                print(form.photo.data.filename)
                form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], form.photo.data.filename))
                games.img = secure_filename(form.photo.data.filename)
            else:
                games.img = None
            games.name = form.name.data
            games.description = form.description.data
            games.price = form.price.data
            games.author_id = current_user.id
            db_sess.commit()
            return redirect('/')
        else:
            os.abort(404)
    return render_template('create_game.html',
                           title='Редактирование игры',
                           form=form
                           )


@app.route('/games_delete/<int:id>', methods=['GET', 'POST'])
def games_delete(id):
    if not current_user.is_authenticated:
        return redirect("/register")
    db_sess = db_session.create_session()
    game = db_sess.query(Games).get(id)
    if not game:
        os.abort(404)
    if current_user.id != game.author_id and current_user.role != 'Администратор':
        os.abort(403)
    for user in db_sess.query(User).all():
        if user.cart:
            cart = user.cart.split(' ')
            if str(id) in cart:
                while str(id) in cart:
                    cart.remove(str(id))
                user.cart = ' '.join(cart)
    db_sess.delete(game)
    db_sess.commit()
    return redirect('/')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if not current_user.is_authenticated:
        return redirect("/register")
    db_sess = db_session.create_session()
    game = []
    if current_user.cart:
        game = current_user.cart.split(' ')
    games = []
    count = {}
    for i in game:
        g = db_sess.query(Games).filter(Games.id == int(i)).first()
        if g.id in count.keys():
            count[g.id] = count[g.id] + 1
        else:
            games.append(g)
            count[g.id] = 1
    total = sum(list(map(lambda x: x.price * count[x.id], games)))
    return render_template('cart.html', games=games, total=total, count=count)


@app.route('/cart_games_add/<int:id>', methods=['GET', 'POST'])
def cart_games_add(id):
    if not current_user.is_authenticated:
        return redirect("/register")
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    if user.cart:
        user.cart = current_user.cart + ' ' + str(id)
    else:
        user.cart = str(id)
    db_sess.commit()
    return redirect('/')


@app.route('/cart_game_delete/<int:id>', methods=['GET', 'POST'])
def cart_game_delete(id):
    if not current_user.is_authenticated:
        return redirect("/register")
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    cart = current_user.cart.split(' ')
    if str(id) in cart:
        cart.remove(str(id))
    user.cart = ' '.join(cart)
    db_sess.commit()
    return redirect('/cart')


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')

#Пмогите меня уже держат на этой планете более 10ти лет, я хочу доммммооооооооооооооооооооооооооооооооооооооооооооооооййййййййййййййй