from backend.retriever import retrieve_documents
from backend.generator import generate_answer


followup_starters = [
    "explain it",
    "summarize",
    "give an example",
    "tell me more",
    "elaborate",
    "rephrase",
    "simplify"
]


def is_followup(question, chat_history):#used above list to identify if or whether it's a followup question or not

    if not chat_history:
        return False

    question_lower = question.lower().strip()

    for starter in followup_starters:
        if question_lower.startswith(starter):
            return True

    return False


def ask_new_question(question):

    result = retrieve_documents(
    question,
    n_results=20) #I have run with multiple n_results but this
    # particular gives best fit as the rest/old things could'nt possibly get the output of who is author of Attention is All you Need
    #as we are using ollama and not very intelligent models like google gemini or so.


    documents = result["documents"][0]

    # DEBUG
    print("\nQUESTION:")
    print(question)

    print("\nDISTANCES:")
    print(result["distances"][0][:5])

    #for safety so that it won't give it's own answer
    best_distance = result["distances"][0][0]

# TEMP THRESHOLD
    if best_distance > 1.0: #this has been to identify new chats as ollama unlike google gemini models are unable to follow the prompt correctly
        return (
            "I couldn't find relevant information about this in the provided research papers.",
            [])
        

    context = "\n\n".join(documents)

    prompt = f"""
    answer only with the provided context

    If the answer is not present in the context, reply EXACTLY:
    
    I couldn't find relevant information about this in the provided research papers.

    CONTEXT:
    {context}

    QUESTION:
    {question}
    """

    answer = generate_answer(prompt)

    sources = set()#To eradicate the duplicate values.

    for meta in result["metadatas"][0]:
        if "source" in meta:
            sources.add(meta["source"])

    return answer, list(sources)


def ask_followup(question, chat_history):

    conversation = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in chat_history
    )

    prompt = f"""
    You are answering a follow-up question.

    Use ONLY the information that already exists in the conversation below.

    Do NOT use outside knowledge.
    Do NOT introduce new facts.
    Do NOT retrieve new information.

    Conversation:

    {conversation}

    Follow-up Question:

    {question}
    """

    answer = generate_answer(prompt)

    return answer  