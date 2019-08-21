from flask import Flask, render_template, url_for
from data import queries

app = Flask('codecool_series')


@app.route('/')
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/design')
def design():
    return render_template('design.html')


@app.route('/shows-by-rating')
def shows_by_rating():
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


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
