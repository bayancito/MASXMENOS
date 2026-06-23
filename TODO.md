# MASXMENOS — Reorganización de permisos y navegación (RBAC)

## Paso 1 — Preparación
- [ ] Crear/actualizar checklist en este archivo.

## Paso 2 — Decoradores RBAC
- [ ] Actualizar `apps/usuarios/decorators.py` con validaciones/redirects por rol:
  - [ ] Decorador para ADMIN
  - [ ] Decorador para COMPRADOR (redirigir a `login` si no autenticado; redirigir a `inicio` si rol inválido)
  - [ ] Decorador para PRODUCTOR (redirigir a `inicio` si rol inválido)
- [ ] Mantener compatibilidad con decoradores actuales (`es_admin`, `es_productor_o_admin`).

## Paso 3 — Proteger reportes globales (ADMIN)
- [ ] Actualizar `apps/reportes/views.py`:
  - [ ] Proteger `reportes`, `exportar_productos_excel`, `exportar_productores_excel`, `exportar_pdf` a ADMIN
  - [ ] Restringir `crear_incidencia` y `incidencia_list` a ADMIN (login requerido + rol ADMIN)

## Paso 4 — Proteger favoritos (COMPRADOR)
- [ ] Actualizar `apps/productos/views_favoritos.py`:
  - [ ] Bloquear `agregar_favorito` y `mis_favoritos` a COMPRADOR (no productores/admin salvo ADMIN según spec: aquí solo COMPRADOR)
  - [ ] Si no está autenticado, redirigir a `login`.

## Paso 5 — Proteger “comprar” (VISITANTE -> login)
- [ ] Actualizar `apps/productos/views.py`:
  - [ ] Asegurar que `solicitar_producto`:
    - [ ] Si VISITANTE -> redirect a `login`
    - [ ] Si rol != COMPRADOR -> redirect a `login` (para cumplir “redirección segura” hacia login)
    - [ ] Mantener `detalle_producto` sin romper rutas existentes.

## Paso 6 — Proteger edición/eliminación de productos (rol consistente)
- [ ] Actualizar `apps/productos/views.py`:
  - [ ] Asegurar que `editar_producto` y `eliminar_producto`:
    - [ ] VISITANTE/COMPRADOR no puedan
    - [ ] PRODUCTOR solo pueda sus productos
    - [ ] ADMIN pueda
  - [ ] Usar decoradores nuevos o validación consistente al inicio.

## Paso 7 — Menú dinámico según rol
- [ ] Actualizar `templates/base.html`:
  - [ ] Render condicional para ocultar/mostrar links según rol:
    - [ ] VISITANTE: sin favoritos, sin paneles, sin reportes
    - [ ] COMPRADOR: favoritos + panel comprador
    - [ ] PRODUCTOR: panel productor (y ocultar favoritos)
    - [ ] ADMIN: acceso a reportes globales (y mantener resto según necesidad)
- [ ] Evitar errores si `request.user.perfil` no existe.

## Paso 8 — Revisión final y validación manual
- [ ] Verificar que no se rompieron rutas existentes (nombres `name=` intactos)
- [ ] Verificar redirecciones seguras
- [ ] Generar informe final: archivos modificados + permisos corregidos
