import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Post

class PostViewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.room_group_name = f'post_{self.post_id}'

        # اتصال به گروه WebSocket
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # خروج از گروه WebSocket
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        post_id = data.get('post_id')

        if post_id:
            post = await self.get_post(post_id)
            post.views += 1
            await self.save_post(post)

            # ارسال تعداد بازدید جدید به کلاینت‌ها
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "send_post_views",
                    "views": post.views
                }
            )

    async def send_post_views(self, event):
        views = event["views"]

        await self.send(text_data=json.dumps({"views": views}))

    @staticmethod
    async def get_post(post_id):
        return await Post.objects.aget(id=post_id)

    @staticmethod
    async def save_post(post):
        await post.asave()
