window.addEventListener("load", function() {

let btnOpen = document.querySelectorAll('.open');
let btnDelete = document.querySelectorAll('.delete');

for (let i = 0; i < btnDelete.length; i++) {
  btnDelete[i].addEventListener("click", function(){
        let xhr = new XMLHttpRequest();
        xhr.open('DELETE', 'http://127.0.0.1:5000/pl_api/' + btnDelete[i].value );
        xhr.responseType = 'json';
        xhr.send();
        xhr.onload = function(){
        console.log("secss")
        location.reload();
        }


})

}

for (let i = 0; i < btnOpen.length; i++) {
  btnOpen[i].addEventListener("click", function(){
  window.location.replace("http://127.0.0.1:5000/playlist/" + btnOpen[i].value);



})

}







})

