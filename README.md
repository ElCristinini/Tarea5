# 🧠 Tarea 5 – Sistemas Operativos

**Autores:** Cristian Olarte y Ana Vargas  
**Fecha:** Mayo 2025

---

## 🚗 Carro Seguidor de Línea  
**Tecnologías:** Tkinter · PID · Docker

Este módulo simula un carro virtual que sigue una pista usando sensores simulados y un controlador PID. Se visualiza en una GUI desarrollada con Tkinter y está preparado para ejecutarse dentro de un contenedor Docker.

---

### 🎥 Demostración en video

> ⚠️ GitHub no permite reproducir videos directamente en el README.  
> Si estás viendo este archivo en GitHub, busca el archivo `Video De Carrito Seguidor.mkv`, haz clic en **“View Raw”** para descargarlo y reproducirlo localmente.

---

### 📁 Estructura del Proyecto

```
carro_seguidor_docker/
├── CarroFinal.py                   # Código fuente principal (PID + GUI)
├── Dockerfile                      # Imagen Docker con entorno gráfico
├── Video De Carrito Seguidor.mkv  # Video de demostración
└── README.md                       # Documentación del proyecto
```

---

### 🔧 Requisitos para ejecución local

- Python 3.10 o superior  
- Tkinter instalado  
- Sistema operativo con entorno gráfico (Linux, Windows o WSL2)

---

### ▶️ Cómo ejecutar localmente

```bash
python CarroFinal.py
```

---

### 🐳 Construcción y ejecución con Docker

#### 🔨 Construcción

```bash
docker build -t carro_gui .
```

#### 🚀 Ejecución en Linux con entorno gráfico

```bash
xhost +local:root

docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --rm \
  carro_gui
```

#### 🪟 En Windows (con VcXsrv o X410)

```bash
docker run -it \
  -e DISPLAY=host.docker.internal:0.0 \
  --rm \
  carro_gui
```

---

### ☁️ Subir imagen a Docker Hub

```bash
docker login
docker tag carro_gui cristian039/carro-seguidor:latest
docker push cristian039/carro-seguidor:latest
```

---

### ⬇️ Descargar y ejecutar desde Docker Hub

```bash
docker pull cristian039/carro-seguidor:latest
docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --rm \
  cristian039/carro-seguidor
```

---

## 🌌 Galaxy Rush – Juego de Naves  
**Tecnologías:** Pygame · Docker

Juego personalizado con:

- Imágenes únicas para naves, enemigos, disparos y fondos  
- Aparición de jefe (boss alien verde)  
- Power-ups: velocidad, disparo doble, disparo rápido  
- Sistema de vidas, colisiones y puntuación  
- Contenedor Docker listo para usar

### 🐳 Docker

```bash
docker pull cristian039/galaxy-rush:latest
docker run -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --rm \
  cristian039/galaxy-rush
```

---

## 🤖 ROS en Docker: Talker & Listener  
**Tecnologías:** ROS Noetic · Docker

Implementación básica de dos nodos:

- `talker.py`: publica mensajes
- `listener.py`: recibe y muestra mensajes

### 🔧 Ejecución

1. Iniciar contenedor con `talker`:

```bash
docker run -it --name tarea5 cristian039/ros-tarea5 ./start_talker.sh
```

2. En otra terminal:

```bash
docker exec -it tarea5 bash -c "source /opt/ros/noetic/setup.bash && python3 listener.py"
```

> 🎥 El video `video de Ros, comprobacion.mkv` muestra la ejecución. Descárgalo desde GitHub si es necesario.

---

## 👥 Créditos

Cristian Olarte y Ana Vargas  
Proyecto educativo para la asignatura **Sistemas Operativos – Tarea 5**.  
Incluye simulaciones gráficas, comunicación entre procesos y ejecución con Docker.

---
