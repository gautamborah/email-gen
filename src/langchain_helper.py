from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableMap

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLM
llm = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.7
)

def generate_restaurant_name_and_items(cuisine: str):
    # Prompt for restaurant name
    prompt_template_name = PromptTemplate(
        input_variables=["cuisine"],
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for this."
    )

    # Prompt for menu items (takes restaurant_name as input)
    prompt_template_items = PromptTemplate(
        input_variables=["restaurant_name"],
        template="Suggest some menu items for {restaurant_name}. Return it as a comma separated string."
    )

    # Define pipeline:
    # First get restaurant name, then feed it into second prompt
    name_chain = prompt_template_name | llm
    items_chain = (
        {"restaurant_name": name_chain}
        | prompt_template_items
        | llm
    )

    # Run both in parallel: cuisine -> {restaurant_name, menu_items}
    chain = {
        "restaurant_name": name_chain,
        "menu_items": items_chain,
    }

    # Invoke pipeline
    response = chain["restaurant_name"].invoke({"cuisine": cuisine})
    response_items = chain["menu_items"].invoke({"cuisine": cuisine})
    return {
        "restaurant_name": response,
        "menu_items": response_items
    }


def generate_restaurant_name_and_items_single_invoke(cuisine: str):
    # Prompt for restaurant name
    prompt_template_name = PromptTemplate(
        input_variables=["cuisine"],
        template="I want to open a restaurant for {cuisine} food. Suggest a fancy name for this."
    )

    # Prompt for menu items (depends on restaurant_name)
    prompt_template_items = PromptTemplate(
        input_variables=["restaurant_name"],
        template="Suggest some menu items for {restaurant_name}. Return it as a comma separated string."
    )

    # Build chains using pipe syntax
    name_chain = prompt_template_name | llm
    items_chain = {"restaurant_name": name_chain} | prompt_template_items | llm

    # Wrap into a RunnableMap so it can be invoked
    chain = RunnableMap({
        "restaurant_name": name_chain,
        "menu_items": items_chain,
    })

    # Invoke the whole pipeline once
    response = chain.invoke({"cuisine": cuisine})
    return response

if __name__ == "__main__":
    result = generate_restaurant_name_and_items_single_invoke("Italian")
    print(result)
