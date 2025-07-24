import { createRouter, createWebHistory } from 'vue-router'
import HomeNavbar from '../views/Home.vue'
import SignupUser from '../views/SignupUser.vue'
import LoginUser from '../views/LoginUser.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue' 
import store from '../store/index.js'
import SubjectManagement  from '../views/SubjectManagement.vue'
import QuizManagement from '../views/QuizManagement.vue'
import QuizAttempt from '@/views/QuizAttempt.vue'
import UserScore from '@/views/UserScore.vue'
import UserDetails from '@/views/UserDetails.vue'
import SummaryAdmin from '@/views/SummaryAdmin.vue'
import SummaryUser from '@/views/SummaryUser.vue'



const routes = [
  {
    path: '/',
    name: 'home',
    component:HomeNavbar,
    meta: { requireGuest : true}
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupUser,
    meta: { requireGuest : true}
  },
  {
    path: '/login',
    name: 'login',
    component: LoginUser,
    meta: {requireGuest: true}
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: {requireAuth:true,roles:['admin']}
  },
  {
    path: '/user-dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: {requireAuth:true,roles:['user']}
  },
  {
    path: '/subject',
    name: 'subject',
    component: SubjectManagement,
    meta: {requireAuth:true,roles:['admin']}
  },
  {
    path: '/quiz-management',
    name: 'QuizManagement',
    component: QuizManagement,
    meta: {requireAuth:true,roles:['admin']},
    
  },
  {
    path:'/admin-summary',
    name: 'SummaryAdmin',
    component: SummaryAdmin,
    meta: {requireAuth:true,roles:['admin']},

  },
  {
    path: '/users',
    name: 'UserDetails',
    component: UserDetails,
    meta: { requireAuth: true, roles: ['admin'] }
  },
  
  {
  path: '/quiz-attempt/:quizId',
  name: 'QuizAttempt',
  component: QuizAttempt,
  meta: {requireAuth:true,roles:['user']}
  },
  {
    path: '/user-score/:userId',
    name: 'UserScore',
    component: UserScore,
    meta: {requireAuth:true,roles:['user']}
  },
 {
    path:'/user-summary',
    name: 'SummaryUser',
    component: SummaryUser,
    meta: {requireAuth:true,roles:['user']},

  },
  


  {
    path: '/about',
    name: 'about',
    
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) {
    // Check if the route requires authentication
    if (!store.getters.isAuthenticated) {
      // Redirect to login if not authenticated
      next('/login');
    } else {
      const userRole = store.getters.userRole;
    
      if (to.meta.roles && !to.meta.roles.includes(userRole)) {
        if (userRole == 'admin') {
          next('/admin-dashboard'); 
        } else if (userRole == 'user') {
          next('/user-dashboard'); 
        } else {
        next('/'); 
        } 
      }else {
        next(); // Proceed to the route
      }
    }
  } else if (to.meta.requireGuest) {
  
    if (store.getters.isAuthenticated) {
      next(); // Redirect to home if already authenticated
    } else {
      next(); // Proceed to the route
    }
  }
});
export default router
