//FUNÇÂO PRA POSTAR

const postar = document.querySelector('#postar')
if (postar) {
    const inform = document.querySelector('.informs')
    const form = inform.querySelector('form')
    
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

//FUNÇÂO PRA CARREGAR POSTS DO BANCO DE DADOS
const posts = document.querySelector('.posts')
const arr = posts.querySelectorAll('div.post')

function createposts(parsed,username) {
    
    if (parsed["post"]){parsed = parsed["post"]}
    let title = parsed['desc'].slice(3,parsed['desc'].lastIndexOf('<t>'))
    let desc = parsed['desc'].slice(parsed['desc'].indexOf('<e>')+3)
    let type = parsed['filename'].slice(parsed['filename'].lastIndexOf('.')+1)
    console.log(title,desc,type,parsed['conte'])
    const newpost = document.createElement('div')
    newpost.classList.add('post')
    const [h3,h3content] = [document.createElement('h3'),document.createTextNode(`${title}`)]
    h3.appendChild(h3content)
    newpost.appendChild(h3)
    const [p,pcontent] = [document.createElement('p'),document.createTextNode(`${desc}`)]
    p.appendChild(pcontent)
    newpost.appendChild(p)
    const container = document.createElement('div')
    //const [container,img] = [document.createElement('div'),document.createElement('img')]
    container.classList.add('container')
    //img.setAttribute('src',`data:img/${type};base64,${parsed['conte']}`)
    //container.appendChild(img)
    container.style.backgroundImage = `url(data:img/${type};base64,${parsed['conte']})`
    newpost.appendChild(container)
    const [h2,h2content] = [document.createElement('h2'),document.createTextNode(`From: ${username}`)]
    h2.appendChild(h2content)
    newpost.appendChild(h2)
    posts.appendChild(newpost)
}

if (arr && arr.length==3) {
    var i=1
    posts.addEventListener('scroll',listener)

    function listener() {

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
                function(value){
                    var parsed = JSON.parse(value)
                    switch (Number(parsed["message"])) {
                        case 0: 
                            posts.removeEventListener('scroll',listener)
                            console.log('oi')
                            break
                        ;
                        case 1:
                            setTimeout(createposts(parsed,parsed["username"]),1000)
                            i++
                            break
                        ;
                        case 2:
                            setTimeout(() =>{
                            for (const post of parsed["post"]) {
                                createposts(post,parsed["username"])
                            }},1000)
                            i++
                            break
                        ;
                    }
                },
                function(error){console.log(error)}
            )
        }
    }
}