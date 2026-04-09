<template>
   <v-container v-if="ticket_id">
       <div class="text-center">
        <v-icon
             x-large
             color="green"

            >
                mdi-check-bold
            </v-icon>
        </div>
        <v-row>
        <v-col cols="12">
                Ticket #{{ ticket_id }} has been created. An accompanying email should be sent to the email address you supplied.
             </v-col>
        </v-row>

   </v-container>
   <v-container v-else>
      <v-dialog v-model="show_submit_confirm">
              <v-card>
                <v-card-title>
                    Warning!
                </v-card-title>
                <v-card-text>
                    <div>
                       If you reset the form all of your work will be lost. Proceed anyway?
                    </div>
                </v-card-text>

                <v-card-actions>
                  <v-btn @click="show_submit_confirm=false">Cancel</v-btn>
                <v-btn @click="reset_all()">Proceed</v-btn>
                </v-card-actions>
              </v-card>
    </v-dialog>



      <v-row>
         <v-col cols="12">
            <h1>{{ heading }}</h1>
         </v-col>
      </v-row>

         <slot/>
         <v-row>
            <v-col cols="12">
               <v-btn
                  class="ma-2"
                  @click="show_submit_confirm=true"
                  :disabled="processing_request">
                  Reset this form
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

      <div v-if="devel_mode">
            {{ submission_display }}
       </div>
  </v-container>


</template>



<script>
  

const authsystem_network = require ("authsystem_network");


import {FormValidationError} from '../js_extra/web_project_error.js'
import ErrorDiv from './ErrorDiv.vue'

const config_data = JSON.parse(process.env.VUE_APP_CONFIG_DATA);


const authsystem_path = config_data.vue_app_path_roots.authsystem;


export default {
   name: 'FormShell',
   components: {
      ErrorDiv
   },
   props: {
        clearFunc: Function,
        validateFunc: Function,
        submissionData: Object,
        heading: String,
        submit_button_label: String,
        formType: String,
        step_num: Number,
        next_page: Function,
        prev_page: Function,
        total_steps: Number,
        ticket_id: {
         type: Number,
         default: null
        }
   },
   data: function() {


      return {
         response_text: '',         
         form_valid: true,
         processing_request: false,
         submit_fail: false,
         submit_error: null,
         devel_mode: process.env.NODE_ENV === 'development',
         show_submit_confirm: false
      };
   },
   methods: {
      

      validate_form: function (page_num){
         return (new Promise((resolve,reject)=>{
            //const validation_result = this.$refs.form.validate();
            const validation_result = this.validateFunc(page_num)();
            if (validation_result){
               resolve(true);  
            }else{
               console.log("OH NO!");
               const err= new FormValidationError();
               reject(err)
            }
         }));
      },

   
      next_page_plus: async function () {
         //this really shouldn't be async now. no point
         this.submit_fail=false;
         console.log("are we really here")
         try {
            console.log(this.step_num);
            await this.validate_form(this.step_num);
             this.next_page();
         }catch(e){
            this.submit_error=e;
            this.processing_request=false;
            this.submit_fail=true;
         }

      },



      reset_all: async function(){
        console.log("RESET ALL is called");
        try {
           await authsystem_network.get_app_token(authsystem_path,"ithelp"); //don't care what the app_token is
        } catch (e){
           if (e instanceof authsystem_network.SessionAuthenticationError){
               //this should cover...missing session cookie, expired session
               //anyhitng that would result in an "401 Unauthorized". Don't forget that
               //the language of 'Unauthorized' in HTTP codes is wrong
               //and really refers to authentication problems.
               this.$router.go();
           }
           //we don't care about other errors that may result. not relevant
        }
        this.clearFunc();
        this.submit_fail=false;
        this.show_submit_confirm=false;
        if (!(typeof window === 'undefined')) {
           window.scrollTo({
            top: 0,
            left: 0,
            behaviour: 'smooth'});
        }
      },
   },
   computed:{
      submission_display: function() {
         return this.submissionData;
      }      
      
   },
   watch:{
   }
}
</script>





