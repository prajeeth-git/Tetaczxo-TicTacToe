from django.shortcuts import render,HttpResponse,redirect
from .models import gameroom

from django.contrib import messages

# Create your views here.
def index(request):
    if request.method=="GET":
        return render(request, 'index.html')
    elif request.method=="POST":
        print(request.POST) 
        roomid = request.POST.get("room-id",None)
        name = request.POST.get("player-name","Unknown User")
        print(roomid,name)
        if roomid:
            try:
                room = gameroom.objects.get(id=roomid)
                return redirect(f"/game/{room.id}/{name}/")

            except gameroom.DoesNotExist:
                messages.error(request, "Invalid Room Code ! ")
                return redirect(f"/")

            # return redirect(f"/game/{roomid}/{name}/")
        else:
            room = gameroom.objects.create()
            return redirect(f"/game/{room.id}/{name}/")

        return HttpResponse("Post request")

def game(request,id=None,name=None):
    try:
        room = gameroom.objects.get(id=id)
        return render(request,'gameui.html',{"room":room,"name":name}) 
    except gameroom.DoesNotExist:
        messages.error(request, "Room Does Not Exist---INVALID------")
        return redirect(f"/")


