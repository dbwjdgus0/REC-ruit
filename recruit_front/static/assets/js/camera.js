// dom(Document Object Model,문서 객체 모델) :  HTML, XML 문서의 프로그래밍 interface
// 이들은 웹 페이지를 스크립트 또는 프로그래밍 언어들에서 사용될 수 있게 연결시켜주는 역할
//  <html>이나 <body> 같은 html문서의 태그들을 JavaScript가 이용할 수 있는 객체(object)로 만들면 그것을 문서 객체
//  Model 모형, 주형이라는 의미도 있고 모듈이라는 의미, 문서 객체를 '인식하는 방식'

// const 블록 범위의 상수를 선언, 상수의 값은 재할당할 수 없고 다시 선언할 수도 없음
// 상수는 let문을 사용해 정의된 변수와 마찬가지로 블록 범위임, 상수의 값은 재할당을 통해 바뀔 수 없고 재선언 될 수 없음.

const recordButton = document.querySelector(".record-button")
const stopButton = document.querySelector(".stop-button")
const playButton = document.querySelector(".play-button")
const downloadButton = document.querySelector(".download-button")
const previewPlayer = document.querySelector("#preview")
const recordingPlayer = document.querySelector("#recording")

const previewDIV = document.getElementById("preview-div")
const recordingDIV = document.getElementById("recoding-div")
const scriptDIV = document.getElementById("recoding-script-div")
//const showRecordViewButton = document.querySelector(".show-recordview-button")


// setting
// const recordingDuration = 15;
let recorder;       // 녹화 중지를 원할히 하기 위해서 바깥으로 뺌, 초기화
let recordedChunks; // 녹화된 내용을 담기 위함


// functions

// 화면 출력 및 화면 녹화
function videoStart() {
    navigator.mediaDevices // navigator를 통해 웹브라우저 기능에 접근을 하고 사용을 할 것
        .getUserMedia({ video: true, audio: true }) // 성공하게 되면 stream 값으로 받게 되고
                                                    // .then(stream => console.log(stream))을 적용시켜보면
                                                    // 1. 미디어 디바이스에 접근 혀용 권한 요청 => 허용
                                                    // 2. 접근 성공 이후 스트림이 찍힘
                                                    // 이 스트림을 바로 비디오 태그에 연결해 주면 화면이 나오게 됨
        .then((stream) => {
            previewPlayer.srcObject = stream; // 비디오 태그 스트림 연결 (보여주는 용도)
            startRecording(                     // 녹화 기능 함수 적용
                previewPlayer.captureStream()); // captureStream() 실시간으로 실행되고 있는 내용을 녹화하기 위해 삽입
        });

    //alert_hide_show
    swal("녹화 시작", "중지 또는 녹화 보기를 누를시 자동 저장 됩니다!", 'info');
	previewDIV.style.display = "";
	recordingDIV.style.display = "none";
	scriptDIV.style.display = "none";
}

// 화면 녹화
function startRecording(stream){ // 스트림을 인자로 넘겨 받고
    recordedChunks = [];
    recorder = new MediaRecorder(stream); // 녹화를 하기 위해서는 미디어 리코더라는 JS 객체를 사용, stream을 파라미터로 넘김
    recorder.ondataavailable = (e) => recordedChunks.push(e.data); // ondataavailable 함수를 추가, 이벤트를 데이터로 받아서 recordedChunks 녹화할 내용이 담기는 변수안에 푸쉬하면 됨
    recorder.start(); // 녹화를 시작하면 recordedChunks 안에 담기게 됨
}

// 녹화 중지
function stopRecording() {
    previewPlayer.srcObject.getTracks().forEach((track) => track.stop()); // 배열 형태의 스트림에 대한 정보 track 중지
    recorder.stop(); // 녹화를 중단함
    // console.log(recordedChunks) recordedChunks 안에 Blob이 담겨 있음, 미디어 객체임
}

// 녹화 영상 실행
function playRecording() {
    const recordedBlob = new Blob(recordedChunks, { type: "video/webm"}); // web 화면 출력용
    const recordedBlob2 = new Blob(recordedChunks, { type: "video/mp4"}); // mp4 필요 피드백 반영
    recordingPlayer.src = URL.createObjectURL(recordedBlob); // src를 적용해 사용함
    recordingPlayer.play()

    downloadButton.href=recordingPlayer.src;
    downloadButton.download = `recording_${new Date()}.webm`;
    downloadButton
    swal("녹화 내용 재생", "녹화된 영상은 다운로드 가능합니다", 'success');
	previewDIV.style.display = "none";
	recordingDIV.style.display  = "";
	scriptDIV.style.display = "";
}

// 실험

function getShow(){
	alert("display : 공백");
	previewDIV.style.display = "";
	recordingDIV.style.display = "none";

}

function getHide(){
	alert("display : none");
	previewDIV.style.display = "none";
	recordingDIV.style.display  = "";

}


// event
recordButton.addEventListener("click", videoStart);
stopButton.addEventListener("click", stopRecording);
playButton.addEventListener("click", playRecording);
