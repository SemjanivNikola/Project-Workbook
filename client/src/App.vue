<template>
	<div id="app">
		<router-view @authenticated="setAuthentication"/>
	</div>
</template>

<script>
	export default {
		name: 'App',
		data () {
			return {
				authenticated: false,
        isConnected: false,
			}
    },
    sockets: {
      connect: function () {
        this.isConnected = true;
        console.log('socket connected');
      }
    },
		methods: {
		  setAuthentication (state) {
		    if (state)  this.$router.replace({path: 'dashboard/'});
      }
    }
	}
</script>

<style>
	* {
		margin: 0;
		padding: 0;
	}
	div, span, a, ul {
		box-sizing: border-box;
		display: block;
	}
	#app {
		width: 100%;
		height: 100vh;
		font-family: Avenir, Helvetica, Arial, sans-serif;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
		text-align: center;
		color: #2c3e50;
		overflow: hidden;
	}
	a {
		text-decoration: none;
		cursor: pointer;
		-webkit-transition: color 200ms ease-in-out;
		-moz-transition: color 200ms ease-in-out;
		-ms-transition: color 200ms ease-in-out;
		-o-transition: color 200ms ease-in-out;
		transition: color 200ms ease-in-out;
	}
	div.row {
		margin-left: 0;
		margin-right: 0;
	}
	/*
	#nav a.router-link-exact-active {
		color: #42b983;
	}
	*/
	.column-inner:before, .column-inner:after {
		display: table;
		content: '';
	}
	.column-inner, .wrapper {
		margin: 0;
		padding: 0;
		border: 0;
		font-size: 100%;
		background: 0 0;
		outline: 0;
	}
	.col-display {
		display: inline-block;
	}
	.img-res {
		height: 100%;
		width: auto;
	}
	.d-table, .d-table-cell {
		height: inherit;
		width: inherit;
	}
	.bg-img-01 {
		height: inherit;
		width: 100%;
		background-image: url("./assets/static/Abstract-3-1200x1080---65.jpg");
		background-position: center;
		background-repeat: no-repeat;
		background-size: cover;
	}
	.custome-designe-btn {
		width: 170px;
		height: 35px;
		text-align: center;
		background-color: #2c3e50;
		border: none;
		outline: none;
		color: #fff;
		cursor: pointer;
		position: relative;
		overflow: hidden;
	}
	.btn-fade-circle {
		position: absolute;
		border-radius: 50%;
		pointer-events: none;
		background-color: rgba(255, 255, 255, .25);
		width: 1px;
		height: 1px;
		z-index: 3;
		animation-name: ripple;
		animation-duration: .3s;
		animation-timing-function: cubic-bezier(.4,0,.6,1);
	}
	@keyframes ripple {
		0% {
			transform: scale(0, 0);
			opacity: 0;
		}
		85% {
			transform: scale(400, 400);
			opacity: .75;
		}
		100% {
			transform: scale(750, 750);
			opacity: 1;
		}
	}

	.custome-designe-btn:before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		width: 0;
		height: 0;
		background-color: ghostwhite;
		opacity: .3;
		-webkit-transition: all 500ms;
		-moz-transition: all 500ms;
		-ms-transition: all 500ms;
		-o-transition: all 500ms;
		transition: all 500ms;
		z-index: 1;
	}
	.custome-designe-btn:focus .custome-designe-btn:before{
		width: 100%;
		height: 100%;
	}
</style>
