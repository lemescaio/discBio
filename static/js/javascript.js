function Check(el) {
    var button = document.getElementById("botaoEnviar");
    var TBra = document.getElementById("ra");
    var TBnome = document.getElementById("nome");
    var TBemail = document.getElementById("email");
    var TAluno_empregado = document.getElementById('aluno_empregado').value;
    var nbr_checked_radios = document.querySelectorAll('input[type=radio]:checked').length;

  if (TBra.value === "" || TBnome.value === "" || TBemail.value === "" || TAluno_empregado === '0') {
    alert(TAluno_empregado);
      alert("Preencha seu nome, e-mail, RA e Situação");
    }
    if (nbr_checked_radios!==24 || TBra.value === "" || TBnome.value === "" || TBemail.value === "" || TAluno_empregado === '0') {
      button.disabled = true;
    } else {
      button.disabled = false;
    }
  }