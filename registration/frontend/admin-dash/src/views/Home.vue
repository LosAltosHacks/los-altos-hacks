<template>
  <div class="main">

    <div class="header">
    </div>
      <!-- <md-table class="fourthTable" md-sort="name" md-sort-order="asc" md-card>
        <thead>
          <md-table-row>
            <md-table-cell v-for="col in columnss" :key="col"><button @click="sortTable(col)">{{col}}</button></md-table-cell>
          </md-table-row>
        </thead>
        <tbody>
          <md-table-row v-for="row in info" :key="row">
            <md-table-cell v-for="col in columnss" :key="col"><md-field><md-input v-model="row[col]" @input="updateVal(row['user_id'], col, row[col])"></md-input></md-field></md-table-cell>
          </md-table-row>
        </tbody>
      </md-table> -->
      <md-table class="fourthTable" md-sort="name" md-sort-order="asc" md-card style="width: 90%; margin:auto; height: 10%" @md-selected="onSelect" v-model="info" :md-selected-value.sync="selectedd">
        <md-table-toolbar>
          <h1 class="md-title">Los Altos Hacks</h1>
          <md-field style="max-width:200px; padding:0px, 10px">
            <md-select v-model="selected" @md-selected="getSelectedData">
              <md-option value="attendees">Attendees</md-option>
              <md-option value="mentors">Mentors</md-option>
            </md-select>
          </md-field>
          <button class="logout" @click="logout">Logout</button>
        </md-table-toolbar>     
<!--             
          <md-table-row>
            <md-table-cell slot="md-table-row" slot-scope="{ item }"><button @click="sortTable(col)">{{item}}</button></md-table-cell>
          </md-table-row> -->
          <md-table-row slot="md-table-row" slot-scope="{ item }" md-selectable="multiple" md-auto-select>
            <md-table-cell md-label="Acceptance Status" md-sort-by="acceptance_status">
              <md-field>
                <md-select v-model="item.acceptance_status" @md-selected="updateVal(item['user_id'], 'acceptance_status', item.acceptance_status)">
                  <md-option value="accepted">Accepted</md-option>
                  <md-option value="rejected">Rejected</md-option>
                </md-select>
                </md-field>
              </md-table-cell>
            <md-table-cell md-label="First Name" md-sort-by="first_name"><md-field><md-input v-model="item.first_name" @input="updateVal(item['user_id'], 'first_name', item['first_name'])"></md-input></md-field></md-table-cell>
            <md-table-cell md-label="Last Name" md-sort-by="last_name"><md-field><md-input v-model="item.last_name" @input="updateVal(item['user_id'], 'last_name', item['last_name'])"></md-input></md-field></md-table-cell>
            <md-table-cell md-label="Email" md-sort-by="email"><md-field><md-input v-model="item.email" @input="updateVal(item['user_id'], 'email', item['email'])"></md-input></md-field></md-table-cell>
            <md-table-cell md-label="Timestamp" md-sort-by="timestamp"><md-field>{{item.timestamp}}</md-field></md-table-cell>
            <md-table-cell md-label="Functions"><md-button @click="show(item)" class="md-raised md-primary">Edit</md-button></md-table-cell>
            <bd-table-cell md-label="Delete"><md-button @click="deletePerson(item)">❌</md-button></bd-table-cell>
          </md-table-row>

          <!-- <md-table-row md-selectable="multiple" md-auto-select>
            <md-table-cell md-label="Name" md-sort-by="name">{{ info }}</md-table-cell>
          </md-table-row> -->
      </md-table>  
      
      <div style="margin:auto; width:fit-content">
        <md-button class="md-raised md-secondary" @click="acceptSelected">Accept Selected</md-button>
        <md-button class="md-raised md-secondary" @click="clearSelected">Clear Selected (Bug)</md-button>
        <md-button class="md-raised md-secondary" @click="showAddNew"></md-button>
      </div>

      
    <modal name="view-all-data" height="auto" :scrollable="true">
      <md-table class="fourthTable" md-sort="name" md-sort-order="asc" md-card>
        <!-- <thead>
          <md-table-row>
            <md-table-cell v-for="col in columnss" :key="col"><button @click="sortTable(col)">{{col}}</button></md-table-cell>
          </md-table-row>
        </thead> -->
          <md-table-toolbar>
            <h1 class="md-title">{{modalinfo['last_name']}}, {{modalinfo['first_name']}}</h1>
          </md-table-toolbar>
        <md-table-row v-for="col in columnss" :key="col">
          <!-- <p>{{row}}</p> -->
          <md-table-cell>{{col}}</md-table-cell>
          <md-table-cell><md-field><md-input v-model="modalinfo[col]" @input="updateVal(modalinfo['user_id'], col, modalinfo[col])"></md-input></md-field></md-table-cell>
          <!-- <md-table-cell v-for="col in columnss" :key="col"><md-field><md-input v-model="row[col]" @input="updateVal(row['user_id'], col, row[col])"></md-input></md-field></md-table-cell> -->
        </md-table-row>
      </md-table>
      <md-button class="md-raised md-primary" @click="close">Ok</md-button>
    </modal>

    <modal name="add-attendee" height="auto" :scrollable="true">
      <md-table>
          <md-table-toolbar>
            <h1>Add New Attendee</h1>
          </md-table-toolbar>
        <md-table-row v-for="col in columnss" :key="col">
          <!-- <p>{{row}}</p> -->
          <md-table-cell>{{col}}</md-table-cell>
          <md-table-cell><md-field><md-input v-model="newAttendee[col]"></md-input></md-field></md-table-cell>
          <!-- <md-table-cell v-for="col in columnss" :key="col"><md-field><md-input v-model="row[col]" @input="updateVal(row['user_id'], col, row[col])"></md-input></md-field></md-table-cell> -->
        </md-table-row>
      </md-table>
      <md-button class="md-raised md-primary" @click="addAttendee">Add</md-button>
    </modal>

  </div>
