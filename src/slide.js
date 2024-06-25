 /*--------------------------------------------------------------------- */

  const constrols = document.querySelectorAll('.constrol')

  let corentItem = 0;
  const items = document.querySelectorAll('.item')
  const maxItems = items.length;

  constrols.forEach(control => {
    control.addEventListener('click', () => {
        const nextLeft = control.classList.contains("bi-chevron-right")


        if (nextLeft){
            corentItem -= 1;
        } 
        else{
            corentItem += 1;
        } 

        if (corentItem >= maxItems){
            corentItem = 0;
        }

        if (corentItem < 0){
            corentItem = maxItems - 1;
        }
        
        items.forEach(item => item.classList.remove('corent-item'));

        items[corentItem].scrollIntoView({
            inline: "center",
            behavior: "smooth",
        })

    })
  });