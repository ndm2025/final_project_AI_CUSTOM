# Sprint 1: Implementación de ContextStore

**Duración:** 1 sesión  
**Objetivo:** Implementar el almacenamiento y recuperación de contexto persistente (ContextStore) y verificar que los endpoints `/api/context` funcionan.

## Sprint Backlog

| ID | Tarea | Responsable | Estado |
|----|-------|-------------|--------|
| HU-01 | Implementar `ContextStore.save()` en `backend/context_store.py` | Norman | Pendiente |
| HU-02 | Implementar `ContextStore.list_for_user()` en `backend/context_store.py` | Norman | Pendiente |
| HU-01 | Verificar que POST /api/context responde 201 | Norman | Pendiente |
| HU-02 | Verificar que GET /api/context recupera contexto | Norman | Pendiente |
| - | Ejecutar tests base (deben seguir pasando) | Norman | Pendiente |
| - | Commit incremental con cambios de ContextStore | Norman | Pendiente |

## Criterios de Aceptación

1. `POST /api/context` con `{user_id, key, value}` → `201 {"saved": true}`
2. `GET /api/context?user_id=X` → `200 {user_id, context: [...]}`
3. Los 3 tests base siguen pasando
4. Cada archivo modificado tiene commit propio

## Definition of Done

- [ ] Código implementado en `context_store.py`
- [ ] Prueba manual con curl o script
- [ ] Tests base pasan
- [ ] Commit creado
