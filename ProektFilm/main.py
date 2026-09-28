from flask import Flask, render_template, request, redirect, session
from themoviedb import TMDb
import random

app = Flask(__name__)
app.secret_key = "любой_секретный_ключ_12345"

tmdb = TMDb(api_key="e8990f247881c86eb03fcf60e9b7bd51", language="ru-RU")


# ==================== ГЛАВНАЯ ====================
@app.route('/')
def index():
    genre = random.choice([28, 12, 16, 35, 80, 18, 14, 27, 878, 53])
    page = random.randint(1, 50)

    kino = tmdb.discover().movie(
        with_genres=genre,
        page=page,
        sort_by="popularity.desc"
    )

    film = random.choice(kino) if kino else None
    return render_template('index.html', film=film)


# ==================== ЛАЙК (сохраняем в избранное) ====================
@app.route('/like')
def like():
    film_data = {
        'id': request.args.get('id'),
        'title': request.args.get('title'),
        'poster_path': request.args.get('poster_path'),
        'release_date': request.args.get('release_date'),
        'vote_average': request.args.get('vote_average'),
    }

    favourites = session.get('favourites', [])

    if not any(f['id'] == film_data['id'] for f in favourites):
        favourites.append(film_data)

    session['favourites'] = favourites
    return redirect('/')


# ==================== СТРАНИЦА ИЗБРАННОГО ====================
@app.route('/favourites')
def favourites():
    favourites_list = session.get('favourites', [])
    return render_template('favourites.html', favourites=favourites_list)


# ==================== ОЧИСТИТЬ ИЗБРАННОЕ ====================
@app.route('/clear')
def clear():
    session['favourites'] = []
    return redirect('/favourites')


# ==================== ПОИСК ====================
@app.route('/search', methods=['GET', 'POST'])
def search_application():
    movies = []
    error = None

    if request.method == 'POST':
        search_id = request.form['search_id'].strip()
        if search_id:
            movies = tmdb.search().movies(search_id)
            if not movies:
                error = "Фильм не найден."
        else:
            error = "Введите название."

    return render_template('search.html', movies=movies, error=error)


# ==================== ДУЭЛИ ====================
@app.route('/duel')
def duel():
    return render_template('duel.html')


if __name__ == '__main__':
    app.run(debug=True)