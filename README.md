# Proyecto Examen Final - Módulo 3

Proyecto base para la evaluación práctica del módulo 3. Los requisitos oficiales están en `Enunciado en la serie II de la evaluación final`.

## Inicio rápido

1. Abra la carpeta `ProyectoExamen`.
2. Ejecute las pruebas base.
3. Levante el backend.
4. Abra el frontend para revisar el estado inicial.

## Estructura

| Ruta | Contenido |
|---|---|
| `backend/` | Código del servidor y lógica base del asistente. |
| `frontend/` | Interfaz web estática para interactuar con el backend. |
| `data/` | Base de conocimiento inicial del proyecto. |
| `tests/base/` | Pruebas base que deben pasar desde el inicio. |
| `tests/validation/` | Pruebas de validación de la entrega final. |
| `docs/` | Espacio para documentación técnica y evidencias del estudiante. |

## Ejecutar pruebas base

```bash
./scripts/run_base_tests.sh
```

Estas pruebas validan que el proyecto inicial funciona correctamente.

## Ejecutar backend

```bash
PYTHONPATH=. python3 -m backend.server
```

El backend queda disponible en `http://127.0.0.1:8000`.

## Abrir frontend

Abra `frontend/index.html` en un navegador. También puede servir la carpeta con un servidor estático local si lo prefiere.

## Validación final

```bash
./test.sh
```

En el proyecto base, la validación final está destinada a fallar. Debe utilizarse como autoevaluación cuando el trabajo solicitado en el enunciado esté completo.
