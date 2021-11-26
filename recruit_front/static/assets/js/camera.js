// dom
const recordButton = document.querySelector(".record-button")
const stopButton = document.querySelector(".stop-button")
const playButton = document.querySelector(".play-button")
const downloadButton = document.querySelector(".download-button")
const previewPlayer = document.querySelector("#preview")
const recordingPlayer = document.querySelector("#recording")

// functions
function videoStart() {
    navigator.mediaDevices.getUserMedia({video: true, audio: true})
        .then(stream => previewPlayer.srcObject = stream)
}


// event
recordButton.addEventListener("click", videoStart)