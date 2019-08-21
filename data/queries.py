from data import data_manager


def get_shows():
    return data_manager.execute_select('SELECT id, title FROM shows;')


def get_15_most_rated_shows(offset=0):
    return data_manager.execute_select("""
                                    SELECT s.id AS id, title, year, runtime, name AS genre, rating, trailer, homepage
                                    FROM show_genres x
                                    JOIN genres g
                                        ON x.genre_id = g.id 
                                    RIGHT JOIN (SELECT * FROM shows 
                                                ORDER BY rating DESC LIMIT 15 OFFSET %(offset)s) s 
                                        ON x.show_id = s.id 
                                    ORDER BY rating DESC;
                                    """, {'offset': offset})


def get_show_by_id(show_id):
    return data_manager.execute_select("""
                                    SELECT s.*, g.name AS genre
                                    FROM show_genres x
                                    JOIN genres g ON x.genre_id = g.id
                                    JOIN shows s on x.show_id = s.id
                                    WHERE s.id = %(show_id)s
                                    """, {'show_id': show_id})


def get_seasons_by_show_id(show_id):
    return data_manager.execute_select("""
                                    SELECT title, overview
                                    FROM seasons
                                    WHERE show_id = %(show_id)s
                                    """, {'show_id': show_id})
