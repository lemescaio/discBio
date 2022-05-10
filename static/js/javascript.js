function Check(el) {
    var button = document.getElementById("botaoEnviar");
    var TBra = document.getElementById("ra");
    var TBnome = document.getElementById("nome");
    var TBemail = document.getElementById("email");
    var nbr_checked_radios = document.querySelectorAll('input[type=radio]:checked').length;

    if (TBra.value === "" || TBnome.value === "" || TBemail.value === "") {
      alert("Preencha seu nome, e-mail e RA");
    }
    if (nbr_checked_radios!==24 || TBra.value === "" || TBnome.value === "" || TBemail.value === "") {
      button.disabled = true;
    } else {
      button.disabled = false;
    }
  }