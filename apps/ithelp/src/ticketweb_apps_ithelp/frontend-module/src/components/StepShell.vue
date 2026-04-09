<template>
  
   <v-stepper-content 
     :step="step_num">
   <v-container>
      <v-form v-if="!submission_step"
          ref="form"
          v-model="form_valid"
          lazy-evaluation>



         <slot/>
      </v-form>
      <slot v-else/>
      

         <v-row>
            <v-col cols="12">
               <v-btn v-if="parseInt(step_num)>1"
                  class="ma-2"
                  @click="prev_page"
                  :disabled="processing_request">
                  PREVIOUS PAGE
               </v-btn>


               <v-btn v-if="submission_step"
                  ref="submitnext"
                  class="ma-2"
                  @click="submit_ticket"
                  :disabled="processing_request">
                  {{ submit_button_label }}
               </v-btn>
               <v-btn v-else
                  ref="submitnext"
                  class="ma-2"
                  @click="next_page_plus">
                  NEXT PAGE
               </v-btn>
            </v-col>
         </v-row>
        

      <v-row>
         <v-col cols="12">
            <v-alert type="error" v-if="submit_fail" v-model="submit_fail" dismissible  close-text="Close Alert">
               <ErrorDiv
                 :error_obj="submit_error">

               </ErrorDiv>
            </v-alert>
         </v-col>
      </v-row>

   </v-container>
   </v-stepper-content>


</template>



<script>
  

const authsystem_network = require ("authsystem_network");
const rt_network = require ("rt_network");


import {FormValidationError} from '../js_extra/web_project_error.js'
import ErrorDiv from './ErrorDiv.vue'

const config_data = JSON.parse(process.env.VUE_APP_CONFIG_DATA);


const authsystem_path = config_data.vue_app_path_roots.authsystem;
const app_server_path = config_data.vue_app_path_roots.app_server;


export default {
   name: 'StepShell',
   components: {
      ErrorDiv
   },
   props: {
        step_num: [Number,String],
        next_page: Function,
        prev_page: Function,
        submit_button_label: String,
        submission_data: Object,
        submission_step: {
           type: Boolean,
           default: false
        },
   },
   data: function() {


      return {
         response_text: '',         
         form_valid: true,
         processing_request: false,
         submit_fail: false,
         submit_error: null,
         devel_mode: process.env.NODE_ENV === 'development',
         ticket_id: null,
      };
   },
   methods: {
      

      validate_form: function (){
         return (new Promise((resolve,reject)=>{
            var validation_result;
            
            validation_result = this.$refs.form.validate()  

            //const validation_result = this.validateFunc(page_num)();
            if (validation_result){
               resolve(true);  
            }else{
               const err= new FormValidationError();
               reject(err)
            }
         }));
      },

   
      next_page_plus: async function () {


         this.submit_fail=false;
         await new Promise(r => setTimeout(r, 1));
         //The reason for this nonsense is this github issue
         //https://github.com/vuetifyjs/vuetify/issues/7329
         //without this you can enter stuff in a combobox, and *before hitting enter*
         //hit "next page". When you do that the rules for the combobox are checked
         //*after* and form.validate returns *true* even though it should return false.
         //Sleeping just one milisecond seems to deal with this.

         const validation_result=this.$refs.form.validate();
         if(validation_result){
            this.next_page();
         }else{
            this.submit_error=new FormValidationError();
            this.processing_request=false;
            this.submit_fail=true;
         }
      },
      submit_ticket: async function () {
         this.processing_request=true;
         this.submit_fail=false;
         var response_json=null;




         try {
            

            response_json = await authsystem_network.get_app_token(authsystem_path,"ithelp")
                            .then(response => rt_network.submit_data(this.submission_data.json,
                                                           this.submission_data.attachments,
                                                           "onboarding",
                                                           response.jwt_token,
                                                           app_server_path));
         } catch(e){
            if (e instanceof authsystem_network.SessionAuthenticationError){
               //this should cover...missing session cookie, expired session
               //anyhitng that would result in an "401 Unauthorized". Don't forget that
               //the language of 'Unauthorized' in HTTP codes is wrong
               //and really refers to authentication problems.
               this.$router.go();
            } else {
               this.submit_error=e;
               this.processing_request=false;
               this.submit_fail=true;
            }
            return;
         }
         this.ticket_id = response_json.id
         this.processing_request=false;
         this.$emit('ticket_id_set',this.ticket_id);
      },
      reset_step(){            
         if(!this.submission_step){
            console.log("yolo")
            const form_ref=this.$refs.form;
            form_ref.resetValidation();
         }else{
            this.ticket_id=null;
         }
         this.submit_fail=false;
      }
      
   },
   computed:{
           
   },
   watch:{
   },
   mounted: function() {
   }
}
</script>





