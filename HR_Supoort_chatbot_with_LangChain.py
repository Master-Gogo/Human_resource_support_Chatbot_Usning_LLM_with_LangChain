# -*- coding: utf-8 -*-
"""Copy of langchain.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1azvCLYum7Vo1AZhQrajGRuXBlLJ4dWWC
"""

! pip install -Uqqq pip --progress-bar off
! pip install -qqq langchain==0.0.228 --progress-bar off
! pip install -qqq chromadb==0.3.26 --progress-bar off
! pip install -qqq sentence-transformers==2.2.2 --progress-bar off
! pip install -qqq auto-gptq==0.2.2 --progress-bar off
! pip install -qqq einops==0.6.1 --progress-bar off
! pip install -qqq unstructured==0.8.1 --progress-bar off
! pip install -qqq transformers==4.30.2 --progress-bar off
! pip install -qqq torch==2.0.1 --progress-bar off

from pathlib import Path
import torch
from auto_gptq import AutoGPTQForCausalLM
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import HuggingFacePipeline
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from transformers import AutoTokenizer, GenerationConfig, pipeline , TextStreamer

questions_dir=Path("HRPolicies")
questions_dir.mkdir(exist_ok=True,parents=True)

def write_file(question, answer, file_path):
  text=f"""
  "Q":{question}
  "A":{answer}""".strip()
  with Path(questions_dir / file_path).open("w") as text_file:
    text_file.write(text)

write_file(question="what is your salary or cost to the company",
          answer='Total Salary (Cost To Company) : 27,50,000'.strip(),
           file_path="text1.txt",)

write_file(question="what is your notice period",
          answer="""Termination/Separation
9. The employment can be terminated by either of the parties by giving 2 months notice period in writing of its intention to do so. An employee is expected to serve the full duration of the notice period to facilitate proper hand over of responsibilities and complete any urgent projects on hand. In exceptional cases, based on Company's discretion, an employee may be permitted to be relieved earlier by tendering notice pay calculated as basic pay divided by 30 and multiplied by number of days of shortfall in notice period. The basic salary is defined as the first element of our existing salary structure
10. In the event of breach of any of the terms & conditions of your employment and/or service conditions and rules, the Company reserves the right to claim damages from you. The Company also reserves the right to terminate your services without giving notice.
11. Your appointment and employment will be subject to your being and remaining medically fit. It is necessary for you to get medically examined by the Medical Officer appointed by the Company as and when required by the Company. If at any stage, you are found to be unfit by the Medical Officer for the job currently being done by you, then you are liable to be terminated on medical grounds.
12. You will retire from the employment of this Company upon reaching the age of 60 years.""".strip(),
           file_path="text2.txt",)

write_file(question="what is your retirement age from the company",
          answer='You will retire from the employment of this Company upon reaching the age of 60 years'.strip(),
           file_path="text3.txt",)

write_file(question="what is your responsibilities?",
          answer="""B) Responsibility
3. During your employment with the Company, you will be governed by Service Conditions more specifically stated in the Annexure
I attached to this letter and other rules and regulations framed by the Management from time to time, which shall be applicable to
you, and also by such legal provisions as may be applicable. You shall perform the roles and responsibility as mentioned in the
Annexure III attached to this letter.
4. You are expected to give to the Company your best efforts, attention and commitment. You are explicitly advised to refrain from
any such activity, whether for monetary or any other considerations, as may become, in our opinion, a hindrance to your
performance . You are, by virtue of employment with this Company, required to do all the work allied, ancillary related or incidental to the
main job. Similarly, you may be asked to do any job within your competence depending upon the exigencies of the situation.
6. Your appointment is a full time job and you will not at any time engage, directly or indirectly, in any paid or honorary
occupation or business outside the Company without obtaining prior written consent of the Company. You shall not by
yourself or on behalf of the Company conduct any external training/s workshops without prior approval from the Company.
Breach of any of the above conditions will render your employment liable to termination without notice.""".strip(),
           file_path="text4.txt",)

