console.log("app.js loaded");

const domain = "localhost";
const port = "5005";
const http = "http://";
const https = "https://";
const api = "/api";
const url = http + domain + ":" + port + api;
const check_arg = "/check";

// check api
var xhr = new XMLHttpRequest();
// give 'check' as url parameter
xhr.open("GET", url + check_arg, true);
xhr.send();
xhr.onreadystatechange = processRequest;
function processRequest(e) {
  if (xhr.readyState == 4 && xhr.status == 200) {
    console.log(xhr.responseText);
  }
}

function milestone_1() {
  const arg = "/milestone1";
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url + arg, true);
  xhr.send();
  xhr.onreadystatechange = processRequest;
  function processRequest(e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
      console.log(xhr.responseText);
      if (xhr.responseText == "OK") {
        alert("Milestone 1 has successfully been completed");
      }
    }
  }
}

function milestone_2() {
  const arg = "/milestone2";
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url + arg, true);
  xhr.send();
  xhr.onreadystatechange = processRequest;
  function processRequest(e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
      console.log(xhr.responseText);
      if (xhr.responseText == "OK") {
        alert("Milestone 2 has successfully been completed");
      }
    }
  }
}
