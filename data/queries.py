from data import data_manager
from json import dumps


def get_shows():
    return data_manager.execute_select('''
                                        SELECT title, year, rating, homepage, trailer, runtime, STRING_AGG(g.name, ', ') AS genre
                                        FROM shows
                                        JOIN show_genres sg on shows.id = sg.show_id
                                        JOIN genres g on sg.genre_id = g.id
                                        GROUP BY shows.id
                                        ORDER BY rating DESC;''')


def get_show_details(title):
    return data_manager.execute_select(f"""
                                        SELECT title, year, rating, runtime, overview, STRING_AGG(g.name, ', ') AS genre
                                        FROM shows
                                        JOIN show_genres sg on shows.id = sg.show_id
                                        JOIN genres g on sg.genre_id = g.id
                                        WHERE title = '{title}'
                                        GROUP BY shows.id;
                                        """)
