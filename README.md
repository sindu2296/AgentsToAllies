# AgentsToAllies

### Topic: 6044:
From Agents to Allies: Empowering Technologists with Multi-Agent AI Workflows

### Abstract: 
This session is built for technologists who want to understand how multi-agent systems work, build them from the ground up, and be part of the rapidly growing ecosystem shaping their future. Instead of abstract concepts, we'll explore this shift through real-time demos and an honest, practical look at the tools and frameworks available today.

## 🚀 Setup

Choose your development environment:

<details>
<summary><b>💻 Option 1: Local Machine Setup</b> (Windows/Mac/Linux)</summary>

### 1. Install/Use an IDE of your choice
We are using Visual Studio Code.
- Visual Studio Code: https://code.visualstudio.com/download

### 2. Clone the Repository
```bash
git clone https://github.com/sindu2296/AgentsToAllies.git
cd AgentsToAllies
```

### 3. Download and Install Python 3.13.9
Download from: https://www.python.org/downloads/

Verify installation:
```bash
python --version
# Should output: Python 3.13.9
```

### 4. Create and activate a Python virtual environment

**Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv env

# Activate virtual environment
.\env\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Unix/MacOS:**
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
source env/bin/activate
```

### 5. Install dependencies
```bash
pip install -r requirements.txt
```

</details>

<details>
<summary><b>☁️ Option 2: GitHub Codespaces Setup</b> (Cloud-based)</summary>

### 1. Create a Codespace

**Option A: From GitHub Repository**
1. Navigate to [https://github.com/sindu2296/AgentsToAllies](https://github.com/sindu2296/AgentsToAllies)
2. Click the **Code** button (green button)
3. Select the **Codespaces** tab
4. Click **Create codespace on main**

**Option B: From GitHub Codespaces Dashboard**
1. Go to [https://github.com/codespaces](https://github.com/codespaces)
2. Click **New codespace**
3. Select repository: `sindu2296/AgentsToAllies`
4. Select branch: `main`
5. Click **Create codespace**

### 2. Wait for Environment Setup
The Codespace will automatically:
- ✅ Pull the repository code
- ✅ Install Python 3.13.9
- ✅ Install all required VS Code extensions
- ✅ Configure port forwarding for applications
- ✅ Set up the development environment

**This takes 2-5 minutes on first creation.**

### 3. Verify Setup
Once the Codespace loads, verify you're in the correct location:
```bash
pwd
# Should show: /workspaces/AgentsToAllies
```

**Note:** No virtual environment needed! The Codespace container provides complete isolation.

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

</details>

---

### Common Setup Steps (Required for Both Options)

Once you've completed either Option 1 or Option 2 above, follow these steps:

#### 1. Create .env file at the root folder
Create a `.env` file in the root directory with the following content:

```env
AZURE_OPENAI_API_KEY= "<your_api_key>"
AZURE_OPENAI_ENDPOINT="<your_endpoint>"
MODEL_NAME="<your_model_name>"
AI_FOUNDRY_AZURE_OPENAI_API_KEY="<your_api_key>"
NEWSAPI_API_KEY="<news_api_key>"
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="<your_model_name>"
AZURE_AI_PROJECT_ENDPOINT="<your_endpoint>"
AZURE_AI_MODEL_DEPLOYMENT_NAME="<your_model_name>"
SERPAPI_API_KEY="<your_serp_api>"
```

#### 2. Get API Keys

**📋 Azure OpenAI credentials:**  
Refer to [AZURE_AIFOUNDRY_SETUP.md](./AZURE_AIFOUNDRY_SETUP.md) for step-by-step instructions on how to set up Azure AI Foundry and get your API key and endpoint values.

**SERPAPI_API_KEY:**  
Sign up at https://serpapi.com/. Register with email and phone number to receive a unique API key.
Update the SERPAPI_API_KEY in the .env file with the key obtained.

**NEWSAPI_API_KEY:**  
Get from https://newsapi.org/. Register with email and password to get the API key.
Update the NEWSAPI_API_KEY in the .env file with the key obtained.

---

## Sample Projects

### 1. Azure OpenAI Chat Sample
A basic example showing how to use Azure OpenAI chat completions API. Found in `AIFoundry_sample.py`.

### 2. Semantic Kernel Plugin Sample
Located in `semantickernel_sample.py`, this demonstrates how to:
- Create and use Semantic Kernel plugins
- Set up chat completion with Azure OpenAI
- Handle interactive conversations using chat history

### 3. News Processing with Multiple Agents
Located in the `news` and `news_maf` folders, these samples show **two different frameworks** for building the same multi-agent news system:

#### Semantic Kernel Implementation (`news/`)
- Basic: Simple sequential processing with one agent
- Sequential: Multiple agents working one after another
- Concurrent: Parallel processing with `ConcurrentOrchestration`
- Uses: Kernel, plugins, `@kernel_function`, `FunctionChoiceBehavior.Auto()`

#### Microsoft Agent Framework Implementation (`news_maf/`)
- Sequential: Multiple agents working one after another
- Concurrent: Parallel processing with `ConcurrentBuilder`
- Uses: `ChatAgent`, function tools, simpler setup
- Run with:
  ```
  cd news_maf
  streamlit run app.py
  ```

Both implementations provide the same functionality but with different patterns and abstractions.


### 4. Job Recommendation with Multi Agents
Located in the `job_recommendation` and `job_recommendation_maf` folders, these samples show different approaches to job recommendation using multiple agents:

#### Semantic Kernel Implementation (`job_recommendation/`)
- Basic: Simple sequential processing with one agent
- Sequential: Multiple agents working one after another (extract, recommend, summarize)
- Concurrent: Parallel processing with multiple agents for efficiency

#### Microsoft Agent Framework Implementation (`job_recommendation_maf/`)
- Sequential: Multiple agents working one after another (extract, recommend, summarize)
- Uses: `ChatAgent`, SerpAPI integration
- Run with:
  ```
  cd job_recommendation_maf
  streamlit run app.py
  ```

Agents use SerpAPI to fetch jobs, recommend relevant ones, and summarize results.

Please refer to README file in the respective folders for more details.
