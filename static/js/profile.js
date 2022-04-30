window.addEventListener("load", function() {
let btnDelete = document.querySelectorAll(".delete");


for (let i = 0; i < btnDelete.length; i++) {
btnDelete[i].addEventListener("click", function(){
                let xhr = new XMLHttpRequest();
        xhr.open('DELETE', 'http://http://ylp3.herokuapp.com/track_del/' + btnDelete[i].value);
        xhr.responseType = 'json';
        xhr.send();
        xhr.onload = function(){
        console.log("secss")
        location.reload();
        }
        })


}


})