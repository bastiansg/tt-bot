def remove_bot_mention(text: str, bot_name: str) -> str:
    text = text.replace(bot_name, "")
    text = text.strip()

    return text


def get_ref_text(refs: list[dict]) -> str:
    ref_text = "\n\n".join(
        "\n".join(f"{k}: {v}" for k, v in ref.items()) for ref in refs
    )

    return ref_text
