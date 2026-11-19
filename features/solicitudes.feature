# language: es
Característica: Solicitudes de compra
  Escenario: Un comprador solicita un producto activo
    Dado que existe un comprador registrado con credenciales válidas
    Y el comprador está autenticado
    Y existe un producto activo de un productor con WhatsApp
    Cuando solicita el producto con cantidad y mensaje válidos
    Entonces se registra una solicitud de compra pendiente
    Y la respuesta redirige a WhatsApp con los datos de la solicitud

  Escenario: El productor propietario acepta una solicitud pendiente
    Dado un productor autenticado con su perfil comercial
    Y tiene una solicitud de compra pendiente
    Cuando acepta la solicitud mediante POST
    Entonces la solicitud queda aceptada

  Escenario: Un productor diferente intenta aceptar una solicitud ajena
    Dado un productor autenticado con su perfil comercial
    Y tiene una solicitud de compra pendiente
    Y se autentica un productor diferente al propietario de la solicitud
    Cuando acepta la solicitud mediante POST
    Entonces se deniega la operación y la solicitud conserva su estado original
