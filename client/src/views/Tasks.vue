<template>
  <div id="tasks">
    <div class="d-flex text-center">
      <div class="min-h-screen d-flex">
        <div v-for="column in columns" :key="column.title" @drop="updateForLeader(column.title, column.color)" @dragstart="draggedItem = $event.target.dataset.id" class="task-column p-3" :style="{backgroundColor: 'rgba(' + column.color + ', .252)'}">
          <p class="text-gray-700 font-semibold font-sans tracking-wide text-sm">{{column.title}}</p>
          <draggable :list="column.tasks" :animation="200" ghost-class="ghost-card" group="tasks">
            <task-item v-for="task in column.tasks" :task="task" :key="task.id"  class="task-item"></task-item>
          </draggable>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import TaskItem from "@/components/TaskItem";
import firebase from "firebase";
	export default {
		name: "Tasks",
    data () {
		  return {
		    myInfo: this.$store.getters.getMyInfo,
        draggedItem: 0,
        columns: [
          {
            title: "Backlog",
            tasks: [],
            color: '102, 51, 0'
          },
          {
            title: "In Progress",
            tasks: [],
            color: '51, 153, 255'
          },
          {
            title: "Need a review",
            tasks: [],
            color: '150, 74, 200'
          },
          {
            title: "Done",
            tasks: [],
            color: '50, 205, 50'
          }
        ]
      }
    },
    created () {
		  this.myInfo = this.$store.getters.getMyInfo;
		  this.requestProjectTable();
    },
    sockets: {
		  teamUpdate: function (data) {
		    this.updateItemStatus(data);
      }
    },
    methods: {
		  updateItemStatus (item) {
		    let index = -1;
		    let colIndex = -1;
		    let tmp = null;
		    this.columns.forEach(function (col, cIndex) {
		      col.tasks.forEach(function (task, tIndex) {
		        if (task.id === item.rowId) {
		          index = tIndex;
		          colIndex = cIndex;
		          tmp = task;
            }
          })
        });
		    this.columns.forEach(function (col) {
          if (col.title === item.text) {
            col.tasks.push(tmp);
          }
        });
		    this.columns[colIndex].tasks.splice(index, 1);
      },
      updateForLeader (colTitle, color) {
        this.$socket.emit('update_to_leader', {
          colTitle: colTitle,
          statusColor: color,
          itemId: this.draggedItem
        });
      },
      requestProjectTable () {
        firebase.database().ref('P-' + this.myInfo.activeProject).once('value', (snap) => {
          let i = snap.val();
          if (i.length > 0) {
            this.sortDataToTable(i[0]);
          }
        }, this);
      },
      sortDataToTable (array) {
        let temp = this.columns;
        let index = 0;
        let img = null;
        let content = null;
        let color = null;
        array.tr.forEach(function (value) {
          index = this.colMapping(value.components[0].value.text);
          value.components.forEach(function (innerValue) {
            if (innerValue.name === 'person-type')  img = innerValue.value.img;
            else if (innerValue.name === 'content-type') {
              content = innerValue.value.text;
              color = innerValue.value.statusColor;
            }
          });
          temp[index].tasks.push({
              id: value.id,
              title: value.title,
              date: value.components[1].value,
              color: color,
              img: img, content: content
            })
        }, this);
        this.columns = temp;
      },
      colMapping (value) {
        const mappings = {
          Backlog: 0,
          "In progress": 1,
          "Need a review": 2,
          Done: 3,
          default: 0
        };
        return mappings[value] || mappings.default;
      }
    },
    components: {TaskItem, draggable},
  }
</script>

<style>
#tasks {
  height: calc(100vh - 60px);
  overflow: auto;
}
#tasks > div.d-flex.text-center {
  margin-bottom: 80px;
}
.task-column {
  min-width: 320px;
  width: 320px;
  padding: .75rem;
  margin-right: 1rem;
  border-radius: .5rem;
  /*background-color: #b7c0cd;*/
}
.task-column p {
  letter-spacing: .025rem;
  color: rgb(74, 85, 104);
  font-size: .875rem;
  font-weight: 600;
}
.ghost-card {
  opacity: 0.5;
  background: #F7FAFC;
  border: 1px solid #4299e1;
}
.task-item {
  padding: .75rem .75rem 1.25rem .75rem;
  margin-top: .75rem;
  cursor: move;
  box-shadow: 0 1px 3px 0 rgba(0,0,0,.1),0 1px 2px 0 rgba(0,0,0,.06);
}
.min-h-screen {
  min-height: 100vh;
  margin: 0 auto;
}
.py-12 {
  padding-top: 3rem;
  padding-bottom: 3rem;
}
.avatar-small {
  width: 30px;
  margin-left: .75rem;
  height: 30px;
  border-radius: 9999px;
  max-width: 100%;
}
.task-date {
  color: #718096;
}
.text-sm {
  font-size: .875rem;
}
.badge-wrapper {
  padding-left: .75rem;
  padding-right: .75rem;
  font-size: .75rem;
  height: 1.5rem;
  font-weight: 600;
  border-radius: 4px;
}
.badge-point {
  width: .5rem;
  margin-right: .25rem;
  height: .5rem;
  border-radius: 9999px;
}
.card-top-wrapper svg {
  font-size: 30px;
}
</style>
