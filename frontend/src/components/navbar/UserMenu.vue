<script setup>   
import { useUserStore } from '@/stores/user.js';
import UserSpaceIcon from './icons/UserSpaceIcon.vue';
import UserProfileIcon from './icons/UserProfileIcon.vue';
import UserLogoutIcon from './icons/UserLogoutIcon.vue';



const user = useUserStore()


function closeMenu() {
  const element = document.activeElement
  if (element && element instanceof HTMLElement) element.blur()
}
</script>

<template>
<div class="dropdown dropdown-end">
  <div tabindex="0" role="button" class="avatar btn btn-circle w-8 h-8 mr-6">
    <div class = "w-8 rounded-full">
        <img :src="user.photo" alt="">
    </div>
  </div>
  <ul tabindex="0" class="dropdown-content menu bg-base-100 rounded-box z-[1] w-52 p-2 shadow-lg">
    <li>
        <router-link @click="closeMenu" :to="{name: 'user-space-index', params: {user_id: user.id}}">
            <div class = "avatar">
                <div class = "w-10 rounded-full">
                    <img :src="user.photo" alt="用户头像" />
                </div>
            </div>
            <span class = "text-base font-bold line-clamp-1">{{ user.username }}</span>
        </router-link>
    </li>
    <li>
        <router-link @click="closeMenu" :to="{name: 'user-space-index', params: {user_id: user.id}}" class="text-sm font-bold py-3“">
            <UserSpaceIcon />
            个人空间
        </router-link>
    </li>
        <li>
        <router-link @click="closeMenu" :to="{name: 'user-profile-index', params: {user_id: user.id}}" class="text-sm font-bold py-3“">
            <UserProfileIcon />
            编辑个人资料
        </router-link>
    </li>
    <li></li>
    <li>
        <a @click="closeMenu" class="text-sm font-bold py-3“">
            <UserLogoutIcon />
            退出登录
        </a >
    </li>
  </ul>
</div>
</template>

<style>

</style>