// Evita envíos duplicados y lleva el foco al primer error al volver del servidor.
(function () {
  var form = document.getElementById('formulario');
  if (form) {
    form.addEventListener('submit', function () {
      var boton = document.getElementById('boton-enviar');
      boton.disabled = true;
      boton.textContent = 'Calculando…';
    });
  }
  var primero = document.querySelector('.con-error input, .con-error select');
  if (primero) { primero.focus(); }
})();
