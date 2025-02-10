const menuMobile = document.querySelector('.menu-mobile')
const body = document.querySelector('body')

menuMobile.addEventListener('click', () => {
    menuMobile.classList.contains("bi-list")
    ? menuMobile.classList.replace("bi-list","bi-x")
    : menuMobile.classList.replace("bi-x","bi-list")
    body.classList.toggle('menu-nav-active')
})

/*Fecha o menu e muda icone para list*/

const navItem = document.querySelectorAll('.nav-item')

navItem.forEach(item => {
    item.addEventListener('click', () => {
        if (body.classList.contains("menu-nav-active")) {
            body.classList.remove("menu-nav-active")
            menuMobile.classList.replace("bi-x", "bi-list");
        }
    })
})

// Botão de login
const loginButton = document.querySelector('.login-container');

// Esconder o botão após o scroll
window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {  // Quando a página for rolada mais de 50px
        loginButton.style.display = 'none';  // Esconde o botão
    } else {
        loginButton.style.display = 'block';  // Mostra o botão novamente
    }
});

// Animar itens data-anime

const item = document.querySelectorAll("[data-anime]");

const animeScroll = () => {
    const windowTop = window.scrollY + window.innerHeight * 0.75;
    
    item.forEach(element => {
        if(windowTop > element.offsetTop) {
            element.classList.add("animate");
        } else{
            element.classList.remove("animate");
        }
    });
};

animeScroll();

window.addEventListener("scroll", ()=>{
    animeScroll();
})