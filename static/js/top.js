

  window.addEventListener("load", function() {
    let audio = document.getElementById("audio");    
    let time = document.querySelector(".time");      
    let btnPlay = document.querySelector(".play");   
    let btnPause = document.querySelector(".pause");
    let btnNext = document.querySelector(".next");
    let btnLike = document.querySelector(".like");
    let btnDislike = document.querySelector(".dislike");
    let playlist = document.getElementById("s1");
    let btnSub = document.querySelector(".sub");
    let trackImg = document.getElementById("track_img");
    let trackName = document.getElementById("name");
    function switchTreck () {
      let xhr = new XMLHttpRequest();
      xhr.open('GET', 'http://ylp3.herokuapp.com/rec_api/Moscow/1');
      xhr.responseType = 'json';
      xhr.send();
      xhr.onload = function() {
          audio.src = '../static/'.concat(xhr.response['track']['tack_path']);
          audio.currentTime = 0;
          trackName.innerHTML = xhr.response['track']["track_name"]
          console.log('../static/' + xhr.response['track']["img_path"])
          trackImg.src =  '../static/' + xhr.response['track']["img_path"]
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




  btnPause.addEventListener("click", function() {
    audio.pause();
    clearInterval(audioPlay) 
});


btnNext.addEventListener("click", function() {
switchTreck();
});

btnLike.addEventListener("click", function(){
        let xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://ylp3.herokuapp.com/pl_api/liked');
        xhr.responseType = 'json';
        xhr.send();
        xhr.onload = function(){
        console.log("-09-0")
        }



})
btnDislike.addEventListener("click", function(){
        let xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://ylp3.herokuapp.com/pl_api/disliked');
        xhr.responseType = 'json';
        xhr.send();
        xhr.onload = function(){
        console.log("-09-0")
        }



})

btnSub.addEventListener("click", function(){
        console.log(playlist.value)
                let xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://ylp3.herokuapp.com/pl_api/' + playlist.value);
        xhr.responseType = 'json';
        xhr.send();
        xhr.onload = function(){
        console.log("secss")
        }
        })
  });

