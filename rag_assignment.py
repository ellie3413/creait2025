# RAG_with_Langchain.py

import pandas as pd
from datasets import load_dataset
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv


load_dotenv()

# 1. Load and preprocess SQuAD dataset
dataset = load_dataset('squad')
validation_data = dataset['validation'].select(range(100))

# Create DataFrame
data = {
    'context': [],
    'question': [],
    'answer': []
}

for item in validation_data:
    context = item['context']
    question = item['question']
    answer = item['answers']['text'][0]
    data['context'].append(context)
    data['question'].append(question)
    data['answer'].append(answer)

df = pd.DataFrame(data)

# 2. Create text chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=128,
    chunk_overlap=64
)

contexts = list(set(df['context'].tolist()))  # Remove duplicates
texts = text_splitter.create_documents(contexts)

# 3. Create vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = FAISS.from_documents(texts, embeddings)

# 4. Create retrieval chain
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(search_kwargs={"k": 1})
)

# 5. Evaluation function
def evaluate_answer(question, true_answer, predicted_answer):
    client = OpenAI()
    
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'system', 'content': 'You will be given a question, answer for that question and a predicted answer made by a model. You have to decide whether the predicted answer is correct or not. If it is right, your answer should be "True", otherwise "False". Remember that your answer must only be "True" or "False".'},
            {'role': 'assistant', 'content': f"Question: {question}\nAnswer: {true_answer}\nPredicted Answer: {predicted_answer}"}
        ],
        temperature=0,
        logprobs=True,
        top_logprobs=2
    )
    
    top_logprobs = response.choices[0].logprobs.content[0].top_logprobs
    is_correct = top_logprobs[0].token
    
    if is_correct == 'True':
        robustness = np.exp(top_logprobs[0].logprob)
        accuracy = 'True'
    else:
        robustness = np.exp(top_logprobs[1].logprob)
        accuracy = 'False'
        
    return accuracy, robustness

# 6. Run evaluation
accuracy_list = []
robustness_list = []

for index, row in df.iterrows():
    question = row['question']
    answer = row['answer']
    
    result = qa_chain.invoke({"query": question})
    predicted_answer = result['result']
    
    accuracy, robustness = evaluate_answer(question, answer, predicted_answer)
    accuracy_list.append(accuracy)
    robustness_list.append(robustness)

# 7. Save results
df['accuracy'] = accuracy_list
df['robustness'] = robustness_list
df.to_csv('./langchain_results.csv', index=False)

# 8. Print metrics
df['accuracy'] = df['accuracy'].map({'True': True, 'False': False})
true_ratio = df['accuracy'].mean()
mean_robustness = df['robustness'].mean()

print(f"Accuracy: {true_ratio:.2f}")
print(f"Mean Robustness: {mean_robustness:.3f}")