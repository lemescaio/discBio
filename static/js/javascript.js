function Check(el) {
    var button = document.getElementById("botaoEnviar");
    var TBra = document.getElementById("ra");
    var TBnome = document.getElementById("nome");
    var TBemail = document.getElementById("email");
    var TAluno_empregado = document.getElementById('aluno_empregado').value;

    if (TBra.value === "" || TBnome.value === "" || TBemail.value === "" || TAluno_empregado === '0') {
      alert("Preencha seu nome, e-mail, RA e Situação");
    }
    if (TBra.value === "" || TBnome.value === "" || TBemail.value === "" || TAluno_empregado === '0') {
      button.disabled = true;
    } else {
      button.disabled = false;
    }
}

function Retorno(el) {

    var TBretorno = document.getElementById("retorno");

    if (TBretorno === "****Responder todas as perguntas****") {
      alert("Responda todas as perguntas!");
    }

}