window.addEventListener("load", function() {
let bShow = document.querySelectorAll('.liked');
let playlist = document.getElementById("s1");
let btnSub = document.querySelectorAll('.sub');
for (let i = 0; i < bShow.length; i++) {
  bShow[i].addEventListener("click", function(){
        let xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://0.0.0.0:5000/pl_api/liked/' + bShow[i].value);
        xhr.responseType = 'json';
        xhr.send();
        xhr.onload = function(){
        console.log("secss")
        }


})
}

for (let i = 0; i < btnSub.length; i++) {
btnSub[i].addEventListener("click", function(){
        console.log(playlist.value)
                let xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://0.0.0.0:5000/pl_api/' + playlist.value + "/" + btnSub[i].value);
        xhr.responseType = 'json';
        xhr.send();
        xhr.onload = function(){
        console.log("secss")
        }
        })


}
}

)
