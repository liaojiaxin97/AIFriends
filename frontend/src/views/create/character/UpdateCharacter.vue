<script setup>
import Photo from './components/Photo.vue';
import Name from './components/Name.vue';
import Profile from './components/Profile.vue';
import BackgroundImage from './components/BackgroundImage.vue';
import { useTemplateRef,ref } from 'vue';
import { base64ToFile } from '@/js/utils/base64_to_file';
import { useUserStore } from '@/stores/user';
import { useRouter, useRoute } from 'vue-router';
import api from '@/js/http/api';
import { onMounted } from 'vue';

const user = useUserStore()
const router = useRouter()
const route = useRoute()
//路由中是character_id,因此这里要写下划线而不是点
const characterId = route.params.character_id
const character = ref(null)

onMounted(async () => {
    try {
        const res = await api.get('/api/create/character/get_single/',{
            params:{
                character_id: characterId,
            }
        })
        const data = res.data

        if (data.result === 'success'){
            character.value = data.character
        }
    } catch(err){
        console.log(err)
    }
})

const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')

const errorMessage = ref('')


async function handleUpdate(){
    const photo = photoRef.value.myPhoto
    const name = nameRef.value.myName?.trim()
    const profile = profileRef.value.myProfile?.trim()
    const backgroundImage = backgroundImageRef.value.myBackgroundImage

    errorMessage.value = ""
    if (!photo || !name || !profile ){
        errorMessage.value = "请完整填写角色信息"
    }else if(!backgroundImage){
        errorMessage.value = "请上传背景图片"
    }
    else {
        //将角色创建所需的数据（如名称、简介、照片和背景图片）添加到表单数据中，
        // 以便通过 HTTP 请求发送到后端
        const formData = new FormData()
        formData.append('character_id', characterId)
        formData.append('name',name)
        formData.append('profile',profile)
        //响应式变量使用时一定要加.value,不然拿到的是ref对象而不是具体的值
        if (photo !== character.value.photo){
        formData.append('photo',base64ToFile(photo,'photo.png'))
        }
        //这里为什么_image?
        //因为在后端模型中是background_image,所以前端也要这样命名
        if (backgroundImage !== character.value.background_image){
            //
        formData.append('background_image',base64ToFile(backgroundImage,'background_image.png'))
        }

        // console.log('FormData content:')
        // for (const [key, value] of formData.entries()) {
        //     console.log(`${key}:`, value);
        // }

    try{
        const res = await api.post('/api/create/character/update/',formData)
        const data = res.data
        if (data.result === "success"){
                //需要打开个人空间-->提前导入11-12行内容
            await router.push({
                name:'user-space-index',
                params:{
                    user_id: user.id,
                }
            })
        }else{
            errorMessage.value = data.result
        }
    }catch (err) {

    }
    }
}
</script>

<template>
    <div v-if = "character" class = "flex justify-center">
        <div class ="card w-120 bg-base-200 shadow-sm mt-16">
            <div class ="card-body">
                <h3 class = "text-lg font-bold my-4">更新角色</h3>
                <!-- html中使用响应式变量，所以无需.value -->
                <Photo ref = "photo-ref" :photo=character.photo />
                <Name ref = "name-ref" :name=character.name />
                <Profile ref = "profile-ref" :profile=character.profile />
                <!-- backgroundImage这里的变量对应Background.vue中的响应式变量 -->
                <BackgroundImage ref = "background-image-ref" :backgroundImage=character.background_image />

                <p v-if = "errorMessage" class = "text-sm text -red-500" >{{ errorMessage }}</p>
                <div class = "flex justify-center">
                    <button @click = "handleUpdate" class = "btn btn-neutral w-60 mt-2">更新</button>
                </div> 
            </div>
        </div>
    </div>

</template>


<style scoped>

</style>