<template>
	<div class="d-table">
		<div class="d-table-cell" style="width: 62%;">
			<div class="bg-img-01"></div>
		</div>
		<div class="d-table-cell" style="vertical-align: top; background-color: rgba(28, 30, 42, 1); border-left-color: #d3412a; border-left-style: solid; border-left-width: 1px;">
			<div class="d-flex flex-row align-items-center" style="height: inherit;">
				<div class="form-group">
					<h3>Sign In</h3>
					<label for="user-code">
						<input id="user-code" v-model="form.userCode" type="text" placeholder="User code">
					</label>
					<label for="password">
						<input id="password" v-model="form.pass" type="password" placeholder="Password">
					</label>
					<button @click="signIn" class="custome-designe-btn" v-rippleeffect>Sign In</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		name: 'SignIn',
		data () {
			return {
				form: {
					userCode: '',
					pass: ''
				}
			}
		},
    methods: {
		  async signIn () {
		    await axios.post('signup', this.form)
        .then((r) => {
          let u = r.data.user;
          let member = {
            id: u[0],
            name: u[1] + ' ' + u[2],
            role: u[5],
            img: 'profile_img.jpg',
            email: u[3],
            tel: u[4],
            permissions: r.data.permissions
          }
          this.$store.commit('setMyInfo', member);
          this.$emit('authenticated', true);
        })
        .catch((error) => {
          console.log('Something went wrong. Error => ', error);
        })
      }
    }
	}
</script>

<style>
	.form-group {
		width: 50%;
		padding: 15px 0;
		box-shadow: 1px 1px 15px 3px #2c3e50;
		border-radius: 10px;
		border: 1px solid #2c3e50;
		margin: 0 auto;
		background-color: #fff;
	}
	.form-group h3 {
		width: 100%;
		text-align: center;
		margin-bottom: 25px;
	}
	.form-group label {
		width: 100%;
		padding: 5px 0;
		display: inline-block;
		margin-bottom: 5px;
	}
	.form-group label input {
		width: 55%;
	}
</style>
