# MASXMENOS — Sprint 8 (Chart.js) — TODO

- [x] Revisar y extender `apps/reportes/views.py` para:
  - [x] Preparar `productos_por_categoria` y `productores_por_municipio`
  - [x] Agregar al contexto: `categorias_labels`, `categorias_data`, `municipios_labels`, `municipios_data`
  - [x] Asegurar que el frontend reciba datos en formato JSON para Chart.js (vía `json.dumps`)
- [x] Actualizar `templates/reportes/reportes.html` para:
  - [x] Incluir CDN de Chart.js
  - [x] Agregar cards con `canvas` para:
    - [x] Barras: `graficoCategorias`
    - [x] Pie: `graficoMunicipios`
  - [x] Agregar JS para renderizar ambos gráficos usando los datos del contexto
- [ ] Verificar que las tablas y cards existentes no se rompan y que los gráficos carguen correctamente
