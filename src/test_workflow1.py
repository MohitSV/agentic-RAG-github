

#test_workflow1.py

import random

import asyncio

import os
from pinecone import Pinecone, ServerlessSpec

from llama_index.core.workflow import (
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
    Context,
)

class EvaluateEvent(Event):
    number: int
    count: int
    count = 0

class RequestGenerateEvent(Event):
    count: int

class LoopExampleWorkflow(Workflow):
    @step
    async def generate(self, ev: StartEvent | RequestGenerateEvent) -> EvaluateEvent:

        # print('camehere', flush=True)
        if hasattr(ev, 'index'):
            print('index sent')
        else:
            print('index not sent')
        if hasattr(ev,'query'):
            print('QUERY sent')
        else:
            print('q not sent')
        if hasattr(ev, 'count'):
            count = ev.count
        else:
            count = 0
        random_number = random.randint(0, 10)
        # print(f"  generate generated random_number: {random_number}",flush=True)
        return EvaluateEvent(number=random_number, count=count)


    @step
    async def evaluate(self, ev:EvaluateEvent) -> RequestGenerateEvent | StopEvent:
        number = ev.number
        count = ev.count
        count += 1
        if number < 9:
            # print(f"count: {count} number: {number} < 7 so trying again")
            return RequestGenerateEvent(count=count)
        else:
            return StopEvent(result=f"finally got number {number} >= 7 after {count} tries")
        

async def execute_loop(query, index):
    wf = LoopExampleWorkflow(verbose=False)
    result = await wf.run(query=query, index=index)
    return result

if __name__=="__main__":

    pinecone_key = os.getenv("PINECONE_API_KEY")

    print(pinecone_key)
    
    index_name = "langchain-test-index-mohit"

    pc = Pinecone(api_key=pinecone_key)

    index = pc.Index(index_name)
    query = 'hi'
    result = asyncio.run(execute_loop(query, index))
    print(result)
