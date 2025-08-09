import os
from dotenv import load_dotenv
from pathlib import Path
import smtplib
from email.mime.text import MIMEText

load_dotenv()

from langchain.agents import tool
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor

from rag_core import create_rag_chain

qa_chain = create_rag_chain(pdf_path="my_document.pdf")

@tool
def rag_tool(query: str) -> str:
    """Answers questions about the content of my_document.pdf. Use this for any questions about the document's contents."""
    result = qa_chain.invoke({"query": query})
    return result['result']

@tool
def email_tool(details: str) -> str:
    """
    Use this tool ONLY when the user explicitly asks to send an email.
    The input to this tool must be a single string containing the recipient's email,
    the subject, and the body, separated by the '|' character.
    For example: test@example.com|Hello|This is the body of the email.
    """
    try:
        # Split the single input string into three parts
        recipient, subject, body = details.split('|', 2) # The '2' ensures we only split twice

        sender_email = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")

        msg = MIMEText(body.strip()) # .strip() removes leading/trailing whitespace
        msg['Subject'] = subject.strip()
        msg['From'] = sender_email
        msg['To'] = recipient.strip()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, password)
            smtp_server.sendmail(sender_email, recipient, msg.as_string())
        
        return "Email sent successfully!"
    except ValueError:
        return "Failed to send email. The input was not in the correct format. It must be 'recipient|subject|body'."
    except Exception as e:
        return f"Failed to send email. Error: {e}"
    
tools = [rag_tool, email_tool]

llm = qa_chain.combine_documents_chain.llm_chain.llm
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm,tools,prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("\nAgent is ready.")
# agent_executor.invoke({
#     "input": "What are the three properties of a Binary Search Tree according to the document?"
# })

#print("Testing the email tool directly...")
# Use your own email as the recipient to easily check if it works
# test_result = email_tool.invoke({
#     "recipient": "youremail@gmail.com", 
#     "subject": "Testing my AI Agent Tool", 
#     "body": "This is a successful test of the email_tool from my LangChain project!"
# })
# print(test_result)