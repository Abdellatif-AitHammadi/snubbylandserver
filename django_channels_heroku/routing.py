from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
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
import requests
config = json.loads(os.environ["FIREBASE_CONFIG"])
firebase = pyrebase.initialize_app(config)
db=firebase.database()


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.id="@"+str(random.randint(1000000000,1999999999))
        self.l=0
        self.id2=0
        self.accept()
    def disconnect(self, close_code):
        levels_pip=db.child('levels_pip').get().val()
        if levels_pip[self.l]==self.id:
            levels_pip[self.l]=""
            db.child('levels_pip').set(levels_pip)
        print(close_code,"disconnecting")
    def receive(self, text_data):
        print("receiveing : ",text_data)
        data=text_data.split()
        if text_data=="":
            pass
        elif text_data=="get":
            self.send(text_data=str(db.child("levels_pip").get().val()))
        elif text_data=="set":
            db.child("levels_pip").set(list(50*[""]))
            self.send(text_data="ok")
        elif len(data)<2:
            self.send(text_data="args must bi >=2")
        elif text_data[0]=="@":
            e,self.l=data[0],int(data[1])
            levels_pip=db.child('levels_pip').get().val()
            if levels_pip==None:
                self.send(text_data="data_base Error")
            elif levels_pip[self.l]=="":
                levels_pip[self.l]=self.id
                db.child('levels_pip').set(levels_pip)
                self.send(text_data=".")
                # while(levels_pip[self.l]==self.id):
                #     levels_pip=db.child('levels_pip').get().val()
                # self.id2=levels_pip[self.l]
                # levels_pip[self.l]=""
                # db.child('levels_pip').set(levels_pip)
            elif levels_pip[self.l]==self.id:
                self.send(text_data=".")
            else :
                self.id2=levels_pip[self.l]
                levels_pip[self.l]=self.id
                db.child('levels_pip').set(levels_pip)
                db.child('snubbyland/%s/%s'%(self.id2,self.id)).set("0 0")
                db.child('snubbyland/%s/%s'%(self.id,self.id2)).set("0 0")
                self.send(text_data=self.id+" VS "+self.id2)
        else:
            x,y=data[0],data[1]
            db.child('snubbyland/%s/%s'%(self.id,self.id2)).set(x+" "+ y)
            self.send(text_data=db.child('snubbyland/%s/%s'%(self.id2,self.id)).get().val())



class LevelConsumer(WebsocketConsumer):
    def connect(self):
        self.id="L"+str(random.randint(100,199))
        self.accept()
    def receive(self, text_data):
        print(text_data)
        #to save level 
        if "serialization::archive" in text_data:
            db.child("levels_data/"+self.id).set(text_data)
            self.send(text_data=self.id)
        elif text_data[0]=="L":#to get level ex: L1545215151
            l=db.child("levels_data/"+text_data[1:]).get().val()
            if l==None:
                self.send(text_data=".")
            else:
                self.send(text_data=l)
        else:
            self.send(text_data="invalide commande")

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("game/stream", GameConsumer),
            path("game/level", LevelConsumer)
        ]),
    ),

})


