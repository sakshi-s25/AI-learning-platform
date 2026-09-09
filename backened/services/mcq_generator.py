import random

def generate_mcqs(text):
    sentences = text.split(".")
    valid_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()
        words = sentence.split()

        if len(words) >= 6:
            valid_sentences.append(sentence)

    mcqs = []

    selected_sentences = valid_sentences[:5]

    for index, sentence in enumerate(selected_sentences):
        words = sentence.split()
        answer = words[-1]

        question_sentence = " ".join(
            words[:-1]
        ) + " _____?"

        options = [
            answer,
            "Data",
            "Statistics",
            "Information"
        ]

        random.shuffle(options)

        mcqs.append({
            "id": index + 1,
            "question": question_sentence,
            "options": options,
            "answer": answer
        })

    return mcqs
