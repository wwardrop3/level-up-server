
from logging import raiseExceptions
from django.http import HttpResponseServerError
from rest_framework import serializers, status
from levelupapi.models import Game
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from levelupapi.models.game_type import GameType
from levelupapi.models.gamer import Gamer


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'game_type', 'title', 'maker', 'gamer', 'number_of_players', 'skill_level')
        
        # depth will return the nested objects that are associated with ids

class UpdateGameSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Game
        fields = ('id', 'game_type', 'title', 'maker', 'number_of_players', 'skill_level')


class GameView(ViewSet):
    
    
  
    def retrieve(self, request, pk):
        
        
        game = Game.objects.get(pk = pk)
        serializer = GameSerializer(game)
        
        return Response(serializer.data)


    # request holds all of the information for the request
    def list(self, request):
        
        games = Game.objects.all()
        
        
        
        
        # query_params is a dictionary of any query parameters in the url
        #searching for query parameter "type", if its not there, it will return None
        game_type = request.query_params.get('type', None)
        
        if game_type is not None:
            # game_type will be the id of the gametype being queried 
            games = games.filter(game_type_id = game_type)
            
        serializer = GameSerializer(games, many=True)
        
        return Response(serializer.data)
    
    
    # EQUIVALENT OF....
#     db_cursor.execute("""
#     select *
#     from levelupapi_game
#     where game_type_id = ?
# """, (game_type,))

    
    def create(self, request):
        
        # each request has the user object of the authorized user that is logged in
    #equivalent to...
        # db_cursor.execute("""
        # select *
        # from levelupapi_gamer
        # where user = ?
        # """, (user,))
        
        #because the Gamer is set as a foreign key on the game database, django will only take the pk of the gamer object and save to the game
        gamer = Gamer.objects.get(user = request.auth.user)
        
        
        # matching up the game_type id on the new game with the gametype database to attach the object to the new game
        game_type = GameType.objects.get(pk=request.data['game_type'])
        
        game = Game.objects.create(
            title = request.data['title'],
            maker = request.data['maker'],
            number_of_players = request.data['number_of_players'],
            skill_level = request.data['skill_level'],
            gamer = gamer,
            game_type = game_type
        
        )
        
        serializer = GameSerializer(game)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        
        game = Game.objects.get(pk=pk)
        serializer = UpdateGameSerializer(game, data=request.data)
        # below gives a better explaination that is easier to understand.
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        
        
        
    def destroy(self, request, pk):
        
        game = Game.objects.get(pk = pk)
        
        game.delete()
        
        return Response(None, status= status.HTTP_204_NO_CONTENT)
        
        
        # OLD---
        # # return the game object that matches the id
        # game = Game.objects.get(pk = pk)
        
        # # update each field with the data in the request
        # game.title = request.data['title']
        # game.maker = request.data['maker']
        # game.number_of_players = request.data['number_of_players']
        # game.skill_level = request.data['skill_level']
        
        # # need to get the whole gametype object before saving it to the game object
        # game_type = GameType.objects.get(pk = request.data["game_type"])
        # gamer = Gamer.objects.get(pk = request.data['gamer'])

        # # add the found objects back on the game object
        # game.game_type = game_type
        # game.gamer = gamer
        
        
        
        # game.save()
        
        # return Response(None, status = status.HTTP_204_NO_CONTENT)
        