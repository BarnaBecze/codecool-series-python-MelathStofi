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


@app.route('/all-shows')
@cache.cached()
def get_all_shows():
    shows = queries.get_shows()
    resp = []
    for show in shows:
        resp.append({
            "title": dumps(show['title']),
            "year": dumps(show['year']),
            "runtime": dumps(show['runtime']),
            "rating": dumps(show['rating']),
            "homepage": dumps(show['homepage']),
            "trailer": dumps(show['trailer'])
        })
    print(resp)
    return make_response(jsonify(resp), 200)


@app.route('/design')
def design():
    return render_template('design.html')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
