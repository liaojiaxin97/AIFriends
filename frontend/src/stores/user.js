import {defineStore} from "pinia";
import {ref} from "vue"

export const useUserStore = defineStore('user', () => {
    const id = ref(0)
    const username = ref('')
    const photo = ref('')
    const profile = ref('')
    const accessToken = ref('')
    const hasPulledUserInfo = ref(false)  // 是否已经从服务器拉取过用户信息了

    function isLogin(){
        return !!accessToken.value  // 必须带value
    }
    function setAccessToken(token){
        accessToken.value = token
    }
    function setUserInfo(data){
        id.value = data.id || data.user_id  // 兼容两种字段名
        username.value = data.username
        photo.value = data.photo
        profile.value = data.profile
    }

    function logout(){
        id.value = 0
        username.value = ''
        photo.value = ''
        profile.value = ''
        accessToken.value = ''
    }
    function setHasPulledUserInfo(newStatus){
        hasPulledUserInfo.value = newStatus
    }
    return {
        id,
        username,
        photo,
        profile,
        accessToken,  //一定要返回！！！！
        setAccessToken,
        setUserInfo,
        isLogin,
        logout,
        hasPulledUserInfo,
        setHasPulledUserInfo,
    }
})

