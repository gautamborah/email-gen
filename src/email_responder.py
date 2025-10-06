from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the OpenAI Chat model
llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",   # You can use "gpt-4o" or "gpt-3.5-turbo"
    temperature=0.7
)

# Define the prompt for replying to an email
prompt = PromptTemplate(
    input_variables=["email_content", "tone"],
    template=(
        "You are a professional email assistant.\n\n"
        "Here is the received email:\n"
        "-----\n"
        "{email_content}\n"
        "-----\n\n"
        "Write a clear, polite, and {tone} response to this email. "
        "Make sure your reply sounds natural and addresses the sender's points appropriately."
    )
)

# Build the LangChain runnable (prompt → llm)
email_response_chain = prompt | llm

def generate_email_response(email_content: str, tone: str = "friendly") -> str:
    """
    Generates an email reply based on input email content and tone.
    """
    response = email_response_chain.invoke({
        "email_content": email_content,
        "tone": tone
    })
    return response.content


if __name__ == "__main__":
    sample_email = """
    Hi Gautam,
    I hope you're doing well. I wanted to check if you’re available this week
    to discuss the progress on the email automation project and any blockers you might have.
    Let me know what time works best for you.

    Thanks,
    Sarah
    """

    reply = generate_email_response(sample_email, tone="professional")
    print("\n--- Generated Reply ---\n")
    print(reply)
