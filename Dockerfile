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
