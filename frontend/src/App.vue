<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import Matches from '@/components/Matches'
import Login from '@/components/Login'

export default {
  name: 'App',
  components: {
    Login,
    Matches

  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
