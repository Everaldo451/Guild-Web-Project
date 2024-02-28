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