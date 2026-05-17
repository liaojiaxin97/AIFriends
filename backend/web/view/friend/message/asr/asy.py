import asyncio
import json
import os
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import websockets


class ASRView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        #从前端接受数据
        audio = request.FILES.get('audio')
        if not audio:
            return Response({
                'result': '音频不存在',
            })
        
        pcm_data = audio.read()
        #调用协程
        text = asyncio.run(self.run_asr_tasks(pcm_data))
        return Response({
            'result': "success",
            'text': text,
        })
        
    
    async def asr_sender(self, pcm_data, ws, task_id):
        chunk = 3200 # 16000采样率，16bit深度，单声道，每100ms的数据量(16000*16/8*0.1)
        for i in range(0, len(pcm_data), chunk):
            await ws.send(pcm_data[i:i+chunk])
            await asyncio.sleep(0.01)  # 模拟实时发送，每10ms发送一次
            
        await ws.send(json.dumps({
               "header": {
                "action": "finish-task",
                "task_id": task_id,
                "streaming": "duplex"
            },
            "payload": {
                "input": {}
            } 
        }))
    async def asr_receiver(self, ws):
        text = ""
        async for msg in ws:
            data  = json.loads(msg)
            event = data['header']['event']
            if event == "result-generated":
                if event == "result-generated":
                    output = data['payload']['output']
                    #print("Received ASR output:", output)  # 打印接收到的ASR输出
                    if output.get('sentence',None) and output['sentence']['sentence_end']:
                        text += output['sentence']['text']
            elif event in ['task-finished','task-failed']:
                break
        
        
        return text
    
    async def run_asr_tasks(self,pcm_data):
        task_id = uuid.uuid4().hex
        api_key = os.getenv("API_KEY")
        wss_url = os.getenv("WSS_BASE")
        
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        async with websockets.connect(wss_url, additional_headers=headers) as ws:
            await ws.send(json.dumps({
                "header": {
                    "action": "run-task",
                    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
                    "streaming": "duplex"
                },
                 "payload": {
                "task_group": "audio",
                "task": "asr",
                "function": "recognition",
                "model": "paraformer-realtime-v2",
                "parameters": {
                    "format": "pcm", 
                    "sample_rate": 16000, 
                },
                "input": {}
                 }
            }))
            #等待发送task-started的时间
            #ws为异步连接
            async for msg in ws:
                if json.loads(msg)['header']['event'] == 'task-started':
                    break
            _,text = await asyncio.gather(
                self.asr_sender(pcm_data, ws, task_id),
                self.asr_receiver(ws),
            )
            
            return text
        