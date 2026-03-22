<script setup>
import { nextTick, useTemplateRef } from 'vue';
import { computed } from 'vue';
import Character from '../Character.vue';

import InputField from './input_field/InputField.vue';
import CharacterFieldPhoto from './character_field_photo/CharacterFieldPhoto.vue';

const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-Ref')
const inputRef = useTemplateRef("input-ref")


async function showModal(){
    modalRef.value.showModal()


    await nextTick()
    inputRef.value.focus()
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
            <InputField 
            v-if = "friend"
            ref = "input-ref"
            :friendId = "friend.id"
            />
            <CharacterFieldPhoto v-if = "friend" :character="friend.character"/>
        </div>
    </dialog>


</template>

<style scoped>

</style>