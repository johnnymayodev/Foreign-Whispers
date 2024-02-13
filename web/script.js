console.log("script.js loaded");

const videoSelect = document.getElementById("videos-select");
console.log("Video select element retrieved");

const PORT = 55055;
const HOST = "127.0.0.1";
const URL = `http://${HOST}:${PORT}`;
console.log("URL for fetching videos set");

const xhr = new XMLHttpRequest();
xhr.open("GET", `${URL}/init`, true);
xhr.send();

const pathToVideos = "web/static/videos.json";
let videoTitles = [];
console.log("Path to videos set");

setTimeout(() => {
  fetch(pathToVideos)
    .then((response) => response.json())
    .then((videos) => {
      console.log("Fetched videos");
      for (var i = 0; i < Object.keys(videos).length; i++) {
        videoTitles.push(videos[i].title);
      }
      console.log("Video titles pushed to array");

      var counter = 0;
      videoTitles.forEach((title) => {
        const option = document.createElement("option");
        option.value = counter;
        option.innerHTML = title;
        videoSelect.appendChild(option);
        counter++;
      });
    });
}, 1000);

function selectVideo() {
  console.log("Select video function called");
  const selected = videoSelect.options[videoSelect.selectedIndex].value;
  document.getElementById("videos-select").disabled = true;
  globalThis.selected = selected;
  console.log("Path to subtitles set");

  fetch(pathToVideos)
    .then((response) => response.json())
    .then((videos) => {
      console.log("Fetched languages");
      const languages = videos[selected].languages;
      const languageSelect = document.getElementById("language-select");
      languageSelect.hidden = false;
      document.getElementById("confirm-2").hidden = false;
      languageSelect.innerHTML = "";

      languages.forEach((language) => {
        const option = document.createElement("option");
        option.value = language;
        option.innerHTML = language;
        languageSelect.appendChild(option);
      });
      console.log("Languages added to language select");
    });

  if (selected != -1) {
    document.getElementById("confirm-1").hidden = true;
  }
}

function getSubtitles() {
  console.log("Get subtitles function called");
  const elem = document.getElementById("test");
  elem.innerHTML = "";
  const pathToSubtitles = "web/static/subtitles.json";
  console.log("Path to subtitles set");
  const languageSelect = document.getElementById("language-select");
  const language = languageSelect.options[languageSelect.selectedIndex].value;

  console.log("Selected video: " + globalThis.selected);
  console.log("Selected language: " + language);

  var xhr = new XMLHttpRequest();
  xhr.open(
    "POST",
    URL + "/select_video/" + globalThis.selected + "/" + language,
    true
  );
  xhr.send();
  console.log("Selected video and language sent to server");

  setTimeout(() => {
    fetch(pathToSubtitles)
      .then((response) => response.text())
      .then((text) => {
        console.log("Fetched subtitles text");
        subtitles_as_json = JSON.parse(text);
        addSubtitlesToPage(subtitles_as_json);
      });
  }, 1000);

  console.log("Subtitles added to page");
  document.getElementById("video-picker").hidden = true;
  document.getElementById("video-enter").hidden = true;

  setTimeout(() => {
    const selected_title = videoTitles[globalThis.selected];
    const selected_language =
      languageSelect.options[languageSelect.selectedIndex].value;

    const path_to_video =
      "web/static/" + selected_language + "/" + selected_title + ".mp4";
    const source = document.createElement("source");
    const video = document.getElementById("video");
    source.src = path_to_video;
    source.type = "video/mp4";
    video.appendChild(source);
    video.append("Your browser does not support the video tag.");
  }, 1000);
}

function addSubtitlesToPage(subtitles_as_json) {
  console.log("Add subtitles to page function called");

  document.getElementById("subtitle-header").style.opacity = 1;
  document.getElementById("video-container").hidden = false;

  var testElem = subtitles_as_json[0];
  var testElem2 = subtitles_as_json[1];
  console.log(testElem);
  console.log(testElem2);

  for (var i = 0; i < Object.keys(subtitles_as_json).length; i++) {
    var start = subtitles_as_json[i].timestamp;
    var text = subtitles_as_json[i].text;
    var translation = subtitles_as_json[i].translated_text;
    new SubtitleElem(start, text, translation);
  }
}

class SubtitleElem {
  constructor(start, text, translation) {
    var newElem = document.createElement("div");
    var newTimeStamp = document.createElement("span");
    var newSubtitle = document.createElement("span");
    var newTranslation = document.createElement("span");

    newTimeStamp.innerHTML = start;
    newSubtitle.innerHTML = text;
    newTranslation.innerHTML = translation;

    newElem.appendChild(newTimeStamp);
    newElem.appendChild(newSubtitle);
    newElem.appendChild(newTranslation);

    newElem.className = "subtitle";
    newTimeStamp.className = "timestamp";
    newSubtitle.className = "subtitle-text";
    newTranslation.className = "translation";

    document.getElementById("test").appendChild(newElem);
  }
}

function sendLink() {
  if (document.getElementById("youtube-link").value == "" || document.getElementById("language-select-2").value == -1) {
    return;
  }

  alert(
    "This could take a long time. Please confirm if you want to continue or not."
  );
  document.getElementById("confirmation").hidden = false;
}

function sendLinkReal() {
  const link = document.getElementById("youtube-link").value;
  const video_id = link.split("=")[1];
  const languageSelect = document.getElementById("language-select-2");
  const language = languageSelect.options[languageSelect.selectedIndex].value;

  document.getElementById("confirmation").hidden = true;
  document.getElementById("video-picker").hidden = true;
  document.getElementById("video-enter").hidden = true;
  document.getElementById("loading").hidden = false;

  var xhr = new XMLHttpRequest();
  xhr.open("POST", URL + "/link_entered/" + video_id + "/" + language, true);
  xhr.send();

  xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      console.log("Selected video and language sent to server");

      alert("Done! Now you can select the video from the dropdown.")
      window.location.reload();
    }
  };
}
