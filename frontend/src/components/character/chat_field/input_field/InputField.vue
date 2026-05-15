<script setup>
import { useTemplateRef,ref } from 'vue';
import MicIcon from '../../icon/MicIcon.vue';
import SendIcon from '../../icon/SendIcon.vue';
import api from '@/js/http/api.js';
import streamApi from '@/js/http/streamApi';
//接受父组件传来的变量
const props = defineProps(['friendId'])
//接受父组件传来的函数
const emit = defineEmits(['pushBackMessage','addToLastMessage'])
const inputRef = useTemplateRef('input-ref')
//响应式变量
const message = ref('')

let isProcessing = false

async function handleSend(){

    if (isProcessing) {
        return
    }
    isProcessing = true
    //取出前端输入消息
    const content = message.value.trim()
    if (!content) return 
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
                if (isDone){
                    isProcessing = false
                } else if (data.content){
                    //后端每返回一条内容，消息就添加进历史消息，同时整个聊天框波动滚动条显示最新消息
                    emit('addToLastMessage',data.content)
                }
            },
            onerror(err){
                isProcessing = false
            }
        })
    } catch (err) {
        console.log(err)
        isProcessing = false
    }
}


function focus(){
    inputRef.value.focus();
}
//暴露focus方法给父组件调用
defineExpose({
    focus,
})
</script>

<template>
    <form @submit.prevent = "handleSend" class = "absolute bottom-4 left-2 w-86 h-12 flex items-center ">
        <input 
        ref = "input-ref"
        v-model = "message"
        class = "input bg-black/30 text-white text-base backdrop-blur-sm pr-20 rounded-2xl  h-full w-full"
        type="text"
        placeholder="请输入消息内容">
        <div @click = "handleSend" class ="absolute w-8 h-8 right-2 flex justify-center items-center cursor-pointer"> 
            <SendIcon/>
        </div>
        <div class="absolute w-8 h-8 right-8 flex justify-center items-center cursor-pointer">
            <MicIcon/>
        </div>
    </form>

</template>

<style scoped>
</style>