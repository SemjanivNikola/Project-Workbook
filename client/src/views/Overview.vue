<template>
	<div id="overview">
		<h1>OVO JE OVERVIEW</h1>
		<div style="height: 80px;"></div>
		<div class="row">
			<div class="col-md-6"></div>
			<div class="col-md-6">
				<div class="o-card">
					<div class="o-card-header">
						<h5 class="o-card-title">Tasks</h5>
						<a class="o-card-link" href="#">View all tasks</a>
					</div>
					<div v-for="task in tasks" :key="task.id" class="o-card-task">
						<label class="o-task-label" :for="task.title + task.id">
							<input :id="task.title + task.id" class="o-task-input" type="checkbox" v-model="task.done">
							{{task.task}}
						</label>
						<span class="o-card-due-date">{{task.dueDate}}</span>
					</div>
				</div>
			</div>
		</div>
		<div class="o-card">
			<div class="o-card-title">

			</div>
			<div class="o-card-body">
				<p>This is o-card body!</p>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		name: "Overview",
		data () {
			return {
				tasks: [],
				ch: true
			}
		},
		created () {
			this.tasks = this.$store.getters.getHighPriorityTask;
		},
		methods: {
			check (event) {
				console.log('e: ', event);
			}
		}
	}
</script>

<style scoped>
	#overview {
		width: 100%;
		height: auto;
	}
	.o-card {
		width: 100%;
		background-color: transparent;
		border: 1px solid #e6eaee;
		-webkit-transition: all 500ms;
		-moz-transition: all 500ms;
		-ms-transition: all 500ms;
		-o-transition: all 500ms;
		transition: all 500ms;
	}
	.o-card-header {
		padding: 25px 30px;
		border-bottom: 1px solid #e6eaee;
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
	}
	.o-card-title {
		font-size: 18px;
		color: #354052;
		font-weight: 500;
		line-height: 27px;
		display: inline-block;
		margin: 0;
	}
	.o-card-link {
		color: #7f8fa4;
		font-size: 12px;
		display: inline-block;
	}
	.o-task-input {
		margin-right: 10px;
	}
	.o-card-task {
		padding: 20px 30px;
		border-top: 1px solid #e6eaee;
		display: flex;
		flex-direction: row;
		align-items: center;
		justify-content: space-between;
	}
	/* NE RADI - NE ZNAM ZASTO
	.o-card .o-card-task:first-child {
		border-top: 0 !important;
	}
	*/
	.o-task-label {
		margin: 0;
	}
	.o-card-due-date-warning {
		color: #ffffff;
		background-color: #ed1c24;
	}
	.o-card-due-date-chill {
		color: #ffffff;
		background-color: #b7c0cd;
	}
	.o-card-body {
		padding: 20px 25px;
	}
	.o-card:hover {
		background-color: #ffffff;
	}

</style>
