import CreateIndex from '@/views/create/CreateIndex.vue';
import NotFoundIndex from '@/views/error/NotFoundIndex.vue';
import FriendIndex from '@/views/friend/FriendIndex.vue';
import HomepageIndex from '@/views/homepage/HomepageIndex.vue';
import LoginIndex from '@/views/user/account/LoginIndex.vue';
import RegisterIndex from '@/views/user/account/RegisterIndex.vue';
import SpaceIndex from '@/views/user/space/SpaceIndex.vue';
import ProfileIndex from '@/views/user/profile/ProfileIndex.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'homepage-index',
      component: HomepageIndex,
      meta:{
        needLogin: false,  // 需要登录才能访问
      }
    },
    {
      path: '/friend/',
      name: 'friend-index',
      component: FriendIndex,
      meta:{
        needLogin: true,  // 需要登录才能访问
      }
      
    },
    {
      path: '/create/',
      name: 'create-index',
      component: CreateIndex,
      meta:{
        needLogin: true,  // 需要登录才能访问
      }
    },
    {
      path: '/404/',
      name: '404',
      component: NotFoundIndex,
      meta:{
        needLogin: false, 
      }
    },
    {
      path: '/user/account/login/',
      name: 'user-account-login-index',
      component: LoginIndex,
      meta:{
        needLogin: false,  // 需要登录才能访问
      }
    },
    {
      path: '/user/account/register/',
      name: 'user-account-register-index',
      component: RegisterIndex,
      meta:{
        needLogin: false,  // 需要登录才能访问
      }
    },
    {
      
      path: '/user/space/:user_id/',
      name: 'user-space-index',
      component: SpaceIndex,
      meta:{
        needLogin: false,  // 需要登录才能访问
      }
    },
    {
      
      path: '/user/profile/',
      name: 'user-profile-index',
      component: ProfileIndex,  
      meta:{  
        needLogin: true,  // 需要登录才能访问
      }
    },     
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: NotFoundIndex,
           meta:{
        needLogin: false,  // 需要登录才能访问
      }
    },  
  ],  
})



router.beforeEach((to, from) => {
  const user = useUserStore()
  if (to.meta.needLogin &&  user.hasPulledUserInfo && !user.isLogin()){
    return {
      name: 'user-account-login-index',
    }
  }
  return true
})

export default router