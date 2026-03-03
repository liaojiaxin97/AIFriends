<script setup>
import { ref,watch } from "vue";
//与主界面面板的照片组件photo名称相同，暂时不做修改
const props = defineProps(['profile'])
const myProfile = ref(props.profile)
watch(() => props.profile, (newVal) => {
    myProfile.value = newVal;
});

defineExpose({
    myProfile,
})
</script>

<template>
    <fieldset class="fieldset">
        <label class="label text-base">个人简介</label>
        <textarea v-model="myProfile" class = "textarea w-100" rows="6" placeholder="个人简介"></textarea>


    </fieldset>

</template>

<style scoped>

</style>