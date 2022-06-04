SELECT
    e.id,
    e.description,
    e.game_id,
    e.organizer_id,
    o.bio,
    g.title
FROM levelupapi_event e
JOIN levelupapi_gamer o
ON e.organizer_id = o.id
JOIN levelupapi_game g
ON e.game_id = g.id



SELECT
    e.id,
    e.date,
    e.description,
    e.organizer_id,
    e.game_id,
    o.bio

FROM levelupapi_event e
JOIN levelupapi_gamer o

Drop Table 

SELECT * FROM Gamer


      SELECT g.id, g.title, g.maker, g.skill_level, g.number_of_players, g.game_type_id, u.first_name || " " || u.last_name as full_name, u.id, g.gamer_id
                FROM levelupapi_game g
                JOIN levelupapi_gamer ga ON g.gamer_id = ga.id
                JOIN auth_user u ON ga.user_id = u.id





SELECT e.id, e.description, e.date, e.time, g.title, e.game_id, ga.bio, u.first_name || " " || u.last_name as attendee_name
FROM levelupapi_event e
JOIN levelupapi_game g ON g.id = e.game_id 
JOIN levelupapi_eventattendees ea ON ea.event_id = e.id
JOIN levelupapi_gamer ga ON ga.id = ea.gamer_id
JOIN auth_user u ON u.id = ga.user_id

    SELECT e.id as event_id, e.date as event_date, e.time as event_time, g.title as game_title, u.first_name || " " || u.last_name as full_name, g.id as gamer_id, e.description
                FROM levelupapi_event e
                JOIN levelupapi_eventgamer eg ON eg.event_id = e.id
                JOIN levelupapi_game g ON e.game_id = g.id
                JOIN levelupapi_gamer ga ON ga.id = eg.gamer_id 
                JOIN auth_user u ON u.id = ga.user_id 
    