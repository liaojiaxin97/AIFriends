<script setup>
import { ref,watch } from "vue";
//与主界面面板的照片组件photo名称相同，暂时不做修改
const props = defineProps(['username'])
const myUsername = ref(props.username)
//第一时间username 为空，第二时间从云端获取后才会有值赋
//监听父组件probs传来的username变化，更新myUsername的值
//如果不进行watch监听，用户名处的留白为空白，无法显示用户名
watch(() => props.username, (newVal) => {
    myUsername.value = newVal;
});

defineExpose({
    myUsername,
})

</script>

<template>
    <fieldset class = "fieldset">
        <label class="label text-base">用户名</label>
        <input v-model = "myUsername" type="text" class = "input w-100">
    </fieldset>

</template>

<style scoped>

</style>