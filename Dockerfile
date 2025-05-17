<<<<<<< HEAD
FROM python:3.10-slim

# Instalar Tkinter y librerías gráficas necesarias
RUN apt-get update && apt-get install -y \
    python3-tk \
    x11-apps \
    libxrender1 libxext6 libsm6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta de trabajo
WORKDIR /app

# Copiar el archivo de la app
COPY CarroFinal.py .

# Comando para ejecutar la GUI
CMD ["python3", "CarroFinal.py"]
=======
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "JueguitoNavesita.py"]
>>>>>>> 0d7be45 (Segunda parte de tarea 5)
