//Cookie verification
window.addEventListener("DOMContentLoaded", (even) => {
   console.log(document.cookie)
})
/*Menu*/
let introduction = document.querySelector('introduction')
let iframe = document.getElementById("headeriframe").contentWindow
console.log('oi')
    iframe.addEventListener('load',(even) => {

        let header = iframe.document.body.querySelector('header')
        var menu = document.querySelector('header')

        menu.innerHTML += header.innerHTML
        

let profile = document.querySelector('.profile')
if (profile) {
    let sair = profile.querySelector('#sair')
    sair.addEventListener('click',(event)=>{
        event.preventDefault()
        let req = new XMLHttpRequest()
        req.open('GET','/auth/logout')
        req.send("")
        req.onreadystatechange = function(){
            if (req.status==200 && req.readyState==4){window.location.assign(this.responseURL)}
        }
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

})
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








