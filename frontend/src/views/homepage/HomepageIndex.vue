<script setup>
import Character from "@/components/character/Character.vue";
import {onBeforeMount, onMounted, ref, useTemplateRef} from "vue";
import api from '@/js/http/api';
import { useRoute } from "vue-router";
import { watch } from "vue";
import { nextTick } from "vue";
const characters = ref([])
const isLoading = ref(false)
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const route = useRoute()

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore(){
  if (isLoading.value || !hasCharacters.value) return
  isLoading.value = true
  //临时你变量存储云端加载的角色信息
  let newCharacters = []    

  try {
    const res = await api.get('/api/homepage/index/',{
      params:{
        items_count:characters.value.length,
        search_query: route.query.q || '',
      }
    })
    const data = res.data
    if (data.result === 'success'){
      newCharacters = data.characters
    }
  }catch (err){ 
    console.log(err)
  } finally {
    isLoading.value = false
    if (newCharacters.length === 0 ){
      hasCharacters.value = false
    } else {
      characters.value.push(...newCharacters)
      await nextTick() // 等待DOM更新完成
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

//重新加载，自动读取url中的搜索参数q，展示搜索结果
function  reset(){
  characters.value = []
  isLoading.value = false
  hasCharacters.value = true
  loadMore()
}
watch(() => route.query.q,newQ => {
  reset()
})



//组件移除前删除资源
onBeforeMount(() => {
  observer?.disconnect()
})
</script>


<template>

  <div class = "flex flex-col items-center mb-12">
    <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
    <Character
        v-for = "character in characters"
        :key = "character.id"
        :character = "character"
    />
    </div>
    <div ref = "sentinel-ref" class = "h-2 mt-8"></div>
    <div v-if = "isLoading" class = "text-gray-500 mt-4">加载中……</div>
    <div v-else-if = "!hasCharacters" class = "text-gray-500 mt-4">没有更多角色了</div>
  </div>

</template>

<style scoped> </style>