# views determines what kind of request is being received....put, post....like a module manager



from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from levelupapi.models import Event, event
from django.http import HttpResponseServerError
from levelupapi.models import gamer
from levelupapi.models.game import Game
from django.core.exceptions import ValidationError
from levelupapi.models.gamer import Gamer
from django.core.exceptions import ValidationError
from rest_framework.decorators import action

# serializer translates python objects into json for transit
class EventSerializer(serializers.ModelSerializer):
    # this will destermine which columns will be returned
    # needs model and fields
    
    
    # meta is any information outside of the python object....model is not a property on event
    class Meta:
        # model to use
        model = Event
        # columns of model to return
        fields = ('id', 'game', 'description', 'date', 'time', 'organizer', 'attendees', 'joined')
    

class UpdateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        
        # this is specifying which parts of the python model we want to return or update or create
        # maybe we only want to update a few things
        fields = ['id', 'game', 'description', 'date', 'time', "organizer"]











# imports methods from viewset class....already has retrieve, list, update.....


class EventView(ViewSet):
    # this will do the get,posts,puts,and updates except with retrieve, list, create, update, and destroy
    
    
    # we are reassigning these methods that have already been defined in viewset....method overriding
    def retrieve(self, request, pk):
        
        event = Event.objects.get(pk = pk)
        
        # passes in the return of the object that matches the id passed in the event.objects
        serializer = EventSerializer(event)
        
        # returns the json result of the serializer to be sent to the client
        return Response(serializer.data)
    
    
    def list(self, request):
        
        events = Event.objects.all()
        gamer = Gamer.objects.get(user = request.auth.user)
        # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event/////returns true/false
            event.joined = gamer in event.attendees.all()
            
        serializer = EventSerializer(events, many= True)
        
        return Response(serializer.data)
    
    
    def create(self, request):
        
        # for the organizer

        gamer = Gamer.objects.get(user = request.auth.user)
        
        game = Game.objects.get(pk = request.data['game'])
        
        event = Event.objects.create(
            game = game,
            description = request.data['description'],
            date = request.data['date'],
            time = request.data['time'],
            organizer = gamer
        )
        
        serializer = EventSerializer(event)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def update(self, request, pk):
        
        
        
        event = Event.objects.get(pk = pk)
        serializer = UpdateEventSerializer(event, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # status= is a kwarg
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    
    def destroy(self, request, pk):
        
        event = Event.objects.get(pk = pk)
        
        event.delete()
        
        return Response(None, status= status.HTTP_204_NO_CONTENT)
        
        
        
        
        
        # OLD---
        # first thing get the event that matches the pk passed in
        
        # event = Event.objects.get(pk = pk)
        
        # event.description = request.data['description']
        # event.date = request.data['date']
        # event.time = request.data['time']
        
        # # get organizer and gamer objects
        
        # organizer = Gamer.objects.get(pk = request.data['organizer'])
        # game = Game.objects.get(pk = request.data['game'])
        
        # event.organizer = organizer
        # event.game = game
        
        # event.save()
        
        # return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    # this turns a method into a new route
    # detail=true includes the pk
    @action(methods = ['post'], detail=True)
    def signup(self, request, pk):
        """post request for a user to sugn up for an event"""
        
        # first get the gamer that is that has a user_id that matches the authenticated token user_id
        gamer = Gamer.objects.get(user = request.auth.user)
        
        # get the event object that matches the pk that is passed in
        event = Event.objects.get(pk = pk)
        
        # add makes a new relationship between event and gamer by creating a bridge table called attendies
        event.attendees.add(gamer)
        return Response({'message': 'Gamer Added'}, status = status.HTTP_201_CREATED)

    # resulting route will be http://localhost:8000/events/2/signup
    
    @action(methods = ["delete"], detail=True)
    def leave(self, request, pk):
        
        gamer = Gamer.objects.get(user = request.auth.user)
        
        event = Event.objects.get(pk = pk)
        
        event.attendees.remove(gamer)
        return Response({'message', "Gamer Deleted"}, status = status.HTTP_204_NO_CONTENT)
    
    