<template>
  <div class="bg-white shadow rounded p-3 border border-white" :data-id="task.id">
    <div class="d-flex justify-content-between card-top-wrapper">
      <p class="text-gray-700 font-semibold font-sans tracking-wide text-sm">{{task.title}}</p>
      <b-icon v-if="task.img === undefined" icon="person-circle"></b-icon>
      <img v-else  class="avatar-small" :src="profileImg(task.img)" alt="Avatar">
    </div>
    <div class="d-flex text-justify justify-content-between" style="margin-top: 85px;">
      <span class="task-date">{{task.date}}</span>
      <badge v-if="task.content !== null" :content="task.content" :color="task.color">{{task.content}}</badge>
    </div>
  </div>
</template>

<script>
const badge = {
  name: 'badge',
  props: {
    content: String,
    color: String
  },
  template: `<div class="badge-wrapper d-flex align-items-center"
                  :style="{backgroundColor: 'rgba(' + color + ', .2)', color: 'rgb(' + color + ')'}">
                <span class="badge-point" :style="{backgroundColor: 'rgb(' + color + ')'}"></span>
                <span><slot></slot></span>
              </div>`
};

export default {
  name: "TaskItem",
  props: {
    task: Object,
    required: false
  },
  data () {
    return {
      badge: 'badge'
    }
  },
  methods: {
    profileImg (img) {
      return require(`../assets/photos/${img}`);
    }
  },
  components: {
    'badge': badge
  }
}
</script>

<style scoped>

</style>