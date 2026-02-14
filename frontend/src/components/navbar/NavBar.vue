<script setup>
//图标导入
// import MenuIcon from "@/components/navbar/icons/MenuIcon_vue"  
import { useUserStore } from '@/stores/user';
import UserMenu from '@/components/navbar/UserMenu.vue';
import UserHomePageIcon from '@/components/navbar/icons/HomepageIcon.vue';
import UserCreateIcon from '@/components/navbar/icons/CreateIcon.vue';
import UserFriendIcon from '@/components/navbar/icons/FriendIcon.vue';
import UserSearchIcon from '@/components/navbar/icons/SearchIcon.vue';
import UserSpaceIcon from './icons/UserSpaceIcon.vue';
const user = useUserStore()

</script>

<template>
<div class="drawer lg:drawer-open">
  <input id="my-drawer-4" type="checkbox" class="drawer-toggle" />
  <div class="drawer-content">
    <!-- Navbar -->
    <nav class="navbar w-full bg-base-300">
        <div class = "navbar-start">
        <label for="my-drawer-4" aria-label="open sidebar" class="btn btn-square btn-ghost">
            <!-- Sidebar toggle icon -->
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-linejoin="round" stroke-linecap="round" stroke-width="2" fill="none" stroke="currentColor" class="my-1.5 inline-block size-4"><path d="M4 4m0 2a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2z"></path><path d="M9 4v16"></path><path d="M14 10l2 2l-2 2"></path></svg>
        </label>      
        <div class="px-4">AIFriends</div>
        </div>
     

        <div class = "navbar-center w-4/5 max-w-180 flex jcustify-center">
        <div class="join w-4/5 flex jcustify-center">
        <input class="input join-item rounded-l-full w-4/5" placeholder="搜索你感兴趣的内容" />
        <button class="btn join-item rounded-r-full gap-0">
            <UserSearchIcon />
            搜索
        </button>
        </div>
        </div>

        <div class="navbar-end">
        <router-link v-if = "user.isLogin()" :to="{name: 'create-index' }" active-class = "btn-active" class= "btn btn-ghost text-base mr-6">
          创作
        </router-link>
        <router-link v-if = "!user.isLogin()" :to = "{ name : 'user-account-login-index' }" active-class = "btn-active" class = "btn btn-ghost text-lg">
          登录
        </router-link>
        <UserMenu v-else>
        </UserMenu>
        </div>
    </nav>

    <!-- Page content here -->
    <div class="p-4">
      <slot></slot>
    </div>
  </div>


  <div class="drawer-side is-drawer-close:overflow-visible">
    <label for="my-drawer-4" aria-label="close sidebar" class="drawer-overlay"></label>
    <div class="flex min-h-full flex-col items-start bg-base-200 is-drawer-close:w-16 is-drawer-open:w-64">
      <!-- Sidebar content here -->
      <ul class="menu w-full grow">
        <!-- List item -->
        <li>
          <router-link :to="{ name: 'homepage-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="首页">
            <!-- Home icon -->
            <UserHomePageIcon />


            <span class="is-drawer-close:hidden text-base ml-2 white-space-nowrap">首页</span>
          </router-link>
        </li>
        <li>
          <router-link :to="{ name : 'friend-index'}"  active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="好友">
              <UserFriendIcon />
              <span class="is-drawer-close:hidden text-base ml-2 white-space-nowrap">好友</span>
          </router-link>
        </li>
        <li>
          <router-link :to="{ name: 'create-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="创作">
            <UserCreateIcon />
            <span class="is-drawer-close:hidden text-base ml-2 white-space-nowrap">创作</span>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</div>
</template>

<style scoped>
</style>