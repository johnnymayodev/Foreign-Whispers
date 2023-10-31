console.log('app.js loaded');

const domain = 'localhost'
const port = '5005'
const http = 'http://'
const https = 'https://'
const api = '/api'
const url = http + domain + ':' + port + api

// check api
var xhr = new XMLHttpRequest();
// give 'check' as url parameter
xhr.open('GET', url + '?check', true);
xhr.send();
xhr.onreadystatechange = processRequest;
function processRequest(e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
        console.log(xhr.responseText);
    }
}
