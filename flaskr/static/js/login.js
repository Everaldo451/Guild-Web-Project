const forms = document.querySelectorAll('form')
for (const x of forms) {
    if (x) {
        const inputs = x.querySelectorAll('input')
        console.log("tem form")

        for (const y of inputs) {
            if (y.getAttribute('type')=="submit"){
                continue
            }
            const parent = y.parentElement
            y.onfocus = function(){
                parent.setAttribute('class','animinput1')
                parent.onanimationstart = function() {console.log("começou a palhaçada")}
            }
            y.addEventListener('focusout',()=>{
                parent.removeAttribute('class')
            })
        }
    }
}

const form = document.getElementById('login1')
if (form) {
    const p = form.querySelector('p')
    const submit = form.querySelector('input[type="submit"]')


    submit.addEventListener('click',(even) =>{
        even.preventDefault()
        data = new FormData(form)
        for (const [key,value] of data){

            if (value != "" & value!=null) {
                continue
            } else {
                p.innerHTML=`O campo "${key}" não foi preenchido corretamente. Escreva novamente.`
                return
            }
        }
        p.innerHTML=""
        form.requestSubmit()
        form.reset()
    })
}