write_file(question="does company provide any training?",
          answer="""Training
7. In furtherance of your employment in this Company and for increasing and honing your skills, you may be required to be
trained technically or otherwise. This may require the Company to provide training either in-house or send you for training
outside the Company in India or abroad, on the terms and conditions as mutually agreed before the commencement of such
training.
""".strip(),
           file_path="text5.txt",)

write_file( question="under what circumstances you can terminated? ",
          answer=""" If at any
stage, you are found to be unfit by the Medical Officer for the job currently being done by you, then you are liable to be
terminated on medical grounds. You will automatically retire from the employment of this Company upon reaching the age of
60 years. 11. Your employment is substantially based on the information, testimonial, documents submitted by you, which you were
required to submit while joining the employment or may be called upon to do so subsequently. The Company shall be within
its right to verify the correctness of such information at any time now or in future. If it is found at any stage that the
information provided by you is incorrect or in case some information is suppressed, then the Company reserves the right to
terminate your services without giving any notice. 12. Your appointment is subject to favourable background screening check report. That the management shall terminate your
services forthwith at its discretion in case there is any adverse report while checking the background or in case any
information is concealed or is found to be false or misleading. So also your services are liable to be terminated without notice
in case while in employment you are involved in any act of moral turpitude 13. You will be solely responsible for the Company property assigned to you to discharge your duties. Loss of any of the items
would be recovered from you, as the Company may deem appropriate. On ceasing to be in the employment of this Company
for any reason, you will promptly settle all the accounts including the return of all Company properties, tools, equipment,
documents, etc. without making or retaining any copies """.strip(),
           file_path="text6.txt",)

write_file(question="what is company notice period?",
          answer="""Termination Separation 8. The employment can be terminated by either of the parties by giving 2 month’s notice in writing informing the other party of
its intention to do so.
""".strip(),
           file_path="text10.txt",)

write_file(question="who much pay you get if you relieved earlier?",
          answer="""ased on Company's discretion, you may
be permitted to be relieved earlier by tendering notice pay calculated as basic pay /30 * no. of days of shortfall in notice
period. The basic salary is defined as the first element of our existing salary structure 9. In the event of breach of any of the terms & conditions of your employment and/or service conditions and rules, the
Company reserves the right to claim damages from you. The Company also reserves the right to terminate your services without giving notice.
10. Your appointment and employment will be subject to your being and remaining medically fit
""".strip(),
           file_path="text11.txt",)

write_file(question="Do I need to inform the company if I changes the residential address",
          answer="""You shall always endeavor to upgrade your skills, knowledge, and expertise from time to time and shall not refuse to undergo
any training or programme undertaken by Company or as directed by the Company for improvement or upgradation of skills,
services performance or such other things necessary for the growth of the Company.
11. Upon leaving the employment you shall return to the Company forthwith all the property, documents drawings, designs,
programmes, data in whatever form, hardware, software, records, etc belonging to the Company or its associates, subsidiary,
clients, or customers.
12. If at any time, whether during or after your association with us, any dispute arises between you and/or your legal heirs and
representative on the one hand and ourselves and/or our assignees and/or successors on the other, whether regarding
interpretation and/or legal effect of all or any of the terms of this agreement and/or whether or not any breach of it was or is
committed by either of us and whether or not the said agreement or any of its terms are reasonable and/or regarding nature,
type, extent and/or quantum of relief, all and every one of them shall be settled by Conciliation and Binding Arbitration
at Pune/Delhi under the Indian Arbitration & conciliation act 1996 by the sole arbitrator appointed by the company having
jurisdiction at Pune, and further that you shall not be entitled to take any of the disputes to any other place and/or to any Civil
Court.
13. All the correspondence, communications by the Company hereinafter shall be made either personally at work place or at the
residential address given by you, at any one of the places at the discretion and convenience of the Company. Should you
change your residence, you shall forthwith inform the address in writing to the Company.
""".strip(),
           file_path="text8.txt",)

