import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'

import VueSocketIo from 'vue-socket.io'
import SocketIO from 'socket.io-client'
Vue.use(new VueSocketIo({
	debug: true,
	connection: SocketIO('http://127.0.0.1:5000'),
	vuex: {
		store,
		actionPrefix: 'SOCKET_',
		mutationPrefix: 'SOCKET_'
	}
}))

import RippleEffect from './directives/rippleEffect'

import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

import axios from 'axios';

import firebase from "firebase/app";
import "firebase/firestore";
import "firebase/database";

const firebaseConfig = {
	apiKey: "AIzaSyBmfiTXgNyxlugNqVIrFshzEBtWfaeh3aU",
	authDomain: "zavrsni-cea71.firebaseapp.com",
	databaseURL: "https://zavrsni-cea71.firebaseio.com",
	projectId: "zavrsni-cea71",
	storageBucket: "zavrsni-cea71.appspot.com",
	messagingSenderId: "122434065323",
	appId: "1:122434065323:web:80a3f331c03694ea2c78ee"
};
firebase.initializeApp(firebaseConfig);


window.axios = axios.create({
	baseURL:`http://localhost:2000/`
});

Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.directive('rippleeffect', RippleEffect);

Vue.config.productionTip = false;

new Vue({
	store,
	router,
	render: h => h(App)
}).$mount('#app');
