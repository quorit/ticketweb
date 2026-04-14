<template>
    
    <v-container>
        <h1>TicketWeb OUR Data Request App</h1>
        <p>This app serves the following page:</p>
        <ul>
            <li><router-link :to="{ name: 'reporting_request_forms', params: { type: 'admissions' } }">Admissions</router-link></li>
            <li><router-link :to="{ name: 'reporting_request_forms', params: { type: 'student' } }">Student</router-link></li>
            <li><router-link :to="{ name: 'reporting_support_form', params: { type: 'rptsupport' }}">Data support</router-link></li>
        </ul>

    </v-container>
    
</template>




<script>






export default {
    name: 'HomeView',

    data: function() {
       return {
       };
    },
    methods: {
    }
}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
