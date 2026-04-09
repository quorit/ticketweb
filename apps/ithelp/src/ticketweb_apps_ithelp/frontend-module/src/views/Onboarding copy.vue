<template>
<FormShell
 :clear-func="clear_func"
 :heading="$route.params.type.charAt(0).toUpperCase() + $route.params.type.slice(1) + ' data request'"
 :init-data="init_data"
 :form-type="route_type"
>  
   <v-stepper
    v-model="step_num"
    vertical
   >
      <StepShell
       step_num="1"
       next_page="next_page"
       prev_page="prev_page"
       submit_button_label="SUBMIT YOUR REQUEST"
       :submission-data="submission_data"
       step_header="Employee info"
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
      
         <v-stepper-content step="2">
            <v-form
                ref="form2"
                v-model="form_valid[1]"
                lazy-evaluation>
                
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
                   
            
             :items="tree_data"
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
            </v-form>

         </v-stepper-content>

         <v-stepper-step
       step="3"
       :complete="step_num > 3"
      >
         Employee work-model and location information.
      </v-stepper-step>
         <v-stepper-content step="3">
            <v-form
                ref="form3"
                v-model="form_valid[2]"
                lazy-evaluation>
      
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



               </div>
            </v-form>
         </v-stepper-content>

         <v-stepper-step
       step="4"
       :complete="step_num > 4"
      >
         Employee hardware requirements.
      </v-stepper-step>
         <v-stepper-content step="4">
            <v-form
                ref="form4"
                v-model="form_valid[3]"
                lazy-evaluation>
      
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
               v-model="position_descr"
               >
               </v-text-field>
               </div>
            </v-form>
         </v-stepper-content>
         <v-stepper-step
       step="5"
       :complete="step_num > 5"
      >
         Supplemental Printers.
      </v-stepper-step>
         <v-stepper-content step="5">
            <v-form
                ref="form5"
                v-model="form_valid[4]"
                lazy-evaluation>
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
            </v-form>
         </v-stepper-content>
         <v-stepper-step
       step="6"
       :complete="step_num > 6"
      >
         File share locations.
      </v-stepper-step>
         <v-stepper-content step="6">
            <v-form
                ref="form6"
                v-model="form_valid[5]"
                lazy-evaluation>
                <h3>Enter in any required file locations</h3>

                <v-combobox
                  v-model="selected_roles"
                  :items="role_choices"
                 label="Enter in any required file share locations"
                 multiple
                 chips
                 clearable
          />

            </v-form>
         </v-stepper-content>

         <v-stepper-step
       step="7"
       :complete="step_num > 7"
      >
         Supplementary mailing lists.
      </v-stepper-step>
         <v-stepper-content step="7">
            <v-form
                ref="form7"
                v-model="form_valid[6]"
                lazy-evaluation>
                <h3>Select any needed supplementary mailing lists needed by the new employee</h3>
                <v-checkbox 
                  v-for="supp_ml in supp_mls" 
                  multiple 
                  v-model="supp_ml_choice" 
                 :key="supp_ml" 
                 :value="supp_ml" 
                 :label="xlat[supp_ml]"
                 hide-details
                  />
            </v-form>
         </v-stepper-content>



         <v-stepper-step
       step="7"
      >
         Submission
      </v-stepper-step>
         <v-stepper-content step="8">
             Submission data. No form here.
      


         </v-stepper-content>


      </v-stepper>


      
      {{tree_data}}
   </FormShell>
</template>



<script>
  
import FormShell from '../components/FormShell'
// import SelectFields from '../components/SelectFields.vue'



