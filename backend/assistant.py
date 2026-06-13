from backend.cag import apply_context
from backend.context_store import get_store
from backend.knowledge import retrieve_snippets


def answer_question(user_id, question):
    store = get_store()
    context_items = store.list_for_user(user_id)

    snippets = retrieve_snippets(question)

    if not snippets:
        base_answer = "No encontre informacion suficiente en la base de conocimiento del curso."
        answer, keys_used = apply_context(user_id, question, base_answer, context_items)
        return {
            "user_id": user_id,
            "answer": answer,
            "sources": [],
            "context_used": keys_used,
        }

    source_text = " ".join(item["content"] for item in snippets)
    base_answer = f"Segun la base de conocimiento del curso: {source_text}"
    answer, keys_used = apply_context(user_id, question, base_answer, context_items)

    return {
        "user_id": user_id,
        "answer": answer,
        "sources": [item["id"] for item in snippets],
        "context_used": keys_used,
    }
