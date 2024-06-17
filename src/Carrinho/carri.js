/*Configuracão da pagina pagamento*/

$(document).ready(function() {
   var botao = $('.menu_cartao-credito');
   var dropDown = $('.menu_form');    
  
      botao.on('click', function(event){
          dropDown.stop(true,true).slideToggle();
          event.stopPropagation();
      });
  });

