<script setup>
import Photo from './components/Photo.vue';
import Name from './components/Name.vue';
import Profile from './components/Profile.vue';
import BackgroundImage from './components/BackgroundImage.vue';
import { useTemplateRef,ref } from 'vue';
import { base64ToFile } from '@/js/utils/base64_to_file';
import { useUserStore } from '@/stores/user';
import { useRouter} from 'vue-router';
import api from '@/js/http/api';


//打开个人空间需要知道打开谁的，user.id
const user = useUserStore()
//创建角色成功后需要跳转到个人空间，需要使用路由
const router = useRouter()

const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')

const errorMessage = ref('')


async function handleCreate(){
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
        formData.append('name',name)
        formData.append('profile',profile)
        formData.append('photo',base64ToFile(photo,'photo.png'))
        formData.append('background_image',base64ToFile(backgroundImage,'background_image.png'))

        // console.log('FormData content:')
        // for (const [key, value] of formData.entries()) {
        //     console.log(`${key}:`, value);
        // }

    try{
        const res = await api.post('/api/create/character/create/',formData)
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
    <div class = "flex justify-center">
        <div class ="card w-120 bg-base-200 shadow-sm mt-16">
            <div class ="card-body">
                <h3 class = "text-lg font-bold my-4">创建角色</h3>
                <Photo ref = "photo-ref"/>
                <Name ref = "name-ref"/>
                <Profile ref = "profile-ref"/>
                <BackgroundImage ref = "background-image-ref"/>

                <p v-if = "errorMessage" class = "text-sm text-red-500" >{{ errorMessage }}</p>
                <div class = "flex justify-center">
                    <button @click = "handleCreate" class = "btn btn-neutral w-60 mt-2">创建</button>
                </div> 
            </div>
        </div>
    </div>

</template>


<style scoped>

</style>