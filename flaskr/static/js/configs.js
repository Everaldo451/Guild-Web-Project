const editar = document.querySelector('button')
const form = document.querySelector('form')
const cancelar = form.querySelector('input[type="button"]')

if (editar) {

const senha = document.getElementById('senhainput')
const inputs = form.querySelectorAll('input')
const labels = form.querySelectorAll('label')


editar.addEventListener('click',()=>{
    editar.style.display="none"
    for (const input of inputs){
        input.style.display="block"
    }
    for (const label of labels){
        if (label.getAttribute('name')){
        label.innerHTML = `<b>${label.getAttribute('name')}</b>`
        }
    }
    senha.style.display="block"
})

cancelar.addEventListener('click',()=>{
    window.location.assign('/configs')
})

}