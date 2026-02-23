<script setup>
import { ref,watch,useTemplateRef } from "vue";


const props = defineProps(['name'])
const myName = ref(props.name)
watch(() => props.name, (newVal) => {
    myName.value = newVal;
});

//暴露图片给父组件用
defineExpose({
    myName,
})

</script>

<template>
    <fieldset class = "fieldset">
        <label class="label text-base">名字</label>
        <input v-model="myName" type = "text" class = "input w-108">
    </fieldset>

</template>


<style scoped>

</style>