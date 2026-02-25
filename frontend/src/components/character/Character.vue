<script setup>
import {useRoute,useRouter} from "vue-router";
import {ref} from "vue";
import { useUserStore } from "@/stores/user.js";
import UpdateIcon from "@/components/character/icon/UpdateIcon.vue";
import RemoveIcon from "./icon/RemoveIcon.vue";
import api from '@/js/http/api.js';
const route = useRoute()
const router = useRouter()

const isHover = ref(false)
//接受外部传来的变量
const props = defineProps(['character','canEdit'])
const emit = defineEmits(['remove'])
const user = useUserStore()
//后端删除逻辑

async function handleRemoveCharacter(){
    try{
        const res = await api.post('/api/create/character/remove/',{
            character_id:props.character.id,
        })
        if (res.data.result === 'success') {
            emit('remove',props.character.id)
        }
    }catch(err){
        console.log(err)
    }
}
</script>

<template>

<div>
    <div class = "avatar cursor-pointer" @mouseover="isHover = true" @mouseout="isHover = false">
        <div class = "w-60 h-100 rounded-2xl relative " :class="{'scale-120': isHover}" >
            <img :src="character.background_image" class = "transition-transform duration-1000"   alt="">
            <div class = "absolute left-0 top-50 w-60 h-50 bg-linear-to-t from-black/40 to-transparent"></div>

            <div v-if = "canEdit && character.author.user_id === user.id" class = "absolute right-0 top-50">
                <router-link :to = "{name: 'update-character', params: {character_id: character.id}}" class = "btn btn-circle btn-ghost bg-transparent">
                  <UpdateIcon />
                </router-link>
                <button @click="handleRemoveCharacter" class ="btn btn-circle btn-ghost bg-transparent">
                    <RemoveIcon/>
                </button>
            </div>
            <div class = "absolute left-4 top-54 avatar">
                <div class = "w-16 rounded-full ring-3 ring-white">
                    <img :src="character.photo" alt="">
                </div>
            </div>
            <div class = "absolute left-24 right-4 top-58 text-white font-bold line-clamp-1 break-all">
                {{character.name}}
            </div>
            <div class = "absolute left-4 right-4 top-72 text-white line-clamp-4 break-all">   
                {{character.profile}}
            </div>
        </div>
    </div>
    <router-link :to="{name:'user-space-index',params:{user_id:character.author.user_id}}" class ="flex items-center mt-4 gap-2 w-60 ">
        <div class ="avatar">
            <div class = "w-7 rounded-full">
                <img :src="character.author.photo" alt="">
            </div>
        </div>
        <div class ="text-sm line-clamp-1 break-all"> {{character.author.username}}</div>
    </router-link>

</div>

</template>



<style scoped>

</style>