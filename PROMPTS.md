# PROMPTS.md - Registro Cronológico de Uso de IA

Estudiante: Norman Merida
Curso: Inteligencia Artificial - Módulo 3
Proyecto: Integración CAG (Context-Augmented Generation)

---

## Prompt 1 - 12/06/2026

**Objetivo:** Analizar el proyecto base y entender su estructura

**Prompt usado:**
> "analiza las instrucciones del proyecto que vamos a trabajar"

**Respuesta de la IA:** Analizó la estructura del proyecto final_project_AI_CUSTOM-main, identificando backend (server, assistant, cag, context_store, knowledge), frontend (HTML+JS+CSS), tests (base y validación), y conocimiento base (knowledge_base.json). Explicó que context_store.py y cag.py son placeholders que lanzan NotImplementedError.

**Decisión humana:** Decidí mantener la arquitectura existente sin cambios drásticos. Aprobarí el análisis como punto de partida.

**Cambios realizados:** Ninguno (solo análisis).

**Verificación:** 3/3 tests base pasan (test_health_returns_ok, test_ask_answers_from_knowledge_base, test_ask_requires_user_and_question).

---

## Prompt 2 - 12/06/2026

**Objetivo:** Decidir qué tecnología usar para almacenamiento CAG

**Prompt usado:**
> "dime que opciones y como se podra implementar cag y que tecnologias se recomienda para implementarlo"

**Respuesta de la IA:** Presentó 4 opciones: (1) Memoria/dict, (2) Archivo JSON, (3) SQLite, (4) Redis. Recomendó opción 1 (memoria) para el examen por simplicidad.

**Decisión humana:** Elegí SQLite (opción 3) porque aunque la IA recomendó memoria, SQLite ofrece persistencia en disco sin dependencias externas (viene con Python) y permite concurrencia. Quería que los datos sobrevivan al reinicio del servidor.

**Cambios realizados:** Ninguno aún.

**Verificación:** Decisión documentada.

---

## Prompt 3 - 12/06/2026

**Objetivo:** Implementar ContextStore con almacenamiento en memoria usando dict

**Prompt usado:**
> "Implementa el método save() en context_store.py que guarde {user_id: {key: value}} en un diccionario"

**Respuesta de la IA:** Implementó ContextStore con self._data = {} en __init__, save() que crea entrada por usuario si no existe y guarda clave-valor, y list_for_user() que retorna lista de dicts con key/value.

**Decisión humana:** Aprobé la implementación. Luego decidí cambiar a SQLite para tener persistencia.

**Cambios realizados:** backend/context_store.py - Versión inicial con dict en memoria.

**Verificación:** No se ejecutaron tests en esta versión porque decidí cambiarla inmediatamente.

---

## Prompt 4 - 12/06/2026

**Objetivo:** Cambiar almacenamiento de dict a SQLite

**Prompt usado:**
> "en lugar de implementar el cag con python , usaremos sqlite"

**Respuesta de la IA:** Confirmó que SQLite se usa desde Python con módulo sqlite3 (incluido) y propuso reemplazar el dict por una tabla SQL con INSERT OR REPLACE y SELECT WHERE.

**Decisión humana:** Confirmé que el resto del proyecto sigue en Python, solo el almacenamiento cambia a SQLite.

**Cambios realizados:** backend/context_store.py - Reescrito completamente: tabla user_context(user_id, key, value) con PRIMARY KEY compuesta, INSERT OR REPLACE en save(), SELECT WHERE en list_for_user(), BD en data/context.db, singleton get_store().

**Verificación:** 6/6 tests pasan (3 base + 3 validación).

---

## Prompt 5 - 12/06/2026

**Objetivo:** Implementar apply_context() para modificar respuestas según contexto

**Prompt usado:**
> "Implementa apply_context() en cag.py para que modifique la respuesta según el contexto del usuario..."

**Respuesta de la IA:** Implementó apply_context() que recorre context_items, detecta clave 'audience' y antepone "Para {valor}: " a la respuesta, detecta 'preferred_style' y agrega nota al final, retorna tupla (respuesta_modificada, claves_usadas).

**Decisión humana:** Aprobé la implementación. La lógica de modificar según audiencia es exactamente lo que piden los tests de validación.

**Cambios realizados:** backend/cag.py - apply_context() completo con 18 líneas.

**Verificación:** Tests de validación pasan.

---

## Prompt 6 - 12/06/2026

**Objetivo:** Integrar CAG en el asistente

