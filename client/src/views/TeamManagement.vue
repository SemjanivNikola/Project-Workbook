<template>
	<div id="team-management" class="position-relative">
    <div class="row row-header">
      <div class="col-md-8 d-flex flex-row justify-content-between">
        <h4>OVO SU Timovi</h4>
        <button @click="toggleViewState">{{viewState.btn}}</button>
      </div>
    </div>
		<div class="row">
			<div class="col-md-12">
				<div class="column-inner">
          <div v-if="toggleView" class="wrapper">
            <div v-if="teams.length === 0">
              <h1>Trenutno nema tinova. Dodajte novi</h1>
              <button @click="toggleView = false">Dodaj novi tim</button>
            </div>
            <table v-else ref="team-table" class="p-table">
              <thead>
              <tr class="table-header">
                <th colspan="2">Team</th>
                <th>Members</th>
                <th>Active Project</th>
                <th></th>
              </tr>
              </thead>
              <tbody>
              <tr v-for="t in teams" :key="t.id" class="table-item" @click="setTeamDetails(t)">
                <td class="table-item-icon"><img src="../assets/static/team_icon.png" alt="Team icon"></td>
                <td>
                  <b>{{t.name}}</b>
                  <i>{{t.leader}}</i>
                </td>
                <td>{{t.membersNum}}</td>
                <td>{{t.activeProject}}</td>
                <td>Options</td>
              </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="wrapper">
            <div class="p-3 section-wrapper">
              <div class="section-header">
                <h5 class="m-0">General information</h5>
              </div>
              <div class="section-form">
                <p class="text-justify">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin erat nunc, viverra sed nibh nec, mattis porta metus. Aenean luctus aliquam nisi, eget vulputate dolor congue in. Aliquam interdum purus efficitur elementum porttitor. Sed sed nisi ac velit volutpat lobortis. Morbi est justo, blandit eu justo ut, laoreet dapibus nisl.</p>
                <form class="two-col-form text-left pl-4 pr-4">
                  <label class="input-label text-left" for="title">
                    Team name
                    <input id="title" type="text" v-model="newTeam.name" v-on:input="checkForm">
                  </label>
                  <label class="select-label text-left" for="tl">
                    Select a team leader
                    <select id="tl" type="text" v-model="newTeam.leaderId" v-on:input="checkForm">
                      <option v-for="m in freeMembers" :key="m.id" :value="m.id">{{m.name}}</option>
                    </select>
                  </label>
                  <label class="select-label text-left" for="team">
                    Select a member to team
                    <select id="team" type="text" v-model="tempMember">
                      <option v-for="m in freeMembers" :key="m.id" :value="m">{{m.name}}</option>
                    </select>
                  </label>
                  <button @click="pushMemberToTeam"><b>+</b></button>
                </form>
                <div class="col-sm-12" style="vertical-align: top;">
                  <div class="column-inner">
                    <div class="wrapper">
                      <b>Stage Goals</b>
                      <ol v-if="newTeam.members.length > 0" class="text-left overflow-auto" style="padding-left: 2rem;">
                        <li v-for="m in newTeam.members" :key="m.id" style="width: 20%; float: left;">{{m.name}}</li>
                      </ol>
                      <div v-else class="">
                        <p>Team currently has no members</p>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-sm-12">
                  <div class="column-inner">
                    <div class="wrapper text-center">
                      <button v-if="formReady" ref="saveBtn" @click="saveTeam">Save</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
		</div>
    <transition name="slideInRight" mode="out-in">
      <div v-if="toggleDetailView" class="bg-white position-absolute side-detail-panel overflow-hidden">
        <div class="column-inner side-panel-inner">
          <div class="wrapper">
            <div class="side-panel-header p-2">
              <div class="col-md-4 col-display">
                <img src="../assets/static/team_icon.png" alt="team icon">
              </div>
              <div class="col-md-8 text-left col-display">
                <h3>{{teamDetails.name}}</h3>
              </div>
              <div class="col-md-12">
                <ul>
                  <li>Transfer</li>
                  <li>Add</li>
                  <li>Remove</li>
                </ul>
              </div>
            </div>
            <div class="side-panel-body">
              <div>
                <table class="p-table">
                  <thead>
                  <tr class="table-header">
                    <th colspan="2">Name</th>
                    <th>Options</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="m in teamDetails.members" :key="m.id" class="table-item">
                    <td>Img</td>
                    <td>{{m.name}}</td>
                    <td>X</td>
                  </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
	</div>
</template>

<script>
	export default {
		name: "TeamManagement",
    data () {
			return {
				teams: [],
        freeMembers: [],
        teamDetails: {},
        toggleDetailView: false,
        // Pregledavanje timovi ili dodavanje novog
        toggleView: true,
        viewState: {
				  btn: 'Add new'
        },
        newTeam: {
				  name: '',
          leaderId: '',
          activeProject: 'None',
          members: []
        },
        tempMember: {},
        formReady: false
			}
    },
    watch: {
		  tempMember (state) {
		    if (this.newTeam.leaderId === state.id) {
          console.log('ovo tako ne moze!');
        }
      }
    },
		created () {
			//this.teams = this.$store.getters.getTeams;
      //this.members = this.$store.getters.getMembers;
      this.requestTeams();
		},
		methods: {
		  async requestTeams () {
		    await axios.get('/team/' + 'all')
        .then((r) => {
          if (r.data.teams === 'none') {
            this.freeMembers = r.data.members;
            this.$store.commit('setMembers', this.freeMembers);
          } else {
            this.teams = r.data.teams;
            this.members = r.data.members;
            this.$store.commit('setTeams', this.teams);
            this.$store.commit('setMembers', this.members);
          }
        })
        .catch((error) => {
          console.log('Error => ', error);
        })
      },
		  checkForm () {
		    this.formReady = this.newTeam.name !== '' && this.newTeam.leaderId !== '' && this.newTeam.members.length > 0;
      },
      setTeamDetails (team) {
		    this.teamDetails = team;
		    this.toggleDetailView = !this.toggleDetailView;
      },
      toggleViewState () {
        this.toggleView = !this.toggleView;
        if (this.toggleView)  this.viewState.btn = 'Add new';
        else  this.viewState.btn = 'Cancel';
      },
      pushMemberToTeam () {
		    event.preventDefault();
        this.newTeam.members.push(this.tempMember);
        this.checkForm();
      },
      saveTeam () {
        let team = {
          name: this.newTeam.name,
          leaderId: this.newTeam.leaderId,
          activeProject: this.newTeam.activeProject,
          members: []
        }
        this.newTeam.members.forEach(function (value) {
          team.members.push(value.id);
        });
        axios.post('/team/' + 'new', team)
          .then((res) => {
            console.log('r: ', res);
          })
          .catch((error) => {
            console.log('Error: => ', error);
          })
      }
    }
	}
</script>

<style scoped>
 tbody tr td b, tbody tr td i {
   display: block;
   text-align: left;
 }
 .table-item-icon {
   padding: 15px 0;
 }
 .table-item-icon img {
   height: 80px;
 }

</style>
