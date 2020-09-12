<template>
  <ul class="main-menu">
    <li class="nav-title">Dashboard</li>
    <li><router-link to="/dashboard/"><span data-hover="Overview">Overview</span></router-link></li>
    <li class="nav-title">Projects</li>
    <li><router-link to="/dashboard/tasks"><span data-hover="Tasks">Tasks</span></router-link></li>
  </ul>
</template>

<script>
export default {
  name: "r-998"
}
</script>

<style>

</style>