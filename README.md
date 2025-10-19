# AgentsToAllies

### Topic: 6044:
From Agents to Allies: Empowering Technologists with Multi-Agent AI Workflows

### Abstract: 
This session is built for technologists who want to understand how multi-agent systems work, build them from the ground up, and be part of the rapidly growing ecosystem shaping their future. Instead of abstract concepts, we'll explore this shift through real-time demos and an honest, practical look at the tools and frameworks available today.

## Setup

1. Install/Use an IDE of your choice. We are using Visual Studio Code.
   Some of the IDE Installers: 
   Visual Studio Code: https://code.visualstudio.com/download

2. Download and Install Python 3.13.9 from: https://www.python.org/downloads/

3. Create and activate a Python virtual environment:
   Powershell command to Create:
   ```
   python -m venv env 
   ```
   Powershell command to activate
   ```
   .\env\Scripts\activate  # Windows
   source env/bin/activate # Unix/MacOS
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create .env file at the root folder and add this 
    ```
    AZURE_OPENAI_API_KEY= "<your_api_key>"
    AZURE_OPENAI_ENDPOINT="<your_openai_endpoint>"
    MODEL_NAME="<your_model_name>"
    AI_FOUNDRY_AZURE_OPENAI_API_KEY="<your_api_key>"
    NEWSAPI_API_KEY="<news_api_key>"
    AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="<your_model_name>"
    AZURE_AI_PROJECT_ENDPOINT="<your_azureaiproject_endpoint>"
    AZURE_AI_MODEL_DEPLOYMENT_NAME="<your_model_name>"
    SERPAPI_API_KEY="<your_serp_api>"
    ```
6. Get SERPAPI_API_KEY by signing up to https://serpapi.com/. Register with the email and phone-number to recieve a unique api key.
   Update the SERPAPI_API_KEY in the .env file with key obtained

7. Get the NEWSAPI_API_KEY from https://newsapi.org/. Register with email and password to get the API key.
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
