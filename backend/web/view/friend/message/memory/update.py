from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from web.models.friend import Friend, Message, SystemPrompt
from web.view.friend.message.memory.graph import MemoryGraph
from langchain_core.messages import HumanMessage, SystemMessage
from django.utils.timezone import now
from pprint import pprint



def create_system_message():
    system_prompts = SystemPrompt.objects.filter(title="记忆").order_by('order_number')
    prompt = ""
    for sp in system_prompts:
        prompt += sp.promtps
    return SystemMessage(prompt)


def create_human_message(friend):
    prompt = f"【原始记忆】\n{friend.memory}\n"
    prompt += f"【最近对话】\n"
    messages = list(Message.objects.filter(friend = friend).order_by('-id')[:10])
    messages.reverse()
    
    for m in messages:
        prompt += f"user:{m.user_message}\n"
        prompt += f"AI:{m.output}\n"
    return HumanMessage(prompt)
    
def update_memory(friend):
    app = MemoryGraph.create_app()
    
    inputs = {
        'messages':[
            create_system_message(),
            create_human_message(friend),
        ]
    }
    
    # pprint(inputs)
    res = app.invoke(inputs)
    friend.memory = res['messages'][-1].content
    # pprint(friend.memory)
    
    friend.update_time = now()
    friend.save()