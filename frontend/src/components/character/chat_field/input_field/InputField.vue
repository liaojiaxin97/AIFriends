<script setup>
import MicIcon from '../../icon/MicIcon.vue';
import SendIcon from '../../icon/SendIcon.vue';
</script>

<template>
    <div class = "absolute bottom-4 left-2 w-86 h-12 flex items-center ">
        <input 
        class = "input bg-black/30 text-white text-base backdrop-blur-sm pr-20 rounded-2xl  h-full w-full"
        type="text"
        placeholder="请输入消息内容">
        <div class ="absolute w-8 h-8 right-2 flex justify-center items-center cursor-pointer"> 
            <SendIcon/>
        </div>
        <div class="absolute w-8 h-8 right-8 flex justify-center items-center cursor-pointer">
            <MicIcon/>
        </div>
    </div>

</template>

<style scoped>
</style>