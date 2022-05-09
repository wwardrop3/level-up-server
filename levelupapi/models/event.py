from django.db import models


class Event(models.Model):
    # cascade means that if the game is deleted, so is this event
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    attendees = models.ManyToManyField("Gamer", related_name="Gamers")

    
    # custom properties do not exist in the database but bul calculate when the request is made
    
    @property
    def joined(self):
        return self.__joined
    @joined.setter
    def joined(self, value):
        self.__joined = value