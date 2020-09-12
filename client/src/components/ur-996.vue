<template>
  <ul class="main-menu">
    <li class="nav-title">Dashboard</li>
    <li><router-link to="/dashboard/"><span data-hover="Overview">Overview</span></router-link></li>
    <li class="nav-title">Projects</li>
    <li><router-link to="/dashboard/project"><span data-hover="Project Overview">Project Overview</span></router-link></li>
    <li><router-link to="/dashboard/workflow"><span data-hover="My Workflow">My Workflow</span></router-link></li>
    <li class="nav-title">Human Resources</li>
    <li><router-link to="/dashboard/team-management"><span data-hover="Teams">Teams</span></router-link></li>
    <li><router-link to="/dashboard/role-management"><span data-hover="Manage Roles">Manage Roles</span></router-link></li>
  </ul>
</template>

<script>
export default {
name: "ur-996"
}
</script>

<style>

</style>