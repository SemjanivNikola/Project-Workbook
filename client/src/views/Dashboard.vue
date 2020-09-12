<template>
	<div id="dashboard" class="d-flex flex-row">
		<Navigation :nav-for-role="nav"></Navigation>
		<div class="main-view">
			<div class="info-nav-bar">
				<div class="d-flex flex-row align-items-center">
					<h4>{{myInfo.role}} Account</h4>
				</div>
				<div class="d-flex flex-row-reverse align-items-center">
          <div class="avatar-wrapper-m">
            <img :src="profileImg(myInfo.img)" alt="User avatar">
          </div>
					<p>Notifications</p>
				</div>
			</div>
			<router-view></router-view>
		</div>
	</div>
</template>

<script>
	import Navigation from '../components/Navigation'
	export default {
		name: "Dashboard",
    data () {
		  return {
		    myInfo: this.$store.getters.getMyInfo,
        nav: 'r-998'
      }
    },
    created () {
		  console.log('hello => ', this.myInfo);
		  this.setNavigationRestriction();
    },
    methods: {
		  setNavigationRestriction () {
		    if (this.myInfo.permissions.rm && this.myInfo.permissions.poa && this.myInfo.permissions.pmso)  this.nav = 'ur-996';
		    else if (this.myInfo.permissions.rm && this.myInfo.permissions.poa && !this.myInfo.permissions.pmso)  this.nav = 'r-992';
        else if (!this.myInfo.permissions.rm && !this.myInfo.permissions.poa && this.myInfo.permissions.pmso) {
          this.nav = 'r-990';
          this.requestTeamInfo();
        }
		    else {
          this.nav = 'r-998';
          this.requestProjectId();
        }
      },
      async requestTeamInfo () {
		    await axios.get('/team/management/leader/' + this.myInfo.id)
        .then((r) => {
          this.$store.commit('setTeams', r.data.team);
        })
        .catch((error) => {
          console.log('Ops, something went wrong. Error => ', error);
        })
      },
      async requestProjectId () {
        await axios.get('/team/management/project/' + this.myInfo.id)
          .then((r) => {
            this.$store.commit('setActiveProjectForMember', r.data.project);
          })
          .catch((error) => {
            console.log('Ops, something went wrong. Error => ', error);
          })
      },
      profileImg (img) {
        return require(`../assets/photos/${img}`);
      }
    },
    components: {
			Navigation
		}
	}
</script>

<style>
.avatar-wrapper-m {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  overflow: hidden;
}
.avatar-wrapper-m img {
  width: 100%;
}
/************************************************************/
                        /*  SCOPED  */
/************************************************************/
	#dashboard {
		height: inherit;
		width: inherit;
	}
	.main-view {
		width: 100%;
		height: inherit;
		background-color: #eff3f6;
	}
	.info-nav-bar {
		width: 100%;
		height: 60px;
		padding: 13px 30px;
		background: transparent;
	}
	.main-view .info-nav-bar .d-flex {
		width: 50%;
		float: left;
		height: 34px;
	}
	.main-view .info-nav-bar .d-flex p {
		margin: 0;
	}
/************************************************************/
                /*  GENERAL ELEMENTS  */
/************************************************************/
/******************SMALL-ELEMENTS****************************/
.col-display {
  display: inline-block;
}
.white-color {
  color: #ffffff;
}

/******************MAIN-VIEW-ELEMENTS****************************/
#project, #team-management {
  width: 100%;
  height: auto;
}

/******************ROW****************************/
.row-header {
  padding: 30px 40px;
  border-bottom: 2px solid #e6eaee;
  justify-content: flex-end;
}

/******************TABLE-ELEMENTS****************************/
.p-table {
  display: table;
  width: 100%;
  max-width: 100%;
  margin: 20px 0;
  border: 1px solid #e6eaee;
  border-radius: 4px;
  background-color: #fff;
  border-collapse: collapse;
}
.table-nav {
  position: relative;
  padding: 25px 30px;
  border: 1px solid #e6eaee;
  border-bottom: 0;
  border-radius: 4px 4px 0 0;
  background-color: #fff;
  color: #354052;
  font-size: 24px;
  text-align: left;
  caption-side: top;
}
.table-nav small {
  display: inline-block;
  margin-left: 10px;
  color: #7f8fa4;
  font-size: 14px;
}
.table-nav small:before {
  content: "";
  display: inline-block;
  position: relative;
  bottom: -2px;
  width: 1px;
  height: 14px;
  margin-right: 12px;
  background-color: #dfe3e9;
}
.table-header, .section-header {
  height: 40px;
  background-color: #eff3f6;
  border-top: 1px solid #e6eaee;
}
.table-header th, .section-header h5 {
  font-size: 15px;
  letter-spacing: 1px;
  text-transform: capitalize;
  font-weight: 300;
  color: #7f8fa4;
}
.table-item, .section-form {
  height: 90px;
  border-top: 1px solid #e6eaee;
  border-bottom: 1px solid #e6eaee;
  border-left: 3px solid transparent;
  background-color: #ffffff;
  color: #7f8fa4;
  -webkit-transition: all 500ms;
  -moz-transition: all 500ms;
  -ms-transition: all 500ms;
  -o-transition: all 500ms;
  transition: all 500ms;
}
.table-item:hover {
  border-left-color: #ed1c24;
}
.table-link {
  position: absolute;
  top: 30px;
  right: 30px;
  color: #7f8fa4;
  font-size: 12px;
}

