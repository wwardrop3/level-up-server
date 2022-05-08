"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType, game, game_type

class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        # the meta class holds the configuration for the serializer....use the gametype model and include the id and label fields        
        
        model = GameType
        
        # this determines which columns we want to return from a database table...you do not have to use them all
        fields = ('id', 'label')



# django REST framework allows logic for related views in a single class.
# we pass in the default ViewSet and specify the methods retrieve and list for gameview because they are related to gametype
class GameTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type
        
        Returns:
            Response -- JSON serialized game type
        """
        try:
            game_type = GameType.objects.get(pk = pk)
            # serializer turns return of sql database into json to send back to client
            serializer = GameTypeSerializer(game_type)
            return Response(serializer.data)
        except GameType.DoesNotExist as ex:
            return Response({'Sawwy doesnt exist', ex.args[0]}, status = status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        
        game_types = GameType.objects.all()
        
        serializer = GameTypeSerializer(game_types, many = True)
        return Response(serializer.data)
    

    def update(self, request, pk):
        "PUT Requests, returns 204 code"
        
        # only need serializer on get requests that are taking from the database and giving to the client
        
        game_type = GameType.objects.get(pk = pk)
        # we are updating the label name in the database for the id we are passing in (pk)
        # the request has a data property that contains the body of the request
        game_type.label(request.data['label'])
        # finally, save it
        game_type.save()
        
        # return no information other than the status code that shows it has completed
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        
        
    
# mvc model view controller....views job is to talk to the data and set up what gets returned

# the serializer turns the data from one type to another....out of database and into json..... from json into database