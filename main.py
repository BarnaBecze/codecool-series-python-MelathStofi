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


@app.route('/15-most-rated-shows')
def _15_most_rated_shows():
    shows = queries.get_15_most_rated_shows()
    return render_template('15_most_rated_shows.html', shows=shows)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
