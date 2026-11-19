# language: es
Característica: Acceso a favoritos
  Escenario: Un visitante intenta acceder a favoritos sin iniciar sesión y es redirigido al login
    Dado un visitante sin iniciar sesión
    Cuando intenta acceder a sus favoritos
    Entonces es redirigido al login
