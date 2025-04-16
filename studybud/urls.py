
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),
    # to make sure all the requests are passed to the urls.py file of base app
    path('',include('base.urls')),
    # now to make sure all the requests with api in the uri goto the url file of api subfolder of base app.
    path('api/',include('base.api.urls')),
    path('realtime/',include('rtchat.urls'))
]

# path comes from the media_url specified in the settings.py and file path comes from the media_root specified there.
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
