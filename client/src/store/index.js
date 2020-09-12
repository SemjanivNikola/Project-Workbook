import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate"

Vue.use(Vuex);

export default new Vuex.Store({
	plugins: [createPersistedState()],
	state: {
		myInfo: {},
		tasks: [
			{id: '1', title: 'New Prototype', highPriority: true, project: 'Kamenjak', task: 'Create new prototype for the landing page', done: true, dueDate: '6.8.2020'},
			{id: '2', title: 'Google Analytics', highPriority: true, project: 'All', task: 'Add new Google Analytics code to all main files', done: false, dueDate: '8.8.2020'},
			{id: '3', title: 'Update', highPriority: true, project: 'Sprint', task: 'Finish Dashboard UI Kit update', done: false, dueDate: '10.8.2020'},
			{id: '4', title: 'Update', highPriority: true, project: 'Sprint', task: 'Update parallax scroll on our web page', done: false, dueDate: '10.8.2020'},
			{id: '5', title: 'Update contact', highPriority: true, project: 'Kamenjak', task: 'Update client contacts - Kamenjak', done: false, dueDate: '10.8.2020'},
			{id: '6', title: 'New Prototype', highPriority: false, project: 'Marvel', task: 'Create a prototype for the landing page', done: false, dueDate: '25.9.2020'}
		],
		projects: [
			{id: '1', title: 'Kamenjak web page', client: 'Javna ustanova Kamenjak', deadLine: '10.8.2020', teamLeader: 'Dario Matkov', team: 'SF Dev Team', budget: '12000', budgetStatus: 'Invoice sent', status: 'Early Stages'},
			{id: '2', title: 'Sprint web page', client: 'Nikola d.o.o.', deadLine: '10.8.2020', teamLeader: 'Dario Matkov', team: 'SF Dev Team', budget: '1242', budgetStatus: 'Paid', status: 'Finishing'},
			{id: '3', title: 'Marvel web page', client: 'Marvel Comics', deadLine: '10.8.2020', teamLeader: 'Dario Matkov', team: 'SF Dev Team', budget: '9676', budgetStatus: 'Delayed', status: 'Waiting for Client'},
			{id: '4', title: 'Landing page', client: 'Airbnb', deadLine: '1.5.2020', teamLeader: 'Dario Matkov', team: 'SF Dev Team', budget: '18500', budgetStatus: 'Paid', status: 'Finished'}
		],
		members: [],
		teams: [],
		projectDetails: {}
	},
	getters: {
		getHighPriorityTask: state =>  {
			return state.tasks.filter(task => task.highPriority)
		},
		getTasks: state => {
			return state.tasks
		},
		getMembers: state => {
			return state.members
		},
		getProjects: state => {
			return state.projects
		},
		getTeams: state => {
			return state.teams
		},
		getMyInfo: state => {
			return state.myInfo
		}
	},
	mutations: {
		setNewProjectDetails (state, payload) {
			state.projectDetails = payload
		},
		setTeams (state, payload) {
			state.teams = payload
		},
		setMembers (state, payload) {
			state.members = payload
		},
		setMyInfo (state, payload) {
			state.myInfo = payload
		},
		setProjects (state, payload) {
			state.projects = payload
		},
		updateProjects (state, payload) {
			state.projects.push(payload)
		},
		setActiveProjectForMember (state, payload) {
			state.myInfo.activeProject = payload
		}
	},
	actions: {
		async checkTeamsData (context) {
			if (context.state.teams.length > 0) {
				return context.getters.getTeams
			} else {
				await axios.get('/team/')
					.then((r) => {
						context.commit('setTeams', r.data.teams);
						context.commit('setMembers', r.data.members);
					})
					.catch((error) => {
						console.log('Ops, something went wrong. Errror => ', error);
					})
			}
		}
	}
})
