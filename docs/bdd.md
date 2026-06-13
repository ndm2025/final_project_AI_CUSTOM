# BDD - Behavior-Driven Development

## Escenarios de Comportamiento - Módulo CAG

### Feature: Guardar Contexto de Usuario

```gherkin
Feature: Guardar Contexto de Usuario
  Como usuario del sistema
  Quiero guardar información de contexto (clave-valor)
  Para que el asistente pueda personalizar sus respuestas

  Scenario: Guardar contexto exitosamente
    Given el usuario "luis" no tiene contexto guardado
    When envía POST /api/context con {"user_id": "luis", "key": "audience", "value": "principiante"}
    Then el sistema responde con status 201
    And el cuerpo contiene {"saved": true}

  Scenario: Sobrescribir contexto existente
    Given el usuario "luis" tiene contexto {"audience": "principiante"}
    When envía POST /api/context con {"user_id": "luis", "key": "audience", "value": "experto"}
    Then el sistema responde con status 201
    And el valor de "audience" es ahora "experto"

  Scenario: Guardar múltiples claves
    Given el usuario "ana" no tiene contexto guardado
    When envía POST /api/context con {"user_id": "ana", "key": "style", "value": "analogias"}
    And envía POST /api/context con {"user_id": "ana", "key": "language", "value": "español"}
    Then el sistema tiene 2 items de contexto para "ana"
```

### Feature: Recuperar Contexto de Usuario

```gherkin
Feature: Recuperar Contexto de Usuario
  Como usuario del sistema
  Quiero recuperar mi contexto guardado
  Para verificar qué información tiene el sistema sobre mí

  Scenario: Recuperar contexto de usuario existente
    Given el usuario "luis" tiene contexto guardado
    When envía GET /api/context?user_id=luis
    Then el sistema responde con status 200
    And el cuerpo contiene "user_id": "luis"
    And el cuerpo contiene una lista "context" con los items guardados

  Scenario: Recuperar contexto de usuario nuevo
    Given el usuario "nuevo" nunca ha guardado contexto
    When envía GET /api/context?user_id=nuevo
    Then el sistema responde con status 200
    And el cuerpo contiene "context": []

  Scenario: Recuperar contexto sin user_id
    When envía GET /api/context
    Then el sistema responde con status 400
    And el cuerpo contiene {"error": "user_id is required"}
```

### Feature: Usar Contexto en Respuestas (CAG)

```gherkin
Feature: Usar Contexto en Respuestas
  Como usuario del sistema
  Quiero que el asistente use mi contexto al responder
  Para obtener respuestas personalizadas según mis preferencias

  Scenario: Respuesta personalizada por audiencia
    Given el usuario "luis" tiene contexto {"audience": "explicar como principiante"}
    When envía POST /api/ask con {"user_id": "luis", "question": "Qué es CAG?"}
    Then el sistema responde con status 200
    And la respuesta contiene "principiante"
    And "context_used" incluye "audience"

  Scenario: Respuesta sin contexto
    Given el usuario "nuevo" no tiene contexto guardado
    When envía POST /api/ask con {"user_id": "nuevo", "question": "Qué es RAG?"}
    Then el sistema responde con status 200
    And "context_used" es []
    And la respuesta contiene el conocimiento del curso

  Scenario: Múltiples contextos aplicados
    Given el usuario "multi" tiene contexto:
      | key             | value              |
      | audience        | experto            |
      | preferred_style | detalles tecnicos  |
    When envía POST /api/ask con {"user_id": "multi", "question": "Qué es CAG?"}
    Then el sistema responde con status 200
    And "context_used" incluye "audience"
    And "context_used" incluye "preferred_style"
    And la respuesta contiene "audience" y "preferred_style"
```

### Feature: Aislamiento de Contexto entre Usuarios

```gherkin
Feature: Aislamiento de Contexto entre Usuarios
  Como usuario del sistema
  Quiero que mi contexto sea privado
  Para que otros usuarios no vean mi información

  Scenario: Contexto aislado por usuario
    Given el usuario "a" guarda contexto {"city": "guatemala"}
    And el usuario "b" guarda contexto {"city": "quetzaltenango"}
    When se recupera el contexto del usuario "a"
    Then el contexto contiene "guatemala"
    And el contexto NO contiene "quetzaltenango"
```

### Feature: Robustez ante Claves Desconocidas

```gherkin
Feature: Robustez ante Claves Desconocidas
  Como sistema
  Quiero ignorar claves de contexto no reconocidas
  Para no romper el flujo de respuesta

  Scenario: Clave desconocida no rompe la respuesta
    Given el usuario "unk" guarda contexto {"some_random_key": "test"}
    When envía POST /api/ask con {"user_id": "unk", "question": "Qué es BDD?"}
    Then el sistema responde con status 200
    And "context_used" NO incluye "some_random_key"
```
