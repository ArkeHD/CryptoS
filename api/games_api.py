import flask
from flask import Flask, render_template, redirect, request, jsonify
import data.db_session as db_session
from data.users import User
from data.games import Games


blueprint = flask.Blueprint(
    'games_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/del_games/<int:game_id>', methods=['DELETE'])
def api_delete_game(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Games).get(game_id)
    if not game:
        return jsonify({'error': 'Not found, cry about it'})
    db_sess.delete(game)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/get_games')
def api_get_games():
    db_sess = db_session.create_session()
    game = db_sess.query(Games).all()
    return jsonify(
        {
            'games':
                [item.to_dict(only=('name', 'id'))
                 for item in game]
        }
    )


@blueprint.route('/api/get_users')
def api_get_users():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('name', 'role'))
                 for item in user]
        }
    )


@blueprint.route('/api/get_developer/<int:game_id>')
def api_get_author(game_id):
    db_sess = db_session.create_session()
    author_id = db_sess.query(Games).filter(Games.id == game_id).first().get(Games.author_id)
    author_name = db_sess.query(Games).filter(User.id == author_id).first().get(User.name)
    if author_name:
        return jsonify({'name': author_name})
    else:
        return jsonify({'error': 'Not found, cry about it'})


@blueprint.route('/api/games/<int:game_id>', methods=['GET'])
def api_get_game(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Games).get(game_id)
    if not game:
        return jsonify({'error': 'Not found, cry about it'})
    return jsonify(
        {
            'games': game.to_dict(only=(
                'name', 'id'))
        }
    )


@blueprint.route('/api/games_pric/<int:game_id>', methods=['GET'])
def api_get_games_price(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Games).get(game_id)
    if not game:
        return jsonify({'error': 'Not found, cry about it'})
    return jsonify(
        {
            'games': game.to_dict(only=(
                'name', 'price'))
        }
    )


@blueprint.route('/api/games_genre/<int:game_id>', methods=['GET'])
def api_get_games_genre(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Games).get(game_id)
    if not game:
        return jsonify({'error': 'Not found, cry about it'})
    return jsonify(
        {
            'games': game.to_dict(only=(
                'name', 'genre'))
        }
    )

@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found, cry about it'})
    return jsonify(
        {
            'users': user.to_dict(only=(
                'name', 'id'))
        }
    )


@blueprint.route('/api/users_balance/<int:user_id>', methods=['GET'])
def api_get_users_balance(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found, cry about it'})
    return jsonify(
        {
            'users': user.to_dict(only=(
                'name', 'balance'))
        }
    )


@blueprint.route('/api/users_cart/<int:user_id>', methods=['GET'])
def api_get_users_cart(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found, cry about it'})
    return jsonify(
        {
            'users': user.to_dict(only=(
                'name', 'cart'))
        }
    )


@blueprint.route('/api/users_email/<int:user_id>', methods=['GET'])
def api_get_users_email(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found, cry about it'})
    return jsonify(
        {
            'users': user.to_dict(only=(
                'name', 'email'))
        }
    )


@blueprint.route('/api/users_role/<int:user_id>', methods=['GET'])
def api_get_users_role(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found, cry about it'})
    return jsonify(
        {
            'users': user.to_dict(only=(
                'name', 'role'))
        }
    )


@blueprint.route('/api/games_genre/<int:game_id>', methods=['GET'])
def api_get_games_genre(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Games).get(game_id)
    if not game:
        return jsonify({'error': 'Not found, cry about it'})
    return jsonify(
        {
            'games': game.to_dict(only=(
                'name', 'genre'))
        }
    )


@blueprint.route('/api/games_description/<int:game_id>', methods=['GET'])
def api_get_games_description(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Games).get(game_id)
    if not game:
        return jsonify({'error': 'Not found, cry about it'})
    return jsonify(
        {
            'games': game.to_dict(only=(
                'name', 'description'))
        }
    )

