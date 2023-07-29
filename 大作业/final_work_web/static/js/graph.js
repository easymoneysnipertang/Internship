const body=document.querySelector('body')
const sidebar=body.querySelector('nav')
const toggle=body.querySelector('.toggle')
const searchBtn=body.querySelector('.search-box')
toggle.addEventListener('click',()=>{
    sidebar.classList.toggle('close')
})
searchBtn.addEventListener('click',()=>{
    sidebar.classList.remove('close')
})
