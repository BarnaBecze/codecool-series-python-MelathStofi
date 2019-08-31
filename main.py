from flask_caching import Cache
from flask import Flask, render_template, url_for, make_response, jsonify
from data import queries
from json import dumps


cache = Cache(config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 300})
app = Flask('codecool_series')
cache.init_app(app)


@app.route('/')
@cache.cached()
def index():
    shows = queries.get_shows()
    return render_template('index.html', shows=shows)


@app.route('/<title>')
def get_title_details(title):
    shows = queries.get_show_details(title)
    resp = []
    for show in shows:
        resp.append({
            "title": dumps(show['title']),
            "year": dumps(str(show['year'])),
            "runtime": dumps(show['runtime']),
            "rating": dumps(str(show['rating'])),
            "genre": dumps(show['genre']),
            "overview": dumps(show['overview'])
        })
    return make_response(jsonify(resp), 200)


@app.route('/design')
def design():
    return render_template('design.html')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
