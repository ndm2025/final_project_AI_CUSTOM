# SDD - Specification-Driven Design

## Documento de Diseño - Módulo CAG

### 1. Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND (HTML/CSS/JS)               │
│  index.html  ←→  app.js  ←→  fetch(/api/*)              │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP (JSON)
                       ▼
┌─────────────────────────────────────────────────────────┐
│                     BACKEND (Python)                     │
│                                                         │
│  server.py ──→ assistant.py ──→ knowledge.py (RAG)      │
│       │               │                                  │
│       │               ▼                                  │
│       │          cag.py (apply_context)                   │
│       │               │                                  │
│       ▼               ▼                                  │
│  context_store.py (SQLite)                                │
└─────────────────────────────────────────────────────────┘
```

### 2. Flujo de Datos

```
POST /api/ask {user_id, question}
  │
  ├─ 1. assistant.answer_question()
  │     ├─ 2. context_store.list_for_user()  → contexto
  │     ├─ 3. knowledge.retrieve_snippets()   → RAG
  │     ├─ 4. cag.apply_context()             → CAG
  │     └─ 5. response {answer, sources, context_used}
  │
  └─ Response 200 JSON
```

### 3. Diseño de la Base de Datos

**Tabla: user_context**

| Columna | Tipo | Restricción |
|---------|------|-------------|
| user_id | TEXT | NOT NULL, PK |
| key | TEXT | NOT NULL, PK |
| value | TEXT | NOT NULL |

**Operaciones SQL:**
- `INSERT OR REPLACE INTO user_context (user_id, key, value) VALUES (?, ?, ?)`
- `SELECT key, value FROM user_context WHERE user_id = ?`

### 4. Diseño de la API

| Método | Endpoint | Request | Response |
|--------|----------|---------|----------|
| GET | /health | - | 200 {status: "ok"} |
| POST | /api/ask | {user_id, question} | 200 {answer, sources, context_used} |
| POST | /api/context | {user_id, key, value} | 201 {saved: true} |
| GET | /api/context | ?user_id=X | 200 {user_id, context: [...]} |

### 5. Diseño de apply_context()

```
Entrada: (user_id, question, base_answer, context_items)
Proceso:
  - Iterar sobre context_items (lista de {key, value})
  - Si key = "audience" → anteponer "Para {value}: " a la respuesta
  - Si key = "preferred_style" → agregar nota al final
  - Si key no reconocida → ignorar sin error
Salida: (answer_modificada, [keys_used])
```

### 6. Decisiones de Diseño

| Decisión | Opción Elegida | Alternativa | Razón |
|----------|---------------|-------------|-------|
| Persistencia | SQLite | Dict en memoria | Los datos sobreviven al reinicio |
| Singleton | get_store() | Inyección de dependencia | Mantiene compatibilidad con tests existentes |
| Formato contexto | Lista de {key, value} | Objeto plano | Formato esperado por tests de validación |
| Modificación respuesta | Prefijo/nota | Prompt dinámico | Simple, verificable, sin dependencias LLM |
