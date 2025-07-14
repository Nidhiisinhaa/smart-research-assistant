from transformers import pipeline
import random
from difflib import SequenceMatcher

# Use T5 or FLAN-T5 for proper question generation
qg_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

def generate_questions(context, num_questions=3):
    sentences = context.split(". ")
    random.shuffle(sentences)

    questions = []
    for sentence in sentences:
        if len(sentence.split()) > 6 and len(questions) < num_questions:
            input_text = f"generate question: {sentence}"
            output = qg_pipeline(input_text, max_length=64, do_sample=True)[0]['generated_text']
            question_text = output.strip()
            questions.append({
                "question": question_text,
                "answer": sentence.strip()
            })
    return questions

def evaluate_answer(user_ans, correct_ans):
    user_ans = user_ans.lower().strip()
    correct_ans = correct_ans.lower().strip()

    similarity = SequenceMatcher(None, user_ans, correct_ans).ratio()

    if similarity > 0.85:
        return "✅ Correct!"
    elif similarity > 0.5:
        return "🟡 Almost correct. Try refining your answer."
    else:
        return f"❌ Incorrect. Correct Answer: {correct_ans}"
