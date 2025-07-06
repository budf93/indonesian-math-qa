# Indonesian Math QA with Fine-Tuned LLM

This is a full-stack web application that uses a custom fine-tuned Large Language Model to answer math questions with step-by-step reasoning in Bahasa Indonesia.

The project leverages the `unsloth/DeepSeek-R1-0528-Qwen3-8B` model, fine-tuned using Group Relative Policy Optimization (GRPO) to force its internal reasoning process into Indonesian. The model is served locally with Ollama and accessed via a FastAPI backend and a Vue.js frontend.

## Tech Stack

  * **Frontend**: Vue.js, Vite, Axios, KaTeX
  * **Backend**: Python, FastAPI, Uvicorn
  * **LLM Serving**: Ollama
  * **Fine-Tuning**: Unsloth, PyTorch, Hugging Face `peft` & `trl`

-----

## Prerequisites

Before you begin, ensure you have the following installed on your system:

  * [Node.js](https://nodejs.org/en) (which includes npm)
  * [Python](https://www.python.org/downloads/)
  * [Ollama](https://ollama.com/)
  * [Git](https://git-scm.com/downloads/)

-----

## Setup and Installation

Follow these steps to get the project running on your local machine.

### 1\. Clone the Repository

First, clone the project from GitHub to your local machine:

```bash
git clone https://github.com/budf93/indonesian-math-qa.git
cd indonesian-math-qa
```

### 2\. Set Up the Backend

The backend requires a Python virtual environment to manage its dependencies.

```bash
# Navigate to the backend directory
cd indonesian-math-qa-backend

# Create a Python virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows (Command Prompt):
venv\Scripts\activate.bat
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install the required Python packages
pip install fastapi "uvicorn[standard]" requests
```

### 3\. Set Up the Frontend

The frontend dependencies are managed by npm.

```bash
# Navigate to the frontend directory from the project root
cd indonesian-math-qa-frontend

# Install all dependencies
npm install
```

-----

## Running the Application

To run the full application, you will need to have **3 separate terminals** open.

### Terminal 1: Run the LLM Server

This terminal will run the custom model in Ollama, waiting for requests.

```bash
ollama run hf.co/budf93/deepseek-r1-qwen3-8b-indonesian-math-qa:Q4_K_M
```

### Terminal 2: Run the Backend Server

This terminal will run the FastAPI API.

```bash
# Navigate to the backend directory
cd indonesian-math-qa-backend

# Activate the virtual environment if it's not already active
# (e.g., venv\Scripts\activate.bat on Windows)

# Start the server
uvicorn main:app --reload
```

### Terminal 3: Run the Frontend Server

This terminal will run the Vue.js development server.

```bash
# Navigate to the frontend directory
cd indonesian-math-qa-frontend

# Start the development server
npm run dev
```

### Accessing the Application

Once all three components are running, open your web browser and go to:
**[http://localhost:5173](https://www.google.com/search?q=http://localhost:5173)**

## Credits and Acknowledgements

This project stands on the shoulders of giants. Special thanks go to the team at Unsloth AI for their incredible work in making high-performance fine-tuning accessible.

The core fine-tuning script, including the GRPO implementation, memory optimization techniques, and reward functions, was heavily based on their official Colab notebook. Please support their work by starring their [GitHub repository](https://github.com/unslothai/unsloth).

- **Source Notebook:** [DeepSeek_R1_0528_Qwen3_(8B)_GRPO.ipynb](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/DeepSeek_R1_0528_Qwen3_(8B)_GRPO.ipynb)