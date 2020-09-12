<template>
  <div id="wf-item" class="pl-4">
    <table id="table-1">
      <thead>
      <tr>
        <th class="group-menu border-0" style="width: 30px;">
          <div class="menu-button-container">
            <a class="menu-button wf-caret-down"></a>
          </div>
        </th>
        <th class="table-title border-0 position-relative" style="color: red;">
          <input type="text" class="dd-input text-left" v-model="table.table" @blur="setNewDataValue('table-title', table.table)">
        </th>
        <th class="border-0">
          <input type="text" class="dd-input" v-model="table.subItem" @blur="setNewDataValue('subitem', table.subItem)">
        </th>
        <th class="static-border-color main-column-first">
          <input type="text" class="dd-input" v-model="table.mainCol" @blur="setNewDataValue('main-col', table.mainCol)">
        </th>
        <th class="static-border-color main-column-second">
          <input type="text" class="dd-input" v-model="table.secCol" @blur="setNewDataValue('sec-col', table.secCol)">
        </th>
        <th class="border-0 pr-2 pl-2 position-relative" v-for="(header, index) in table.th" :key="'table-' + index" @mouseleave="colMenu = false">
          <input type="text" class="dd-input dd-header-input-w" v-model="header.title" @blur="setNewDataValue('update-item-th-title', {index: index, asset: header.title})">
          <div class="dd-col-menu">
            <a @click="colMenu = !colMenu" class="menu-button wf-caret-down"></a>
            <div v-if="colMenu" class="new-cell-picker-wrapper">
              <ul>
                <li @click="deleteColumn(header, index, 'main')">Delete Column</li>
              </ul>
            </div>
          </div>
        </th>
        <th class="border-0 position-relative" @click="toggleNewCellDD = !toggleNewCellDD" style="cursor: pointer;">
          <span style="background-color: #0C0C0C; border-radius: 50%; width: 20px; height: 20px; color: #ffffff; font-size: 20px; font-weight: 700;">+</span>
          <div v-if="toggleNewCellDD" class="position-absolute new-cell-picker-wrapper">
            <ul>
              <li @click="newCell('status', 'main')">Status</li>
              <li @click="newCell('origin', 'main')">Origin</li>
              <li @click="newCell('content', 'main')">Content</li>
              <li @click="newCell('priority', 'main')">Priority</li>
              <li @click="newCell('date', 'main')">Date</li>
              <li @click="newCell('person', 'main')">Person</li>
            </ul>
          </div>
        </th>
      </tr>
      </thead>
      <tbody>
        <template v-for="(row, index) in table.tr">
          <tr :key="row.id">
            <td class="border-0"></td>
            <td class="static-border-color d-flex flex-row align-items-center">
              <div class="wf-item-selector-container">
                <span class="wf-item-selector overflow-hidden">
                <b-form-checkbox v-model="row.itemStatus"></b-form-checkbox>
                </span>
              </div>
              <span class="wf-item-title"><input type="text" class="dd-input text-left" v-model="row.title"></span>
            </td>
            <td class="static-border-color" @click.stop="row.show = !row.show"><b-icon icon="diagram2" class="mr-3"></b-icon>{{row.subItems.length}}</td>
            <component v-for="c in row.components" :key="c.id" :is="c.name" :row-data="c" :personnel="team" :parent="index" @update-table-values="setNewDataValue" @ws-canvas-update="sendUpdateToTeam"></component>
            <td class="border-0"></td>
          </tr>
          <component v-if="row.show" :is="subItem" :items="row.subItems" :gen="table.sub" :col-num="table.colNum" :team="team" :parent="index" @new-subitem="insertNewSubItemInRow" @new-sub-cell="newCell" @del-col="deleteColumn" @update-table-values="setNewDataValue" @ws-canvas-update="sendUpdateToTeam"></component>
        </template>
        <tr>
          <td class="border-0"></td>
          <td :colspan="table.colNum" class="add-item static-border-color" style="background-color: transparent;">
            <div class="d-flex flex-row align-items-center" style="width: 100%; height: 100%;">
              <span class="wf-item-selector-faded"></span>
              <form @submit="newTableRow" style="width: 100%;">
                <input ref="newRowInput" type="text" placeholder="+ Add" v-model="newRowTitle">
              </form>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

