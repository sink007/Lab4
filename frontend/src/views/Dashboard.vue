<template>
  <v-container>
    <v-row>
      <v-col cols="1" >
        <sheet width="1000px">
          <v-slider class="w-80" color="green" direction="vertical" width="50%" thumb-label="always"
            v-model="radar" :max="100" :min="0" step="0.01"
            label="Height (in)">
          </v-slider>
        </sheet>
      </v-col>
      <v-col justify="left" cols="11">
        <sheet>
          <figure class="highcharts-figure">
            <div id="container0"></div>
          </figure>
        </sheet>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="8">
        <sheet>
          <figure class="highcharts-figure">
            <div id="container1"></div>
          </figure>
        </sheet>
      </v-col>
      <v-col cols="4">
        <v-sheet class="sheet" max-width="350px">
          <v-card class="mb-5"  title="Water Level" style="max-width: 350px" variant="outlined" color="primary"
            density="compact"
            rounded="lg"
            subtitle="Capacity Remaining">
          
            <div id="container2"></div>
          </v-card>
        </v-sheet>
      </v-col>

    </v-row>
    <v-row align="center">
      <v-col >
        <v-dialog width="400" v-model="radarcheck">
            <template v-slot:default="{ radarcheck }">
              <v-card font-size="300px"  align="center" color="purple">
                  <v-card-text align="center">
                    Overflow detected!
                  </v-card-text>
              </v-card>
            </template>
        </v-dialog>
     </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
/** JAVASCRIPT HERE */

// IMPORTS

import { useMqttStore } from "@/store/mqttStore"; // Import Mqtt Store
import { storeToRefs } from "pinia";
const Mqtt = useMqttStore();
const { payload, payloadTopic } = storeToRefs(Mqtt);

// Highcharts, Load the exporting module and Initialize exporting module.
import Highcharts from "highcharts";
import more from "highcharts/highcharts-more";
import Exporting from "highcharts/modules/exporting";
Exporting(Highcharts);
more(Highcharts);

import {
  ref,
  reactive,
  watch,
  onMounted,
  onBeforeUnmount,
  computed,
} from "vue";
import { useRoute, useRouter } from "vue-router";

// VARIABLES
const points = ref(10); // Specify the quantity of points to be shown on the live graph simultaneously.
const shift = ref(false); // Delete a point from the left side and append a new point to the right side of the graph.
const router = useRouter();
const route = useRoute();
var radar = ref(null);
var radarcheck= ref(null);
const areaChart = ref(null);
const gauge = ref(null);
var fluid = new FluidMeter();
const percentage = ref(null);

// FUNCTIONS

const CreateCharts = async () => {
  // TEMPERATURE CHART
  areaChart.value = Highcharts.chart("container0", {
    chart: { zoomType: "x" },
    title: { text: "Water Reserves(10 min)", align: "left" },
    yAxis: {
      title: {
        text: "Water Level",
        style: { color: "#000000" },
      },
      labels: { format: "{value} Gal" },
    },
    xAxis: {
      type: "datetime",
      title: { text: "Time", style: { color: "#000000" } },
    },
    tooltip: { shared: true },
    series: [
      {
        name: "Water",
        type: "area",
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[0],
      },
    ],
  });

  gauge.value = Highcharts.chart("container1", {
    title: { text: "Water Reserves", align: "left" },
    // the value axis
    yAxis: {
      min: 0,
      max: 1000,
      tickPixelInterval: 72,
      tickPosition: "inside",
      tickColor: Highcharts.defaultOptions.chart.backgroundColor || "#FFFFFF",
      tickLength: 20,
      tickWidth: 2,
      minorTickInterval: null,
      labels: { distance: 20, style: { fontSize: "14px" } },
      lineWidth: 0,
      plotBands: [
        { from: 0, to: 200, color: "#DF5353", thickness: 20 },
        { from: 200, to: 600, color: "#DDDF0D", thickness: 20 },
        { from: 600, to: 1000, color: "#55BF3B", thickness: 20 },
      ],
    },
    tooltip: { shared: true },
    pane: {
      startAngle: -90,
      endAngle: 89.9,
      background: null,
      center: ["50%", "75%"],
      size: "110%",
    },
    series: [
      {
        type: "gauge",
        name: "Water Capacity",
        data: [0],
        tooltip: { valueSuffix: " Gal" },
        dataLabels: {
          format: "{y} Gal",
          borderWidth: 0,
          color:
            (Highcharts.defaultOptions.title &&
              Highcharts.defaultOptions.title.style &&
              Highcharts.defaultOptions.title.style.color) ||
            "#333333",
          style: { fontSize: "16px" },
        },
        dial: {
          radius: "80%",
          backgroundColor: "gray",
          baseWidth: 12,
          baseLength: "0%",
          rearLength: "0%",
        },
        pivot: { backgroundColor: "gray", radius: 6 },
      },
    ],
  });

  fluid.init({
    targetContainer: document.getElementById("container2"),
    fillPercentage: percentage,
    options: {
      fontSize: "70px",
      fontFamily: "Arial",
      fontFillStyle: "white",
      drawShadow: true,
      drawText: true,
      drawPercentageSign: true,
      drawBubbles: true,
      size: 300,
      borderWidth: 25,
      backgroundColor: "#e2e2e2",
      foregroundColor: "#fafafa",
      foregroundFluidLayer: {
        fillStyle: "purple",
        angularSpeed: 100,
        maxAmplitude: 12,
        frequency: 30,
        horizontalSpeed: -150,
      },
      backgroundFluidLayer: {
        fillStyle: "pink",
        angularSpeed: 100,
        maxAmplitude: 9,
        frequency: 30,
        horizontalSpeed: 150,
      },
    },
  });
};


watch(payload, (data) => {
    if(points.value > 0){ points.value -- ; }
    else{ shift.value = true; }

    // Update the area chart
    areaChart.value.series[0].addPoint({y:parseFloat(data.percentage.toFixed(2)) ,x: data.timestamp * 1000 },
    true, shift.value);
   
    // Update the gauge chart
    gauge.value.series[0].points[0].update(parseFloat(data.reserve.toFixed(2)));
    
    // Update the fluid meter
    fluid.setPercentage(parseFloat(data.percentage.toFixed(2)));

    radar.value= parseFloat(data.radar.toFixed(2))

    if (radar.value<= 16.737){
      radarcheck.value= true
    }
    else{
      radarcheck.value= false
    }
  }
);

// COMPUTED PROPERTIES

onMounted(()=>{
        // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
    CreateCharts();
    
    Mqtt.connect(); // Connect to Broker located on the backend
    setTimeout( ()=>{
    // Subscribe to each topic
    Mqtt.subscribe("620155784");
    Mqtt.subscribe("620155784_pub");
    Mqtt.subscribe("620155784_sub");
    },3000);
    
    
});


onBeforeUnmount(()=>{
    // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
    // unsubscribe from all topics
  Mqtt.unsubcribeAll();
});
</script>

<style scoped>
/** CSS STYLE HERE */
figure {
  border: 2px solid black;
}

.w-80 {
  width: 80%;
}

</style>
