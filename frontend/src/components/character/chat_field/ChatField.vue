<script setup>
import { useTemplateRef,nextTick } from 'vue';
import { computed } from 'vue';
import Character from '../Character.vue';


//用来接收父组件传下来的数据
const props = defineProps(['friend'])
//用来拿模板里某个元素或子组件的引用
const modalRef = useTemplateRef('modal-Ref')
const inputRef = useTemplateRef('input-ref')
import InputField from './input_field/InputField.vue';
import CharacterFieldPhoto from './character_field_photo/CharacterFieldPhoto.vue';
//展示模态框
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
            <InputField ref = "input-ref" v-if = "friend" :friendId = "friend.id"/>
            <CharacterFieldPhoto v-if = "friend" :character="friend.character"/>
        </div>
    </dialog>


</template>

<style scoped>

</style>