import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter);

const routes = [
	{
		path: '/',
		name: 'SignIn',
		component: () => import('../views/SignIn.vue')
	},
	{
		path: '/dashboard',
		name: 'Dashboard',
		component: () => import('../views/Dashboard.vue'),
		children: [
			{path: '/dashboard/', component: () => import('../views/Overview.vue')},
			{path: '/dashboard/project', component: () => import('../views/Project.vue')},
			{path: '/dashboard/workflow', component: () => import('../views/Workflow')},
			{path: '/dashboard/team-management', component: () => import('../views/TeamManagement.vue')},
			{path: '/dashboard/role-management', component: () => import('../views/RoleManagement.vue')},
			{path: '/dashboard/tasks', component: () => import('../views/Tasks.vue')}
		]
	}
];

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes
});

export default router
