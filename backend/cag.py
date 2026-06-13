def apply_context(user_id, question, base_answer, context_items):
    answer = base_answer
    keys_used = []

    for item in context_items:
        key = item.get("key", "")
        value = item.get("value", "")

        if key == "audience":
            keys_used.append(key)
            answer = f"Para {value}: {answer}"
            continue

        if key == "preferred_style":
            keys_used.append(key)
            answer = f"{answer}\n(Estilo preferido: {value})"

    return answer, keys_used
