# Sprint 2: Integración CAG en el Asistente

**Duración:** 1 sesión  
**Objetivo:** Implementar `apply_context()` en CAG e integrarlo en el asistente para personalizar respuestas según el contexto del usuario. Pasar las 3 pruebas de validación.

## Sprint Backlog

| ID | Tarea | Responsable | Estado |
|----|-------|-------------|--------|
| HU-03 | Implementar `apply_context()` en `backend/cag.py` | Norman | Pendiente |
| HU-03 | Integrar CAG en `assistant.py` | Norman | Pendiente |
| HU-05 | Ejecutar tests de validación CAG (deben pasar) | Norman | Pendiente |
| HU-04 | Documentar proceso Scrum (ejecución y cierre) | Norman | Pendiente |
| HU-07 | Crear PROMPTS.md cronológico | Norman | Pendiente |
| HU-08 | Capturar evidencias (pantallazos) | Norman | Pendiente |
| HU-09 | Crear Pull Request y mergear a main | Norman | Pendiente |
| HU-06 | Actualizar README.md con documentación final | Norman | Pendiente |

## Criterios de Aceptación

1. `test_saves_context_for_user` pasa ✅
2. `test_retrieves_context_for_user` pasa ✅
3. `test_ask_uses_context` pasa ✅ (respuesta contiene "principiante" y context_used incluye "audience")
4. PROMPTS.md completo y cronológico
5. Carpeta docs/evidencias/ con capturas
6. README.md documentado
7. PR creado y mergeado a main

## Definition of Done

- [ ] Código implementado en `cag.py` y `assistant.py`
- [ ] 6/6 pruebas pasan (3 base + 3 validación)
- [ ] PROMPTS.md actualizado
- [ ] Evidencias capturadas
- [ ] PR mergeado
- [ ] README actualizado
