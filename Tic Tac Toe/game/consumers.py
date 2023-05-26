from channels.generic.websocket import AsyncJsonWebsocketConsumer
import contextlib
import random
from game.winlogic import checkwin,checkdraw
class opponent(AsyncJsonWebsocketConsumer):
    
    board = {
        0:'',1:'',2:'',
        3:'',4:'',5:'',
        6:'',7:'',8:'',
    }
    
    
    
    async def connect(self):
        print(self.scope['url_route']['kwargs']['id'])
        self.room_id=self.scope['url_route']['kwargs']['id']
        self.opp_name = f"opp_{self.room_id}"
        
        with contextlib.suppress(KeyError):
            if (len(self.channel_layer.groups[self.opp_name])>=2):
                await self.accept()
                await self.send_json({
                    "event": "show_error",
                    "error": "This room is full"
                    
                })
                return await self.close(3)
        
        
        
        
        await self.accept()
        await self.channel_layer.group_add(self.opp_name,self.channel_name)

        if (len(self.channel_layer.groups[self.opp_name])==2):
            temp = list(self.channel_layer.groups[self.opp_name])
            print(temp)
            first_player = random.choice(temp)
            temp.remove(first_player)
            final_group = [first_player,temp[0]]
            print(final_group)
            for i,channel_name in enumerate(final_group):
                await self.channel_layer.send(channel_name,{
                    "type":"gameData.send",
                    "data": {
                        "event" : "game_start",
                        "board": self.board,
                        "myTurn" : True if i==0 else False,
                    }
                })

        print(self.channel_layer.groups[self.opp_name])

    async def receive_json(self,content,**kwargs):
        
        print(content)
        if (content['event']=="boardData_send"):
            print(content['board'])
            check  = checkwin(content['board'])
            if check:
                return await self.channel_layer.group_send(self.opp_name,{
                    "type":"gameData.send",
                    "data": {
                        "event" : "won",
                        "board": content['board'],
                        "winner":check,
                        "myTurn" : False 
                        
                    }        
                })
            elif (checkdraw(content['board'])):
                    return await self.channel_layer.group_send(self.opp_name,{
                        "type":"gameData.send",
                        "data": {
                            "event" : "draw",
                            "board": content['board'],
                            "myTurn" : False 
                            
                        }        
                    })
            else:
                for channel_name in self.channel_layer.groups[self.opp_name]:
                    await self.channel_layer.send(channel_name,{
                        "type":"gameData.send",
                        "data": {
                            "event" : "boardData_send",
                            "board": content['board'],
                            "myTurn" : False if self.channel_name==channel_name else True
                            
                        }        
                    })
                return await super().receive_json(content,**kwargs)
        
        elif (content['event']=='restart'):
            if (len(self.channel_layer.groups[self.opp_name])==2):
                temp = list(self.channel_layer.groups[self.opp_name])
                print(temp)
                first_player = random.choice(temp)
                temp.remove(first_player)
                final_group = [first_player,temp[0]]
                print(final_group)
                for i,channel_name in enumerate(final_group):
                    await self.channel_layer.send(channel_name,{
                        "type":"gameData.send",
                        "data": {
                            "event" : "game_start",
                            "board": self.board,
                            "myTurn" : True if i==0 else False
                        }
                    })

    
    
    async def disconnect(self, code):
        if (code==3):
            return
        await self.channel_layer.group_discard(self.opp_name,self.channel_name)

        await self.channel_layer.group_send(self.opp_name,{
                    "type":"gameData.send",
                    "data": {
                        "event" : "opponent_left",
                        "board":self.board,
                        "myTurn" : False,
                    }
                })        
        print(self.channel_layer.groups[self.opp_name])

    async def gameData_send(self,context):
        await self.send_json(context['data'])