**Prompt usado:**
> "Modifica answer_question() en assistant.py para integrar CAG..."

**Respuesta de la IA:** Modificó answer_question() para: (1) obtener contexto con get_store().list_for_user(), (2) obtener snippets con retrieve_snippets(), (3) aplicar apply_context() con el contexto, (4) retornar response con context_used en lugar de lista vacía.

**Decisión humana:** Aprobé la integración. El flujo contexto → RAG → CAG es limpio y mantenible.

**Cambios realizados:** backend/assistant.py - Integración completa de CAG.

**Verificación:** Tests base y validación pasan.

---

## Prompt 7 - 12/06/2026

**Objetivo:** Agregar pruebas propias para validar casos adicionales

**Prompt usado:**
> "SI" (confirmación para generar pruebas propias)

**Respuesta de la IA:** Generó archivo tests/test_cag_own.py con 6 pruebas: contexto vacío, sobrescribir clave, aislamiento entre usuarios, respuesta sin contexto, múltiples items de contexto, y clave desconocida.

**Decisión humana:** Aprobé las 6 pruebas. Cubren casos borde que los tests de validación no contemplan.

**Cambios realizados:** tests/test_cag_own.py - 6 pruebas unitarias (89 líneas).

**Verificación:** 6/6 pruebas propias pasan. Total: 12/12 tests.

---

## Prompt 8 - 12/06/2026

**Objetivo:** Inicializar git y crear commits incrementales

**Prompt usado:**
> "Inicializa git en el proyecto, crea commits incrementales por cada archivo modificado..."

**Respuesta de la IA:** Inicializó git, configuró usuario, y creó 7 commits incrementales: (1) estructura base, (2) context_store.py con SQLite, (3) cag.py, (4) assistant.py, (5) server.py, (6) tests propias, (7) documentación Scrum.

**Decisión humana:** Decidí usar conventional commits (feat, test, docs, refactor, chore) y commits separados por cada archivo lógico.

**Cambios realizados:** Repositorio git inicializado con 7 commits.

**Verificación:** git log muestra historial limpio e incremental.

---

## Prompt 9 - 12/06/2026

**Objetivo:** Crear Pull Request y merge a main en el fork

**Prompt usado:**
> (Instrucciones dadas paso a paso para crear PR en GitHub)

**Respuesta de la IA:** Guió el proceso de creación del PR desde feature/cag a main dentro del fork ndm2025/final_project_AI_CUSTOM. El PR #1 fue mergeado exitosamente con 8 commits, 426 adiciones y 13 eliminaciones.

**Decisión humana:** Decidí que el PR fuera dentro de mi fork (ndm2025:main ← ndm2025:feature/cag) y no al repositorio original (rortizs).

**Cambios realizados:** PR #1 mergeado a main en GitHub.

**Verificación:** Repositorio local sincronizado con git pull origin main.

---

## Prompt 10 - 12/06/2026

**Objetivo:** Crear documentación Scrum

**Prompt usado:**
> "Documente backlog, planificación de sprints, ejecución y cierre de sprints dentro del repositorio"

**Respuesta de la IA:** Creó 7 artefactos Scrum en docs/scrum/: BACKLOG.md (9 HU), SPRINT1_PLAN.md, SPRINT1_EXECUTION.md, SPRINT1_REVIEW.md, SPRINT2_PLAN.md, SPRINT2_EXECUTION.md, SPRINT2_REVIEW.md.

**Decisión humana:** Aprobé la estructura de 2 sprints: Sprint 1 (ContextStore) y Sprint 2 (Integración CAG). Los sprints fueron planificados como sesiones únicas.

**Cambios realizados:** docs/scrum/ - 7 archivos de documentación Scrum.

**Verificación:** Documentación completa y coherente con el trabajo realizado.

---

## Prompt 11 - 12/06/2026

**Objetivo:** Generar este PROMPTS.md

**Prompt usado:**
> "Crea el archivo PROMPTS.md en la raíz del proyecto con el registro cronológico de todas las interacciones que tuvimos..."

**Respuesta de la IA:** Generó PROMPTS.md con 11 entradas cronológicas documentando cada interacción, incluyendo objetivo, prompt, respuesta, decisión humana, cambios y verificación.

**Decisión humana:** Revisé y aprobé el contenido del registro.

**Cambios realizados:** PROMPTS.md - Registro completo de uso de IA.

**Verificación:** Archivo creado en la raíz del proyecto con formato solicitado.
