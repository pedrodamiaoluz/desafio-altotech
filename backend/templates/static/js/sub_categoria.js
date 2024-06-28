const MENU_BASE = '#menu_ul';

function action_categoria(id) {
    const MENU_ID = MENU_BASE + id
    const MENU = document.querySelector(MENU_ID);
    MENU.style.display = MENU.style.display === 'none' ? 'block' : 'none'
};
