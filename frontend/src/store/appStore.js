import {defineStore} from 'pinia'
import {ref} from 'vue'


export const useAppStore =  defineStore('app', ()=>{

    /*  
    The composition API way of defining a Pinia store
    ref() s become state properties
    computed() s become getters
    function() s become actions  
    */ 

    // STATES 
  


    // ACTIONS
    const setPass = async (passcode) => {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        //console.log(passcode);
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(() => { controller.abort() }, 60000);
        const form = new FormData(); // Create form
        form.append("passcode", passcode); // Add variable to form
        console.log(form)
        const URL = `/api/set/combination/${passcode}`;
        try {
            const response = await fetch(URL, { method: 'POST', signal: signal,body: form, });
            if (response.ok) {
                const data = await response.json();
                let keys = Object.keys(data);
                if (keys.includes("status")) {
                    if (data["status"] == "complete") {
                        console.log(data["data"]);
                        return data["data"];
                    }
                    if (data["status"] == "failed"
                    ) {
                        console.log("setPasscode returned no data");
                    }
                }
            }
            else {
                const data = await response.text();
                console.log(data);
            }
        }
        catch (err) {
            console.error('setPasscode error: ', err.message);
        }
        return []
    }

    
    const checkPass = async(passcode) => {
        const URL = `/api/check/combination/${passcode}`;
        // FETCH REQUEST WILL TIMEOUT AFTER 60 SECONDS
        console.log(passcode)
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(()=>{controller.abort()},60000);
        const form = new FormData(); // Create form
        form.append("passcode", passcode); // Add variable to form
        try {
            const response = await fetch(URL,{ method: 'POST',body:form, signal: signal });
            if(response.ok){
                const data = await response.json();
                let keys = Object.keys(data);
                console.log(data);
                if (keys.includes("status")){
                    if (data["status"] === "found"){
                        console.log(data["data"]);
                        return data["data"]
                    }
                    else if (data["status"] === "failed"){
                       console.log("Unable to check passcode");
                       console.log(form);
                    }
                }
            }
            else{
                const data = await response.text();
                console.warn(data);
            }
        }
        catch(err){
            loading.value = false;
            if( err.message === "The user aborted a request."){
                console.log("REQUEST TIMEDOUT");
            }
            console.error('checkPass error: ', err.message);
        }
        return 0
    }

    const getTimestamp = async (start, end) => {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(() => { controller.abort() }, 60000);
        const URL = `/api/reserve/${start}/${end}`;
        try {
            const response = await fetch(URL, { method: 'GET', signal: signal });
            if (response.ok) {
                const data = await response.json();
                let keys = Object.keys(data);
                if (keys.includes("status")) {
                    if (data["status"] == "found") {
                        console.log(data["data"]);
                        return data["data"];
                    }
                    if (data["status"] == "failed"
                    ) {
                        console.log("getTimestamp returned no data");
                    }
                }
            }
            else {
                const data = await response.text();
                console.log(data);
            }
        }
        catch (err) {

            console.error('getTimestamp error:', err.message);
        }
        return []
    }

    const getAverage = async (start, end) => {
        // FETCH REQUEST WILL TIMEOUT AFTER 20 SECONDS
        const controller = new AbortController();
        const signal = controller.signal;
        const id = setTimeout(() => { controller.abort() }, 60000);
        const URL = `/api/avg/${start}/${end}`;
        try {
            const response = await fetch(URL, { method: 'GET', signal: signal });
            if (response.ok) {
                const data = await response.json();
                let keys = Object.keys(data);
                if (keys.includes("status")) {
                    if (data["status"] == "found") {
                        console.log(data["data"]);
                        return data["data"];
                    }
                    if (data["status"] == "failed"
                    ) {
                        console.log("getAverage returned no data");
                    }
                }
            }
            else {
                const data = await response.text();
                console.log(data);
            }
        }
        catch (err) {

            console.error('getAverage error:', err.message);
        }
        return []
    }


 
   
 
 
    return { 
    // EXPORTS
       setPass,
       getTimestamp,
       getAverage,
       checkPass
    }
},{ persist: true  });