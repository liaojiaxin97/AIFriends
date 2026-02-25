<script setup>
//初始值为空
defineProps(['userProfile'])
</script>

<template>
    <div v-if="userProfile" class = "flex mt-12 gap-8">
        <div class = "avatar">
            <div class = "rounded-full w-44">
                <img :src="userProfile.photo" alt="">
            </div>
        </div>
        <!-- flex col 竖直排列 注意区别 水平 -->
        <div class = "flex flex-col justify-center w-64 h-44">
            <div class = "text-2xl font-bold line-clamp-1 break-all">{{userProfile.username}}</div>
            <div class = "text-sm mt-2 text-gray-500">AIFriend ID:{{userProfile.user_id}}</div>
            <div class = "text-sm h-20 mt-4 line-clamp-1 break-all">{{userProfile.profile}}</div>
        </div>
    </div>

</template>



<style scoped>

</style>