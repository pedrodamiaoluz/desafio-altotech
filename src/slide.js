 /*--------------------------------------------------------------------- */

  const constrols = document.querySelectorAll('.constrol')

  let corentItem = 0;
  const items = document.querySelectorAll('.item')
  const maxItem = items.length;

  constrols.forEach(control => {
    control.addEventListener('click', () => {
        const right = control.classList.contains("bi-chevron-right")


        if (right){
            corentItem -= 1;
        } 
        else{
            corentItem += 1;
        } 

        if (corentItem >= maxItem){
            corentItem = 0;
        }

        if (corentItem < 0){
            corentItem = maxItem - 1;
        }
        
        items.forEach(item => item.classList.remove('corent-item'));

        items[corentItem].scrollIntoView({
            inline: "center",
            behavior: "smooth",
        })

    })
  });