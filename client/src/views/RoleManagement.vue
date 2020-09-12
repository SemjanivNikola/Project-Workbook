<template>
	<div id="role-management">
		<div class="row row-header">
			<div class="col-md-8 d-flex flex-row justify-content-between">
				<label for="search">
					<input id="search" v-model="search">
				</label>
				<button @click="toggleViewState">{{viewState.btn}}</button>
			</div>
		</div>
		<div class="row">
			<div class="col-md-12" style="overflow-y: scroll; height: 780px;">
				<table v-if="toggleView" class="p-table">
					<thead>
            <tr class="table-header">
              <th class="text-left pl-5" rowspan="2">Name</th>
              <th class="text-left"  rowspan="2">Role</th>
              <th colspan="6">Permissions</th>
            </tr>
            <tr class="table-header">
              <th>RM</th>
              <th>TM</th>
              <th>PM</th>
              <th>PMSO</th>
              <th>PO(A)</th>
            </tr>
          </thead>
					<tbody>
            <tr v-for="member in members" :key="member.id" class="table-item">
              <td class="text-left pl-5">{{member.name}}</td>
              <td class="text-left">{{member.role}}</td>
              <td><b-form-checkbox v-model="member.permissions.rm" name="check-button" switch size="lg"></b-form-checkbox></td>
              <td><b-form-checkbox v-model="member.permissions.tm" name="check-button" switch size="lg"></b-form-checkbox></td>
              <td><b-form-checkbox v-model="member.permissions.pm" name="check-button" switch size="lg"></b-form-checkbox></td>
              <td><b-form-checkbox v-model="member.permissions.pmso" name="check-button" switch size="lg"></b-form-checkbox></td>
              <td><b-form-checkbox v-model="member.permissions.poa" name="check-button" switch size="lg"></b-form-checkbox></td>
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
                <div class="col-sm-3 col-display" style="vertical-align: top;">
                  <div class="column-inner">
                    <div class="wrapper">
                      <div class="profile-img-drop p-1">
                        <div class="inner-drop-wrapper p-2 d-flex flex-column align-items-center justify-content-center">
                          <p>Drop Image here or Click Button to Choose</p>
                          <button>Drop</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-sm-9 col-display" style="vertical-align: top;">
                  <div class="column-inner">
                    <div class="wrapper">
                      <form class="two-col-form text-left">
                        <label class="w-45 text-left mr-5" for="fn">
                          First Name
                          <input id="fn" type="text" v-model="newMember.firstName">
                        </label>
                        <label class="text-left" for="userCode">
                          User Code
                          <input id="userCode" type="text" v-model="newMember.userCode">
                        </label>
                        <label class="w-45 mr-5 text-left" for="ln">
                          Last Name
                          <input id="ln" type="text" v-model="newMember.lastName">
                        </label>
                        <label class="w-3 text-left" for="pass">
                          Password
                          <input id="pass" type="password" v-model="newMember.pass">
                        </label>
                        <label class="w-75 block text-left" for="email">
                          Email
                          <input id="email" type="email" v-model="newMember.email">
                        </label>
                        <label class="w-3 mr-5 text-left" for="tel">
                          Phone
                          <input id="tel" type="tel" v-model="newMember.tel">
                        </label>
                        <label class="w-3 text-left" for="role">
                          Role
                          <input id="role" type="text" v-model="newMember.role">
                        </label>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="p-3 section-wrapper">
              <div class="section-header">
                <h5 class="m-0">Permissions</h5>
              </div>
              <div class="section-form">
                <table>
                  <thead>
                  <tr style="border-bottom: 1px solid rgb(196, 196, 196);">
                    <th>OVERVIEW & MANAGEMENT</th>
                  </tr>
                    <tr>
                      <th>Role</th>
                      <th>Team Management</th>
                      <th>Project Management</th>
                      <th>Project Overview(A)</th>
                      <th>Project Management Self Only</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td><b-form-checkbox v-model="newMember.permissions.rm" name="check-button" switch size="lg"></b-form-checkbox></td>
                      <td><b-form-checkbox v-model="newMember.permissions.tm" name="check-button" switch size="lg"></b-form-checkbox></td>
                      <td><b-form-checkbox v-model="newMember.permissions.pm" name="check-button" switch size="lg"></b-form-checkbox></td>
                      <td><b-form-checkbox v-model="newMember.permissions.poa" name="check-button" switch size="lg"></b-form-checkbox></td>
                      <td><b-form-checkbox v-model="newMember.permissions.pmso" name="check-button" switch size="lg"></b-form-checkbox></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="col-sm-12">
              <div class="column-inner">
                <div class="wrapper text-center">
                  <button @click="saveMember">Save</button>
                </div>
              </div>
            </div>
          </div>
        </div>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		name: "RoleManagement",
		data () {
			return {
				search: '',
				members: [],
        toggleView: true,
        viewState: {
				  btn: 'Add new'
        },
        newMember: {
				  img: '',
          firstName: '',
          lastName: '',
          userCode: '',
          email: '',
          tel: '',
          pass: '',
          role: '',
          permissions: {
				    rm: false,
            tm: false,
            pm: false,
            pmso: false,
            poa: false,
          }
        }
			}
		},
		created () {
			//this.members = this.$store.getters.getMembers;
			this.requestMembers();
		},
    methods: {
		  async requestMembers () {
		    await axios.get('/member/' + 'all')
        .then((r) => {
          console.log('r: ', r);
          this.members = r.data.members;
          this.members.forEach(function (m) {
            m.permissions.rm = this.checkPermissions(m.permissions.rm);
            m.permissions.tm = this.checkPermissions(m.permissions.tm);
            m.permissions.pm = this.checkPermissions(m.permissions.pm);
            m.permissions.pmso = this.checkPermissions(m.permissions.pmso);
            m.permissions.poa = this.checkPermissions(m.permissions.poa);
          }, this);
        })
        .catch((error) => {
          console.log('Error => ', error);
        })
      },
      checkPermissions (value) {
        return value === 1;
      },
		  saveMember () {
		    let newMember = {
		      firstName: this.newMember.firstName,
          lastName: this.newMember.lastName,
          userCode: this.newMember.userCode,
          pass: this.newMember.pass,
          email: this.newMember.email,
          tel: this.newMember.tel,
          role: this.newMember.role,
          memberPermissions: [this.newMember.permissions.rm, this.newMember.permissions.tm, this.newMember.permissions.pm, this.newMember.permissions.pmso, this.newMember.permissions.poa]
        }
		    axios.post('/member/' + 'new', newMember)
        .then((res) => {
          console.log('resppnse: ', res.data.member);
          let m = {
            id: res.data.member,
            name: newMember.firstName + ' ' + newMember.lastName,
            email: newMember.email,
            tel: newMember.tel,
            role: newMember.role,
            permissions: {
              rm: newMember.memberPermissions[0],
              tm: newMember.memberPermissions[1],
              pm: newMember.memberPermissions[2],
              pmso: newMember.memberPermissions[3],
              poa: newMember.memberPermissions[4],
            }
          }
          this.members.push(m);
          this.resetForm();
        })
        .catch((error) => {
          console.log('Error occured. => ', error);
        })
      },
		  toggleViewState () {
		    this.toggleView = !this.toggleView;
		    if (this.toggleView)  this.viewState.btn = 'Add new';
		    else  this.viewState.btn = 'Cancel';
      },
      resetForm () {
		    this.newMember = {
          img: '',
          firstName: '',
          lastName: '',
          userCode: '',
          email: '',
          tel: '',
          pass: '',
          role: '',
          permissions: {
            rm: false,
            tam: false,
            pam: false,
            pmso: false,
            par: false,
          }
        }
      }
    }
	}
</script>

<style scoped>
	#role-management {
		width: 100%;
		height: auto;
	}
  .two-col-form .block {
    display: block;
  }
  .two-col-form .w-3 {
    width: 30%;
  }
  .two-col-form .w-45 {
    width: 45%;
  }
  .two-col-form .w-75 {
    width: 75%;
  }

</style>
