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


def get_search_result(_input):
    subject = f"%{_input}%"
    return data_manager.execute_select("""
                                    SELECT * FROM shows
                                    WHERE title ILIKE %(subject)s
                                    """, {'subject': subject})


def get_ep_for_each_shows():
    return data_manager.execute_select("""
                                    SELECT s.title, COUNT(e.*) episodes
                                    FROM seasons se
                                    JOIN episodes e on se.id = e.season_id
                                    JOIN shows s on se.show_id = s.id
                                    WHERE se.title != 'Specials'
                                    GROUP BY s.title
                                    """)


def get_top_ten_actors_by_character():
    return data_manager.execute_select("""
                                    SELECT a.*, COUNT(sc.*) characters
                                    FROM actors a
                                    JOIN show_characters sc on a.id = sc.actor_id
                                    GROUP BY a.id
                                    ORDER BY characters DESC, a.name LIMIT 10
                                    """)


def get_10_most_rated_shows_by_genre(genre):
    return data_manager.execute_select("""
                                    SELECT s.title, s.year, ROUND(s.rating, 1) rating, string_agg(g.name, ',') genres
                                    FROM show_genres x
                                    JOIN genres g on x.genre_id = g.id
                                    JOIN shows s on x.show_id = s.id
                                    WHERE g.name = %(genre)s
                                    GROUP BY s.id
                                    ORDER BY s.rating DESC, s.title LIMIT 10
                                    """, {'genre': genre})


def get_selection_list():
    return data_manager.execute_select("""
                                    SELECT g.name
                                    FROM show_genres x
                                    JOIN genres g on x.genre_id = g.id
                                    JOIN shows s on x.show_id = s.id
                                    GROUP BY g.id
                                    ORDER BY g.name
                                    """)


def get_what_a_year():
    return data_manager.execute_select("""
                                    SELECT year, ROUND(AVG(rating), 1) avg_rating, COUNT(id) shows
                                    FROM shows
                                    WHERE year >= '1970-01-01' AND year < '2010-01-01'
                                    GROUP BY year
                                    ORDER BY year;
                                    """)
