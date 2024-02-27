<template>
  <v-container>
    <v-row>
      <v-col>
            <v-text-field v-model="start" label="Start date" type="date" dense solo-inverted class="mr-5" 
                    :style="{ maxWidth: '300px' }" flat
                    >
            </v-text-field>
            <v-text-field v-model="end" label="End date" type="date" dense solo-inverted
                :style="{ maxWidth: '300px' }"
                flat >
            </v-text-field>
            <v-spacer></v-spacer>
            <VBtn @click="updateLineCharts(); updateScatterCharts(); updateCards();" text="Analyze" color="primary" variant="tonal" >
          </VBtn>
      </v-col>
      <v-col>
          <v-sheet width="200px">
              <v-card class="mb-5" align="center" style="max-width: 200px" color="surface" title="Average"
                     subtitle="For the selected period">
                       <span class="text-onSecondaryContainer text-h3">{{ reserveAvg }}</span>
                      Gal
              </v-card>
         </v-sheet>
      </v-col>
    </v-row>
    <v-row>
        <v-col>
          <figure class="highcharts-figure">
              <div id="container0"></div>
          </figure>
        </v-col>
    </v-row>
    <v-row>
       <v-col>
           <figure class="highcharts-figure">
             <div id="container1"></div>
           </figure>
       </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import Highcharts from "highcharts";
import more from "highcharts/highcharts-more";
import Exporting from "highcharts/modules/exporting";
import { withDirectives } from "vue";
Exporting(Highcharts);
more(Highcharts);

import { useMqttStore } from "@/store/mqttStore";
import { storeToRefs } from "pinia";

import { useAppStore } from "@/store/appStore";
import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed } from "vue";  
import { useRoute, useRouter } from "vue-router";

const router = useRouter();
const route = useRoute();
const Mqtt = useMqttStore();
const AppStore = useAppStore();
var start = ref("");
var end = ref("");
var reserveAvg = ref(null);
const lineChart = ref(null);
const scatterChart = ref(null);

const CreateCharts = async () => {
  lineChart.value = Highcharts.chart("container0", {
    chart: { zoomType: "x" },
    title: { text: "Water Management Analysis", align: "left" },
    yAxis: {
      title: {
        text: "Water Reserve",
        style: { color: "#000000" },
      },
      labels: { format: "{value} Gal" },
    },
    tooltip: {
      pointFormat: "Time: {point.x} s <br/> Water Reserve: {point.y} Gal",
    },
    xAxis: {
      type: "datetime",
      title: { text: "Time", style: { color: "#000000" } },
    },
    tooltip: { shared: true },
    series: [
      {
        name: "Water Reserve",
        type: "line",
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[0],
      },
    ],
  });

  scatterChart.value = Highcharts.chart("container1", {
    chart: { zoomType: "x" },
    title: {
      text: "Height Level and Water Level Correlation Analysis",
      align: "left",
    },
    yAxis: {
      title: {
        text: "Height",
        style: { color: "#000000" },
      },
      labels: { format: "{value} in" },
    },
    xAxis: {
      title: { text: "Water Height", style: { color: "#000000" } },
      labels: { format: "{value} in" },
    },
    tooltip: {
      shared: true,
      pointFormat: "Water Height: {point.x} in <br/> Height: {point.y} in",
    },
    series: [
      {
        name: "Analysis",
        type: "scatter",
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[0],
      },
    ],
  });
};

const updateCards = async () => {
  if (!!start.value && !!end.value) {
    let startDate = new Date(start.value).getTime() / 1000;
    let endDate = new Date(end.value).getTime() / 1000;
    const avg = await AppStore.getAverage(startDate, endDate);
    reserveAvg.value = avg[0].avg.toFixed(2);
  }
};

const updateLineCharts = async ()=>{
    if(!!start.value && !!end.value){
        // Convert output from Textfield components to 10 digit timestamps
        let startDate = new Date(start.value).getTime() / 1000;
        let endDate = new Date(end.value).getTime() / 1000;
        // Fetch data from backend
        const data = await AppStore.getTimestamp(startDate,endDate);
        // Create arrays for each plot
        let reserve = [];
        // Iterate through data variable and transform object to format recognized by highcharts
        data.forEach(row => {
            reserve.push({"x": row.timestamp * 1000, "y": parseFloat(row.reserve.toFixed(2)) });
        });

        lineChart.value.series[0].setData(reserve);
    }
}

const updateScatterCharts = async () => {
  if (!!start.value && !!end.value) {
    // Convert output from Textfield components to 10 digit timestamps
    let startDate = new Date(start.value).getTime() / 1000;
    let endDate = new Date(end.value).getTime() / 1000;
    // Fetch data from backend
    const data = await AppStore.getTimestamp(startDate, endDate);
    // Create arrays for each plot
    let distance = [];
    // Iterate through data variable and transform object to format recognized by highcharts
  
    data.forEach((row) => {
      distance.push({"x": parseFloat(row.waterheight.toFixed(2)), "y": parseFloat(row.radar.toFixed(2)),
      });
    });
    scatterChart.value.series[0].setData(distance);
  }
};


onMounted(() => {
  CreateCharts();
  Mqtt.connect();
  setTimeout(() => {
    Mqtt.subscribe("620155784");
    Mqtt.subscribe("620155784_sub");
  }, 3000);
});

onBeforeUnmount(() => {
  Mqtt.unsubcribeAll();
});

</script>

<style scoped>
</style>