write_file(question="what is intellectual property related clauses",
          answer="""AGREEMENT CONCERNING EMPLOYEE INVENTIONS. INTELLECTUAL PROPERTY
PERSONAL DATA AND CONFIDENTIAL INFORMATION
In consideration of my employment, the continuation of my employment and/or other consideration I have received or will
receive in connection with my employment by XYZ Technologies Private Limited or any of its affiliates, including
subsidiaries, partnerships or entities heretofore or hereafter controlling, controlled by, or under common control with it
(collectively "XYZ") """.strip(),
           file_path="text12.txt",)

DEVICE="cuda:0" if torch.cuda.is_available() else "cpu"
print(DEVICE)

model_name_or_path = "TheBloke/Nous-Hermes-13B-GPTQ"
model_basename = "nous-hermes-13b-GPTQ-4bit-128g.no-act.order"

use_triton = False

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

model = AutoGPTQForCausalLM.from_quantized(model_name_or_path,
        model_basename=model_basename,
        use_safetensors=True,
        trust_remote_code=True,
        device="cuda:0",
        use_triton=use_triton,
        quantize_config=None)

generation_config=GenerationConfig.from_pretrained(model_name_or_path)

question=(" which language is better to understand for the beginner python or java?")

prompt=f"""
### instruction:{question}
### response: """.strip()

print(prompt)

input_ids = tokenizer(prompt, return_tensors='pt').input_ids.cuda(DEVICE)
with torch.inference_mode():
  output = model.generate(inputs=input_ids, temperature=0.7, max_new_tokens=512)

print(tokenizer.decode(output[0]))

generation_config

streamer=TextStreamer(tokenizer,skip_prompt=True, skip_special_tokens=True,use_multiprocessing=False)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.7,
    top_p=0.95,
    repetition_penalty=1.15,
    generation_config=generation_config,
    streamer=streamer,
    batch_size=1,
)

print(pipe(prompt)[0]['generated_text'])

llm=HuggingFacePipeline(pipeline=pipe)

response=llm(prompt)

embeddings= HuggingFaceEmbeddings(
    model_name="embaas/sentence-transformers-multilingual-e5-base",
    model_kwargs= {"device": DEVICE},
)

loader=DirectoryLoader("./HRPolicies/",glob="**/*txt")
documets=loader.load()
len(documets)

textsplitter=CharacterTextSplitter(chunk_size=512, chunk_overlap=0)
texts=textsplitter.split_documents(documets)

texts[0]

db=Chroma.from_documents(texts,embeddings)

db.similarity_search("notice period")

template="""
### Instruction: your are customer support agent  talking to employees for answer Human Rerource policies related queries. use
only chat history and following  information {context}
to anser helpful manner to the question. if you dont know the answer say that - you dont know.
keep your reply short and informative.
{chat_history}
### Input : {question}
### Response: """.strip()

prompt=PromptTemplate(input_variables=['question','context','chat_history'], template=template)

memory=ConversationBufferMemory(
      memory_key='chat_history',
      human_prefix="### Input",
      ai_prefix='### Response',
      output_key='answer',
      return_messages=True
)

chain=ConversationalRetrievalChain.from_llm(llm,
                                            chain_type="stuff",
                                            retriever=db.as_retriever(),
                                            memory=memory,
                                            combine_docs_chain_kwargs={'prompt':prompt},
                                            return_source_documents=True,)

question=" what is notice period"
answer=chain(question)

answer.keys()

answer['source_documents']

#QA chain with memeory

memory=ConversationBufferMemory(
      memory_key='chat_history',
      human_prefix="### Input",
      ai_prefix='### Response',
      input_key='question',
      output_key='output_text',
      return_messages=True,
)

chain=load_qa_chain(
    llm,
    chain_type="stuff",
    prompt=prompt,
    memory=memory,
    verbose=True
)

question=' what is company notice period?'
docs=db.similarity_search(question)
answer=chain.run({"input_documents":docs,"question": question})

question=' does company provide trainings?'
docs=db.similarity_search(question)
answer=chain.run({"input_documents":docs,"question": question})