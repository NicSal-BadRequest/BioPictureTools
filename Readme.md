## Descripción

BioPictureTools es un conjunto de herramientas escritas en Python para procesar y analizar imágenes de microscopía. Permite, entre otras cosas:

    -Detección y rastreo de núcleos
    -Análisis de fluorescencia
    -Manejo de sets de imágenes
    -Versiones compatibles con ambientes locales y Google Colab

## Características

Interfaz de línea de comando / scripts fáciles de usar

Utiliza bioio y bioio_bioformats para leer formatos comunes de bioimagen

Modular: varios scripts para distintos tipos de análisis

## Requisitos

Para poder usar BioPictureTools, necesitas tener:

    -Python 3.x
    -Java (OpenJDK u otra distribución compatible)
    -Dependencias de Python que puedan estar en requirements.txt (o las que los scripts usen)

## Instalación

Aquí los pasos para instalar/configurar el entorno en una PC con Linux (u otro sistema *nix).

```bash
# Ver qué versión de Java está siendo usada o dónde está instalado:
readlink -f $(which java)

# Si usás bash:
nano ~/.bashrc

# O si usás zsh:
nano ~/.zshrc

# Agregar/editar estas líneas en el archivo correspondiente:
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH

# Luego recargar el archivo de configuración:

source ~/.bashrc
# o si usás zsh
source ~/.zshrc

```

Instala las dependencias 

```bash
pip3 install -r requirements.txt
```

## Estructura del proyecto:

```bash
BioPictureTools/
├── BioImageHandler/        # scripts relacionados con manejo de imágenes
├── RastreadorNucleos/      # scripts para detección/rastreo de núcleos
├── SetImagenes_1/          # ejemplos o procesamiento por lotes de conjuntos
├── VersionColab/           # notebooks / scripts preparados para Google Colab
├── main.py                 # script principal
├── LICENSE
├── README.md
└── (otros scripts .py / notebooks / recursos)
```

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, revisá el archivo LICENSE.
