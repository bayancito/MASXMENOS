# 📋 Guía para Personalizar Login y Registro

## ¿Cómo cambiar el fondo y las imágenes?

El archivo [auth-styles.css](../../static/css/auth-styles.css) contiene variables CSS que puedes personalizar fácilmente.

### 🎨 Variables Disponibles

En la sección `:root` del archivo `auth-styles.css` encontrarás:

```css
:root {
    /* COLORES DEL GRADIENTE DE FONDO */
    --bg-gradient-1: #a855f7;      /* Color 1 (púrpura) */
    --bg-gradient-2: #ec4899;      /* Color 2 (rosa) */
    --bg-gradient-3: #f97316;      /* Color 3 (naranja) */
    
    /* IMAGEN DE FONDO (opcional - comentar para usar solo gradiente) */
    --bg-image: none;
    --bg-image-size: cover;
    --bg-image-position: center;
    
    /* IMAGEN DEL PANEL IZQUIERDO (opcional) */
    --left-panel-bg-image: none;
    --left-panel-bg-size: cover;
    --left-panel-bg-position: center;
    
    /* COLORES GENERALES */
    --accent-color: #3b82f6;        /* Color azul de botones */
    --accent-hover: #2563eb;        /* Color azul al pasar cursor */
}
```

---

## 📝 Ejemplos de Personalización

### ✅ Ejemplo 1: Cambiar solo los colores del gradiente

```css
:root {
    --bg-gradient-1: #1e40af;   /* Azul oscuro */
    --bg-gradient-2: #06b6d4;   /* Cian */
    --bg-gradient-3: #10b981;   /* Verde */
}
```

### ✅ Ejemplo 2: Agregar una imagen de fondo

```css
:root {
    --bg-image: url('/media/fondo-campos.jpg');
    --bg-image-size: cover;
    --bg-image-position: center;
}
```

### ✅ Ejemplo 3: Agregar imagen en el panel izquierdo

```css
:root {
    --left-panel-bg-image: url('/media/agricultura.jpg');
    --left-panel-bg-size: cover;
    --left-panel-bg-position: center;
}
```

### ✅ Ejemplo 4: Combinación completa

```css
:root {
    /* Gradiente de fondo */
    --bg-gradient-1: #059669;   /* Verde agrícola */
    --bg-gradient-2: #10b981;
    --bg-gradient-3: #34d399;
    
    /* Imagen de fondo opcional */
    --bg-image: url('/media/campo-fondo.jpg');
    --bg-image-size: cover;
    --bg-image-position: center;
    
    /* Panel izquierdo */
    --left-panel-bg-image: url('/media/productor.jpg');
    --left-panel-bg-size: cover;
    --left-panel-bg-position: center;
    
    /* Color de énfasis */
    --accent-color: #059669;
    --accent-hover: #047857;
}
```

---

## 🚀 Cómo usar URLs de imágenes

### Rutas relativas (recomendado):
```css
--bg-image: url('/static/img/fondo.jpg');
--left-panel-bg-image: url('/media/imagen.jpg');
```

### URLs externas:
```css
--bg-image: url('https://example.com/imagen.jpg');
```

### Con Static files de Django:
```css
--bg-image: url('/static/img/fondo-campos.jpg');
```

---

## 📂 Dónde guardar tus imágenes

1. **Para imágenes estáticas:** `static/img/`
   - Ejemplo: `/static/img/fondo.jpg`

2. **Para imágenes de media:** `media/`
   - Ejemplo: `/media/imagen.jpg`

---

## 🎯 Cambios en vivo

1. Abre [auth-styles.css](../../static/css/auth-styles.css)
2. Modifica las variables en `:root`
3. Guarda el archivo (Ctrl+S)
4. Recarga la página del navegador (F5)

---

## 💡 Consejos

- **Usar degradados puros:** Deja `--bg-image: none;`
- **Mezclar gradiente + imagen:** Ambas opciones funcionan juntas, la imagen aparece sobre el gradiente
- **Imágenes responsivas:** Usa `background-size: cover` para que la imagen se adapte a cualquier pantalla
- **Prueba diferentes colores:** Visita https://coolors.co/ para inspiración

---

## ⚙️ Parámetros CSS disponibles

| Variable | Propósito | Ejemplo |
|----------|-----------|---------|
| `--bg-gradient-1/2/3` | Colores del gradiente principal | `#a855f7` |
| `--bg-image` | Imagen de fondo (cuerpo) | `url('/static/img/fondo.jpg')` |
| `--bg-image-size` | Tamaño de la imagen | `cover`, `contain`, `100% 100%` |
| `--bg-image-position` | Posición de la imagen | `center`, `top left`, `bottom right` |
| `--left-panel-bg-image` | Imagen del panel izquierdo | `url('/media/imagen.jpg')` |
| `--left-panel-bg-size` | Tamaño del panel | `cover`, `contain` |
| `--left-panel-bg-position` | Posición del panel | `center` |
| `--accent-color` | Color botones | `#3b82f6` |
| `--accent-hover` | Color al pasar cursor | `#2563eb` |

---

## 🔧 Posibles valores para background-size

- `cover` - Cubre todo el elemento (puede cortar)
- `contain` - Muestra completa la imagen (puede dejar espacios)
- `100% 100%` - Estira la imagen
- `auto` - Tamaño original

---

## 📱 Responsividad

El diseño es 100% responsivo. En móviles:
- Las dos columnas se apilan verticalmente
- Las imágenes se adaptan automáticamente
- Los botones y formularios son touch-friendly

