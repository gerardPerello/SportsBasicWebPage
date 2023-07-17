<template>
  <div class="container py-5 h-100">
    <div class="container">
      <header class="d-flex flex-wrap justify-content-between py-3 mb-4 border-bottom">
        <h1 class="fs-4 mb-3 mb-md-0 me-md-auto"> Sport Matches </h1>
      </header>
    </div>
    <div class="row d-flex justify-content-center align-items-center h-100">
      <div class="col-12 col-md-8 col-lg-6 col-xl-5">
        <div class="card shadow-2-strong" style="border-radius: 1rem;">
          <div v-if="login" class="card-body p-5 text-center">

            <h3 class="mb-5">Sign in</h3>

            <div class="form-label-group">
              <label for="inputEmail">Username</label>
              <input type="username" id="inputUsername" class="form-control"
              placeholder="Username" required autofocus v-model="username">
            </div>
            <div class="form-label-group">
              <br>
              <label for="inputPassword">Password</label>
              <input type="password" id="inputPassword" class="form-control"
              placeholder="Password" required v-model="password">
              <br>
            </div>

            <button class="btn btn-primary btn-lg btn-block"
                    @click="checkLogin()">Sign in</button>
            <button class="btn btn-lg btn-block btn-success"
              @click="switchLogin()"> Create account</button>
            <button class="btn btn-lg btn-block btn-secondary mb-2"
              @click="$router.push('/')">Back to matches</button>

          </div>
          <div v-else class="card-body p-5 text-center">

            <h3 class="mb-5">Create Account</h3>

            <b-form>
              <b-form-group id="input-group-1"
               label="Username"
               descriptions="Put your starred username">

                <b-form-input
                  id="usernameInput"
                  v-model="addUserForm.username"
                  placeholder="Enter username"
                  required
                >

                </b-form-input>
              </b-form-group>

              <b-form-group id="input-group-2"
               label="Password"
               descriptions="We won't share your password.">

                <b-form-input
                  id="passwordInput"
                  v-model="addUserForm.password"
                  type="password"
                  placeholder="Enter password"
                  required
                >
                </b-form-input>
              </b-form-group>
            </b-form>
            <button class="btn btn-primary btn-lg btn-block"
                    @click="checkAddAccount()">Submit</button>
            <button class="btn btn-lg btn-block btn-secondary mb-2"
              @click="switchLogin()"> Back to log in</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios'

export default {
  data () {
    return {
      logged: false,
      username: null,
      password: null,
      token: null,
      login: true,
      addUserForm: {
        username: null,
        password: null
      }
    }
  },
  methods: {
    checkLogin () {
      const parameters = {
        username: this.username,
        password: this.password
      }
      const path = 'https://a12-sportsmaster1.herokuapp.com/login'
      axios.post(path, parameters)
        .then((res) => {
          this.logged = true
          this.token = res.data.token
          this.$router.push({ path: '/', query: { username: this.username, logged: this.logged, token: this.token } })
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          alert('Username or Password incorrect')
        })
    },
    checkAddAccount () {
      const path = 'https://a12-sportsmaster1.herokuapp.com/account'
      const parameters = {
        username: this.addUserForm.username,
        password: this.addUserForm.password,
        is_admin: false
      }
      axios.post(path, parameters)
        .then((res) => {
          this.username = parameters.username
          this.password = parameters.password
          this.checkLogin()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error)
          alert('This username is already in use')
        })
    },
    switchLogin () {
      this.login = !this.login
      if (this.login === false) {
        this.initCreateForm()
      }
    },
    initCreateForm () {
      this.addUserForm.username = null
      this.addUserForm.password = null
    }
  },
  created () {
    this.logged = this.$route.query.logged === 'true'
    this.username = this.$route.query.username
    this.token = this.$route.query.token
    if (this.logged === undefined) {
      this.logged = false
    }
  }
}
</script>
