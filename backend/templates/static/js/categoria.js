const toggleMenuButton = document.querySelector('.button1');
const menu = document.querySelector('#menu_ul1');
const toggleMenuButtonct = document.querySelector('.button2');
const menu2 = document.querySelector('#menu_ul2');
const toggleMenuButtonmc = document.querySelector('.button3');
const menu3 = document.querySelector('#menu_ul3'); 


toggleMenuButton.addEventListener('click', () =>{
   menu.style.display = menu.style.display === 'none' ? 'block' : 'none'
});

toggleMenuButtonct.addEventListener('click', () =>{
   menu2.style.display = menu2.style.display === 'none' ? 'block' : 'none'
});

toggleMenuButtonmc.addEventListener('click', () =>{
   menu3.style.display = menu3.style.display === 'none' ? 'block' : 'none'
});
