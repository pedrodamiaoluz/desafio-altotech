
if (document.readyState == "loading") {
    document.addEventListener("DOMContentLoaded", ready)
} else {
    ready()
}

function ready() {
    const quantInput = document.getElementsByClassName("input__quantidade")
    for (var i = 0; i < quantInput.length; i++) {
        quantInput[i].addEventListener("change", totalProduto)
    }
}

function totalProduto() {
    let totalGeral = 0
    const cartProdut = document.getElementsByClassName("produto-adicionado")
    for (var i = 0; i < cartProdut.length; i++) {

        const produtoPreco = cartProdut[i].getElementsByClassName("produto-preco")[0].innerText.replace("R$", "").replace(",", ".")
        const inputQuantidade = cartProdut[i].getElementsByClassName("input__quantidade")[0].value

        totalGeral += produtoPreco * inputQuantidade
    }
    totalGeral = totalGeral.toFixed(2)
    totalGeral = totalGeral.replace(".", ",")
    document.querySelector(".total__geral span").innerText = "R$" + totalGeral
}

/*Configuracão da pagina pagamento*/

$(document).ready(function() {
    var botao = $('.menu_cartao-credito');
    var dropDown = $('.menu_form');    
   
        botao.on('click', function(event){
            dropDown.stop(true,true).slideToggle();
            event.stopPropagation();
        });
});