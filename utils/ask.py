from transformers import pipeline

qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def answer_question(question, context):
    if not context.strip():
        return {"answer": "No context provided.", "justification": "Please upload a valid document."}

    result = qa_pipeline(question=question, context=context)
    answer = result['answer']

    # Try to extract a window of context around the answer
    start = max(0, result['start'] - 50)
    end = min(len(context), result['end'] + 50)
    justification = context[start:end].replace('\n', ' ')

    return {
        "answer": answer,
        "justification": f"...{justification}..."
    }
