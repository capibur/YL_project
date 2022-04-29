window.addEventListener("load", function() {
    let audio = document.getElementById("audio");
    let time = document.querySelector(".time");
    let btnPlay = document.querySelector(".play");
    let btnPause = document.querySelector(".pause");
    let btnNext = document.querySelector(".next");
    let btnDelete = document.querySelectorAll(".delete");

    let trackName = document.getElementById("name");


     function switchTreck () {
      let xhr = new XMLHttpRequest();
      xhr.open('GET', 'http://127.0.0.1:5000/track_pl/' + btnPlay.value);
      xhr.responseType = 'json';
      xhr.send();
      xhr.onload = function() {

          audio.src = '../static/'.concat(xhr.response['track']['tack_path']);
          audio.currentTime = 0;
          console.log(xhr.response["track"])
          trackName.innerHTML = xhr.response['track']["track_name"]
          track_now = xhr.response['track']["id"]
          audio.play();
          console.log( '../'.concat(xhr.response['track']['tack_path']))
      }

  }


  btnPlay.addEventListener("click", function() {
      audio.play();

      audioPlay = setInterval(function() {
          time.style.width = (Math.round(audio.currentTime) * 100) / Math.round(audio.duration) + '%';
          if (Math.round(audio.duration) == Math.round(audio.currentTime) ) {
              switchTreck();
          }
      }, 10)
  });


for (let i = 0; i < btnDelete.length; i++) {
  btnDelete[i].addEventListener("click", function(){
        let xhr = new XMLHttpRequest();
        xhr.open('DELETE', 'http://127.0.0.1:5000/track_pl/' + btnPlay.value +"/"+ btnDelete[i].value );
        xhr.responseType = 'json';
        xhr.send();
        xhr.onload = function(){
        console.log("secss")
        location.reload();
        }


})

}

  btnPause.addEventListener("click", function() {
    audio.pause();
    clearInterval(audioPlay)
});


btnNext.addEventListener("click", function() {
switchTreck();
});

    })