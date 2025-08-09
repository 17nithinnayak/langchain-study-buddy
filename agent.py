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
def email_tool(recipient: str, subject: str, body: str) -> str:
    """Sends an email. Use this to send an email to a specified recipient with a given subject and body."""
    try:
        sender_email = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient
        with smtplib.SMTP_SSL('smtp.gmail.com', 465)  as smtp_server:
            smtp_server.login(sender_email, password)
            smtp_server.sendmail(sender_email, recipient, msg.as_string())
        return "Email sent successfully"
    except Exception as e:
        return f"Failed to send email. Error: {e}"
    
tools = [rag_tool, email_tool]

llm = qa_chain.combine_documents_chain.llm_chain.llm
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm,tools,prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("\nAgent is ready.")
agent_executor.invoke({
    "input": "What are the three properties of a Binary Search Tree according to the document?"
})