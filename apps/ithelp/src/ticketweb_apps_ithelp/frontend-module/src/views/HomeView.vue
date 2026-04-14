<template>
    
    <v-container>
        <h1>TicketWeb IT Help App</h1>
        <p>This app serves the following page:</p>
        <ul>
            <li><router-link :to="{ name: 'onboarding_form', params: { type: 'onboarding' } }">Staff onboarding</router-link></li>
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
