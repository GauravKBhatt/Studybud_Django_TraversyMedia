# from the django rest documentation
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
# from django.http import JsonResponse
from base.models import Room
from .serializers import RoomSerializer

# to provide the URIs for the APOs
@api_view(["GET"])
def getRoutes(request):
    routes=[
        # for nothing entered.
        'GET /api',
        # for the list of room.
        'GET /api/rooms',
        # for some particular room.
        'GET /api/rooms/:id'
    ]
    return Response(routes)
# safe= false indicates that more than a python list can be entered as parameter in the JSONresponse. This essentially lets us transfer Javascript objects through APIs.

@api_view(["GET"])
def getRooms(request):
    rooms=Room.objects.all()
    # resposne cannot return a python object but can only return a JS object thus, we need to serialize the list rooms first.
    serializer = RoomSerializer(rooms,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getRoom(request,pk):
    room=Room.objects.get(id=pk)
    serializer = RoomSerializer(room,many=False)
    return Response(serializer.data)