<script setup>

import {useRoute} from "vue-router";
import UserInfoField from "./components/UserInfoField.vue";
import {nextTick, onMounted, ref,useTemplateRef,onBeforeUnmount} from "vue";
import api from '@/js/http/api';
import Character from "@/components/character/Character.vue";


const userProfile = ref(null)
const characters = ref([])
const isloading = ref(false)
const hasCharacters = ref(null)
const sentinelRef = useTemplateRef('sentinel-ref')
//user_id在url中，因此要使用路由
const route = useRoute()
let newCharacters = []
function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  //视窗上为0 下为innerHeight
  //判断红线是否在视窗内：如果红线的顶部在视窗内rect.top < window.innerHeight，
  // 并且红线的底部也在视窗内rect.bottom > 0，那么就说明红线在视窗内
  return rect.top < window.innerHeight && rect.bottom > 0
}


//循环体，看不见哨兵就一直加载更多内容，直到看见哨兵或者没有更多内容了
async function loadMore() {
    if (isloading.value || hasCharacters.value) return 
    isloading.value = true
    try {
        const res = await api.get('/api/create/character/get_list/',{
            //赋值，告诉后端已经加载了多少角色了，以及当前用户的id（因为个人空间是根据用户id来区分的）
            params:{
                items_count: characters.value.length,
                user_id: route.params.user_id,
            }
        })
        const data = res.data
        //观察流式加载
        //console.log(data)
        if (data.result === 'success'){
            userProfile.value = data.user_profile
            newCharacters = data.characters
        }
    } catch (err){
        console.log(err)
    } finally {
        isloading.value = false
        if (newCharacters.length === 0 ){
            hasCharacters.value = false
        } else {
            //将列表元素展开[1,2,3] --> 1,2,3
            //将newCharacters中的元素拼接到characters列表中
            characters.value.push(...newCharacters)
            await nextTick() // 等待DOM更新完成
            //检查哨兵是否可见，如果可见则继续加载更多内容
            if (checkSentinelVisible()){
                await loadMore()
        }

    }
}}
// 检测红色哨兵是否出现在视窗中，如果在视窗中则加载更多内容
let observer = null
onMounted(async () => {
  await loadMore()  // 加载新元素

  observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
        //console.log("哨兵元素被看到，加载更多内容")
        loadMore()
        }
      })
    },
    {root: null, rootMargin: '2px', threshold: 0}
  )

  //监听哨兵元素， 每次哨兵被看到时，都会触发一次
  observer.observe(sentinelRef.value)
})
//传递给子组件
function removeCharacter(characterId){
    characters.value = characters.value.filter(character => character.id !== characterId)
}

onBeforeUnmount(() => {
  observer?.disconnect()  // 解绑监听器
})

</script>


<template>
    <!-- 创建一个垂直排列的容器。将容器内的所有子元素水平居中对齐。 -->
    <div class ="flex flex-col items-center">
        <UserInfoField :userProfile = "userProfile"/>

        <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
            <Character
            v-for = "character in characters"
            :key = "character.id"
            :character = "character"
            :canEdit = "true"
            @remove = "removeCharacter"
            />

        </div>
        <!-- 红线在视窗内时，持续加载更多内容（卡片） -->
        <div ref = "sentinel-ref" class = "h-2 mt-2"> </div>
        <div v-if = "isloading" class="text-gray-500 mt-4">加载中...</div>
        <div v-else-if="!hasCharacters" class = "text-gray-500 mt-">没有更多角色了</div>
    
    </div>
</template>



<style scoped>

</style>