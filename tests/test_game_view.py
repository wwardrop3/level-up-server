from urllib import response
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Game, Gamer
from levelupapi.views.GameView import GameSerializer

class GameTests(APITestCase):
    #add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events']
    
    def setUp(self):
        #Grab the first gamer object from the database and add their token to the headers
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user = self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION = f"Token {token.key}")
    
    def test_create_game(self):
        # create game test
        url = "/games"
        
        game = {
            "title": "Clue",
            "maker": "Milton Bradley",
            "skill_level": 5,
            "number_of_players": 6,
            "game_type": 1,
        }
        
        response = self.client.post(url, game, format="json")
        
        # The _expected_ output should come first when using the assertion with 2 arguments
        # The _actual_ output will be the second argument
        #We _expect_ the status to be status.HTTP_201_Created and it _actually_ was response.status_code
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        #Get the last game added to the database, it should be the one just created
        new_game = Game.objects.last()
        
        # Since the create method should return the serializer version of the newly created game,
        # Use the serializer you're using in the cretae method to serialize the "new_game"
        # Depending on your code this might be different
        
        expected = GameSerializer(new_game)
        
        # Now we can test that the expected output matches what was actually returned
        self.assertEqual(expected.data, response.data)
        
        
    
    def test_get_game(self):
        
        
        # grab game from database that will be used as expected data as it already worked
        game = Game.objects.first()
        
        url = f'/games/{game.id}'
        
        # getting the response data that is being tested
        response = self.client.get(url)
        
        # 
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        #run the game through the serializer thats being used in view
        expected = GameSerializer(game)
        
        self.assertEqual(expected.data, response.data)
        
        
    def test_all_games(self):
        
        url = "/games"
        
        response = self.client.get(url)
        
        all_games = Game.objects.all()
        expected = GameSerializer(all_games, many = True)
        
        # check response code first
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        self.assertEqual(expected.data, response.data)
        
        
    def test_update_game(self):
        
        game = Game.objects.first()
        
        url = f'/games/{game.id}'
        
        updated_game = {
            "title": f'{game.title} updated',
            "maker": game.maker,
            "skill_level": game.skill_level,
            "number_of_players": game.number_of_players,
            "game_type": game.game_type.id
        }
        
        response= self.client.put(url, updated_game, format = "json")
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        
        game.refresh_from_db()
        
        self.assertEqual(updated_game['title'], game.title)
        
        
    
    def test_delete_game(self):
        # testing creates temp databases to use without altering your own data
        game = Game.objects.first()
        
        url = f'/games/{game.id}'
        
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        
        #  test that it was deleted by trying to get the game
        # response should be 404
        
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)