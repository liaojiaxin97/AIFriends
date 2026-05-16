<script setup>
import { useTemplateRef,nextTick } from 'vue';
import { computed,ref } from 'vue';
import Character from '../Character.vue';
import InputField from './input_field/InputField.vue';
import CharacterFieldPhoto from './character_field_photo/CharacterFieldPhoto.vue';
import ChatHistory from './chat_history/ChatHistory.vue';

//用来接收父组件传下来的数据
const props = defineProps(['friend'])
//用来拿模板里某个元素或子组件的引用
const modalRef = useTemplateRef('modal-Ref')
const inputRef = useTemplateRef('input-ref')
const chatHistoryRef = useTemplateRef("chat-history-ref")
//全局变量
const history = ref([])

//展示模态框
async function showModal(){
    modalRef.value.showModal()
    await nextTick()
    inputRef.value.focus()
}

//把一条新的消息对象直接追加到历史数组末尾
function handlePushBackMessage(msg) {
  history.value.push(msg)
  chatHistoryRef.value.scrollToBottom()
}
//不是新增消息，而是把 delta 这段内容追加到最后一条消息的 content 上。
function handleAddToLastMessage(delta){
  history.value.at(-1).content += delta
  chatHistoryRef.value.scrollToBottom()
}

//用于滚动条上滚时，历史消息的出现。往上添加消息
function handlePushFrontMessage(msg){
  history.value.unshift(msg)
}


defineExpose({
    showModal,
})
const modalStyle = computed(() => {
  if (props.friend) {
    return {
      backgroundImage: `url(${props.friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  } else {
    return {}
  }
})
</script>

<template>  

    <dialog ref="modal-Ref" class = "modal">
        <div class = "modal-box w-90 h-150" :style="modalStyle">
            <button @click="modalRef.close()" class = "btn btn-sm btn-circle btn-ghost bg-transparent absolute right-1 top-1">x</button>
            <ChatHistory 
            ref = "chat-history-ref"
            v-if = "friend"
            :history = "history"
            :friendId = "friend.id"
            :character = friend.character
            @pushFrontMessage = "handlePushFrontMessage"
            />
            <InputField 
            ref = "input-ref" 
            v-if = "friend" 
            :friendId = "friend.id"
            @pushBackMessage = "handlePushBackMessage"
            @addToLastMessage = "handleAddToLastMessage"
            />
            <CharacterFieldPhoto v-if = "friend" :character="friend.character"/>
        </div>
    </dialog>


</template>

<style scoped>

</style>