# Chrotrixum

Chrotrixum es un navegador de escritorio experimental construido con Python, PyQt6 y QtWebEngine.

> **Estado:** desarrollo temprano. No se considera listo para manejar información sensible.

## Requisitos

- Python 3.10 o posterior.
- Dependencias de sistema necesarias para QtWebEngine en tu distribución de Linux.

## Instalación en Fedora/Linux

```bash
git clone https://github.com/programador777lolxddd-dot/Chrotrixum.git
cd Chrotrixum

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Ejecutar

```bash
python main.py
# O, tras instalar el proyecto:
chrotrixum
```

## Desarrollo

Instala herramientas de revisión opcionales:

```bash
python -m pip install ruff pytest
ruff check .
pytest
```

## Seguridad

Chrotrixum está en una fase inicial. Antes de recomendarlo para uso diario, el proyecto necesita una revisión específica de seguridad, incluyendo gestión de permisos web, descargas, certificados TLS, perfiles y datos privados. No desactives la validación de certificados para hacer que un sitio cargue.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE.
