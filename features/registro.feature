# language: es
Característica: Validación del registro
  Escenario: Registro con contraseñas diferentes
    Dado que un visitante completa el formulario de registro
    Y escribe contraseñas diferentes
    Cuando envía el formulario
    Entonces el sistema muestra un error de validación
    Y no registra un nuevo usuario
