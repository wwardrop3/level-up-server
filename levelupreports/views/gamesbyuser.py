
from venv import create
from django.db import connection
from django.shortcuts import render
from django.views import View
from levelupreports.views.helpers import dict_fetch_all


class UserGameList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:
            
            # Write query to get all games along with the gamer first name, last name, and id
            db_cursor.execute(
                """
                SELECT g.id, g.title, g.maker, g.skill_level, g.number_of_players, g.game_type_id, u.first_name || " " || u.last_name as full_name, u.id, g.gamer_id
                FROM levelupapi_game g
                JOIN levelupapi_gamer ga ON g.gamer_id = ga.id
                JOIN auth_user u ON ga.user_id = u.id
    
                """
            )
                
            
                # pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            games_by_user = []
            
            dataset = dict_fetch_all(db_cursor)
            
            for row in dataset:
            # TODO: Create a dictionary called game that includes 
            # the name, description, number_of_players, maker,
            # game_type_id, and skill_level from the row dictionary
                game = {
                    "title": row['title'],
                    "number_of_players": row['number_of_players'],
                    "maker": row['maker'],
                    "game_type": row['game_type_id'],
                    "skill_level": row['skill_level'],
                }
                  
                user_dict = None
                
                # see if the gamer has been added to the games_by_user list already
                for user_game in games_by_user:
                    if user_game in games_by_user:
                        user_dict = user_game
                
                if user_dict:
                    # if the user_dict is already in the games_by_user_list already
                    # add the game to the user_dict
                    user_dict['games'].append(game)
                
                else:
                    #  if the user is not on the games_by_user list, create and add the user to the list
                    games_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "games": [game]
                        
                    })
                    
            # the template string must match the file name of the html template
            template = 'users/list_with_games.html'
            
            # the context will be a dictionary that the template can access to show data
            context = {
                "usergame_list": games_by_user
            }
                    
            return render(request, template, context)
                
                
                
                
                
                
                
                
                
                
                
                
                
                # Take the flat data from the dataset, and build the
                # following data structure for each gamer.
                # This will be the structure of the games_by_user list:
                #
                # [
                #   {
                #     "id": 1,
                #     "full_name": "Admina Straytor",
                #     "games": [
                #       {
                #         "id": 1,
                #         "title": "Foo",
                #         "maker": "Bar Games",
                #         "skill_level": 3,
                #         "number_of_players": 4,
                #         "game_type_id": 2
                #       },
                #       {
                #         "id": 2,
                #         "title": "Foo 2",
                #         "maker": "Bar Games 2",
                #         "skill_level": 3,
                #         "number_of_players": 4,
                #         "game_type_id": 2
                #       }
                #     ]
                #   },
                # ]
                
        