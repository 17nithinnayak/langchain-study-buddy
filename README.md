# Smart Study Buddy AI Agent 🤖

A conversational AI agent that uses a Retrieval-Augmented Generation (RAG) pipeline to answer questions about a specific document. The agent is equipped with multiple tools, allowing it to perform actions like answering questions and sending emails based on user commands.

This project is a demonstration of building a modular, agentic AI application using LangChain, Groq, and local vector stores.

## ✨ Features

-   **Document-Grounded Q&A:** The agent uses a RAG pipeline with a FAISS vector store to answer questions based *only* on the content of a provided PDF document.
-   **Multi-Tool Capability:** Built with a ReAct (Reasoning and Acting) agent that can intelligently choose between different tools:
    -   `rag_tool`: For answering questions about the document.
    -   `email_tool`: For sending emails on the user's behalf.
-   **Interactive Interface:** Accepts commands via keyboard input and provides spoken responses using text-to-speech.
-   **High-Speed Inference:** Powered by the fast Groq API for real-time LLM responses.

---

## 🏗️ Architecture

The application follows a modular agentic architecture where user input is interpreted by an agent, which then decides which tool to use to fulfill the request.

![Flowchart of the AI agent's architecture](https://i.imgur.com/8aZ2XyM.png)

1.  **Input:** The user types a command.
2.  **Agent Executor:** The LangChain agent receives the input and, based on its prompt and the descriptions of available tools, decides on a plan.
3.  **Tools:** The agent executes the chosen tool:
    -   If it's a question, it uses the **RAG Tool**, which queries the FAISS vector store for relevant context and passes it to the LLM.
    -   If it's a request to email, it uses the **Email Tool**, which formats the content and sends it via an SMTP server.
4.  **Output:** The agent's final answer is converted to speech and spoken back to the user.

---

## 🛠️ Tech Stack

-   **Core AI/Orchestration:** LangChain
-   **LLM Provider:** Groq (`llama3-8b-8192`)
-   **Embeddings:** Hugging Face `sentence-transformers`
-   **Vector Database:** FAISS (for local similarity search)
-   **Document Loading:** PyPDF
-   **Voice Output:** pyttsx3
-   **Email:** smtplib (Python Standard Library)

---

## 🚀 Setup and Installation

Follow these steps to get the project running on your local machine.

#### 1. Clone the Repository

```bash
git clone [https://github.com/YourUsername/langchain-study-buddy.git](https://github.com/YourUsername/langchain-study-buddy.git)
cd langchain-study-buddy
```

#### 2. Create and Activate a Virtual Environment

-   **Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
-   **macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

#### 3. Install Dependencies

Install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables

You need to provide API keys and credentials for the services to work.

1.  Create a file named `.env` in the root of the project directory.
2.  Open the `.env` file and add your credentials:

    ```env
    # Get from [https://console.groq.com/](https://console.groq.com/)
    GROQ_API_KEY="gsk_YourGroqKeyHere"

    # Your Gmail address
    EMAIL_ADDRESS="your.email@gmail.com"

    # Your 16-character Gmail App Password
    # See [https://support.google.com/accounts/answer/185833](https://support.google.com/accounts/answer/185833)
    EMAIL_PASSWORD="your16characterapppassword"
    ```

    > **Important:** To get a Gmail `EMAIL_PASSWORD`, you must have 2-Factor Authentication enabled on your Google account.

#### 5. Add a Document

Place a PDF document that you want the agent to read in the root of the project folder and name it `my_document.pdf`.

---

## ▶️ Usage

Once the setup is complete, run the main application from your terminal:

```bash
python main.py
```

The application will start, and the agent will greet you. You can then type your commands at the prompt.

**Example Commands:**

-   `What are the main properties of a Binary Search Tree?`
-   `Send an email to test@example.com with the subject Project Update and body The agent is working perfectly.`
-   `What is a BST and can you email the answer to myfriend@example.com`
-   `quit` (to exit the application)

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
