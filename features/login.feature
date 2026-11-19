# language: es
Característica: Inicio de sesión
  Escenario: Inicio de sesión correcto de un comprador
    Dado que existe un comprador registrado con credenciales válidas
    Cuando introduce sus credenciales en el formulario de login
    Entonces el sistema lo autentica y redirige al inicio
