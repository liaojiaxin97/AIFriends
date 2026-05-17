<script setup>
import { useTemplateRef,ref } from 'vue';
import MicIcon from '../../icon/MicIcon.vue';
import SendIcon from '../../icon/SendIcon.vue';
import api from '@/js/http/api.js';
import streamApi from '@/js/http/streamApi';
import Microphone from './Microphone.vue';
//接受父组件传来的变量
const props = defineProps(['friendId'])
//接受父组件传来的函数
const emit = defineEmits(['pushBackMessage','addToLastMessage'])
const inputRef = useTemplateRef('input-ref')
//响应式变量
const message = ref('')
const showMic = ref(false)
//全局变量
let processId = 0

//event 参数内置，想要传语音信息需要从第二个开始传
async function handleSend(event,audio_msg){
    //检测是语音还是文字消息
    let content
    if (audio_msg){
        content = audio
    } else {
        //取出前端输入消息
        content = message.value.trim()
        if (!content) return 
    }



    //函数内变量，全局变量变化会导致跟每次调用函数的函数内变量不一致
    const curId = ++ processId

    message.value = ''
    //先发出一条消息
    emit('pushBackMessage',{role:'user',content:content,id:crypto.randomUUID()})
    //插一条空的消息占位，为ai做占位
    emit('pushBackMessage',{role:'ai',content:'',id:crypto.randomUUID()})

    try {
        await streamApi('/api/friend/message/chat/',{
            body:{
                friend_id: props.friendId,
                message: content,
            }, 
            onmessage(data,isDone){
                if (curId != processId) return 
                if (data.content){
                    //后端每返回一条内容，消息就添加进历史消息，同时整个聊天框波动滚动条显示最新消息
                    emit('addToLastMessage',data.content)
                }
            },
            onerror(err){
            }
        })
    } catch (err) {
    }
}


function focus(){
    inputRef.value.focus();
}

function close(){
    //更新版本号后，所有旧的内容都不在更新，如 42行 if (curId != processId) return 
    ++ processId
    showMic.value = false
}

function handleStop(){
    ++ processId
}
//暴露focus方法给父组件调用
defineExpose({
    focus,
    close,
})
</script>

<template>
    <form @submit.prevent = "handleSend" v-if = "!showMic" class = "absolute bottom-4 left-2 w-86 h-12 flex items-center ">
        <input 
        ref = "input-ref"
        v-model = "message"
        class = "input bg-black/30 text-white text-base backdrop-blur-sm pr-20 rounded-2xl  h-full w-full"
        type="text"
        placeholder="请输入消息内容">
        <div @click = "handleSend" class ="absolute w-8 h-8 right-2 flex justify-center items-center cursor-pointer"> 
            <SendIcon/>
        </div>
        <div @click = "showMic = true" class="absolute w-8 h-8 right-8 flex justify-center items-center cursor-pointer">
            <MicIcon/>
        </div>
    </form>
    <Microphone 
    v-else 
    @close = "showMic = false"
    @send = "handleSend"
    @stop = "handleStop"/>
</template>

<style scoped>
</style>