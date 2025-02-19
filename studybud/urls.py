
from django.contrib import admin
from django.urls import path,include




urlpatterns = [
    path('admin/', admin.site.urls),
    # to make sure all the requests are passed to the urls.py file of base app
    path('',include('base.urls'))
]
