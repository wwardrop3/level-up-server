
from venv import create
from django.db import connection
from django.shortcuts import render
from django.views import View
from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            # Write query to get all games along with the gamer first name, last name, and id
            db_cursor.execute(
                """
                SELECT e.id as event_id, e.date as event_date, e.time as event_time, g.title as game_title, u.first_name || " " || u.last_name as full_name, g.id as gamer_id, e.description
                FROM levelupapi_event e
                JOIN levelupapi_eventgamer eg ON eg.event_id = e.id
                JOIN levelupapi_game g ON e.game_id = g.id
                JOIN levelupapi_gamer ga ON ga.id = eg.gamer_id 
                JOIN auth_user u ON u.id = ga.user_id 
    
                """
            )
                
            
                # pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            event_by_user = []
            
            dataset = dict_fetch_all(db_cursor)
            
            for row in dataset:
            # TODO: Create a dictionary called game that includes 
            # the name, description, number_of_players, maker,
            # game_type_id, and skill_level from the row dictionary
                event = {
                    "id": row['event_id'],
                    "event_date": row['event_date'],
                    "event_time": row['event_time'],
                    "game_name": row['game_title']
                }
                  
                user_dict = None
                
                # see if the gamer has been added to the event_by_user list already
                for user_event in event_by_user:
                    if user_event in event_by_user:
                        user_dict = user_event
                
                if user_dict:
                    # if the user_dict is already in the event_by_user_list already
                    # add the game to the user_dict
                    user_dict['events'].append(event)
                
                else:
                    #  if the user is not on the event_by_user list, create and add the user to the list
                    event_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                        
                    })
                    
            # the template string must match the file name of the html template
            template = 'users/list_with_events.html'
            
            # the context will be a dictionary that the template can access to show data
            context = {
                "userevent_list": event_by_user
            }
                    
            return render(request, template, context)
                
                
                
                
                
                
                
                
                
                
                
                
# [
#   {
#     "gamer_id": 1,
#     "full_name": "Molly Ringwald",
#     "events": [
#       {
#         "id": 5,
#         "date": "2020-12-23",
#         "time": "19:00",
#         "game_name": "Fortress America"
#       }
#     ]
#   }
# ]