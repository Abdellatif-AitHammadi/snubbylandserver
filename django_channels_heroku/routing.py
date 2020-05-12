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
import requests
config = json.loads(os.environ["FIREBASE_CONFIG"])
firebase = pyrebase.initialize_app(config)
db=firebase.database()




class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.id="@"+str(random.randint(1000000000,1999999999))
        self.id2="-1"
        self.l=0
        self.is_online=1
        self.accept()
    # Receive message from the group
    def channel_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
    def disconnect(self, close_code):
        levels_pip=db.child('levels_pip').get().val()
        if levels_pip[self.l]==self.id:
            self.is_online=0
            levels_pip[self.l]=""
            db.child('levels_pip').set(levels_pip)
            print("this is 43 line")
        print(close_code,"disconnecting")
    def receive(self, text_data):
        if text_data[0]=="*":
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "2020",
                {
                    'type': 'channel_message',
                    'message': text_data
                }
            )
            return
        if text_data=="-":
            self.close()
        if text_data[0]=="@":
            e,l=text_data.split()
            self.l=int(l)
            levels_pip=db.child('levels_pip').get().val()
            if levels_pip[self.l]=="":
                levels_pip[self.l]=self.id
                db.child('levels_pip').set(levels_pip)
                while(levels_pip[self.l]==self.id and self.is_online):
                    levels_pip=db.child('levels_pip').get().val()
                self.id2=levels_pip[self.l]
                levels_pip[self.l]=""
                db.child('levels_pip').set(levels_pip)
            if levels_pip[self.l]!="":
                self.id2=levels_pip[self.l]
                levels_pip[self.l]=self.id
                db.child('levels_pip').set(levels_pip)
                db.child('snubbyland/%s/%s'%(self.id2,self.id)).set("0 0")
                db.child('snubbyland/%s/%s'%(self.id,self.id2)).set("0 0")
            self.send(text_data=self.id+" VS "+self.id2)
            return
        x,y=text_data.split()
        db.child('snubbyland/%s/%s'%(self.id,self.id2)).set(x+" "+ y)
        self.send(text_data=db.child('snubbyland/%s/%s'%(self.id2,self.id)).get().val())




application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("game/stream", GameConsumer),
        ]),
    ),

})