/******************SIDE-DETAIL-PANEL****************************/
.side-detail-panel {
  right: 0;
  top: 0;
  width: 532px;
  height: auto;
  border: 1px solid #e6eaee;
  border-radius: 10px 0 0 0;
  box-shadow: 0 1px 10px 2px #e6eaee;
  padding: 1.5rem;
}
.side-panel-inner {
  width: 100%;
  min-width: 485px;
}
.side-panel-header {
  border-bottom: 1px solid #e6eaee;
}
.side-panel-header ul {
  margin-top: 1rem;
  width: 100%;
  text-align: center;
  padding: .25rem;
  list-style-type: none;
}
.side-panel-header ul li {
  width: 125px;
  padding: 5px 15px;
  margin-right: 15px;
  color: #ffffff;
  background-color: #7f8fa4;
  border-radius: 5px;
  text-transform: uppercase;
  font-size: 16px;
  transition: 500ms ease-out;
  display: inline-block;
  cursor: pointer;
}
.side-panel-header ul li:last-child {
  margin-right: 0;
}
.side-panel-header ul li:first-child:hover {
  color: #b7c0cd;
  background-color: #4f5678;
}
.side-panel-header ul li:nth-child(2):hover {
  color: #b7c0cd;
  background-color: greenyellow;
}
.side-panel-header ul li:nth-child(3):hover {
  color: #b7c0cd;
  background-color: #d3412a;
}
.side-panel-body {
  overflow-y: scroll;
  height: 540px;
}

/******************FORM-SECTION****************************/
.section-wrapper {

}
.section-header {
  padding: 12px 0 12px 50px;
  text-align: left;
  background-color: #ffffff;
}
.section-wrapper .section-form {
  height: auto;
  padding: 15px 0;
  background-color: #eff3f6;
  border-bottom: none;
}
.two-col-form input, .two-col-form textarea, .two-col-form select {
  display: block;
  width: 100%;
}
.two-col-form input, .two-col-form select {
  height: 32px;
  font-size: 14px;
}
input, textarea, select {
  color: #383535;
}
.input-label, .select-label {
  width: 27.33%;
  margin-right: 25px;
  margin-bottom: 25px;
  vertical-align: middle;
}
.ta-label {
  width: 100%;
  margin-right: 25px;
  margin-bottom: 25px;
}
input:disabled {
  color: rgb(154, 154, 154);
}
.section-wrapper .section-form table {
  width: 100%;
}
.section-wrapper .section-form table thead tr th {
  padding: 10px 0;
}
.section-wrapper .section-form table tbody tr {
  height: 80px;
  border-top: 1px solid #e6eaee;
  color: #7f8fa4;
}
.section-wrapper:last-child {
  margin-bottom: 220px;
}
.profile-img-drop {
  height: 270px;
  background-color: #f7f7f7;
  border: 2px solid #a9a9a9;
  border-radius: 5px;
}
.inner-drop-wrapper {
  height: 100%;
  width: 100%;
  background: transparent;
  color: #a9a9a9;
  border: 1px dashed #a9a9a9;
  border-radius: 5px;
}

/************************************************************/
                    /*  ANIMATIONS  */
/************************************************************/
.slideInRight-enter-active, .slideInRight-leave-active {
  transition: all 500ms ease-out;
}
.slideInRight-enter, .slideInRight-leave-to {
  width: 1px;
  padding: 0;
}
.slideInRight-enter-to, .slideInRight-leave {
  width: 532px;
  padding: 1.5rem;
}
.fadeIn-enter-active, .fadeIn-leave-active, .slideInLeft-enter-active, .slideInLeft-leave-active  {
  transition: all 300ms ease-out;
}
.fadeIn-enter, .fadeIn-leave-to {
  opacity: 0;
  transform: translateY(-80px);
}
.fadeIn-enter-to, .fadeIn-leave {
  opacity: 1;
  transform: translateY(0);
}
.slideInLeft-enter, .slideInLeft-leave-to {
  opacity: .5;
  transform: translateX(-90px);
}
.slideInLeft-enter-to, .slideInLeft-leave {
  opacity: 1;
  transform: translateX(0);
}

</style>
