<script setup>

import { nextTick, onBeforeMount, useTemplateRef,onMounted } from 'vue';
import Message from './message/Message.vue';
import api from '@/js/http/api.js';
const props = defineProps(['history','friendId','character'])
const scrollRef = useTemplateRef('scroll-ref')
const sentinelRef = useTemplateRef('sentinel-ref')
const emit = defineEmits(['pushFrontMessage'])
let isLoading = false
let hasMessages = true
let lastMessageId = 0


function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const sentinelRect = sentinelRef.value.getBoundingClientRect()
  const scrollRect = scrollRef.value.getBoundingClientRect()
  return sentinelRect.top < scrollRect.bottom && sentinelRect.bottom > scrollRect.top
}



async function loadMore(){
    if (isLoading || !hasMessages) return 
    isLoading = true

    let newMessage = []

    try{
        
        const res = await api.get("/api/friend/message/chat/get_history/",{
            params:{
                last_message_id:lastMessageId,
                friend_id:props.friendId,
            }
        })
        const data  =  res.data
        if (data.result === 'success'){
            newMessage = data.message
            
        }
        } catch (err) {
            console.log(err)
        } finally {
            isLoading = false

            if (newMessage.length === 0){
                hasMessages = false
            } else{
                const oldHeight = scrollRef.value.scrollHeight
                const oldTop = scrollRef.value.scrollTop
                //in 是输出下标，of是数组内元素
                for (const m of newMessage ){
                    emit('pushFrontMessage',{
                        role:"ai",
                        content:m.output,
                        id:crypto.randomUUID(),
                    })
                    emit('pushFrontMessage',{
                        role:"user",
                        content:m.user_message,
                        id:crypto.randomUUID(),
                    })
                    lastMessageId = m.id
                }

                await nextTick()

                const newHeight = scrollRef.value.scrollHeight
                scrollRef.value.scrollTop = oldTop +  newHeight - oldHeight

                if (checkSentinelVisible()){
                    await loadMore()
                }
            }
        }
    }

// 检测红色哨兵是否出现在视窗中，如果在视窗中则加载更多内容
let observer = null
onMounted(async () => {
  await loadMore()  // 加载新元素

  observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
             loadMore()
        }
      })
    },
    {root: null, rootMargin: '2px', threshold: 0}
  )

  //监听哨兵元素， 每次哨兵被看到时，都会触发一次
  observer.observe(sentinelRef.value)
})
onBeforeMount(() => {
    observer?.disconnect()
})
//滚动视窗
async function scrollToBottom(){
    await nextTick()

    scrollRef.value.scrollTop = scrollRef.value.scrollHeight
}

defineExpose({
    scrollToBottom
})
</script>


<template>

    <div  ref = "scroll-ref" class = "absolute top-18 left-0 w-90 h-112 overflow-y-scroll no-scrollbar">
        <div ref = "sentinel-ref" class = "h-2">        </div>
        <Message
        v-for = "message in history"
        :key = "message.id"
        :message = "message"
        :character = "character"
        />

    </div>

</template>


<style scoped>
/* 隐藏 Chrome, Safari 和 Opera 的滚动条 */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

/* 隐藏 IE, Edge 和 Firefox 的滚动条 */
.no-scrollbar {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}
</style>