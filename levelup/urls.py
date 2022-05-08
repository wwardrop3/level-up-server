# purpose of this module is to listen for urls and route the api to modules
from lib2to3.pgen2.token import SLASH
from rest_framework import routers
from levelupapi.views import GameTypeView
from levelupapi.views import EventView
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from levelupapi.views import register_user, login_user
from levelupapi.views.GameView import GameView


router = routers.DefaultRouter(trailing_slash = False)

# 'gametypes' is setting up the url
# GameTypeView tells server which view to use when it sees 'gametypes'
# third parameter gametype is the base name, only will see if there is an error, usually the singular version of the first parameter


# THESE ARE THE ENDPOINTS
router.register(r'gametypes', GameTypeView, 'gametype')
router.register(r'games', GameView, 'game')
router.register(r'events', EventView, 'events')



urlpatterns = [
    # path listens for the first parameter and then invokes the second parameter
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    # if the route is not one of the built in routes above, look to the ones definied outside of the url patterns
    path('', include(router.urls))
]

# endpoint are where resources are pointing to