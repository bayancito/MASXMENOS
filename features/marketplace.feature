# language: es
Característica: Operaciones principales del marketplace
  Escenario: Búsqueda de productos por nombre
    Dado un visitante sin iniciar sesión
    Y existen los productos Papa amarilla y Tomate
    Cuando busca papa en el catálogo
    Entonces aparece solamente Papa amarilla en los resultados

  Escenario: Favoritos sin duplicados
    Dado que existe un comprador registrado con credenciales válidas
    Y el comprador está autenticado
    Y existe un producto para agregar a favoritos
    Cuando agrega dos veces el mismo producto a favoritos
    Entonces se conserva un único favorito del comprador para ese producto

  Escenario: Un comprador tiene restringida la creación de productos
    Dado que existe un comprador registrado con credenciales válidas
    Y el comprador está autenticado
    Cuando intenta acceder y enviar datos a la creación de productos
    Entonces se le impide crear productos y es redirigido al inicio

  Escenario: Publicación de un producto por su productor
    Dado un productor autenticado con su perfil comercial
    Cuando completa los datos válidos y publica un producto
    Entonces el producto queda registrado y asociado al productor correspondiente
