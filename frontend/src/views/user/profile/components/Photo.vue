<script setup>
import { ref,watch,useTemplateRef, nextTick, onBeforeUnmount } from "vue";
import CameraIcon from "./icon/CameraIcon.vue";
import Croppie from 'croppie'
import 'croppie/croppie.css'
//与主界面面板的照片组件photo名称相同，暂时不做修改
const props = defineProps(['photo'])
const myPhoto = ref(props.photo)
watch(() => props.photo, (newVal) => {
    myPhoto.value = newVal;
});

const fileInputRef = useTemplateRef('file-input-ref')
//为了每次都触发上传弹窗操作，
//将input的value置空，确保每次选择文件都会触发change事件
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
//该变量不会显示是在前端，故无需 响应式ref
let croppie = null


async function crop(){
    if(!croppie) return 

    myPhoto.value = await croppie.result({
        type:'base64',
        size:'viewport',
    })
    modalRef.value.close()
}

function onFileChange(e){
    const file = e.target.files[0]
    e.target.value = ''
    if (!file) return 

    const reader = new FileReader()
    
    reader.onload = (event) => {
        //console.log(reader.result)
        openModal(reader.result)
    }
    reader.readAsDataURL(file)
}

//暴露图片给父组件用
defineExpose({
    myPhoto,
})
async function openModal(photo){
    //console.log(modalRef.value)
    modalRef.value.showModal()
    await nextTick()

    if (!croppie){
        croppie = new Croppie(croppieRef.value, {  // 创建croppie对象
            viewport: {width: 200, height: 200, type: 'square'},
            boundary: {width: 300, height: 300},
            enableOrientation: true,
            enforceBoundary: true,
        })
    }
    croppie.bind({  
        url: photo,
    })
}
//清空crop对象，防止数据泄露
//croppie为空 不执行. 操作，否则执行
onBeforeUnmount(() => {
    croppie?.destroy()
})

</script>

<template>
    <div class = "flex justify-center">
        <div class = "avatar relative">
            <div class = "w-28 rounded-full">
                <img :src="myPhoto" alt="">
            </div>
            <div @click = "fileInputRef.click()" class = "absolute left-0 top-0 w-28 h-28 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
                <CameraIcon/>
            </div>
        </div>
    </div>
    
<input ref = "file-input-ref" type="file" accept = "img/*" class = "hidden" @change = "onFileChange">
<!-- model 的属性中自带relative 所以无需再添加relative属性 -->
<dialog  ref = "modal-ref" class = "modal"  >
    <div class = "modal-box transition-none">
        <button @click = "modalRef.close()" class = "btn btn-circle btn-sm btn-ghost absolute right-2 top-2"">x</button>
        <div ref = "croppie-ref" class = "flex flex-col justify-center my-4"> </div>
        <div class = "modal-action"> 
            <button @click = "modalRef.close()" class = "btn">取消</button>
            <button @click="crop" class = "btn btn-neutral">确定</button>
        </div>
    </div>
</dialog>

</template>

<style scoped>

</style>