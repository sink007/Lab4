<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title align="center">Combination</v-card-title>
          <v-card-subtitle align="center">Enter Combination</v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="3">
        <v-card>
          <v-card-title>Digit 1</v-card-title>
          <v-card-text>
            <v-text-field v-model="input1" :maxlength="1"></v-text-field>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="3">
        <v-card>
          <v-card-title>Digit 2</v-card-title>
          <v-card-text>
            <v-text-field v-model="input2" :maxlength="1"></v-text-field>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="3">
        <v-card>
          <v-card-title>Digit 3</v-card-title>
          <v-card-text>
            <v-text-field v-model="input3" :maxlength="1"></v-text-field>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="3">
        <v-card>
          <v-card-title>Digit 4</v-card-title>
          <v-card-text>
            <v-text-field v-model="input4" :maxlength="1"></v-text-field>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col cols="auto">
        <v-btn @click="passing();" color="primary">Submit</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
/** JAVASCRIPT HERE */

// IMPORTS
import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed } from "vue";  
import { useRoute ,useRouter } from "vue-router";
import { useAppStore } from "@/store/appStore";
import { useMqttStore } from '@/store/mqttStore'; // Import Mqtt Store
import { storeToRefs } from "pinia";


// IMPORTS

// VARIABLES
const AppStore = useAppStore();
const Mqtt = useMqttStore();
const { payload, payloadTopic } = storeToRefs(Mqtt);
 
// VARIABLES
const router      = useRouter();
const route       = useRoute();  

const input1 = ref(""); 
const input2  = ref("");
const input3 = ref(""); 
const input4 = ref("");
const passcode=ref("")
// FUNCTIONS

onMounted(()=>{
        // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
        /*Mqtt.connect(); // Connect to Broker located on the backend
        setTimeout( ()=>{
        // Subscribe to each topic
        Mqtt.subscribe("620155784");
        Mqtt.subscribe("620155784_pub");
        Mqtt.subscribe("620155784_sub");
        },3000);*/
    });


    onBeforeUnmount(()=>{
        // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
        // unsubscribe from all topics
        Mqtt.unsubcribeAll();
    });


const combineNum = async () => {
  passcode.value= input1.value + input2.value+ input3.value +input4.value;
}

const passing= async () => {
  combineNum();
  const data = await AppStore.setPass(passcode.value);
  console.log(data);
}




</script>


<style scoped>
/** CSS STYLE HERE */


</style>
