from django.urls import path
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.generic.websocket import WebsocketConsumer
from django.http.response import StreamingHttpResponse
from django.shortcuts import render
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
import json
import pyrebase
from asgiref.sync import async_to_sync
import requests
config = json.loads(os.environ["FIREBASE_CONFIG"])
firebase = pyrebase.initialize_app(config)
db=firebase.database()




class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
    def chat_message(self, event):
        print("evvvvv",event)
        m = event['message']
        self.send(text_data=m)
    def disconnect(self, close_code):
        print(close_code,"disconnecting")
    def receive(self, text_data):
        if text_data=="DATAZERO":
            players={"id":  {
                        "x":"0",
                        "y":"0",
                        "level":"0",
                        "token": "00",
                        "id2":''
                    }}
            levels_pip=list(50*[""])
            db.child('players').set(players)
            db.child('levels_pip').set(levels_pip)
            self.send(text_data="data reset succesfully .")
            return
        if text_data[0]=="+":
            players=dict(db.child('players').get().val())
            levels_pip=db.child('levels_pip').get().val()   
            id="@"+str(random.randint(1000000000,1999999999))
            requests.post("http://snubby.herokuapp.com/api",data={"@":id})
            players[id]={
                                    "x":"555",
                                    "y":"666",
                                    "level":"todo",
                                    "id2":'12'
                                }
            db.child('players').set(players)
            self.send(text_data=id)
            return
        if text_data[0]=="@":
            id,l=text_data.split()
            l=int(l)
            players=dict(db.child('players').get().val())
            levels_pip=db.child('levels_pip').get().val()
            if levels_pip[l]=="":
                levels_pip[l]=id
                db.child('levels_pip').set(levels_pip)
                while(levels_pip[l]==id):
                    levels_pip=db.child('levels_pip').get().val()
                players=dict(db.child('players').get().val())
                self.send(text_data=players[id]["id2"])
            if levels_pip[l]!="":
                id2=levels_pip[l]
                levels_pip[l]=''
                players[id]['id2']=id2
                players[id2]['id2']=id
                db.child('players').set(players)
                db.child('levels_pip').set(levels_pip)  
                db.child('snubbyland/%s/%s'%(id2,id)).set("0 0")
                db.child('snubbyland/%s/%s'%(id,id2)).set("0 0")
                self.send(text_data=id2)
            self.send(text_data="@abdellatif")
            return
        x,y,id,id2=text_data.split()
        db.child('snubbyland/%s/%s'%(id,id2)).set(x+" "+ y)
        self.send(text_data=db.child('snubbyland/%s/%s'%(id2,id)).get().val())




application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("game/stream", GameConsumer),
        ]),
    ),

})