</template>

<script>
import axios from 'axios'
import store from '../store';
export default {
  data() {
    return{
      age: 1,
      selectedd: [],
      newAttendee: [],
      ascending: false,
      info: [],
      sortColumn: '',
      modalinfo: '',
      selected: ['attendees'],
      columns: [ 'user_id', 'education', 'signed_waiver', 'previous_hackathons', 
      'first_name', 'school', 'outdated', 'github_username', 'last_name', 'grade', 
      'timestamp', 'linkedin_profile', 'email', 'phone_number', 'goals', 'email_token', 
      'guardian_name', 'id', 'special', 'email_verified', 'guardian_email', 'tshirt_size', 
      'guardian_phone_number', 'age', 'ethnicity', 'dietary_restrictions', 'gender', 'acceptance_status'],
      actualcols: ['acceptance_status', 'first_name', 'last_name', 'email', 'timestamp'],
      mentordata: [
      { id: 1, name: "Chandler Bing", phone: '305-917-1301', profession: 'IT Manager' },
      { id: 2, name: "Ross Geller", phone: '210-684-8953', profession: 'Paleontologist' },
      { id: 3, name: "Rachel Green", phone: '765-338-0312', profession: 'Waitress'},
      { id: 4, name: "Monica Geller", phone: '714-541-3336', profession: 'Head Chef' },
      { id: 5, name: "Joey Tribbiani", phone: '972-297-6037', profession: 'Actor' },
      { id: 6, name: "Phoebe Buffay", phone: '760-318-8376', profession: 'Masseuse' }
    ]
    }
  },
  name: 'home',
  created(){
    this.getSelectedData();
  },
  methods: {
    showAddNew(){
      this.$modal.show("add-attendee");
    },
    addAttendee(){
      const data = this.newAttendee;
      const config = {
        headers: {'Authorization': "bearer " + store.state.token}
      };
      axios.post('http://localhost:8000/attendees/', data, config)
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    },
    deletePerson(i){
      const config = {
        headers: {'Authorization': "bearer " + store.state.token}
      };
      axios.delete('http://localhost:8000/attendees/' + i.user_id, config).then(function (response){console.log(response)});
    },
    clearSelected(){
      console.log(this.selectedd);
      this.selectedd = []
      console.log(this.selectedd);
    },
    close(){
      this.$modal.hide('view-all-data');
      this.modalinfo = '';
    },
    show(i){
      this.modalinfo = i;
      console.log(this.modalinfo)
      this.getHistory(i);
      this.$modal.show('view-all-data');
    },
    getHistory(i){
      const config = {
        headers: {'Authorization': "bearer " + store.state.token}
      };
      axios.get('http://localhost:8000/attendees/' + i.user_id + '/history', config)
      .then(function (response) {
        console.log('history');
        console.log(response);
      })
    },
    acceptSelected(){
      let i = 0; 
      for(i; i < this.selectedd.length; i++){
        this.updateVal(this.selectedd[i].user_id, 'acceptance_status', 'accepted');
      }
      this.$router.go();
    },
    onSelect (items) {
      this.selectedd = items
    },
    test(){
      console.log('test');
    },
    "sortTable": function sortTable(col) {
      if (this.sortColumn === col) {
        this.ascending = !this.ascending;
      } else {
        this.ascending = true;
        this.sortColumn = col;
      }

      var ascending = this.ascending;

      this.info.sort(function(a, b) {
        if (a[col] > b[col]) {
          return ascending ? 1 : -1
        } else if (a[col] < b[col]) {
          return ascending ? -1 : 1
        }
        return 0;
      })
    },
    getSelectedData(){
      this.clear();
      if(this.selected.includes('attendees')){
        this.getaAtendees();
      } 
      if(this.selected.includes("mentors")){
        this.getMentors();
      }
      console.log(this.selected);
      if(this.selected.length == 0){
        this.info = [];
      }
      console.log(this.info);
    },
    clear(){
      this.info = [];
    },
    styleData(){
      var i;
      for(i = 0; i < this.info.length; i++){
        console.log();
      }
    },
    logout() {
        this.$store.dispatch('logout')
        .then(() => {
          this.$router.push('/login')
        })
    },
    updateVal(user_id, column, value){
      console.log(user_id, column, value)
      var config = {
        headers: {'Authorization': "bearer " + store.state.token,}
      };
      console.log(user_id, column, value);
      const finalurl = 'http://localhost:8000/attendees/' + user_id;
      const finalpayload = JSON.stringify({[column]:value});
      console.log(finalpayload);
      axios.patch(finalurl, finalpayload, config)
    },
    getMentors(){
      // const self = this;
      // var config = {
      //   headers: {'Authorization': "bearer " + store.state.token}
      // };
      // axios.get('http://localhost:8000/attendees/', config, {
      // headers: { 'Access-Control-Allow-Origin': '*',}})
      // .then(function (response) {
      //   var i;
      //   for(i = 0; i < response.data.length; i++){
      //     self.info.push(response.data[i]);
      //   }
      // })
      this.info = this.mentordata;
      console.log('Info: ');
      console.log(this.info);
    },
    getaAtendees(){
      const self = this;
      var config = {
        headers: {'Authorization': "bearer " + store.state.token}
      };
      axios.get('http://localhost:8000/attendees/', config, {
      headers: { 'Access-Control-Allow-Origin': '*',}})
      .then(function (response) {
        console.log(response)
        self.info = response.data;
        console.log(self.info);
      })
    }
  },
  computed: {
  "columnss": function columnss() {
      if (this.info.length == 0) {
        return [];
      }
      console.log('cols');
      console.log(Object.keys(this.info[0]))
      return Object.keys(this.info[0])
    }
  }
}
</script>

<style lang="css">

button .logout {
  font-family: "Roboto", sans-serif;
  text-transform: uppercase;
  outline: 0;
  background: #5F80FF;
  width: 10%;
  border: 0;
  padding: 15px;
  color: #FFFFFF;
  font-size: 14px;
  -webkit-transition: all 0.3 ease;
  transition: all 0.3 ease;
  cursor: pointer;
}

/* button {
  color: #FFFFFF;
  background: linear-gradient(90deg, rgba(52,32,158,1) 0%, rgba(48,48,217,1) 26%, rgba(0,212,255,1) 100%);
} */

button:hover {
  background: #466AFF;
}

.md-menu{
  max-width: 200px;
}


.header{
  width: 100%;
  align-self: auto;
}
.md-table-cell-container {
    padding: 0px, 10px !important;
    text-align: center; 
    vertical-align: middle;
  }
  .md-table-head{
    padding-right: 0px !important;
    text-align: center; 
    vertical-align: middle;
  }
  .md-table-cell {
    text-align: center; 
    vertical-align: middle;
  }
</style>
