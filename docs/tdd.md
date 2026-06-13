# TDD - Test-Driven Development

## Ciclo TDD: Rojo → Verde → Refactor

### Ciclo 1: ContextStore

**Paso 1 - Rojo:** Ejecutar tests de validación (fallan porque ContextStore no está implementado)

```
test_saves_context_for_user → 501 NotImplementedError ✗
test_retrieves_context_for_user → 501 NotImplementedError ✗
test_ask_uses_context → 501 NotImplementedError ✗
```

**Paso 2 - Verde:** Implementar ContextStore con SQLite

```python
# context_store.py
class ContextStore:
    def save(self, user_id, key, value):
        # INSERT OR REPLACE INTO user_context
        return True

    def list_for_user(self, user_id):
        # SELECT key, value FROM user_context WHERE user_id = ?
        return [{"key": k, "value": v}]
```

**Resultado:**
```
test_saves_context_for_user → 201 ✔
test_retrieves_context_for_user → 200 ✔
test_ask_uses_context → 200 ✔ (pero context_used vacío)
```

**Paso 3 - Refactor:** Agregar singleton get_store() para compartir entre módulos.

---

### Ciclo 2: apply_context()

**Paso 1 - Rojo:** test_ask_uses_context falla porque context_used es []

```python
self.assertIn("principiante", body["answer"].lower())  # ✗
self.assertIn("audience", body["context_used"])  # ✗
```

**Paso 2 - Verde:** Implementar apply_context()

```python
# cag.py
def apply_context(user_id, question, base_answer, context_items):
    for item in context_items:
        if item["key"] == "audience":
            answer = f"Para {item['value']}: {answer}"
            keys_used.append("audience")
    return answer, keys_used
```

**Resultado:**
```
test_ask_uses_context → "principiante" encontrado ✔
test_ask_uses_context → "audience" en context_used ✔
```

---

### Ciclo 3: Integración en assistant.py

**Paso 1 - Rojo:** assistant.py no usaba contexto (context_used = [])

**Paso 2 - Verde:** Integrar flujo completo

```python
# assistant.py
def answer_question(user_id, question):
    context_items = get_store().list_for_user(user_id)
    snippets = retrieve_snippets(question)
    answer, keys_used = apply_context(user_id, question, base_answer, context_items)
    return {"answer": answer, "context_used": keys_used, ...}
```

**Resultado:** Todos los tests de validación pasan.

---

### Ciclo 4: Pruebas Propias

**Paso 1 - Diseñar:** Identificar casos borde no cubiertos

| Caso | Test |
|------|------|
| Usuario sin contexto | test_context_empty_for_new_user |
| Sobrescribir clave | test_save_overwrites_existing_key |
| Aislamiento usuarios | test_multiple_users_context_isolated |
| Sin contexto al preguntar | test_ask_without_context_returns_normal_answer |
| Múltiples items | test_ask_with_multiple_context_items |
| Clave desconocida | test_unknown_context_key_does_not_break |

**Paso 2 - Ejecutar:** 6/6 pruebas propias pasan ✔

---

## Resultado Final

| Suite | Pruebas | Estado |
|-------|---------|--------|
| Tests Base (test_base_api.py) | 3 | ✅ Pasan |
| Tests Validación (test_cag_contract.py) | 3 | ✅ Pasan |
| Tests Propios (test_cag_own.py) | 6 | ✅ Pasan |
| **Total** | **12** | **✅ 100%** |

## Cobertura de Funcionalidades

| Funcionalidad | Probada por |
|--------------|-------------|
| Servidor responde | test_health_returns_ok |
| RAG responde con conocimiento | test_ask_answers_from_knowledge_base |
| Validación de request | test_ask_requires_user_and_question |
| Guardar contexto | test_saves_context_for_user |
| Recuperar contexto | test_retrieves_context_for_user |
| CAG modifica respuesta | test_ask_uses_context |
| Contexto vacío para nuevo usuario | test_context_empty_for_new_user |
| Sobrescritura de claves | test_save_overwrites_existing_key |
| Aislamiento entre usuarios | test_multiple_users_context_isolated |
| Respuesta normal sin contexto | test_ask_without_context_returns_normal_answer |
| Múltiples items de contexto | test_ask_with_multiple_context_items |
| Robustez ante claves desconocidas | test_unknown_context_key_does_not_break |