const dateType = {
  name: 'date-type',
  props: {
    rowData: Object,
    parent: Number,
    personnel: {
      type: Array,
      required: false
    }
  },
  data () {
    return {
      dv: this.rowData.value
    }
  },
  watch: {
    dv () {
      this.$emit('update-table-values', 'main-component-value', {index: this.parent, compIndex: this.rowData.id - 1, asset: this.dv})
    }
  },
  template: `<td class="static-border-color"><input type="date" class="dd-input" v-model="dv"></td>`
};
const originType = {
  name: 'origin-type',
  props: {
    rowData: Object,
    parent: Number,
    personnel: {
      type: Array,
      required: false
    }
  },
  data () {
    return {
      toggleDD: false,
      origin: [
        {id: '1', value: 'Email', color: '240, 128, 128'},
        {id: '2', value: 'Blog post', color: '50, 205, 50'},
        {id: '3', value: 'Press release', color: '255, 105, 108'},
        {id: '4', value: 'Web page/app', color: '128, 0, 255'},
        {id: '5', value: 'Design', color: ' 32, 218, 165'},
        {id: '6', value: 'Print', color: '99, 151, 136'}
      ]
    }
  },
  methods: {
    toggleStatusPickerDD () {
      if (event.target.classList.contains('parent-cell')) this.toggleDD = !this.toggleDD;
      else  event.preventDefault();
    },
    setNewValue (r, o, compId) {
      r.text = o.value;
      r.statusColor = o.color;
      this.toggleDD = false;
      this.$emit('update-table-values', 'main-component-value', {index: this.parent, compIndex: compId - 1, asset: {text: r.text, statusColor: r.statusColor}})
    }
  },
  template: `
    <td :id="'dd-' + rowData.id" class="white-color position-relative parent-cell border-0" @click="toggleStatusPickerDD" :style="{backgroundColor: 'rgb(' + rowData.value.statusColor + ')', cursor: 'pointer'}">{{rowData.value.text}}
      <div v-if="toggleDD" class="dd-status-picker-wrapper">
        <div class="dd-status-picker-color-inner overflow-hidden">
          <div v-for="o in origin" :key="o.id" class="dd-color-box overflow-hidden">
            <div @click="setNewValue(rowData.value, o, rowData.id)" :key="1" class="dd-status-color" :style="{backgroundColor: 'rgb(' + o.color + ')'}">
              <span>{{o.value}}</span>
            </div>
          </div>
        </div>
      </div>
    </td>
  `
};
const contentType = {
  name: 'content-type',
  props: {
    rowData: Object,
    parent: Number,
    personnel: {
      type: Array,
      required: false
    }
  },
  data () {
    return {
      toggleDD: false,
      content: [
        {id: '1', value: 'QA', color: '0, 128, 128'},
        {id: '2', value: 'Backend', color: '0, 205, 502'},
        {id: '3', value: 'Frontend', color: '162, 181, 255'},
        {id: '4', value: 'Prototype', color: '62, 197, 255'},
        {id: '5', value: 'Feature Request', color: '128, 0, 128'},
        {id: '6', value: 'Brainstorming', color: '255, 154, 164'}
      ]
    }
  },
  methods: {
    toggleStatusPickerDD () {
      if (event.target.classList.contains('parent-cell')) this.toggleDD = !this.toggleDD;
      else  event.preventDefault();
    },
    setNewValue (r, c, compId) {
      r.text = c.value;
      r.statusColor = c.color;
      this.toggleDD = false;
      this.$emit('update-table-values', 'main-component-value', {index: this.parent, compIndex: compId - 1, asset: {text: r.text, statusColor: r.statusColor}})
    }
  },
  template: `
    <td :id="'dd-' + rowData.id" class="white-color position-relative parent-cell border-0" @click="toggleStatusPickerDD" :style="{backgroundColor: 'rgb(' + rowData.value.statusColor + ')', cursor: 'pointer'}">{{rowData.value.text}}
      <div v-if="toggleDD" class="dd-status-picker-wrapper">
        <div class="dd-status-picker-color-inner overflow-hidden">
          <div v-for="c in content" :key="c.id" class="dd-color-box overflow-hidden">
            <div @click="setNewValue(rowData.value, c, rowData.id)" :key="1" class="dd-status-color" :style="{backgroundColor: 'rgb(' + c.color + ')'}">
              <span>{{c.value}}</span>
            </div>
          </div>
        </div>
      </div>
    </td>
  `
};
const priorityType = {
  name: 'priority-type',
  props: {
    rowData: Object,
    parent: Number,
    personnel: {
      type: Array,
      required: false
    }
  },
  data () {
    return {
      toggleDD: false,
      priority: [
        {id: 1, value: 'Very Low', color: '223, 199, 101'},
        {id: 2, value: 'Low', color: '202, 154, 93'},
        {id: 3, value: 'Normal', color: '168, 107, 53'},
        {id: 4, value: 'Medium', color: '162, 61, 12'},
        {id: 5, value: 'High', color: '153, 0, 0'},
        {id: 6, value: '', color: '245, 245, 245'}
      ]
    }
  },
  methods: {
    toggleStatusPickerDD () {
      if (event.target.classList.contains('parent-cell')) this.toggleDD = !this.toggleDD;
      else  event.preventDefault();
    },
    setNewValue (r, p, compId) {
      r.text = p.value;
      r.statusColor = p.color;
      this.toggleDD = false;
      this.$emit('update-table-values', 'main-component-value', {index: this.parent, compIndex: compId - 1, asset: {text: r.text, statusColor: r.statusColor}})
    }
  },
  template: `
    <td :id="'dd-' + rowData.id" class="white-color position-relative parent-cell border-0" @click="toggleStatusPickerDD" :style="{backgroundColor: 'rgb(' + rowData.value.statusColor + ')', cursor: 'pointer'}">{{rowData.value.text}}
      <div v-if="toggleDD" class="dd-status-picker-wrapper">
        <div class="dd-status-picker-color-inner overflow-hidden">
          <div v-for="p in priority" :key="p.id" class="dd-color-box overflow-hidden">
            <div @click="setNewValue(rowData.value, p, rowData.id)" :key="1" class="dd-status-color" :style="{backgroundColor: 'rgb(' + p.color + ')'}">
              <span>{{p.value}}</span>
            </div>
          </div>
        </div>
      </div>
    </td>
  `
};
const statusType = {
  name: 'status-type',
  props: {
    rowData: Object,
    parent: Number,
    personnel: {
      type: Array,
      required: false
    }
  },
  data () {
    return {
      toggleDD: false,
      status: [
        {id: '1', value: 'Backlog', color: '102, 51, 0'},
        {id: '2', value: 'In Progress', color: '51, 153, 255'},
        {id: '3', value: 'Need a review', color: '150, 74, 200'},
        {id: '4', value: 'Done', color: '50, 205, 50'},
        {id: '5', value: '', color: '245, 245, 245'}
      ],
    }
  },
  methods: {
    toggleStatusPickerDD () {
      if (event.target.classList.contains('parent-cell')) this.toggleDD = !this.toggleDD;
      else  event.preventDefault();
    },
    setNewValue (r, s, compId) {
      r.text = s.value;
      r.statusColor = s.color;
      this.toggleDD = false;
      this.$emit('update-table-values', 'main-component-value', {
        index: this.parent,
        compIndex: compId - 1,
        asset: {text: r.text, statusColor: r.statusColor}
      })
      this.$emit('ws-canvas-update', {rowId: this.parent + 1, text: r.text, statusColor: r.statusColor})
    }
  },
  template: `
    <td :id="'dd-' + rowData.id" class="white-color position-relative parent-cell border-0" @click="toggleStatusPickerDD" :style="{backgroundColor: 'rgb(' + rowData.value.statusColor + ')', cursor: 'pointer'}">{{rowData.value.text}}
    <div v-if="toggleDD" class="dd-status-picker-wrapper">
      <div class="dd-status-picker-color-inner overflow-hidden">
        <div v-for="s in status" :key="s.id" class="dd-color-box overflow-hidden">
          <div @click="setNewValue(rowData.value, s, rowData.id)" :key="1" class="dd-status-color" :style="{backgroundColor: 'rgb(' + s.color + ')'}">
            <span>{{s.value}}</span>
          </div>
        </div>
      </div>
    </div>
    </td>
  `
};
const personType = {
  name: 'person-type',
  props: {
    rowData: Object,
    parent: Number,
    personnel: {
      type: Array,
      required: true
    }
  },
  data () {
    return {
      personnelDD: false
    }
  },
  methods: {
    profileImg (img) {
      return require(`@/assets/photos/${img}`);
    },
    setNewValue (r, s, compId) {
      console.log('S -> ', s);
      r.value = {
        id: s.id,
        name: s.name,
        img: s.img
      };
      console.log('rowdata: ', this.rowData);
      this.personnelDD = false;
      this.$emit('update-table-values', 'main-component-value', {index:this.parent, compIndex: compId - 1, asset: this.rowData.value})
    }
  },
  template: `<td class="static-border-color position-relative"><div class="avatar-wrapper-s" style="cursor: pointer;">
    <b-icon @click="personnelDD = !personnelDD" v-if="rowData.value === 'None'" icon="person-circle"></b-icon>
    <img @click="personnelDD = !personnelDD" v-else class="rounded-circle" :src="profileImg(rowData.value.img)" alt="Profile avatar">
    <div v-if="personnelDD" class="personnel-picker-wrapper">
      <div class="d-flex flex-row align-items-center p-3">
        <div v-for="p in personnel" class="avatar-wrapper">
          <img @click="setNewValue(rowData, p, rowData.id)" :src="profileImg(p.img)" alt="Avatar image">
        </div>
      </div>
    </div>
  </div></td>`
};
const subItem = {
  name: 'sub-item',
  props: {
    colNum: Number,
    parent: Number,
    items: Array,
    gen: Object,
    team: Array
  },
  data () {
    return {
      dateType: 'date-type',
      statusType: 'status-type',
      originType: 'origin-type',
      contentType: 'content-type',
      priorityType: 'priority-type',
      personType: 'person-type',
      
      subColMenu: false,
      
      toggleNewCellDD: false,
      subItems: [],
      newSubItemTitle: ''
    }
  },
  created () {
    if (this.items.length === 0 && this.gen.colNum === 4) {
      let item = {
        id: 1,
        title: 'New Subitem',
        itemStatus: false,
        data: [
          {
            id: 1,
            name: 'status-type',
            value: {
              text: '',
              statusColor: '245, 245, 245'
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
      this.$emit('new-subitem', this.parent, item);
      //this.subItems.push(item);
    } else if (this.items.length === 0 && this.gen.colNum > 4) {
      let item = {
        id: 1,
        title: 'New Subitem',
        itemStatus: false,
        data: this.setNewRowItemData()
      }
      this.$emit('new-subitem', this.parent, item);
    } else this.subItems = this.items;
  },
  methods: {
    newSubItem () {
      event.preventDefault();
      let item = {
        id: this.items.length + 1,
        title: this.newSubItemTitle,
        itemStatus: false,
        data: this.setNewRowItemData()
      }
      this.newSubItemTitle = '';
      this.$refs['subRowInput'].blur();
      this.$emit('new-subitem', this.parent, item)
    },
    setNewRowItemData () {
      let data = [
        {
          id: 1,
          name: 'status-type',
          value: {
            text: '',
            statusColor: 'whitesmoke'
          }
        },
        {
          id: 2,
          name: 'date-type',
          value: '2020-09-01'
        }
      ]
      this.gen.th.forEach(function (value) {
        if (value.type === 'person') {
          data.push({id: data.length + 1, name: value.type + '-type', value: 'None'})
        } else if (value.type === 'status') {
          data.push({id: data.length + 1, name: value.type + '-type', value: {text: '', statusColor: '245, 245, 245'}})
        } else if (value.type === 'date') {
          data.push({id: data.length + 1, name: value.type + '-type', value: '2020-09-01'})
        }
      })
      return data
    },
    setNewDataValue (statement, value) {
      statement = 'sub-component-value';
      let v = {
        asset: value.asset,
        index: this.parent,
        subItemIndex: value.index,
        compIndex: value.compIndex
      }
      this.$emit('update-table-values', statement, v);
    }
  },
  components: {
    'date-type': dateType,
    'status-type': statusType,
    'origin-type': originType,
    'content-type': contentType,
    'priority-type': priorityType,
    'person-type': personType
  },
  template: `
    <tr>
      <td class="border-0"></td>
      <td class="border-0 subitems-row" :colspan="colNum + 1">
        <table style="width: 100%;">
          <thead>
            <tr>
              <th class="table-title border-0">Subitems</th>
              <th class="static-border-color col-set-width main-column-first"><input type="text" class="dd-input" v-model="gen.mainCol" @blur="$emit('update-table-values', 'sub-main-col', gen.mainCol)"></th>
              <th class="static-border-color col-set-width main-column-second"><input type="text" class="dd-input" v-model="gen.secCol" @blur="$emit('update-table-values', 'sub-sec-col', gen.secCol)"></th>
              <th class="border-0 col-set-width position-relative pl-2 pr-2" v-for="(header, index) in gen.th" @mouseleave="subColMenu = false">
                <input type="text" class="dd-input dd-subheader-input-w" v-model="header.title" @blur="$emit('update-table-values', 'update-sub-th-title', {index: index, asset: header.title})">
                <div class="dd-col-menu">
                  <a @click="subColMenu = !subColMenu" class="menu-button wf-caret-down"></a>
                  <div v-if="subColMenu" class="new-cell-picker-wrapper">
                    <ul>
                      <li @click="$emit('del-col', header, index, 'sub')">Delete Column</li>
                    </ul>
                  </div>
                </div>
              </th>
              <th class="border-0 position-relative" @click="toggleNewCellDD = !toggleNewCellDD" style="cursor: pointer;">
                <span style="background: transparent; border: 1px solid gray; border-radius: 50%; width: 20px; height: 20px; color: gray; font-size: 20px; font-weight: 700;">+</span>
                <div v-if="toggleNewCellDD" class="position-absolute new-cell-picker-wrapper">
                  <ul>
                    <li @click="$emit('new-sub-cell', 'status', 'sub')">Status</li>
                    <li @click="$emit('new-sub-cell', 'origin', 'sub')">Origin</li>
                    <li @click="$emit('new-sub-cell', 'content', 'sub')">Content</li>
                    <li @click="$emit('new-sub-cell', 'priority', 'sub')">Priority</li>
                    <li @click="$emit('new-sub-cell', 'date', 'sub')">Date</li>
                    <li @click="$emit('new-sub-cell', 'person', 'sub')">Person</li>
                  </ul>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
          <tr v-for="(item, index) in items" :key="item.id">
            <td class="static-border-color d-flex flex-row align-items-center">
              <div class="wf-item-selector-container">
                <span class="wf-item-selector overflow-hidden">
                  <b-form-checkbox v-model="item.itemStatus"></b-form-checkbox>
                </span>
              </div>
              <span class="wf-item-title"><input type="text" class="dd-input" v-model="item.title" @blur="$emit('update-table-values', 'sub-item-title', {rowIndex: parent, srIndex: index, asset: item.title})"></span>
            </td>
            <component v-for="c in item.data" :key="c.id" :is="c.name" :row-data="c" :personnel="team" :parent="index" @update-table-values="setNewDataValue"></component>
            <td class="border-0"></td>
          </tr>
          <tr>
            <td class="add-subitem border-0 text-left" :colspan="gen.colNum" style="color: rgb(230, 233, 239);">
              <form @submit="newSubItem">
                <input ref="subRowInput" id="new-subitem" placeholder="+ Add" v-model="newSubItemTitle">
                <label for="new-subitem"></label>
              </form>
            </td>
          </tr>
          </tbody>
        </table>
      </td>
    </tr>`
};

export default {
  name: "WorkflowItem",
  props: {
    tableProp: Object,
    activeProject: String,
    team: Array,
    require: true
  },
  data () {
    return {
      table: this.tableProp,
      toggleNewCellDD: false,
      newRowTitle: '',
      colMenu: false,
      
      subItem: 'sub-item',
      dateType: 'date-type',
      statusType: 'status-type',
      originType: 'origin-type',
      contentType: 'content-type',
      priorityType: 'priority-type',
      personType: 'person-type'
    }
  },
  sockets: {
    updateItemStatus: function (data) {
      this.table.tr[data.itemId - 1].components[0].value.text = data.colTitle;
      this.table.tr[data.itemId - 1].components[0].value.statusColor = data.statusColor;
    }
  },
  created () {
    this.table = this.tableProp
  },
  methods: {
    sendUpdateToTeam (value) {
      this.$socket.emit('update_to_team', value);
    },
    setNewDataValue (statement, value) {
      this.$emit('update-table', statement, value, this.table.id);
    },
    newTableRow () {
      event.preventDefault();
      this.table.tr.push({
        id: this.table.tr.length + 1,
        itemStatus: false,
        title: this.newRowTitle,
        subItems: [],
        show: false,
        components: this.table.tr[0].components
      });
      this.newRowTitle = '';
      this.$refs['newRowInput'].blur();
      this.setNewDataValue('tr-new-item', this.table.tr);
    },
    insertNewSubItemInRow (index, subitem) {
      this.table.tr[index].subItems.push(subitem);
      let updateData = {
        asset: this.table.tr[index].subItems,
        index: index
      }
      this.$emit('update-table', 'new-sub-item', updateData, this.table.id);
    },
    newCell (type, lvl) {
      if (lvl === 'main') {
        this.table.th.push({title: type, type: type});
        this.table.colNum++;
        this.table.tr.forEach(function (row) {
          if (type === 'person')  row.components.push({id: row.components.length + 1, name: 'person-type', value: 'None'});
          else if (type === 'date')  row.components.push({id: row.components.length + 1, name: 'date-type', value: '2020-09-01'});
          else  row.components.push({id: row.components.length + 1, name: type + '-type', value: {text: '', statusColor: '245, 245, 245'}});
        }, this);
        this.requestTableUpdate('tr-item-new-component', this.table.colNum, this.table.th);
      } else {
        this.table.sub.th.push({title: type, type: type});
        this.table.sub.colNum++;
        this.table.tr.forEach(function (row) {
          if (row.components.length > 0) {
            row.subItems.forEach(function (subRow) {
              if (type === 'person') subRow.data.push({id: subRow.data.length + 1, name: 'person-type', value: 'None'});
              else if (type === 'date' || type === 'link') subRow.data.push({id: subRow.data.length + 1, name: 'date-type', value: '2020-09-01'});
              else subRow.data.push({id: subRow.data.length + 1, name: 'status-type', value: {text: '', statusColor: '245, 245, 245'}});
            }, this);
          }
        }, this);
        this.requestTableUpdate('sub-item-new-component', this.table.sub.colNum, this.table.sub.th);
      }
    },
    deleteColumn (col, index, type) {
      if (type === 'main') {
        this.table.tr.forEach(function (row) {
          row.components.splice(index + 2, 1);
        });
        this.$delete(this.table.th, index);
        this.table.colNum--;
        this.requestTableUpdate('tr-item-new-component', this.table.colNum, this.table.th);
      } else {
        this.table.tr.forEach(function (row) {
          row.subItems.forEach(function (subRow) {
            subRow.data.splice(index + 2, 1);
          })
        });
        this.$delete(this.table.sub.th, index);
        this.table.sub.colNum--;
        this.requestTableUpdate('sub-item-new-component', this.table.sub.colNum, this.table.sub.th);
      }
    },
    requestTableUpdate (statement, colNum, th) {
      let updateData = {
        colNum: colNum,
        th: th,
        tr: this.table.tr
      }
      this.$emit('update-table', statement, updateData, this.table.id);
    }
  },
  components: {
    'sub-item': subItem,
    'date-type': dateType,
    'status-type': statusType,
    'origin-type': originType,
    'content-type': contentType,
    'priority-type': priorityType,
    'person-type': personType
  }
}
</script>

<style>
table {
  
  /*table-layout: fixed;*/
  width: max-content;
  
}
.table-title {
  font-family: "Roboto", helvetica, arial, sans-serif;
  font-size: 17px;
  font-weight: 300;
  line-height: 27px;
  color: inherit;
  text-align: left;
  padding-left: 10px;
  width: 400px;
}
th, td {
  height: 40px;
  border: 1px solid black;
  font-family: "Roboto", helvetica, arial, sans-serif;
  font-size: 13px;
  font-weight: 300;
  line-height: 19px;
}
tr td:last-child {
  border-right: 1px solid rgb(230, 233, 239);
}
.group-menu:hover > .menu-button-container .menu-button {
  background-color: #ffffff;
}
.group-menu:hover > .menu-button-container .menu-button:after {
  border-top-color: purple;
}
.menu-button {
  background-color: red;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  font-size: 14px;
  border: 1px solid red;
  transition: color 0.1s ease, background-color 0.1s ease, opacity 0.1s ease;
}
.wf-caret-down:after {
  content: "";
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
  border-top: 5px dashed #ffffff;
}
.wf-item-selector-container {
  width: 34px;
  height: 100%;
  margin-right: 0;
}
.wf-item-selector {
  display: flex;
  width: 8px;
  height: 100%;
  flex-direction: row;
  align-items: center;
  padding-left: 8px;
  background-color: red;
  transition: all 100ms ease-in;
}
.wf-item-selector-container:hover .wf-item-selector {
  width: 34px;
}
.wf-item-selector-faded {
  width: 8px;
  height: 100%;
  background-color: #ff5454;
  transition: all 100ms ease-in;
}
.wf-item-selector-faded:hover {
  background-color: #ff0000;
}
.wf-item-title {
  margin-left: 14px;
}
.static-border-color {
  background-color: rgb(245, 246, 248);
  border-top-color: rgb(230, 233, 239);
  border-bottom-color: rgb(230, 233, 239);
  border-right-color: rgb(255, 255, 255);
  border-left-style: none;
  background-clip: content-box;
}
th.main-column-first {
  border-top-left-radius: 10px;
  border-top-style: none;
  border-right-color: rgb(245, 246, 248);
}
th.main-column-second {
  border-top-right-radius: 10px;
  border-top-style: none;
  border-left-color: rgb(245, 246, 248);
}
.subitems-row {
  padding: 20px 0 20px 50px;
}
.add-subitem input, .add-item input{
  width: 100%;
  height: 28px;
  line-height: 28px;
  padding-top: 4px;
  padding-left: 16px;
  border: 1px solid transparent;
  transition: border-color 0.1s ease;
}
.add-subitem input:focus, .add-item input:focus {
  border-color: rgb(0, 133, 255);
}
/******************************************************************/
/*                DROP DOWN PERSONNEL PICKER                     */
/****************************************************************/
.personnel-picker-wrapper {
  width: auto !important;
}
.personnel-picker-wrapper .d-flex .avatar-wrapper {
  width: 50px;
  height: 50px;
  margin-right: 15px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
}
.personnel-picker-wrapper .d-flex .avatar-wrapper:last-child {
  margin-right: 0;
}

/******************************************************************/
/*                  DROP DOWN STATUS PICKER                      */
/****************************************************************/
.dd-status-picker-wrapper {
  display: block;
  position: absolute;
  background-color: #ffffff;
  width: 245px;
  min-width: 245px;
  z-index: 1;
  margin-top: 10px;
  margin-bottom: 100px;
  border: 1px solid #c4c4c4;
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.32);
  border-radius: 4px;
  font-size: 13px;
  transition: width 0.1s;
  pointer-events: all;
  left: 50%;
  transform: translateX(-50%);
}
.dd-status-picker-wrapper:before {
  content: "";
  position: absolute;
  right: 50%;
  bottom: 97.5%;
  transform: translateX(50%) rotateZ(45deg);
  border-left: 1px solid #c4c4c4;
  border-top: 1px solid #c4c4c4;
  background-color: #ffffff;
  width: 15px;
  height: 15px;
}
.dd-status-picker-color-inner {
  padding: 10px 6px;
  align-content: space-between;
  height: 220px;
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
}
.dd-status-edit-wrapper {
  background-color: #ffffff;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  color: cornflowerblue;
  border-top: 1px solid rgb(230, 233, 239);
  height: 45px;
  transition: all 300ms ease-out;
  cursor: pointer;
}
.dd-status-edit-wrapper:hover {
  background-color: cornflowerblue;
  color: #ffffff;
}
.dd-color-box {
  display: inline-block;
  width: 112px;
  height: 32px;
  line-height: 32px;
  text-align: center;
  margin-bottom: 8px;
  color: #ffffff;
  font-weight: 400;
  cursor: pointer;
  transition: transform 0.1s ease-in-out, opacity 0.1s ease-in-out;
  position: relative;
}
.dd-status-color, .dd-status-color-edit {
  width: 100%;
  height: 32px;
  line-height: 32px;
  text-align: center;
}
.dd-status-color:after {
  content: "";
  position: absolute;
  pointer-events: none;
  width: 100%;
  height: 100%;
  left: 0;
  right: 0;
  top: 0;
}
.dd-status-color-edit:hover > .color-picker-del, .dd-status-color-edit:hover > .color-picker-label svg {
  opacity: 1;
}
.color-picker-label {
  display: inline-block;
  width: 16px;
  height: 32px;
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
  padding: 1px;
  cursor: pointer;
}
.color-picker-label svg {
  opacity: 0;
}
.color-picker-input {
  width: 88px;
  height: 32px;
  font-size: 12px;
  display: inline-block;
  border: 1px solid transparent;
  background-color: rgb(230, 233, 239);
  margin-right: 2px;
  padding-left: 5px;
  border-top-right-radius: 3px;
  border-bottom-right-radius: 3px;
  overflow: hidden;
  text-overflow: ellipsis;
}
.color-picker-input:focus {
  border-color: cornflowerblue;
}
a.color-picker-del {
  width: 10px;
  height: 10px;
  display: inline-block;
  font-size: 10px;
  line-height: 11px;
  background-color: #c4c4c4;
  color: #ffffff;
  border-radius: 50px;
  opacity: 0;
}
.color-pallet {
  width: 100%;
  border-top: 1px solid #f1f1f1;
  border-bottom: 1px solid #f1f1f1;
  background-color: #f7f7f7;
}
.pallet-color-item {
  position: relative;
  height: 20px;
  width: 20px;
  display: inline-block;
  border: 0 solid #ffffff;
  margin: 4px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 100ms ease-out;
}
.pallet-color-item:before {
  content: "";
  position: absolute;
  right: -4px;
  top: -4px;
  bottom: -4px;
  left: -4px;
}
.pallet-color-item:hover {
  transform: scale(1.2);
  box-shadow: 0 1px 8px -2px #0C0C0C;
  border-width: 1px;
}
.new-dd-color-box {
  display: inline-block;
  width: 112px;
  height: 32px;
  line-height: 32px;
  text-align: center;
  border: 1px dashed rgb(196, 196, 196);
  color: rgb(196, 196, 196);
  background-color: #ffffff;
  outline: none;
  border-radius: 5px;
}
/******************************************************************/
/*                  DROP DOWN NEW CELL PICKER                    */
/****************************************************************/
.new-cell-picker-wrapper, .personnel-picker-wrapper {
  position: absolute;
  background-color: #ffffff;
  width: 105px;
  min-width: 105px;
  z-index: 1;
  margin-top: 10px;
  margin-bottom: 100px;
  border: 1px solid #c4c4c4;
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.32);
  border-radius: 4px;
  font-size: 13px;
  transition: width 0.1s;
  pointer-events: all;
  right: 0;
}
.new-cell-picker-wrapper ul {
  list-style-type: none;
  text-align: center;
  margin: 0;
}
.new-cell-picker-wrapper ul li {
  border-bottom: 1px solid rgb(196, 196, 196);
  color: rgb(196, 196, 196);
  padding: 12px 0;
  cursor: pointer;
  transition: all 400ms ease-out;
}
.new-cell-picker-wrapper ul li:hover {
  color: #ffffff;
  background-color: #4f5678;
}

/******************************************************************/
/*                      CUSTOM INPUT                            */
/****************************************************************/
.editable {
  width: auto;
  height: auto;
}
.editable .editable-inner {
  width: 100%;
  height: 100%;
  border: 1px solid transparent;
  padding: 0 2px;
}
.editable .editable-inner span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-transform: capitalize;
}
.editable:hover > .editable-inner, .editable:focus > .editable-inner, .dd-input:hover, .dd-input:focus {
  border: 1px dashed rgb(196, 196, 196);
}
.dd-input {
  display: inline-block;
  border: 1px dashed transparent;
  background: transparent;
  color: inherit;
  text-align: center;
  text-transform: capitalize;
}
.dd-col-menu {
  visibility: hidden;
  display: inline-block;
  width: 16px;
  margin-left: 10px;
  background: transparent;
}
.dd-col-menu > a {
  background: #b7c0cd;
  border: none;
  color: #0C0C0C;
}
th:hover .dd-col-menu {
  visibility: visible;
}
th:hover .dd-col-menu > a {
  background-color: #b7c0cd;
  color: #0C0C0C;
}
.dd-header-input-w {
  width: calc(100% - 26px);
}
.dd-subheader-input-w {
  width: calc(100% - 36px);
}
.avatar-wrapper-s {
  width: 30px;
  height: 30px;
  margin: 0 auto;
}
.avatar-wrapper-s img {
  width: 100%;
}
.avatar-wrapper-s svg {
  font-size: 30px;
}
.show {
  visibility: visible;
}
/*
#wf-item {
  animation-name: revealMe;
  animation-direction: normal;
  animation-duration: 500ms;
  height: 690px;
}
@keyframes revealMe {
  from {height: 1px}
  to {height: 690px}
}
 */


</style>