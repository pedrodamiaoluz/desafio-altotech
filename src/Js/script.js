
if (document.readyState == "loading") {
    document.addEventListener("DOMContentLoaded" , ready)
}else{
    ready()
}

function ready(){
    const removebutton = document.getElementsByClassName("button-remov")
    for (var i = 0; i < removebutton.length; i++){
        removebutton[i].addEventListener("click", removeProdut)
    }

    const quantInput = document.getElementsByClassName("input__quantidade")
    for (var i = 0; i < quantInput.length; i++){
        quantInput[i].addEventListener("change", totalProduto)
    }

   const buttonadicionarcarrinho = document.getElementsByClassName("button__adicionar-carrinho")
   for (var i = 0; i < buttonadicionarcarrinho.length; i++){
    buttonadicionarcarrinho[i].addEventListener("click", buttonAdicionar)
   }
}

function buttonAdicionar(event){
    const button = event.target
    const produtoInform = button.parentElement
    const produtoImage = produtoInform.getElementsByClassName("alimentos-img")[0].src
    const produtoTitle = produtoInform.getElementsByClassName("produto-title")[0].innerText
    const prodPreco = produtoInform.getElementsByClassName("preco")[0].innerText
    
    let creatProduto =  document.createElement("tr")
    creatProduto.classList.add("produto-adicionado")

    creatProduto.innerHTML = 
    `
    <td class="carrinho__conteudo-img">
    <img src="${produtoImage}" alt="">
    <span class="produto-title">${produtoTitle}</span>
</td>
<td>
    <span class="produto-preco">${prodPreco}</span>
</td>
<td class="remover__quantidade">
    <input class="input__quantidade" type="number" value="1" min="0">
    <button type="button" class="button-remov">Remover</button>
</td>
    `
    console.log(creatProduto)
    const tableBody =  document.getElementsByClassName(".tbody")
    tableBody.append(creatProduto)
}

function removeProdut(event){
    event.target.parentElement.parentElement.remove()
    totalProduto()
}


function totalProduto(){
let totalGeral = 0
const cartProdut = document.getElementsByClassName("produto-adicionado")
for (var i = 0; i < cartProdut.length; i++){
    
    const produtoPreco = cartProdut[i].getElementsByClassName("produto-preco")[0].innerText.replace("R$", "").replace(",", ".")
    const inputQuantidade = cartProdut[i].getElementsByClassName("input__quantidade")[0].value
    
    totalGeral += produtoPreco * inputQuantidade
}
totalGeral = totalGeral.toFixed(2)
totalGeral = totalGeral.replace(".", ",")
document.querySelector(".total__geral span").innerText = "R$" + totalGeral
}


