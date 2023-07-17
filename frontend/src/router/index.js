import Vue from 'vue'
import Router from 'vue-router'
import Matches from '@/components/Matches'
import Cistella from '@/components/Cistella'
import Login from '@/components/Login'
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Matches',
      component: Matches
    },
    {
      path: '/userlogin',
      name: 'Login',
      component: Login
    },
    {
      path: '/cistella',
      name: 'Cistella',
      component: Cistella
    }
  ]
})
