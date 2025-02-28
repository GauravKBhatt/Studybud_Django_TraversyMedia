
from django.contrib import admin
from django.urls import path,include




urlpatterns = [
    path('admin/', admin.site.urls),
    # to make sure all the requests are passed to the urls.py file of base app
    path('',include('base.urls')),
    # now to make sure all the requests with api in the uri goto the url file of api subfolder of base app.
    path('api/',include('base.api.urls'))
]