export default {
   name: 'OnboardingForm',
   components: { 
      FormShell,
      // SelectFields,
   },
   data: function() {
      const route_type=this.$route.params.type;

      console.log(this.$store.state.init_data);
      const xlat=this.$store.state.init_data.xlat;
      const org_tree=this.$store.state.init_data.org_tree;

      var job_title_id_map = [];

      function build_tree_data (parent_path,org_tree){
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
               children = build_tree_data(new_path,child);
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


      var org_tree_data = build_tree_data([],org_tree);



      org_tree_data.push({
         id: job_title_id_map.length,
         name: "Other...",
         children: []
      });


      return {
         org_tree: org_tree,
         job_title_ids: [],
         tree_data: org_tree_data,
         job_title_id_map: job_title_id_map,

         form_valid: [true,true,true,true,true],
         replacement_pos: 0,
         former_employee: "",
         start_date: '',
         xlat: xlat,
         netID_Rules: [
            v => /^([a-z0-9])*$/.test(v) || "Must be lower-case alphanumeric"
         ],
         employeeNameRules: [
            //
         ],

         startDateRules: [
            v => {
               if (!v){
                  return 'Start date is required.'
               } //else {
               //   const rightNow = new Date();
               //   const [year, month_str_pre, day_str_pre] = [rightNow.getFullYear(),"0" + (rightNow.getMonth() + 1), "0" + rightNow.getDate()];
               //   const month_str = month_str_pre.substr(month_str_pre.length -2);
               //   const day_str = day_str_pre.substr(day_str_pre.length -2);
               //   const date_str = year + "-" + month_str + "-" + day_str;
               //   const today = Date.parse(date_str);
               //   const input_date = Date.parse(v);
               //   const time_diff = (input_date - today);
               //   if (time_diff < 0){
               //      return 'Due date cannot be in the past';
               //   }else{
               //      return true;
               //   }

               //}
               else {
                  return true;
               }
            }
         ],

         route_type: route_type,
         step_num: 1,
         total_steps: 8,
         employee_name: "",
         employee_net_id: "",
         date_menu: false,
         form_refs: [],
         position_descr: "",
         selected_roles: [],
         work_models: this.$store.state.init_data.work_models,

         work_model_selection: "hybrid",
         rooms: this.$store.state.init_data.rooms,
         room_selection: "gor100",
         room_sublocation: "",
         phone_ext_options: this.$store.state.init_data.phone_extensions,
         phone_ext_choice: "has_phone_not_required",
         hw_choices: this.$store.state.init_data.hw_choices,
         hw_choice: "hw_choice1",
         hw_choice_selection: "hybrid",
         laptop_explanation: "",
         supp_prints: this.$store.state.init_data.supp_prnts,
         supp_print_choice: [],
         supp_mls: this.$store.state.init_data.supp_mls,
         supp_ml_choice: [],

      };
   },
   methods: {


      next_page: function(){
         console.log("CALLED")
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
         this.replace_pos='';
         this.$refs.form1.resetValidation();
            this.$refs.form2.resetValidation();
      }
   },
   computed:{

      role_choices: function(){
         if (this.job_title_ids.length==0 || this.other_job_title_selected){
            return [];

         }else{
            const job_title_id = this.job_title_ids[0];
            const path=this.job_title_id_map[job_title_id];
            var child=this.org_tree;
            var new_child;
            var element;
            for (element of path){
               new_child=child[element];
               child = new_child;
            }
            //return child;
            return child.map(x=>this.xlat[x]);

         }
      },

      other_job_title_selected: function(){
         if (this.job_title_ids.length>0){
            const job_title_id = this.job_title_ids[0];
            return job_title_id == this.job_title_id_map.length;
         }else{
            return false;
         }
      },

      job_title_path: function() {
         if (this.job_title_ids.length>0){
            if (this.other_job_title_selected){
               return {
                  job_title_type: "other"
               };
            }else{
               const job_title_id = this.job_title_ids[0];
               return{
                  job_title_type: "standard",
                  job_title_path: this.job_title_id_map[job_title_id]
               }
            }
         }else{
            return null;
         }
      },

      submission_display: function() {
         return this.submission_data();
      },

      init_data: function(){
         console.log("WHERE ARE WE?");
         return this.$store.state.init_data;
      },
     
      field_dict: function(){
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


         var content_data = {
            json: { 
               start_date: this.start_date
            }
         };
         content_data.attachments=[];
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
      }

   },
   mounted(){
      this.form_refs=this.$refs;
   }
}
</script>



