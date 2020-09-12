<template>
  <div id="workflow" class="bg-white" style="height: 880px;">
    <div class="col-sm-12" style="border-bottom: 1px solid #e6eaee; height: 22%;">
      <div class="column-inner">
        <div class="wrapper text-left">
          <div class="d-flex flex-row justify-content-between">
            <h5>My Workspace</h5>
            <p>Neki dodatci ce biti i opcije</p>
          </div>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.<br>Proin erat nunc, viverra sed nibh nec, mattis porta metus.<br>Aenean luctus aliquam nisi, eget vulputate dolor congue in.<br>Aliquam interdum purus efficitur elementum porttitor.</p>
          <div class="d-flex flex-row justify-content-between">
            <span>Main Table</span>
            <ul>
              <li><button>New Post</button></li>
              <li>Search</li>
              <li>Members</li>
              <li>Filter</li>
              <li>Sort</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="pt-5 pb-5 pr-0" style="height: 78%; overflow-x: scroll; overflow-y: scroll;" :style="{width: ww}">
      <div class="column-inner" style="height: 100%;">
        <div class="wrapper" style="height: 100%;">
          <div v-if="firstTimeMsg">
            <p class="text-justify" style="width: 550px; margin: 0 auto;">It looks like this is your first time in <i>Workbook</i>. I suggest you to start a quick tutorial around. Of course, nothing is stopping you to explore things on your own. Ether way, good luck and happy managing :)</p>
            <div class="col-sm-12 text-center">
              <button class="mr-4">Start tutorial</button>
            </div>
            <p class="text-justify" style="width: 550px; margin: 0 auto;">Start managing your work by adding new table <span class="col-display" @click="setNewProjectTable">Here</span>.</p>
          </div>
          <div v-else>
            <workflow-item
              v-for="w in workflowItems"
              :active-project="userInfo.team.activeProject"
              :key="w.id" :table-prop="w"
              :team="personnel"
              @update-table="updateTableData"
            ></workflow-item>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WorkflowItem from "../components/WorkflowItem";
