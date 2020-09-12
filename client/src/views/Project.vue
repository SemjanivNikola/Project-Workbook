<template>
	<div id="project">
		<div class="row row-header">
			<div class="col-md-8 d-flex flex-row justify-content-between">
				<h4>OVO SU PROJEKTI</h4>
        <button @click="toggleViewState">{{viewState.btn}}</button>
			</div>
		</div>
		<div class="row">
			<div class="col-md-12" style="height: 780px; overflow-y: scroll;">
				<table v-if="toggleView" class="p-table">
					<caption class="table-nav">
						Ongoing Projects
						<small>{{projects.length}} Projects</small>
						<a class="table-link" href="#">Completed Projects</a>
					</caption>
					<thead>
						<tr class="table-header">
							<th class="pl-5 text-left">Project</th>
							<th class="text-left">Deadline</th>
							<th class="text-left">Leader + Team</th>
							<th class="text-left">Budget</th>
							<th class="text-left">Status</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="p in projects" :key="p.id" class="table-item" @click="setProjectDetailsActive(p)">
							<td class="pl-5 text-left"><b>{{p.title}}</b><small>{{p.client}}</small></td>
							<td class="text-left">{{p.deadLine}}</td>
							<td class="text-left">
                <div class="avatar-wrapper">
                  <img class="rounded-circle" :src="profileImg(p.team.leader.profileImg)" alt="Avatar icon">
                </div>
                <div class="info-wrapper">
                  <b>{{p.team.leader.name}}</b>
                  <small>{{p.team.name}}</small>
                </div>
              </td>
							<td class="text-left">{{p.budget}}<small>{{p.budgetStatus}}</small></td>
							<td class="text-left">
                <svg height="22" width="22">
                  <circle cx="11" cy="11" r="7" stroke="pink" stroke-width="3" fill="none"/>
                  Sorry, your browser does not support inline SVG.
                </svg>
                {{p.jobType}}
              </td>
						</tr>
					</tbody>
				</table>
        <div v-else class="column-inner">
          <div class="wrapper">
            <div class="p-3 section-wrapper">
              <div class="section-header">
                <h5 class="m-0">General information</h5>
              </div>
              <div class="section-form">
                <p class="text-justify">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin erat nunc, viverra sed nibh nec, mattis porta metus. Aenean luctus aliquam nisi, eget vulputate dolor congue in. Aliquam interdum purus efficitur elementum porttitor. Sed sed nisi ac velit volutpat lobortis. Morbi est justo, blandit eu justo ut, laoreet dapibus nisl.</p>
                <form class="two-col-form text-left pl-4 pr-4">
                  <label class="input-label text-left" for="title">
                    Title
                    <input id="title" type="text" v-model="newProject.title">
                  </label>
                  <label class="select-label text-left" for="team">
                    Team
                    <select id="team" type="text" v-model="newProject.team">
                      <option v-for="t in teams" :key="t.id" :value="t.id">{{t.name}}</option>
                    </select>
                  </label>
                  <label class="input-label text-left" for="client">
                    Client
                    <input id="client" type="text" v-model="newProject.client">
                  </label>
                  <label class="ta-label text-left" for="description">
                    Description
                    <textarea id="description" rows="3" cols="80" v-model="newProject.description"></textarea>
                  </label>
                  <label class="input-label text-left" for="status">
                    Status
                    <input id="status" type="text" v-model="newProject.status" disabled>
                  </label>
                  <label class="input-label text-left" for="cs">
                    Current Stage
                    <input id="cs" type="text" v-model="newProject.currStage" disabled>
                  </label>
                  <label class="ta-label text-left" for="cd">
                    Customer Details
                    <textarea id="cd" rows="3" cols="80" v-model="newProject.customerDetails"></textarea>
                  </label>
                  <label class="input-label text-left" for="budget">
                    Budget
                    <input id="budget" type="number" v-model="newProject.budget">
                  </label>
                  <label class="select-label text-left" for="jy">
                    Job Type
                    <select id="jy" type="text" v-model="newProject.jobType">
                      <option value="prototip">Prototip</option>
                    </select>
                  </label>
                  <label class="input-label text-left" for="dl">
                    Deadline
                    <input id="dl" type="date" v-model="newProject.deadline">
                  </label>
                </form>
              </div>
            </div>
            <div class="p-3 section-wrapper">
              <div class="section-header">
                <h5 class="m-0">Stages</h5>
              </div>
              <div class="section-form">
                <p class="text-justify">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin erat nunc, viverra sed nibh nec, mattis porta metus. Aenean luctus aliquam nisi, eget vulputate dolor congue in. Aliquam interdum purus efficitur elementum porttitor. Sed sed nisi ac velit volutpat lobortis. Morbi est justo, blandit eu justo ut, laoreet dapibus nisl.</p>
                <b-card no-body>
                  <b-tabs card>
                    <!-- Render Tabs, supply a unique `key` to each tab -->
                    <b-tab v-for="s in tabs" :key="'dyn-tab-' + s" :title="'Stage ' + s">
                      <form class="two-col-form text-left" @submit="saveNewGoal(newProject.stages[s - 1].goals)">
                        <label class="input-label text-left" :for="'s-order-'+s">
                          Stage
                          <input :id="'s-order-'+s" type="text" v-model="newProject.stages[s - 1].order" disabled>
                        </label>
                        <label class="input-label text-left" :for="'s-title-'+s">
                          Title
                          <input :id="'s-title-'+s" type="text" v-model="newProject.stages[s - 1].title">
                        </label>
                        <label class="input-label text-left" :for="'s-status-'+s">
                          Status
                          <input :id="'s-status-'+s" type="text" v-model="newProject.stages[s - 1].status">
                        </label>
                        <label class="ta-label text-left" :for="'s-description-'+s">
                          Description
                          <textarea :id="'s-description-'+s" rows="3" cols="80" v-model="newProject.stages[s - 1].description"></textarea>
                        </label>
                        <label class="input-label text-left" :for="'s-tc-'+s">
                          Time Created
                          <input :id="'s-tc-'+s" type="text" v-model="newProject.stages[s - 1].timeCreated" disabled>
                        </label>
                        <label class="input-label text-left" :for="'s-efd-'+s">
                          Expected Finish Date
                          <input :id="'s-efd-'+s" type="date" v-model="newProject.stages[s - 1].expectedFinishDate">
                        </label>
                        <label class="input-label text-left" for="g-title" style="width: 45%;">
                          Add important goals
                          <input id="g-title" type="text" v-model="gdesc">
                        </label>
                        <button><b>+</b></button>
                      </form>
                      <div class="col-sm-12" style="vertical-align: top;">
                        <div class="column-inner">
                          <div class="wrapper">
                            <b>Stage Goals</b>
                            <ol v-if="newProject.stages[s - 1].goals.length > 0" class="text-left overflow-auto" style="padding-left: 2rem;">
                              <li v-for="(i, index) in newProject.stages[s - 1].goals" :key="index" style="width: 20%; float: left;">{{i}}</li>
                            </ol>
                            <div v-else class="">
                              <p>No goals at the moment</p>
                            </div>
                          </div>
                        </div>
                      </div>
                      <b-button size="sm" variant="danger" class="float-right" @click="closeTab(s)">
                        Close stage
                      </b-button>
                    </b-tab>
      
                    <!-- New Tab Button (Using tabs-end slot) -->
                    <template v-slot:tabs-end>
                      <b-nav-item role="presentation" @click.prevent="newTab" href="#"><b>Add new +</b></b-nav-item>
                    </template>
      
                    <!-- Render this if no tabs -->
                    <template v-slot:empty>
                      <div class="text-center text-muted">
                        There are no open stages<br>
                        Make a new stage using the <b>Add new +</b> button above.
                      </div>
                    </template>
                  </b-tabs>
                </b-card>
              </div>
            </div>
            <div class="p-3 section-wrapper">
              <div class="section-header">
                <h5 class="m-0">Goals</h5>
              </div>
              <div class="section-form">
                <p class="text-justify">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin erat nunc, viverra sed nibh nec, mattis porta metus. Aenean luctus aliquam nisi, eget vulputate dolor congue in. Aliquam interdum purus efficitur elementum porttitor. Sed sed nisi ac velit volutpat lobortis. Morbi est justo, blandit eu justo ut, laoreet dapibus nisl.</p>
                <form class="two-col-form" @submit="saveNewGoal">
                  <label class="select-label text-left" for="g-purpose">
                    Purpose
                    <select id="g-purpose" type="text" v-model="gid">
                      <optgroup label="Current Project">
                        <option :value="newProject.tempId">{{newProject.title}}</option>
                      </optgroup>
                      <optgroup label="Stages">
                        <option v-for="s in newProject.stages" :value="s.id" :key="s.id">{{s.title}}</option>
                      </optgroup>
                    </select>
                  </label>
                  <label class="input-label text-left" for="g-gtitle">
                    Description
                    <input id="g-gtitle" type="text" v-model="gdesc">
                  </label>
                  <button><b>+</b></button>
                </form>
                <div class="col-sm-6 col-display" style="vertical-align: top;">
                  <div class="column-inner">
                    <div class="wrapper">
                      <b>Project Goals</b>
                      <ol v-if="newProject.pGoal.length > 0">
                        <li v-for="(i, index) in newProject.pGoal" :key="index">{{i.description}}</li>
                      </ol>
                      <div v-else class="">
                        <p>No goals at the moment</p>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-sm-6 col-display" style="vertical-align: top;">
                  <div class="column-inner">
                    <div class="wrapper">
                      <b>Stage Goals</b>
                      <ol v-if="newProject.sGoal.length > 0">
                        <li v-for="(i, index) in newProject.sGoal" :key="index">{{i.description}}</li>
                      </ol>
                      <div v-else class="">
                        <p>No goals at the moment</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="p-3 text-center">
              <button @click="saveProject">Save</button>
            </div>
          </div>
        </div>
			</div>
		</div>
	</div>
