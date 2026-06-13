# Proyecto Examen Final - Módulo 3: CAG + SQLite

Asistente inteligente con **Context-Augmented Generation (CAG)** y persistencia en **SQLite**. El contexto del usuario (audiencia, estilo preferido, etc.) se guarda en BD y se inyecta en las respuestas del asistente.

---

## Estructura del proyecto

| Ruta | Contenido |
|---|---|
| `backend/` | Código del servidor y lógica del asistente |
| `backend/server.py` | API REST (FastAPI) |
| `backend/assistant.py` | Orquestación: contexto → RAG → CAG |
| `backend/cag.py` | CAG: modifica respuestas según contexto del usuario |
| `backend/context_store.py` | Persistencia SQLite (tabla `user_context`) |
| `backend/knowledge.py` | Búsqueda en base de conocimiento |
| `frontend/` | Interfaz web estática |
| `data/` | Base de conocimiento (`knowledge_base.json`) y BD SQLite |
| `tests/base/` | 3 pruebas base del proyecto original |
| `tests/validation/` | 3 pruebas de validación de la entrega |
| `tests/test_cag_own.py` | 6 pruebas propias (casos borde) |
| `docs/scrum/` | Artefactos Scrum: backlog, 2 sprints (plan, ejecución, revisión) |
| `docs/sdd.md` | Documento de diseño (arquitectura, flujo, BD, API) |
| `docs/bdd.md` | 10 escenarios Given/When/Then en 5 features |
| `docs/tdd.md` | 4 ciclos TDD (Rojo→Verde→Refactor) |
| `docs/evidencias/` | Evidencias de pruebas y validación |
| `PROMPTS.md` | Trazabilidad de uso de IA (11 entradas cronológicas) |

---

## CAG (Context-Augmented Generation)

El flujo CAG funciona en 3 pasos:

1. **Guardar contexto** → `POST /api/context` con `user_id`, `key`, `value`
2. **Recuperar contexto** → Se obtiene de SQLite al preguntar
3. **Modificar respuesta** → `apply_context()` inyecta contexto en la respuesta

### Claves de contexto soportadas

| Clave | Efecto |
|---|---|
| `audience` | Antepone "Para {valor}:" a la respuesta |
| `preferred_style` | Agrega nota de estilo al final |
| Cualquier otra | Se ignora sin romper |

### Ejemplo

```
# Guardar contexto
POST /api/context {"user_id": "alumno1", "key": "audience", "value": "estudiantes"}

# Preguntar
POST /api/ask {"user_id": "alumno1", "question": "¿Qué es CAG?"}

# Respuesta modificada por CAG
"Para estudiantes: Según la base de conocimiento del curso: CAG usa contexto persistente..."
```

---

## Pruebas

### 12/12 pruebas pasan

| Suite | Archivo | Tests | Estado |
|---|---|---|---|
| Base | `tests/base/test_base_api.py` | 3 | ✅ |
| Validación | `tests/validation/test_cag_contract.py` | 3 | ✅ |
| Propias | `tests/test_cag_own.py` | 6 | ✅ |

### Ejecutar pruebas

```bash
# Todas
PYTHONPATH=. python -m unittest discover -s tests -p "test_*.py" -v

# Individuales
PYTHONPATH=. python -m unittest tests.base.test_base_api -v
PYTHONPATH=. python -m unittest tests.validation.test_cag_contract -v
PYTHONPATH=. python -m unittest tests.test_cag_own -v
```

### Pruebas propias (casos borde)

| Test | Qué verifica |
|---|---|
| `test_context_empty_for_new_user` | Usuario nuevo tiene contexto vacío |
| `test_save_overwrites_existing_key` | Sobrescritura de clave existente |
| `test_multiple_users_context_isolated` | Aislamiento entre usuarios |
| `test_ask_without_context_returns_normal_answer` | Respuesta normal sin contexto |
| `test_ask_with_multiple_context_items` | Múltiples claves combinadas |
| `test_unknown_context_key_does_not_break` | Clave desconocida no rompe |

---

## API Reference

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado del servidor |
| POST | `/api/ask` | Preguntar al asistente (usa RAG + CAG) |
| POST | `/api/context` | Guardar contexto del usuario |
| GET | `/api/context?user_id=X` | Listar contexto del usuario |

---

## Scrum

Metodología Scrum con 2 sprints documentada en `docs/scrum/`:

| Archivo | Contenido |
|---|---|
| `BACKLOG.md` | 9 historias de usuario priorizadas |
| `SPRINT1_PLAN.md` | Planificación sprint 1 (ContextStore + CAG) |
| `SPRINT1_EXECUTION.md` | Ejecución sprint 1 |
| `SPRINT1_REVIEW.md` | Revisión y retrospectiva sprint 1 |
| `SPRINT2_PLAN.md` | Planificación sprint 2 (pruebas + documentación) |
| `SPRINT2_EXECUTION.md` | Ejecución sprint 2 |
| `SPRINT2_REVIEW.md` | Revisión y retrospectiva sprint 2 |

---

## Inicio rápido

```bash
# 1. Instalar dependencias
pip install fastapi uvicorn

# 2. Ejecutar backend
$env:PYTHONPATH="."; python -m backend.server

# 3. Abrir frontend
# Abrir frontend/index.html en el navegador

# 4. Probar salud
curl http://127.0.0.1:8000/health
```

---

## Tecnologías

- **FastAPI** + **uvicorn** — API REST
- **SQLite** — Persistencia de contexto (sin dependencias externas)
- **HTML/CSS/JS** — Frontend estático
- **unittest** — Pruebas

---

## Repositorio

Fork: `github.com/ndm2025/final_project_AI_CUSTOM`