import firebase from 'firebase/app'
export default {
  name: "Workflow",
  data () {
    return {
      ww: '',
      firstTimeMsg: true,
      workflowItems: [],
      userInfo: this.$store.getters.getMyInfo,
      personnel: []
    }
  },
  created () {
    this.ww = window.innerWidth - 250 + 'px';
    this.userInfo.team = this.$store.getters.getTeams;
    this.requestProjectTable();
  },
  methods: {
    getTableIndex (tableId) {
      return this.workflowItems.findIndex(i => i.id === tableId);
    },
    updateTableData (statement, value, tableId) {
      let index = this.getTableIndex(tableId);
      let updates = {};
      switch (statement) {
        case 'table-title':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/title'] = value;
          break;
        case 'subitem':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/subItem'] = value;
          break;
        case 'main-col':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/mainCol'] = value;
          break;
        case 'sec-sol':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/secCol'] = value;
          break;
        case 'tr-new-item':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/tr'] = value;
          break;
        case 'tr-item-title':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/tr/' + value.index + '/title'] = value.asset;
          break;
        case 'tr-item-new-component':
          value.tr.forEach(function (row, rowIndex) {
            updates['P-' + this.userInfo.team.activeProject + '/' + index + '/tr/' + rowIndex + '/components'] = row.components;
          }, this);
          updates['P-' + this.userInfo.team.activeProject + '/' +  index +  '/th'] = value.th;
          updates['P-' + this.userInfo.team.activeProject + '/' +  index +  '/colNum'] = value.colNum;
          break;
        case 'update-item-th-title':
          updates['P-' + this.userInfo.team.activeProject + '/' +  index +  '/th/' + value.index + '/title'] = value.asset;
          break;
        case 'main-component-value':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/tr/' + value.index + '/components/' + value.compIndex + '/value'] = value.asset;
          break;
        case 'sub-component-value':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/tr/' + value.index + '/subItems/' + value.subItemIndex + '/data/' + value.compIndex + '/value'] = value.asset;
          break;
        case 'sub-item-title':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/tr/' + value.rowIndex + '/subItems/' + value.srIndex + '/title'] = value.asset;
          break;
        case 'sub-main-col':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/sub/mainCol'] = value;
          break;
        case 'sub-sec-col':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/sub/secCol'] = value;
          break;
        case 'sub-item-new-component':
          value.tr.forEach(function (row, rIndex) {
            row.subItems.forEach(function (subRow, srIndex) {
              updates['P-' + this.userInfo.team.activeProject + '/' + index + '/tr/' + rIndex + '/subItems/' + srIndex + '/data' ] = subRow.data;
            }, this);
          }, this);
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/sub/colNum'] = value.colNum;
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/sub/th'] = value.th;
          break;
        case 'update-sub-th-title':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/sub/th/' + value.index + '/title'] = value.asset;
          break;
        case 'new-sub-item':
          updates['P-' + this.userInfo.team.activeProject + '/' + index + '/tr/' + value.index + '/subItems'] = value.asset;
          break;
      }
      firebase.database().ref().update(updates)
      .then(() => {
        console.log('Update successful!');
      });
    },
    requestProjectTable () {
      firebase.database().ref('P-' + this.userInfo.team.activeProject).once('value', (snap) => {
        this.workflowItems = [];
        this.workflowItems = snap.val();
        this.checkSubItems();
        if (this.workflowItems.length === 0) this.setNewProjectTable();
      }, this);
    },
    setNewProjectTable () {
      const tableId = firebase.database().ref().push().key;
      let item = {
        id: tableId,
        table: 'Group Title',
        subItem: 'Subitems',
        colNum: 5,
        mainCol: 'Status',
        secCol: 'Date',
        th: [
          {title: 'person', type: 'person'}
        ],
        sub: {
          colNum: 4,
          mainCol: 'Status',
          secCol: 'Date',
          th: [
            {title: 'person', type: 'person'}
          ]
        },
        tr: [
          {
            id: 1,
            itemStatus: false,
            title: 'Table item 1',
            subItems: [],
            show: false,
            components: [
              {
                id: 1,
                name: 'status-type',
                value: {
                  text: 'Done',
                  statusColor: '50, 205, 50'
                }
              },
              {
                id: 2,
                name: 'date-type',
                value: '2020-09-01'
              },
              {
                id: 3,
                name: 'person-type',
                value: {
                  id: 1,
                  name: this.userInfo.name,
                  img: this.userInfo.img
                }
              }
            ]
          },
          {
            id: 2,
            itemStatus: false,
            title: 'Table item 2',
            subItems: [],
            show: false,
            components: [
              {
                id: 1,
                name: 'status-type',
                value: {
                  text: 'Done',
                  statusColor: '50, 205, 50'
                }
              },
              {
                id: 2,
                name: 'date-type',
                value: '2020-09-01'
              },
              {
                id: 3,
                name: 'person-type',
                value: {
                  id: 1,
                  name: this.userInfo.name,
                  img: this.userInfo.img
                }
              }
            ]
          },
          {
            id: 3,
            itemStatus: false,
            title: 'Table item 3',
            subItems: [],
            show: false,
            components: [
              {
                id: 1,
                name: 'status-type',
                value: {
                  text: 'Done',
                  statusColor: '50, 205, 50'
                }
              },
              {
                id: 2,
                name: 'date-type',
                value: '2020-09-01'
              },
              {
                id: 3,
                name: 'person-type',
                value: 'None'
              }
            ]
          }
        ]
      };
      let items = [];
      items.push(item);
      firebase.database().ref('P-' + this.userInfo.team.activeProject).set(items)
      .then((r) => {
        console.log('Project successfully created!');
      })
      firebase.database().ref('P-' + this.userInfo.team.activeProject).once('value', (snap) => {
        this.workflowItems = snap.val();
        this.checkSubItems();
      });
    },
    checkSubItems () {
      this.workflowItems.forEach(function (wfItem) {
        wfItem.tr.forEach(function (row) {
          if (row.subItems === undefined) {
            row.subItems = [];
          }
        })
      })
      this.setPersonnel();
    },
    setPersonnel () {
      this.personnel = this.userInfo.team.members;
      this.personnel.push({id: this.userInfo.id, name: this.userInfo.name, img: this.userInfo.img})
      this.firstTimeMsg = false;
    }
  },
  components: {WorkflowItem}
}
</script>

<style scoped>
ul li {
  display: inline-block;
  width: 90px;
  margin-right: 15px;
  text-align: center;
}

</style>