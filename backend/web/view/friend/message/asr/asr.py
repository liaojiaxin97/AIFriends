import asyncio
import json
import os
import uuid

import websockets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class ASRView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 这里你可以处理上传的音频文件，进行ASR识别
        # 假设你已经完成了ASR识别，并得到了文本结果
        audio = request.FILES.get('audio')
        
        if not audio:
            return Response({
                "result": "音频不存在",
            })
        
        pcm_data = audio.read()
        text = asyncio.run(self.run_asr_tasks(pcm_data))

        return Response({
            "result": "success",
            "text": text,
        })

    async def run_asr_tasks(self, pcm_data):
        task_id = uuid.uuid4().hex
        api_key = os.getenv("API_KEY")
        wss_url = os.getenv("WSS_URL")

        headers = {
            "Authorization": f"Bearer {api_key}",
        }

        async with websockets.connect(wss_url, additional_headers=headers) as ws:
            await ws.send(json.dumps({
                "header": {
                    "streaming": "duplex",
                    "task_id": task_id,
                    "action": "run-task",
                },
                "payload": {
                    "model": "gummy-realtime-v1",
                    "parameters": {
                        "sample_rate": 16000,
                        "format": "pcm",
                        "transcription_enabled": True,
                    },
                    "input": {},
                    "task": "asr",
                    "task_group": "audio",
                    "function": "recognition",
                },
            }))

            async for msg in ws:
                if json.loads(msg)["header"]["event"] == "task-started":
                    break

            _, text = await asyncio.gather(
                self.asr_sender(pcm_data, ws, task_id),
                self.asr_receiver(ws),
            )

            return text

    async def asr_sender(self, pcm_data, ws, task_id):
        chunk = 3200
        for i in range(0, len(pcm_data), chunk):
            await ws.send(pcm_data[i:i + chunk])
            await asyncio.sleep(0.1)

        await ws.send(json.dumps({
            "header": {
                "action": "finish-task",
                "task_id": task_id,
                "streaming": "duplex",
            },
            "payload": {
                "input": {},
            },
        }))

    async def asr_receiver(self, ws):
        text = ""

        async for msg in ws:
            data = json.loads(msg)
            event = data["header"]["event"]

            if event == "result-generated":
                output = data["payload"]["output"]
                transcription = output.get("transcription")
                if transcription and transcription.get("sentence_end"):
                    text += transcription.get("text", "")
            elif event in ["task-finished", "task-failed"]:
                break

        return text
