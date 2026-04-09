<template>
    <FormShell v-if="$store.state.init_data"
    :clear-func="clear_func"
    :heading="$route.params.type.charAt(0).toUpperCase() + $route.params.type.slice(1) + ' data request'"
    :form-type="route_type"
    :ticket_id="ticket_id"

    >

     
       <v-stepper
          v-model="step_num"
          vertical
       >
       <v-stepper-step
      :complete="step_num > 1"
      step="1"
      >
       Employee HR info
      </v-stepper-step>

      <StepShell
       ref="step1"
       step_num="1"
       :next_page="next_page"
       >

         <v-row>

           <v-col cols="6">
               <v-text-field
                  maxlength="50"
                  v-model="employee_name"
                  label="Employee full name"
                  counter="50"
                  :rules="[v => !!v || 'Employee full name is required']"
                  />
            </v-col>
            <v-col cols="6">
               <v-text-field
                  maxlength="50"
                  v-model="employee_net_id"
                  v-bind:counter="50"
                  label="Employee net id (optional)"
                  :rules="netID_Rules"/>
            </v-col>
         </v-row>
         <v-row>
            <v-col cols="6">
            <v-menu
        v-model="date_menu"
        :close-on-content-click="false"
        :nudge-right="40"
        transition="scale-transition"
        offset-y
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
            v-model="start_date"
            label="Start date"
            prepend-icon="mdi-calendar"
            readonly
            v-bind="attrs"
            v-on="on"
            clearable
            :rules="startDateRules"
          ></v-text-field>
        </template>
        <v-date-picker
          v-model="start_date"
          @input="date_menu = false"
        ></v-date-picker>
      </v-menu>
            </v-col>
         </v-row>
         

      </StepShell>
         <v-stepper-step
       :complete="step_num > 2"
       step="2"
      >
         Employee position information
      </v-stepper-step>
      
      <StepShell
       ref="step2"
       step_num="2"
       :next_page="next_page"
       :prev_page="prev_page"
       >
                
            <v-row>
            <v-col cols="12">
               <p>
                    Is the new hire replacing a former/outgoing one?
                    <v-btn-toggle 
                     v-model="replacement_pos"
                     mandatory>
                       <v-btn>
                          Yes
                       </v-btn>
                       <v-btn>
                          No
                       </v-btn>
                    </v-btn-toggle>
               </p>
            </v-col>
         </v-row>
         <v-row>
            <v-col cols="12">
               <p v-if="replacement_pos==0" > 
                  <v-text-field
                  maxlength="50"
                  v-model="former_employee"
                  label="Please provide the name of the former/outgoing employee"
                  counter="50"
                  :rules="[v => !!v || 'Answer is required']"
                  />
               </p>
            </v-col>
         </v-row>
         <v-row>
         <v-col cols="12">
            <h4>Please select an employee position</h4>
         <v-input 
                   :rules="[v=>v.length>0 || 'You must select a job title']"
                   :value="job_title_ids"
                 > 
           

           
            <v-container 
            :style="{'border-style':'solid','border-width':'2px','border-radius':'5px','padding':'3px'}"
            
            >      
            <v-treeview
                   
             ref="job_tree"
             :items="org_tree.org_tree"
             activatable
             open-on-click
             :active.sync="job_title_ids"
            >
         
            </v-treeview>

            </v-container>

              



        


               </v-input>
               </v-col>
            </v-row>

               <v-text-field v-if="other_job_title_selected"
               label="Please provide a brief description of the employee position"
               :counter="100"
               :rules = "[v=>!!v || 'Input required']"
               v-model="position_descr"
               >
               </v-text-field>

               <v-combobox
            v-model="selected_roles"
            :items="role_choices"
            label="Select any appropriate employee roles (e.g. 'OSAP Programs') from the drop down and/or enter them in manually."
            multiple
            chips
            clearable
          />

            </StepShell>

         <v-stepper-step
       step="3"
       :complete="step_num > 3"
      >
         Employee work-model and location information.
      </v-stepper-step>
      <StepShell
      ref="step3"
       step_num="3"
       :next_page="next_page"
       :prev_page="prev_page"
       >
 
                <h3>What is the new employee's work model?</h3>
                <v-radio-group v-model="work_model_selection">
                  <v-radio
                   v-for="work_model in work_models"
                   :key="work_model"
                   :label="xlat[work_model]"
                   :value="work_model"
                   
                  >
                  </v-radio>
                </v-radio-group>
                <div v-if="work_model_selection != 'remote'">
                <h3>Where in the office will the new employee require an in-office setup?</h3>
                <v-radio-group v-model="room_selection">
                  <v-radio
                   v-for="room in rooms"
                   :key="room"
                   :label="xlat[room]"
                   :value="room"
                   
                  >
                  </v-radio>
                </v-radio-group>
                <h3>Whereabouts in <b>{{xlat[room_selection]}}</b> will the new employee's workstation be situated? (Optional)</h3>
               <v-text-field
               label="Provide a description"
               :counter="100"
               v-model="room_sublocation"
               >
               </v-text-field>
           



               </div>
            </StepShell>

         <v-stepper-step
       step="4"
       :complete="step_num > 4"
      >
         Employee hardware requirements.

      
      </v-stepper-step>
      <StepShell
       ref="step4"
       step_num="4"
       :next_page="next_page"
       :prev_page="prev_page"
       >
      
                <h3>What hardware configuration should the new employee have?</h3>
                <v-radio-group v-model="hw_choice">
                  <v-radio
                   v-for="hw_config in (work_model_selection=='hybrid')?hw_choices['hybrid']:hw_choices['other']"
                   :key="hw_config"
                   :label="xlat[hw_config]"
                   :value="hw_config"
                   
                  >
                  </v-radio>
                </v-radio-group>
                <div v-if="hw_choice=='hw_choice2' || hw_choice=='hw_choice4'">
                <h3>Why does the new employee require a laptop?</h3>

                <v-text-field
               label="Please provide a brief explanation."
               :counter="100"
               :rules = "[v=>!!v || 'Input required']"
               v-model="laptop_explanation"
               >
               </v-text-field>
               </div>
               <h3>Specify any additional hardware requirements</h3>
               <v-textarea
               outlined
               v-model="extra_hardware_reqs"
               maxlength="200"
        ></v-textarea>
            </StepShell>










            <v-stepper-step
       step="5"
       :complete="step_num > 5"
      >
         Employee phone requirements.

      
      </v-stepper-step>
      <StepShell
       ref="step5"
       step_num="5"
       :next_page="next_page"
       :prev_page="prev_page"
       
       >

       <h3>Personal phone extension options</h3>
                <v-radio-group v-model="phone_ext_choice">
                  <v-radio
                   v-for="choice in phone_ext_options"
                   :key="choice"
                   :label="xlat[choice]"
                   :value="choice"
                   
                  >
                  </v-radio>
                </v-radio-group>

      <h3>Shared telephone groups</h3>

      <v-alert
      border="top"
      colored-border
      type="info"
      elevation="2"
    >
      A <i>call queue</i> routes calls to each line in a set of telephone lines sequentially.
      A <i>ring group</i> routes calls to all lines in a set of a set of telephone lines simultaenously.
   </v-alert>
    <h4>Call queues</h4>
      <v-combobox
                  v-model="call_queues"
                  :items="[]"
                 label="Enter in any call queues the new employees' telephone line should belong to."
                 multiple
                 chips
                 clearable
          />
          <h4>Ring groups</h4>
      <v-combobox
                  v-model="ring_groups"
                  :items="[]"
                 label="Enter in any ring groups the new employees' telephone line should belong to."
                 multiple
                 chips
                 clearable
          />
            </StepShell>





















         <v-stepper-step
       step="6"
       :complete="step_num > 6"
      >
         Supplemental Printers.
      </v-stepper-step>

      <StepShell
       ref="step6"
       step_num="6"
       :next_page="next_page"
       :prev_page="prev_page"
       >
                <h3>Select any needed supplementary printers needed by the new employee</h3>
                <v-checkbox 
                  v-for="supp_print in supp_prints" 
                  multiple 
                  v-model="supp_print_choice" 
                 :key="supp_print" 
                 :value="supp_print" 
                 :label="xlat[supp_print]"
                 hide-details
                  />
        </StepShell>
         <v-stepper-step
       step="7"
       :complete="step_num > 7"
      >
         File share locations.
      </v-stepper-step>
      <StepShell
       ref="step7"
       step_num="7"
       :next_page="next_page"
       :prev_page="prev_page"
       >
                <h3>Enter in any required file locations</h3>

                <v-combobox
                  v-model="selected_file_shares"
                  :items="[]"
                 label="Enter in any required file share locations"
                 multiple
                 chips
                 clearable
          />

   </StepShell>

         <v-stepper-step
       step="8"
       :complete="step_num > 8"
      >
         Supplementary mailing lists and shared email accounts.
      </v-stepper-step>
      <StepShell
       ref="step8"
       step_num="8"
       :next_page="next_page"
       :prev_page="prev_page"
       >

                <h3>Supplementary mailing lists</h3>
                <v-checkbox 
                  ref="supp_ml_ref"
                  v-for="supp_ml in supp_mls" 
                  multiple 
                  v-model="supp_ml_choice" 
                 :key="supp_ml" 
                 :value="supp_ml" 
                 :label="xlat[supp_ml]"
                 hide-details
                  />
                  <br/>
                  <h3>Shared email accounts</h3>
               <v-combobox
                ref="shared_emails_ref"
                v-model="shared_emails"
               :items="[]"
               multiple
               chips 
               clearable
               :rules="shared_email_rules">
             <template v-slot:label>
               Enter in any shared email accounts required by the new employee (e.g <i>timetabl@queensu.ca)</i>
             </template>
            </v-combobox>
   </StepShell>

   <v-stepper-step
       step="9"
       :complete="step_num > 9"
      >
         Supplemental specialised software items.
      </v-stepper-step>
      <StepShell
       ref="step9"
       step_num="9"
       :next_page="next_page"
       :prev_page="prev_page"
       >
                <v-combobox
                  v-model="spec_software_items"
                  :items="[]"
                 label="Enter in any required supplemental specialised software items"
                 multiple
                 chips
                 clearable
          />

   </StepShell>

         <v-stepper-step
       step="10"
      >
         Review and submit
      </v-stepper-step>
      <StepShell
       ref="step10"
       step_num="10"
       :prev_page="prev_page"
       submission_step
       :submission_data="submission_data"
       submit_button_label="SUBMIT ONBOARDING REQUEST"
       @ticket_id_set="set_ticket_id"
       >



       <v-row style="background-color:#0D47A1;color:white">
         <v-col cols="1">1.</v-col>
         <v-col cols="11"><h4 >Employee HR Info</h4></v-col>
      </v-row>
      <v-row>
         <v-col></v-col>
         <v-col cols="11">
         <dl>
         <dt><b>Employee full name</b></dt>
         <dd>
            {{ submission_data.json.employee_name }}
         </dd>
         <dt v-if="'employee_net_id' in submission_data.json"><b>Employee net id</b></dt>
         <dd v-if="'employee_net_id' in submission_data.json">
            {{ submission_data.json.employee_net_id }}
         </dd>
         <dt><b>Start date</b></dt>
         <dd>
            {{ submission_data.json.start_date }}
         </dd>
         </dl>
         </v-col>
      </v-row>
      <v-row style="background-color:#0D47A1;color:white">
         <v-col cols="1">2.</v-col>
         <v-col cols="11"><h4 >Employee Position Info</h4></v-col>
      </v-row>
      <v-row>
         <v-col></v-col>
         <v-col cols="11">
         <dl>
         <dt><b>Is the employee replacing a former/outgoing one?</b></dt>
         <dd>
            {{ (submission_data.json.replacement_pos)?"Yes":"No" }}
         </dd>
         <dt v-if="submission_data.json.replacement_pos"><b>Name of former/outgoing employee</b></dt>
         <dd v-if="submission_data.json.replacement_pos">
            {{ submission_data.json.former_employee }}
         </dd>
         <dt><b>Employee position</b></dt>
         <dd v-if="submission_data.json.job_title_path && submission_data.json.job_title_path.job_title_type=='standard'">
            {{ submission_data.json.job_title_path.job_title_path.map(x => xlat[x]).join(" >> ") }}
         </dd>
         <dd v-else-if="submission_data.json.job_title_path">
            {{ submission_data.json.job_title_path.position_descr}} <i>(manually input)</i>
         </dd>
         <dt v-if="'selected_roles' in submission_data.json"><b>Job roles</b></dt>
         <dd v-if="('selected_roles' in submission_data.json)">
            <ul>
               <li
                v-for="(role,index) in selected_roles"
                :key="index"
               >
                  {{ role }}
               </li>
            </ul>
         </dd>
         </dl>
         </v-col>
      </v-row>
      <v-row style="background-color:#0D47A1;color:white">
         <v-col cols="1">3.</v-col>
         <v-col cols="11"><h4 >Employee Work-Model and Location Info</h4></v-col>
      </v-row>
      <v-row>
         <v-col></v-col>
         <v-col cols="11">
         <dl>
         <dt><b>Employee work model</b></dt>
         <dd>
            {{ xlat[submission_data.json.work_model_selection] }}
         </dd>
         <dt v-if="'room_selection' in submission_data.json"><b>Employee in-office location</b></dt>
         <dd v-if="'room_selection' in submission_data.json">
            {{ xlat[submission_data.json.room_selection] }}
         </dd>
         <dt v-if="'room_sublocation' in submission_data.json"><b>Employee sublocation</b></dt>
         <dd v-if="'room_sublocation' in submission_data.json">
            {{ submission_data.json.room_sublocation }}
         </dd>
         

         </dl>
         </v-col>
      </v-row>
      
      <v-row style="background-color:#0D47A1;color:white">
         <v-col cols="1">4.</v-col>
         <v-col cols="11"><h4 >Employee Hardware Requirements</h4></v-col>
      </v-row>
      <v-row>
         <v-col></v-col>
         <v-col cols="11">
         <dl>
         <dt><b>Employee hardware configuration</b></dt>
         <dd>
            {{ xlat[submission_data.json.hw_choice] }}
         </dd>
         <dt v-if="'laptop_explanation' in submission_data.json"><b>Reason for provision of laptop</b></dt>
         <dd v-if="'laptop_explanation' in submission_data.json">
            {{ submission_data.json.laptop_explanation }}
         </dd>
         <dt v-if="'extra_hardware_reqs' in submission_data.json"><b>Extra hardware requirements</b></dt>
         <dd v-if="'extra_hardware_reqs' in submission_data.json">
            {{ submission_data.json.extra_hardware_reqs }}
         </dd>



         </dl>
         </v-col>
      </v-row>

      <v-row style="background-color:#0D47A1;color:white">
         <v-col cols="1">5.</v-col>
         <v-col cols="11"><h4 >Employee Phone Requirements</h4></v-col>
      </v-row>
      <v-row>
         <v-col></v-col>
         <v-col cols="11">
         <dl>
           <dt v-if="'phone_ext_choice' in submission_data.json"><b>Personal phone extension info</b></dt>
           <dd v-if="'phone_ext_choice' in submission_data.json">
            {{ xlat[submission_data.json.phone_ext_choice] }}
           </dd>
           <dt v-if="'call_queues' in submission_data.json"><b>Call queues</b></dt>
           <dd v-if="'call_queues' in submission_data.json">
            <ul>
               <li
                v-for="(call_queue,index) in submission_data.json.call_queues"
                :key="index"
               >
                  {{ call_queue }}
               </li>
            </ul>
           </dd>
           
           <dt v-if="'ring_groups' in submission_data.json"><b>Ring groups</b></dt>
           <dd v-if="'ring_groups' in submission_data.json">
            <ul>
               <li
                v-for="(ring_group,index) in submission_data.json.ring_groups"
                :key="index"
               >
                  {{ ring_group }}
               </li>
            </ul>
           </dd>

         </dl>
         </v-col>
      </v-row>



      <v-row style="background-color:#0D47A1;color:white">
         <v-col cols="1">6.</v-col>
         <v-col cols="11"><h4 >Supplemental Printers</h4></v-col>
      </v-row>
      <v-row>
         <v-col></v-col>
         <v-col cols="11">
         <dl>
         <dt v-if="'supp_print_choice' in submission_data.json"><b>Supplemental printers needed by new employee</b></dt>
         <dd v-if="'supp_print_choice' in submission_data.json">
            <ul>
               <li
                v-for="(supp_prnt,index) in submission_data.json.supp_print_choice"
                :key="index"
               >
                  {{ xlat[supp_prnt] }}
               </li>
            </ul>
         </dd>
         </dl>
         </v-col>
      </v-row>
      <v-row style="background-color:#0D47A1;color:white">
         <v-col cols="1">7.</v-col>
         <v-col cols="11"><h4 >File Share Locations</h4></v-col>
      </v-row>
      <v-row>
         <v-col></v-col>
         <v-col cols="11">
         <dl>
         <dt v-if="'selected_file_shares' in submission_data.json"><b>File share locations needed by new employee</b></dt>
         <dd v-if="'selected_file_shares' in submission_data.json">
            <ul>
               <li
                v-for="(selected_file_share,index) in submission_data.json.selected_file_shares"
                :key="index"
               >
                  {{ selected_file_share }}
               </li>
            </ul>
         </dd>
         </dl>
         </v-col>
      </v-row>
      <v-row style="background-color:#0D47A1;color:white">
         <v-col cols="1">8.</v-col>
         <v-col cols="11"><h4 >Supplementary Mailing Lists and Shared Email Accounts</h4></v-col>
      </v-row>
      <v-row>
         <v-col></v-col>
         <v-col cols="11">
         <dl>
         <dt v-if="'supp_ml_choice' in submission_data.json"><b>Supplementary mailing lists needed by new employee</b></dt>
         <dd v-if="'supp_ml_choice' in submission_data.json">
            <ul>
               <li
                v-for="(selected_ml,index) in submission_data.json.supp_ml_choice"
                :key="index"
               >
                  {{ xlat[selected_ml] }}
               </li>
            </ul>
         </dd>
         <dt v-if="'shared_emails' in submission_data.json"><b>Shared email accounts needed by new employee</b></dt>
         <dd v-if="'shared_emails' in submission_data.json">
            <ul>
               <li
                v-for="(shared_email,index) in submission_data.json.shared_emails"
                :key="index"
               >
                  {{ shared_email }}
               </li>
            </ul>
         </dd>
         </dl>
         </v-col>
      </v-row>
      <v-row style="background-color:#0D47A1;color:white">
         <v-col cols="1">9.</v-col>
         <v-col cols="11"><h4 >Supplementary Specialised Software Items</h4></v-col>
      </v-row>
      <v-row>
         <v-col></v-col>
         <v-col cols="11">
         <dl>
         <dt v-if="'spec_software_items' in submission_data.json"><b>Supplementary specialised software items required by new employee</b></dt>
         <dd v-if="'spec_software_items' in submission_data.json">
            <ul>
               <li
                v-for="(selected_item,index) in submission_data.json.spec_software_items"
                :key="index"
               >
                  {{ selected_item }}
               </li>
            </ul>
         </dd>
         </dl>
         </v-col>
      </v-row>

      </StepShell>


      </v-stepper>


   </FormShell>
