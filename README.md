# 🚗 Carro Seguidor de Línea (Tkinter + PID + Docker)

Este proyecto implementa un carro virtual que sigue una pista utilizando sensores simulados y un controlador PID. Usa *Tkinter* para mostrar la GUI y está preparado para correr en *Docker*, con opción de ser publicado en **Docker Hub** y alojado en *GitHub*.

---

## 🎥 Demostración en video

> ⚠️ GitHub no permite reproducción embebida de video directamente en el README. Sin embargo, si estás viendo este archivo desde una página web (como GitHub Pages), el video se mostrará a continuación:

<video width="720" controls>
  <source src="Video De Carrito Seguidor.mkv" type="video/x-matroska">
  Tu navegador no puede reproducir este video.
</video>

O simplemente [descárgalo aquí](./Video%20De%20Carrito%20Seguidor.mkv)

---

## 📁 Estructura del proyecto

```
carro_seguidor_docker/
├── CarroFinal.py        # Código fuente con el PID y GUI
├── Dockerfile           # Imagen Docker para ejecutar con entorno gráfico
├── Video De Carrito Seguidor.mkv  # Video de demostración
└── README.md            # Documentación del proyecto
```

---

## 🔧 Requisitos para ejecución local

- Python 3.10 o superior
- Tkinter instalado (incluido en la mayoría de distribuciones)
- Linux, Windows o WSL2 con entorno gráfico

---

## ▶️ Ejecución local

```bash
python CarroFinal.py
```

El programa abrirá una ventana con el carro recorriendo la pista. Está diseñado para seguir una línea negra sobre fondo claro.

---

## 🐳 Construcción y ejecución con Docker

### 🔨 Construcción

```bash
docker build -t carro_gui .
```

### 🚀 Ejecución (en Linux con GUI y X11)

```bash
xhost +local:root

docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --rm \
  carro_gui
```

### 🪟 En Windows con XServer (VcXsrv o X410)

```bash
docker run -it \
  -e DISPLAY=host.docker.internal:0.0 \
  --rm \
  carro_gui
```

---

## ☁️ Subir imagen a Docker Hub

### 1. Inicia sesión:

```bash
docker login
```

### 2. Etiqueta tu imagen:

```bash
docker tag carro_gui cristian039/carro-seguidor:latest
```

### 3. Sube la imagen:

```bash
docker push cristian039/carro-seguidor:latest
```

---

## ⬇️ Descargar y ejecutar desde Docker Hub

```bash
docker pull cristian039/carro-seguidor:latest
```

```bash
docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --rm \
  cristian039/carro-seguidor
```

---

## 🧠 Características del código

- Simulación gráfica con sensores y ruedas
- Control PID con suavizado de movimiento
- Pista curva personalizada
- Parada en estaciones (ej. “Control”)
- Optimizado para entorno Docker + GUI

---

## 🧑‍💻 Autor

**Cristian039**  
Proyecto educativo de simulación y control con Python y Docker.

---
