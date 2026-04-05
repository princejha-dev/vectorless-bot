from src.client import pi_client

def ask_chat_api(question, doc_id):
    try:
        response = pi_client.chat_completions(
            messages=[{"role": "user", "content": question}],
            doc_id=doc_id
        )
    except Exception as e:
        print(f"Error: {e}")
        return "❌ Sorry, something went wrong. Please try again."

    answer = response["choices"][0]["message"]["content"]
    return answer