from flask import Flask, render_template, request, redirect, url_for
from data import queries

app = Flask('codecool_series')
offset = 0


@app.route('/')
def index():
    genre_selection = queries.get_selection_list()
    if '?search' in request.full_path:
        search = request.args['search']
        result = queries.get_search_result(search)
        return render_template('index.html', shows=result, genre_selection=genre_selection)
    shows = queries.get_shows()
    return render_template('index.html',
                           shows=shows,
                           genre_selection=genre_selection)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows-by-rating')
def shows_by_rating():
    global offset
    if 'next' in request.full_path:
        offset += 15
        query_result = queries.get_15_most_rated_shows(offset=offset)
    elif 'back' in request.full_path and offset != 0:
        offset -= 15
        query_result = queries.get_15_most_rated_shows(offset=offset)
    else:
        query_result = queries.get_15_most_rated_shows()
    shows = []
    _id = None
    count = -1
    for show in query_result:
        if show['id'] == _id:
            shows[count]['genre'] += f", {show['genre']}"
        else:
            _id = show['id']
            shows.append(show)
            count += 1

    return render_template('shows_by_rating.html', shows=shows)


@app.route('/tv-show/<show_id>')
def details_of_show(show_id):
    query = queries.get_show_by_id(show_id)
    show = None
    for i in range(len(query)):
        if i == 0:
            show = query[0]
        else:
            show['genre'] += f", {query[i]['genre']}"
    show['trailer'] = show['trailer'].replace('watch?v=', 'embed/') if show['trailer'] else None
    seasons = queries.get_seasons_by_show_id(show_id)
    return render_template('details_of_show.html',
                           show=show,
                           seasons=seasons)


@app.route('/episodes-for-each-shows')
def ep_for_each_shows():
    shows = queries.get_ep_for_each_shows()
    for show in shows:
        if show['episodes'] >= 100:
            show['is_long'] = True
        else:
            show['is_long'] = False
    print(shows)
    return render_template('ep_for_each_shows.html', shows=shows)


@app.route('/top-10-actors-by-character')
def top_10_actors_by_character():
    actors = queries.get_top_ten_actors_by_character()
    for i, actor in enumerate(actors):
        if i == 0:
            actor['medal'] = 'https://encrypted-tbn0.gstatic.com/' \
                             'images?q=tbn:ANd9GcR7p_4GwF4YPCBcDBqV96u-8Kp3gMWRJ5G1F1s-jIYLh5WxFWwi'
        elif i == 1:
            actor['medal'] = 'https://encrypted-tbn0.gstatic.com/' \
                             'images?q=tbn:ANd9GcQiDVHfCupN5PnzjC1NyEqdZvkYbg4DDm7dOD7wmgftN02lOqjL'
        elif i == 2:
            actor['medal'] = 'https://st3.depositphotos.com/' \
                             '2899123/17890/v/1600/depositphotos_' \
                             '178901942-stock-illustration-bronz-trophy-award-medal.jpg'
    return render_template('top_10_actors_by_character.html', actors=actors)


@app.route('/ten-most-rated-shows')
def ten_most_rated_shows_by_genre():
    genre = request.args['genre']
    shows = queries.get_10_most_rated_shows_by_genre(genre)
    return render_template('ten_most_rated_shows_by_genre.html',
                           shows=shows,
                           genre=genre)


@app.route('/what-a-year')
def what_a_year():
    years = queries.get_what_a_year()
    return render_template('what_a_year.html', years=years)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