</template>

<script>
import img from '../assets/photos/profile_img.jpg'
	export default {
		name: "Project",
		data () {
			return {
				projects: [],
        teams: [],
        toggleView: true,
        viewState: {
          btn: 'Add new'
        },
        newProject: {
				  tempId: '',
				  team: '',
				  title: '',
          description: '',
          client: '',
          status: 'Early Stages',
          customerDetails: '',
          currStage: 'Analysis',
          budget: '',
          budgetStatus: 'Preparing Invoice',
          jobType: '',
          deadline: '',
          stages: [],
          totalStages: 0,
          pGoal: [],
          sGoal: []
        },
        tabs: [],
        gid: '',
        gdesc: ''
			}
		},
		created () {
			//this.projects = this.$store.getters.getProjects;
			this.teams = this.$store.dispatch('checkTeamsData');
			this.teams = this.$store.getters.getTeams;
			console.log('TEAMS: ', this.teams);
			this.requestProjects();
		},
    methods: {
		  async requestProjects () {
		    await axios.get('/project/' + 'all')
        .then((r) => {
          this.projects = r.data.projects;
        })
        .catch((error) => {
          console.log('Error => ', error)
        })
      },
      saveProject () {
		    let p = {
		      teamId: this.newProject.team,
          title: this.newProject.title,
          client: this.newProject.client,
          description: this.newProject.description,
          customerDetails: this.newProject.customerDetails,
          budget: this.newProject.budget,
          budgetStatus: this.newProject.budgetStatus,
          jobType: this.newProject.jobType,
          deadline: this.newProject.deadline
        }
        axios.post('/project/' + 'new', p)
        .then((r) => {
          p.id = r.data.p;
          this.$store.commit('updateProjects', p);
          this.projects.push(p);
        })
        .catch((error) => {
          console.log('Error => ', error);
        })
      },
      closeTab(x) {
        for (let i = 0; i < this.newProject.stages.length; i++) {
          if (this.newProject.stages[i] === x) {
            this.newProject.stages.splice(i, 1)
          }
        }
      },
      setProjectDetailsActive (project) {
        console.log('Project: ', project);
        //this.$store.commit('setNewProjectDetails', project)
      },
      newTab() {
        this.newProject.totalStages++;
        let s = this.newProject.totalStages;
        this.tabs.push(s);
        this.newProject.stages.push({id: s,title: '', order: 'Stage ' + s, description: '', res: 'not now', status: '', timeCreated: '', expectedFinishDate: '', goals: []})
        console.log('s: ', this.tabs, this.newProject.stages);
      },
      toggleViewState () {
        this.toggleView = !this.toggleView;
        if (this.toggleView)  this.viewState.btn = 'Add new';
        else  this.viewState.btn = 'Cancel';
        this.newProject.tempId = Math.floor(Math.random() * 1000) + 101;
      },
      saveNewGoal (array) {
        event.preventDefault();
        array.push(this.gdesc);
        this.gdesc = '';
        /*
        let t = {
          id: this.gid,
          description: this.gdesc
        };
        this.gid = '';
        this.gdesc = '';
        if (t.id === this.newProject.tempId) {
          this.newProject.pGoal.push(t);
        } else  {
          this.newProject.sGoal.push(t);
        }
         */
      },
      profileImg(img) {
        return require(`@/assets/photos/${img}`);
      }
    }
	}
</script>

<style>
tr td svg {
  margin-right: 25px;
}
tr td b, tr td small {
  display: block;
}
.avatar-wrapper {
  width: 50px;
  height: 50px;
  display: inline-block;
  margin-right: 12px;
}
.avatar-wrapper img {
  width: 100%;
}
.info-wrapper {
  display: inline-block;
  vertical-align: middle;
}

</style>
