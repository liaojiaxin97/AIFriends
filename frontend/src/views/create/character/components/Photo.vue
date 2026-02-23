<script setup>
import { ref,watch,useTemplateRef, nextTick, onBeforeUnmount } from "vue";
import CameraIcon from './icon/CameraIcon.vue';
import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)
watch(() => props.photo, (newVal) => {
    myPhoto.value = newVal;
});

//暴露图片给父组件用
defineExpose({
    myPhoto,
})

const fileInputRef = useTemplateRef("file-input-ref")

const modalRef = useTemplateRef('modal-ref')

const croppieRef = useTemplateRef('croppie-ref')

//不需要在前端显示，所以不需要响应式
let croppie = null

async function openModal(photo){
    //js调用响应式变量 使用.value
    modalRef.value.showModal()

    if (!croppie){
        croppie = new Croppie(croppieRef.value, {  // 创建croppie对象
            viewport: {width: 200, height: 200, type: 'square'},
            boundary: {width: 300, height: 300},
            enableOrientation: true,
            enforceBoundary: true,
        })
    }
    croppie.bind({
        url: photo
    })
}

async function crop(){
    if(!croppie) return

    myPhoto.value = await croppie.result({
        type:'base64',
        size:'viewport',
    })

    modalRef.value.close()
}

function onFileChange(e) {
    const file = e.target.files[0]
    //确保每次用户上传图片，都能打开选择图片框
    e.target.value = ''
    if (!file) return 

    const reader = new FileReader()
    reader.onload = () => {
        openModal(reader.result)
    }
    reader.readAsDataURL(file)
}
//释放内存
onBeforeUnmount(() => {
    croppie?.destroy()
})
</script>

<template>
    <div class = "flex justify-center">
        <div class = "avatar relative">
            <div v-if ="myPhoto" class = "w-28 rounded-full">
                <img :src="myPhoto" alt="">
            </div>
            <div v-else class = "w-28 h-28 rounded-full bg-base-300"></div>
            <!-- html中调用响应式变量 无需加value -->
            <div  @click = "fileInputRef.click()" class = "w-28 h-28 rounded-full bg-black/50 absolute left-0 top-0 flex justify-center items-center cursor-pointer">
                <CameraIcon />
            </div>
        </div>
    </div>
    <input ref = "file-input-ref" type="file" class = "hidden" accept = "image/*" @change="onFileChange">
    <dialog ref = "modal-ref" class = "modal">
        <div class=" modal-box transition-none">
            <button @click="modalRef.close()" class=" btn btn-sm btn-circle btn-ghost absolute right-2 top-2">x</button>
            <div ref = "croppie-ref" class = "flex flex-col my-4"> </div>
        <div class = "modal-action"> 
            <div @click = "modalRef.close()" class ="btn">取消</div>
            <div @click = "crop" class = "btn btn-neutral">确定</div>
        </div> 

        </div>
    </dialog>
</template>


<style scoped>

</style>