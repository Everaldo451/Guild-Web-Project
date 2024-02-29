const postar = document.querySelector('#postar')
if (postar) {
    const inform = document.querySelector('.informs')
    const form = inform.querySelector('form')
    console.log(inform)
    postar.addEventListener('click',()=>{
        form.style.display = "block"
        postar.style.display = "none"
    })
    const cancelar = form.querySelector('input[type="button"]')
    cancelar.addEventListener('click',()=>{
        form.style.display = "none"
        postar.style.display = "block"
    })
}

const posts = document.querySelector('.posts')
const arr = posts.querySelectorAll('div.post')
console.log(arr,arr.length)
if (arr && arr.length==3) {
    var i=1
    posts.addEventListener('scroll',(even)=>{

        console.log(posts.scrollHeight,posts.scrollTop,posts.clientHeight)
        if (posts.scrollTop == posts.scrollHeight - posts.clientHeight){

            const promise = new Promise(function(resolve,reject) {
            const http = new XMLHttpRequest()
            var y = window.location.pathname.lastIndexOf('/')
            http.open('GET',`/gp/getposts?username=${window.location.pathname.slice(y+1)}&f=${3*i}`)
            http.onload = function(){
                if (http.status=200) {resolve(http.response)}
                else{reject('error')}
            }
            http.send()
            })
            promise.then(
                function(value){console.log(value)},
                function(error){console.log(error)}
            )
        }
    })
}