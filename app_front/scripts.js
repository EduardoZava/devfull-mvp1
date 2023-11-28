/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/fornecedores';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.fornecedor.forEach(item => insertList(item.nome, item.descricao))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()


/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputFornecedor, inputDescription) => {
  const formData = new FormData();
  formData.append('nome', inputFornecedor);
  formData.append('descricao', inputDescription);


  let url = 'http://127.0.0.1:5000/fornecedor';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}


/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/fornecedor?nome=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo Fornecedor com nome, descricao
  --------------------------------------------------------------------------------------
*/
const newItem = () => {
  console.log("newItem")
  let inputFornecedor = document.getElementById("newInput").value;
  let inputDescription = document.getElementById("newDescription").value;
  

  if (inputFornecedor === '') {
    alert("Preencha o nome do Fornecedor!");
  } else if (inputDescription === '' ) {
    alert("Descricao deve ser preenchida!");
  } else if (insertList(inputFornecedor, inputDescription)) {
    postItem(inputFornecedor, inputDescription)
    alert("Fornecedor adicionado!")
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (nameFornecedor, description) => {
  var item = [nameFornecedor, description]
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  // Verifica se o fornecedor já existe na lista
  var existingFornecedores = Array.from(table.getElementsByTagName('td'), cell => cell.textContent);
  if (existingFornecedores.includes(nameFornecedor)) {
     alert("Esse fornecedor já existe na lista!");
    return;
  }

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1))
  document.getElementById("newInput").value = "";
  document.getElementById("newDescription").value = "";

  removeElement()
}