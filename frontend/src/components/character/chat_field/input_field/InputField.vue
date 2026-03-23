<script setup>
import { useTemplateRef,ref } from 'vue';
import MicIcon from '../../icon/MicIcon.vue';
import SendIcon from '../../icon/SendIcon.vue';
import streamApi from '@/js/http/steamApi';
const props = defineProps(['friendId'])
const emit = defineEmits(['pushBackMessage','addToLastMessage'])
const inputRef = useTemplateRef("input-ref")
const message = ref('')

let isProcessing = false

async function handleSend(){
    if (isProcessing) return 

    //取出输入内容
    const content = message.value.trim()
    if (!content) return 
    isProcessing = true
    //输入内容回车后，清楚输入框内容
    message.value = ''

    emit('pushBackMessage', {role:'user',content:content, id: crypto.randomUUID()})
    emit('pushBackMessage',{role:'ai',content:'',id:crypto.randomUUID()})

    //给后端发送请求
    try{
        await streamApi('/api/friend/message/chat/',{
            body:{
                friend_id:props.friendId,
                message:content,
            },
            onmessage(data,isDone){ 
                if (isDone){
                    isProcessing = false
                }else if (data.content){
                    emit("addToLastMessage",data.content)
                }
            },
            onerror(err){
                isProcessing = false
            }
        })
    } catch (err){
        console.log(err)
        isProcessing = false 
    }

}

function focus(){
    inputRef.value.focus()
}
defineExpose({
    focus,
})
</script>

<template>
    <form @submit.prevent="handleSend" class = "absolute bottom-4 left-2 w-86 h-12 flex items-center ">
        <input
        ref = "input-ref"
        v-model = "message"
        class = "input bg-black/30 text-white text-base backdrop-blur-sm pr-20 rounded-2xl  h-full w-full"
        type="text"
        placeholder="请输入消息内容">
        <div @click="handleSend" class ="absolute w-8 h-8 right-2 flex justify-center items-center cursor-pointer"> 
            <SendIcon/>
        </div>
        <div class="absolute w-8 h-8 right-8 flex justify-center items-center cursor-pointer">
            <MicIcon/>
        </div>
    </form>

</template>

<style scoped>
</style>