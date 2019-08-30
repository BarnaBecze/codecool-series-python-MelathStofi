from data import data_manager


def get_shows():
    return data_manager.execute_select('''
                                        SELECT title, year, rating, homepage, trailer, runtime, STRING_AGG(g.name, ', ') AS genre
                                        FROM shows
                                        JOIN show_genres sg on shows.id = sg.show_id
                                        JOIN genres g on sg.genre_id = g.id
                                        GROUP BY shows.id
                                        ORDER BY rating DESC;''')
