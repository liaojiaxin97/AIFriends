<script setup>
import { nextTick, useTemplateRef } from 'vue';
import { computed } from 'vue';
import Character from '../Character.vue';
import { ref } from 'vue';
import InputField from './input_field/InputField.vue';
import CharacterFieldPhoto from './character_field_photo/CharacterFieldPhoto.vue';
import ChatHistory from './chat_history/ChatHistory.vue';
const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-Ref')
const inputRef = useTemplateRef("input-ref")
const chatHistoryRef = useTemplateRef('chat-history-ref')
const history = ref([])


async function showModal(){
    modalRef.value.showModal()


    await nextTick()
    inputRef.value.focus()
}

function handlePushFrontMessage(msg){
  history.value.unshift(msg)
}


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

function handlePushBackMessage(msg){
  history.value.push(msg)
  chatHistoryRef.value.scrollToBottom()
}
function handleAddToLastMessage(delta){
  history.value.at(-1).content += delta
  chatHistoryRef.value.scrollToBottom()
}


function handleClose(){
  modalRef.value.close()
  inputRef.value.close()
}


defineExpose({
    showModal,
})
</script>

<template>  

    <dialog ref="modal-Ref" class = "modal">
        <div class = "modal-box w-90 h-150" :style="modalStyle">
            <button @click="handleClose" class = "btn btn-sm btn-circle btn-ghost bg-transparent absolute right-1 top-1">x</button>
            <ChatHistory 
              ref = "chat-history-ref"
              v-if = "friend"
              :history = "history"
              :friendId = "friend.id"
              :character = "friend.character"
              @pushFrontMessage = "handlePushFrontMessage"
            />
            <InputField 
            v-if = "friend"
            ref = "input-ref"
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