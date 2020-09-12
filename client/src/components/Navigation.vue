<template>
  <div id="nav" class="position-relative">
    <h4>IME APLIKACIJE</h4>
    <div style="height: 100px;"></div>
    <div class="nav-item-wrapper-top">
      <ul class="main-menu">
        <component :is="currentNavComponent"></component>
      </ul>
    </div>
    <div class="nav-item-wrapper-bottom">
      <ul class="inner-menu-bottom">
        <li><span data-hover="Minimize">Minimize</span></li>
      </ul>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Navigation',
  props: {
    navForRole: String,
    required: true
  },
  data () {
    return {
      nav: '',
    }
  },
  components: {
    'ur996': () => import('./ur-996'),
    'r998': () => import('./r-998'),
    'r990': () => import('./r-990'),
    'r992': () => import('./r-992'),
  },
  computed: {
    currentNavComponent: function () {
      return this.navForRole;
    }
  }
}
</script>


<style>
#nav {
  height: inherit;
  width: 250px;
  background-color: rgb(28, 30, 42);
  color: #fff;
  padding: 50px 0;
}
.nav-item-wrapper-top {
  height: auto;
  width: inherit;
}
.nav-item-wrapper-bottom {
  width: inherit;
  position: absolute;
  bottom: 0;
  left: 0;
}
  .main-menu {
    padding-left: 20px;
    width: 100%;
    list-style-type:  none;
    text-align: left;
  }
  .main-menu li.nav-title {
    margin: 25px 0 10px;
    font-size: 12px;
    text-transform: uppercase;
    color: #4f5678;
  }
  .main-menu li, .inner-menu-bottom li {
    overflow: hidden;
  }
  .main-menu li a, .inner-menu-bottom li {
    width: 100%;
    color: #fff;
    text-decoration: none;
    border-right: 3px solid transparent;
    border-radius: 0;
    cursor: pointer;
    -webkit-transition: all 0.3s;
    -moz-transition: all 0.3s;
    transition: all 0.3s;
  }
  .main-menu li a span, .inner-menu-bottom li span {
    position: relative;
    display: inline-block;
    width: 100%;
    text-transform: capitalize;
    -webkit-transition: -webkit-transform 0.3s;
    -moz-transition: -moz-transform 0.3s;
    transition: transform 0.3s;
  }
  .main-menu li a span:before, .inner-menu-bottom li span:before {
    content: attr(data-hover);
    position: absolute;
    bottom: 0;
    left: 0;
    font-weight: 700;
    color: #ffffff;
    -webkit-transform: translateY(25px);
    -moz-transform: translateY(25px);
    -ms-transform: translateY(25px);
    -o-transform: translateY(25px);
    transform: translateY(25px);
  }
  .main-menu li:hover span, .inner-menu-bottom li:hover span {
    -webkit-transform: translateY(-25px);
    -moz-transform: translateY(-25px);
    transform: translateY(-25px);
  }
  .main-menu li:hover a, .inner-menu-bottom li:hover {
    border-right-color: #fff;
  }
  .inner-menu-bottom {
    padding-left: 20px;
    color: #fff;
    width: 100%;
    height: auto;
    text-align: left;
  }
</style>
