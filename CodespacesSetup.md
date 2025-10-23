# AgentsToAllies - GitHub Codespaces Setup

### Topic: 6044:
From Agents to Allies: Empowering Technologists with Multi-Agent AI Workflows

### Abstract: 
This session is built for technologists who want to understand how multi-agent systems work, build them from the ground up, and be part of the rapidly growing ecosystem shaping their future. Instead of abstract concepts, we'll explore this shift through real-time demos and an honest, practical look at the tools and frameworks available today.

## Setup

### 1. Create a Codespace

#### Option A: From GitHub Repository
1. Navigate to [https://github.com/sindu2296/AgentsToAllies](https://github.com/sindu2296/AgentsToAllies)
2. Click the **Code** button (green button)
3. Select the **Codespaces** tab
4. Click **Create codespace on main**

#### Option B: From GitHub Codespaces Dashboard
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
Once the Codespace loads, the integrated terminal will open automatically in the repository root.
Verify you're in the correct location:
```bash
pwd
# Should show: /workspaces/AgentsToAllies
```

### 4. Install dependencies
**Note**: No virtual environment needed! The Codespace container provides complete isolation.

```bash
pip install -r requirements.txt
```

### 5. Create .env file at the root folder and add this 
```
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

**Using Terminal to create .env:**
```bash
cat > .env << 'EOF'
AZURE_OPENAI_API_KEY= "<your_api_key>"
AZURE_OPENAI_ENDPOINT="<your_endpoint>"
MODEL_NAME="<your_model_name>"
AI_FOUNDRY_AZURE_OPENAI_API_KEY="<your_api_key>"
NEWSAPI_API_KEY="<news_api_key>"
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="<your_model_name>"
AZURE_AI_PROJECT_ENDPOINT="<your_endpoint>"
AZURE_AI_MODEL_DEPLOYMENT_NAME="<your_model_name>"
SERPAPI_API_KEY="<your_serp_api>"
EOF
```

**Or Using VS Code:**
1. Right-click in the Explorer pane
2. Select **New File**
3. Name it `.env`
4. Add your configuration as shown above

### 6. **📋 For Azure OpenAI credentials:** 
Refer to [AZURE_AIFOUNDRY_SETUP.md](./AZURE_AIFOUNDRY_SETUP.md) for step-by-step instructions on how to set up Azure AI Foundry and get your API key and endpoint values.

### 7. Get SERPAPI_API_KEY
Sign up to https://serpapi.com/. Register with the email and phone-number to receive a unique api key.
Update the SERPAPI_API_KEY in the .env file with key obtained

### 8. Get the NEWSAPI_API_KEY
Get from https://newsapi.org/. Register with email and password to get the API key.
Update the NEWSAPI_API_KEY in the .env file with key obtained

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
  ```bash
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
  ```bash
  cd job_recommendation_maf
  streamlit run app.py
  ```

Agents use SerpAPI to fetch jobs, recommend relevant ones, and summarize results.

Please refer to README file in the respective folders for more details.
