
<script setup>
import {ref} from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from 'vue-router';
import api from "@/js/http/api.js";
const username = ref('')
const password = ref('')
const errorMessage = ref('')

const user = useUserStore()
//router 跳转
//router 获取链接
const router = useRouter()
async function handleLogin(){
  errorMessage.value = ''
  if (!username.value.trim()){
    errorMessage.value = '用户名不能为空'
  } else if (!password.value.trim()){
    errorMessage.value = "密码不能为空"
  } else {
    try{
      const res = await api.post('/api/user/account/login/', {
        username: username.value,
        password: password.value,
      })
      const data = res.data
      //console.log(data.result)
      if (data.result === 'success') {
        
        user.setAccessToken(data.access)
        user.setUserInfo(data)
        await router.push({
          name:'homepage-index'
        })
      }else { 
        errorMessage.value= data.result
        //console.log("登陆成功")
      }
    } catch (err){
      console.log(err)
    }
  }
}

</script>

<template>
<div class = "flex justify-center mt-30">
  <form @submit.prevent = "handleLogin" class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
  <legend class="fieldset-legend">Login</legend>

  <label class="label">用户名</label>
  <input v-model = "username" type="text" class="input" placeholder="Email" />

  <label class="label">密码</label>
  <input v-model = "password" type="password" class="input" placeholder="Password" />
  <p v-if = "errorMessage" class="text-sm text-red-500 mt-1">{{ errorMessage}}</p>
  <button class="btn btn-neutral mt-4">登录</button>
  <div class = "flex justify-end">
    <router-link :to = "{ name : 'user-account-register-index'}" class = "btn btn-sm btn-ghost text-gray-500" >
      注册
    </router-link>

  </div>
  </form>
</div>


</template>


<style >

</style>