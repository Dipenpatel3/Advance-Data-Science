import os
import logging
from typing import Tuple, Dict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langgraph.schema import TypedDict
from langchain.schema import Document

# Set up logging
logging.basicConfig(level=logging.INFO)

class GraphState(TypedDict):
    error: str
    messages: list
    generation: str
    iterations: int

# Define the nodes for the LangGraph workflow

def retrieve_requirements(state: GraphState) -> GraphState:
    logging.info('Retrieving requirements...')
    requirements = state['messages'][-1]  # Get the last message
    return {'error': '', 'messages': state['messages'], 'generation': requirements, 'iterations': state['iterations']}


def generate_code(state: GraphState) -> GraphState:
    logging.info('Generating code...')
    requirements = state['generation']
    # Use OpenAI to generate code based on requirements
    llm = ChatOpenAI(model='gpt-4', temperature=0)
    response = llm.invoke({'messages': [('user', requirements)]})
    code = response['content']
    return {'error': '', 'messages': state['messages'], 'generation': code, 'iterations': state['iterations']}


def document_code(state: GraphState) -> GraphState:
    logging.info('Documenting code...')
    code = state['generation']
    documentation = f'"""
Generated Code:
{code}
"""'
    return {'error': '', 'messages': state['messages'], 'generation': documentation, 'iterations': state['iterations']}


def explain_code(state: GraphState) -> GraphState:
    logging.info('Explaining code...')
    code = state['generation']
    explanation = f'This code does the following: {code}'  # Simplified explanation
    return {'error': '', 'messages': state['messages'], 'generation': explanation, 'iterations': state['iterations']}

# Create the LangGraph workflow
workflow = StateGraph(GraphState)
workflow.add_node('retrieve_requirements', retrieve_requirements)
workflow.add_node('generate_code', generate_code)
workflow.add_node('document_code', document_code)
workflow.add_node('explain_code', explain_code)

# Define the edges
workflow.add_edge(START, 'retrieve_requirements')
workflow.add_edge('retrieve_requirements', 'generate_code')
workflow.add_edge('generate_code', 'document_code')
workflow.add_edge('document_code', 'explain_code')
workflow.add_edge('explain_code', END)

# Compile the application
app = workflow.compile()

# Function to generate code based on user input

def generate_code(user_input: str, openai_key: str) -> Tuple[str, str, str]:
    os.environ['OPENAI_API_KEY'] = openai_key
    inputs = {'messages': [user_input], 'error': '', 'generation': '', 'iterations': 0}
    output = app.stream(inputs)
    code = ''
    documentation = ''
    explanation = ''
    for result in output:
        code = result['generation'] if 'generation' in result else code
        documentation = result['generation'] if 'generation' in result else documentation
        explanation = result['generation'] if 'generation' in result else explanation
    return code, documentation, explanation