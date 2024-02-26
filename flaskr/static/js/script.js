//Cookie verification
window.addEventListener("DOMContentLoaded", (even) => {
   console.log(document.cookie)
})

//Menu Load
if (document.querySelector('nav')) {
   
var mypromise = new Promise(function(resolve,reject) {
    
    const http = new XMLHttpRequest()
    http.open('GET','/menu.html')

    http.onload = function() {
        if (http.status == 200) {
            resolve(http.response)
        }
        else {reject("<h3>Not found</h3>")}
    }

    http.send()
})
mypromise.then(

    function (value) {
        const nav = document.querySelector('nav')
        nav.innerHTML = value
        //If Profile
        if (nav.querySelector('.profile')) {
            const profile = nav.querySelector('.profile')
            let sair = profile.querySelector('#sair')
            sair.addEventListener('click',(event)=>{
                event.preventDefault()
                let req = new XMLHttpRequest()
                req.open('GET','/auth/logout')
                req.send()
                req.onreadystatechange = function(){
                    if (req.status==200 && req.readyState==4){window.location.assign(this.responseURL)}
                }
            })
        }
        //Profile end
    },

    function (error) {
        document.querySelector('nav').innerHTML = error
    })
}

/*Inicial Page Text Animation*/
if (document.location.pathname == "/") {

    var pstorm = document.getElementById('pstorm')
    let text = pstorm.innerHTML
    let i = 0
    pstorm.innerHTML=""
    pstorm.style.display="block"
            
    let interval = setInterval(async function() {
        pstorm.innerHTML += text[i]
        if (i==text.length-1) {clearInterval(interval)}
            i++
},50)}

//})
//Login Page Cookies
//coname=1
function getCookie(coname) {
    let cookies = decodeURIComponent(document.cookie)
    cookies = cookies.replace("\s","")
    
    let index = cookies.indexOf(`${coname}=`)

    if (index != -1) {
        if (cookies.indexOf(";",index+coname.length+1)!=-1){
            return cookies.slice(index+coname.length+1,cookies.indexOf(";",index+coname.length+1))

        }else{return cookies.slice(index+coname.length+1)}
    }else{return false}
}








