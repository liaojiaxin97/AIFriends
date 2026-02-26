<script setup>
import Character from "@/components/character/Character.vue";
import {onBeforeMount, onMounted, ref, useTemplateRef} from "vue";
import api from '@/js/http/api';

const characters = ref([])
const isLoading = ref(false)
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')


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

//定义监听界面
let observer = null
onMounted(async()=>{
  await loadMore() // 刚进入页面就加载一些角色
 
  observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting){
          loadMore()
        }
      })
    },
    {root:null,rootMargin:'2px',threshold:0}
  )
  observer.observe(sentinelRef.value)
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