</template>



<script>
  
import FormShell from '../components/FormShell'
import StepShell from '../components/StepShell.vue'


export default {
   name: 'OnboardingForm',
   components: { 
      FormShell,
      StepShell,
      // SelectFields,
   },
   data: function() {
      const route_type=this.$route.params.type;

      // console.log(this.$store.state.init_data);

      
      const total_steps=8;

      return {
         job_title_ids: [],


         replacement_pos: 0,
         former_employee: "",
         start_date: '',
         netID_Rules: [
            v => /^([a-z0-9])*$/.test(v) || "Must be lower-case alphanumeric"
         ],
         employeeNameRules: [
            //
         ],

         startDateRules: [
            v => !!v || "Start date is required"
         ],

         route_type: route_type,
         step_num: 1,
         total_steps: total_steps,
         employee_name: "",
         employee_net_id: "",
         date_menu: false,
         position_descr: "",
         selected_roles: [],
         work_model_selection: "hybrid",
         room_selection: "gor110",
         room_sublocation: "",
         phone_ext_choice: "has_phone_not_required",
         hw_choice: "hw_choice1",
         hw_choice_selection: "hybrid",
         laptop_explanation: "",
         supp_print_choice: [],
         supp_ml_choice: [],
         selected_file_shares: [],
         reset_funcs: [],
         //reset_funcs: new Array(total_steps-1),
         ticket_id: null,
         extra_hardware_reqs: "",
         call_queues: [],
         ring_groups: [],
         spec_software_items: [],
         shared_emails: [],
         shared_email_rules: [
            v => {
               var email;
               for (email of v){
                  if (!(/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/).test(email)){
                     return `Invalid email: '${email}'` 
                  }
               }
               return true;
            }
         ]

      };
   },
   methods: {
      //reset_func_set: function(page_num,event){
         // this.reset_funcs[page_num]=event;
         //don't do anyhing

      //},
      set_ticket_id: function(ticket_id){
         this.ticket_id=ticket_id;
      },

      next_page: function(){
         this.step_num++;
      },
      prev_page: function(){
         this.step_num--;
      },

      clear_func(){

         this.start_date='';
         this.job_title_ids=[];
         this.employee_name='';
         this.employee_net_id='';
         this.replacement_pos=0;
         this.step_num=1;
         this.former_employee='';
         this.position_descr='';
         this.selected_roles=[];
         this.work_model_select="hybrid";
         this.room_selection="gor110";
         this.room_sublocation="";
         this.phone_ext_choice="has_phone_not_required";
         this.hw_choice_selection="hw_choice1";
         this.laptop_explanation="";
         this.supp_print_choice="";
         this.supp_ml_choice="";
         this.selected_file_shares=[];
         this.extra_hardware_reqs="";
         this.call_queues=[];
         this.ring_groups=[];
         this.spec_software_items=[];
         this.shared_emails=[];

         this.$refs.job_tree.updateAll(false);

         var reset_func;
         for (reset_func of this.reset_funcs){
            reset_func();
         }
      }

   },
   computed:{
      role_choices: function(){
         if (this.job_title_ids.length==0 || this.other_job_title_selected){
            return [];

         }else{
            const job_title_id = this.job_title_ids[0];
            const path=this.org_tree.job_title_id_map[job_title_id];
            console.log(path);
            var child=this.org_tree.org_tree_init;
            console.log(child)
            var new_child;
            var element;
            for (element of path){
               new_child=child[element];
               console.log("ELEMENT IS");
               console.log(element);
               child = new_child;
               console.log("CHILD IS");
               console.log(child);
            }
            //return child;
            return child.map(x=>this.xlat[x]);

         }
      },

      other_job_title_selected: function(){
         if (this.job_title_ids.length>0){
            const job_title_id = this.job_title_ids[0];
            return job_title_id == this.org_tree.job_title_id_map.length;
         }else{
            return false;
         }
      },

      job_title_path: function() {
         if (this.job_title_ids.length>0){
            if (this.other_job_title_selected){
               return {
                  job_title_type: "other",
                  position_descr: this.position_descr
               };
            }else{
               const job_title_id = this.job_title_ids[0];
               return{
                  job_title_type: "standard",
                  job_title_path: this.org_tree.job_title_id_map[job_title_id]
               }
            }
         }else{
            return null;
         }
      },

      submission_display: function() {
         return this.submission_data();
      },

   

      xlat: function(){
         return this.$store.state.init_data.xlat;
      },
      org_tree: function(){
         var job_title_id_map = [];
         const org_tree_init = this.$store.state.init_data.org_tree;

      
         function build_tree_data (parent_path,org_tree,xlat){
            var result_list=[];
            var live_id_count=job_title_id_map.length;
            for (const key of Object.keys(org_tree)){
               var new_path = [...parent_path]
               new_path.push(key);
               job_title_id_map.push(new_path);
               const label=xlat[key]
               const child=org_tree[key];
               var children;
               if (child.constructor!=Array){
                  children = build_tree_data(new_path,child,xlat);
               }else{
                  children=[];
               }
               const result_obj = {
                  id: live_id_count,
                  name: label,
                  children: children
               }
               result_list.push(result_obj);
               live_id_count=job_title_id_map.length;
            }
            return result_list
         }


         var org_tree_data = build_tree_data([],org_tree_init,this.xlat);



         org_tree_data.push({
            id: job_title_id_map.length,
            name: "Other...",
            children: []
         });
         return {
            org_tree_init: org_tree_init, 
            org_tree: org_tree_data,
            job_title_id_map: job_title_id_map
         }

      },
      work_models: function(){
         return this.$store.state.init_data.work_models;
      },
      rooms: function(){
         return this.$store.state.init_data.rooms;
      },
      phone_ext_options: function (){
         return this.$store.state.init_data.phone_extensions;
      },

      hw_choices: function (){
         return this.$store.state.init_data.hw_choices;
      },

      supp_prints: function (){
         return this.$store.state.init_data.supp_prnts;
      },

      supp_mls: function(){
         return this.$store.state.init_data.supp_mls;
      },
      field_dict: function(){
         // var field_listX;
         // if ("standard_fields" in this.$store.state.init_data){
         //   field_listX = this.$store.state.init_data.standard_fields[this.$route.params.type];
         // }else{
         //   field_listX = [];
         //}
         const field_list = this.$store.state.init_data.standard_fields[this.$route.params.type];
         var field_dict = {};
         var i;
         for (i=0;i<field_list.length;i++){
            const this_field = field_list[i];
            field_dict[this_field]= this.$store.state.init_data.field_defs[this_field];
         }
         return field_dict;

      },

      submission_data: function(){


         var json= { 
               start_date: this.start_date,
               employee_name: this.employee_name,
               job_title_path: this.job_title_path,
               replacement_pos: !this.replacement_pos,
               work_model_selection: this.work_model_selection,
               hw_choice: this.hw_choice
         };
         if(this.selected_roles.length>0){
            json.selected_roles=this.selected_roles;
         }
         if(this.employee_net_id){
            json.employee_net_id=this.employee_net_id;
         }
         if(!this.replacement_pos){
            json.former_employee=this.former_employee;
         }
         if(this.work_model_selection!="remote"){
            json.room_selection=this.room_selection;
            if(this.room_sublocation){
               json.room_sublocation=this.room_sublocation;
            }
         }
         json.phone_ext_choice=this.phone_ext_choice;
         if(this.call_queues.length>0){
               json.call_queues=this.call_queues;
         }
         if (this.ring_groups.length>0){
               json.ring_groups=this.ring_groups;
         }
         if(this.hw_choice=="hw_choice2" || this.hw_choice=="hw_choice4"){
            json.laptop_explanation=this.laptop_explanation;
         }
         if(this.extra_hardware_reqs){
            json.extra_hardware_reqs=this.extra_hardware_reqs
         }
         if(this.supp_print_choice.length>0){
            json.supp_print_choice=this.supp_print_choice;
         }
         if(this.selected_file_shares.length>0){
            json.selected_file_shares=this.selected_file_shares;
         }
         if(this.spec_software_items.length>0){
            json.spec_software_items=this.spec_software_items;
         }


         if(this.supp_ml_choice.length>0){
            json.supp_ml_choice=this.supp_ml_choice;
         }
         
         if(this.shared_emails.length>0){
            json.shared_emails=this.shared_emails;
         }
         

 

         var content_data = {
            json: json,
            attachments: []
         };

         return content_data;
      }

      
   },

   watch:{ 
      work_model_selection(new_val,old_val){
         console.log(old_val);
         console.log(new_val);
         if(old_val=="hybrid" && new_val != "hybrid"){
            this.hw_choice="hw_choice3"
         }else if (old_val != "hybrid" && new_val == "hybrid"){
            this.hw_choice="hw_choice1"
         }
      },
   },
   async mounted(){
      this.reset_funcs=[
         this.$refs.step1.reset_step,
         this.$refs.step2.reset_step,
         this.$refs.step3.reset_step,
         this.$refs.step4.reset_step,
         this.$refs.step5.reset_step,
         this.$refs.step6.reset_step,
         this.$refs.step7.reset_step,
         this.$refs.step8.reset_step,
         this.$refs.step9.reset_step
      ];
                
   },
}
</script>



