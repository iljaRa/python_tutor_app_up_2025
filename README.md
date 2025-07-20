# Python Programming Tutor

An interactive Python programming tutor that uses AI to generate questions and evaluate student answers.

## Features

- Generate Python programming questions based on difficulty level and topic
- Submit your solutions and get detailed feedback
- AI-powered evaluation of your code
- Interactive Gradio interface


> **⚠️ Warning:** Some costs could arise from using this project:
> - **Together API** and **Langchain API** may charge for usage depending on your API plan.
> - **DockerHub** may charge for private repositories or high usage (optional).
> - **Azure** may charge for running web apps or other resources (optional).
> 
> Please review the pricing of these services before using them extensively. 


## Setup

1. Clone this repository using `git clone https://github.com/iljaRa/python_tutor_app_up_2025.git`
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. You will find a `.env.example file`, which illustrates the environmental variables that you need. These variables should hold your tokens. **DO NOT ENTER YOUR TOKENS INTO THE .env.example FILE!!!** Instead, copy `.env.example` to `.env`.
   ```bash
   cp .env.example .env
   ```
Bear in mind that `.env.example` and `.env` files may be invisible by default (because their names start with a `.` - this is a convention). You can easily find online instructions on how to show hidden files, depending on your operating system (OS).
4. Edit the `.env` file to replace <your_together_token> and <your_langchain_token> with the actual tokens. Also, replace <your_invented_username> and <your_invented_password> with whatever username and password you choose.
The trick here is that another file, called `.gitignore`, defines which files to ignore when the code is saved to the git repository. As defined in `.gitignore`, the `.env` file is ignored, so it will never be automatically sent to the remote repository, so nobody will see `.env`'s contents.

## Running the Application

To start the application with Docker, run:
```bash
# Build the Docker images
docker-compose build

# Start the application
docker-compose up

# Stop the application
docker-compose down
```

The application will be available at `http://localhost:7860` by default. Note that you might get a message that your application is available at `http://0.0.0.0:7860`, which will probably not work. Use `http://localhost:7860`!

## Usage

1. Select a difficulty level (Beginner, Intermediate, or Advanced)
2. Enter a topic (e.g., "Lists", "Functions", "Classes")
3. Click "Generate New Question" to get a Python programming question
4. Write your solution in the "Your Answer" text box
5. Click "Submit Answer" to get AI-powered feedback on your solution

## Requirements

- Python 3.8+
- Together API key
- Langchain API key
- Required Python packages (see requirements.txt). These will be installed automatically by Docker when you enter `docker-compose build`.

# Your first CI/CD experience
Now that you have the code and it is running on your computer, let us begin setting it up for deployment. This will allow you to move the app to the cloud (in our case Azure but AWS, Google Cloud, OVHCloud, Hetzner, etc., will also work). When your app runs on the cloud, you can access it from other devices, for example your phone or another computer. 

It might take you a few hours to complete the setup but that's OK! You will learn a lot about the practical aspects of app deployment. Moreover, when you develop another app (perhaps as an additional hobby project), you will need to follow almost exactly the same steps as below. In other words: the process may look intimidating now but once you complete it, it will be much more intuitive and you will be able to apply it to your future projects! So let's get started :)

## Create Your Own Repository

To prepare for deployment and CI/CD, you should create your own Git repository and push your code there. Follow these steps:

1. **Create a new repository on GitHub**
   - Go to [GitHub](https://github.com/) and log in.
   - Click the "+" icon in the top right and select **New repository**.
   - Give your repository a name (e.g., `python-tutor-up-2025`) and click **Create repository**.

2. **Initialize your local repository (if not already done)**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **Add your new GitHub repository as a remote and push your code**
   Replace `<your-username>` and `<your-repo>` with your actual GitHub username and repository name:
   ```bash
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git branch -M main
   git push -u origin main
   ```

## Continuous Integration and Deployment with GitHub Actions

This project includes a GitHub Actions workflow for deploying the app to Azure. GitHub Actions is a powerful automation tool that can build, test, and deploy your code whenever you push changes to your repository.

- The workflow file for deploying to Azure is already present in this folder (look for a `.github/workflows/` directory).
- When you push your code to GitHub, the workflow will automatically run and deploy your app to Azure, provided you have set up the required secrets.

### Setting Up GitHub Actions Secrets

To securely provide your API keys and credentials to the workflow, you need to set them as GitHub Actions secrets:

1. Go to your repository on GitHub.
2. Click on **Settings**.
3. In the left sidebar, click **Secrets and variables** > **Actions**.
4. Click **New repository secret** for each of the following:
   - `TOGETHER_API_KEY`
   - `LANGCHAIN_API_KEY`
   - `PYTUTOR_USERNAME`
   - `PYTUTOR_PASSWORD`

Paste the appropriate values for each secret. These will be used by the GitHub Actions workflow to deploy your app securely.

You are now ready to collaborate, deploy, and iterate on your Python Tutor app using modern DevOps practices! You can see the progress of your workflow when you go to your GitHub repository and click on **Actions**. However, your workflow will fail for several reasons, which we will fix in the following.

## This project's workflow, step by step

Let's break down what happens in the GitHub Actions workflow file `.github/workflows/azure-webapps-python.yml`. This file automates the process of building your app, pushing it to Docker Hub, and deploying it to Azure. Here’s what each part does:

1. **Workflow Name and Triggers**
   - The workflow is named **Deploy frontend**.
   - It runs automatically whenever you push to the `main` branch, or you can trigger it manually from GitHub (using `workflow_dispatch`).

2. **Job Definition**
   - The main job is called `build-and-deploy` and runs on the latest Ubuntu runner provided by GitHub. A runner is essentially a separate computer where GitHub Actions runs your code.
   - It sets permissions for reading repository contents and writing ID tokens (for authentication).

3. **Steps in the Job**
   - **Checkout the Code**
     - Uses the `actions/checkout@v4` action to pull your repository’s code into the workflow runner.

   - **Login to Docker Hub**
     - Uses the `docker/login-action@v3` action to log in to Docker Hub using your Docker Hub username and password (stored as GitHub secrets: `DOCKERHUB_USERNAME` and `DOCKERHUB_PASSWORD`).

   - **Build the Docker Image**
     - Runs a command to build your Docker image using `docker compose`, passing in your API keys and credentials as build arguments. These are securely provided from your GitHub secrets.

   - **Tag the Docker Image**
     - Tags the built Docker image with your Docker Hub username and the tag `latest` (e.g., `yourusername/up_projects:latest`).

   - **Push the Docker Image to Docker Hub**
     - Pushes the tagged image to your Docker Hub repository so it can be accessed by Azure.

   - **Login to Azure App Service**
     - Uses the `azure/login@v1` action to authenticate with Azure using credentials stored in the `AZURE_CREDENTIALS` secret.

   - **Deploy to Azure App Service**
     - Uses the `azure/webapps-deploy@v2` action to deploy your Docker image from Docker Hub to your Azure App Service. The `app-name` is set to `python-tutor`, and the image is pulled from your Docker Hub repository.

### Summary Table
| Step                        | What it does                                                      |
|-----------------------------|-------------------------------------------------------------------|
| Checkout                    | Gets your code onto the runner                                    |
| Docker Hub Login            | Authenticates to Docker Hub                                       |
| Build Docker Image          | Builds your app’s Docker image with secrets as build args          |
| Tag Docker Image            | Tags the image for Docker Hub                                     |
| Push Docker Image           | Uploads the image to Docker Hub                                   |
| Azure Login                 | Authenticates to Azure                                            |
| Deploy to Azure App Service | Deploys your app from Docker Hub to Azure App Service             |

This workflow automates the entire process of building, publishing, and deploying your app every time you push changes to your repository, making your development and deployment process much smoother and more reliable.

## Setting up Docker credentials
As described above, the workflow will try to login to your DockerHub, then build, tag and push this app's Docker image. For this to work, you need to follow the steps below.

### 1. Create a Private Repository on DockerHub

1. Go to [DockerHub](https://hub.docker.com/) and log in or create an account if you don't have one.
2. In the top menu, click on your profile icon and select **Repositories**.
3. Click the **Create Repository** button.
4. Set the **Repository Name** to `up_projects`.
5. Make sure to select **Private** so only you can access and push images to this repository.
6. Click **Create** to finish.

### 2. Find Your DockerHub Username

- Your DockerHub username is shown in the top right corner after you log in. You can also find it in your [DockerHub account settings](https://hub.docker.com/settings/profile).

### 3. Get Your DockerHub Password (or Create a Personal Access Token)

- **Recommended:** Instead of your main password, create a [DockerHub Access Token](https://hub.docker.com/settings/security) for better security:
  1. Go to your DockerHub **Account Settings** > **Security**.
  2. Click **New Access Token**.
  3. Give it a name (e.g., `github-actions`) and click **Generate**.
  4. Copy the token (this is your "password" for GitHub Actions). You won't be able to see it again!

### 4. Store Your DockerHub Credentials as GitHub Actions Secrets

1. Go to your GitHub repository.
2. Click on **Settings**.
3. In the left sidebar, click **Secrets and variables** > **Actions**.
4. Click **New repository secret** and add:
   - `DOCKERHUB_USERNAME` — your DockerHub username
   - `DOCKERHUB_PASSWORD` — your DockerHub password or access token (recommended)

Now, your workflow will be able to log in to DockerHub and push your app’s Docker image securely!

## Azure credentials
Great! Most of the workflow is covered and we are almost done. The final step is to get the Azure credentials so the workflow can authenticate to Azure and use your Docker image as a web app.

> **⚠️ Caution:** An Azure web app could cost you ca. $10 per month! The costs could balloon even further if you deviate from the below instructions!

Follow these steps to set up your Azure environment and collect all the necessary credentials:

### 1. Log in to Azure
If you haven't already, install the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) and log in:
```bash
az login
```

### 2. Create a Resource Group (if you don't have one)
A resource group is a container for your Azure resources.
```bash
az group create --name <ResourceGroupName> --location <AzureRegion>
```
Example:
```bash
az group create --name MyResourceGroup --location westeurope
```

### 3. Create an App Service Plan
This defines the compute resources for your web app.
```bash
az appservice plan create -g <ResourceGroupName> -n <AppServicePlanName> -l <AzureRegion> --is-linux --sku B1
```
Example:
```bash
az appservice plan create -g MyResourceGroup -n MyAppServicePlan -l westeurope --is-linux --sku B1
```
To the best of my knowledge, B1 is the cheapest service plan. There is also a free tier but, in my experience, it doesn't work well and your app might not be deployed as expected.

### 4. Create the Web App (using your DockerHub image)
```bash
az webapp create -g <ResourceGroupName> -p <AppServicePlanName> -n <WebAppName> --deployment-container-image-name <DockerHubUsername>/up_projects:latest
```
Example:
```bash
az webapp create -g MyResourceGroup -p MyAppServicePlan -n my-web-app --deployment-container-image-name yourdockerhubusername/up_projects:latest
```

### 5. Configure the Web App to Use Your DockerHub Image (if needed)
```bash
az webapp config container set -g <ResourceGroupName> -n <WebAppName> --docker-custom-image-name <DockerHubUsername>/up_projects:latest --docker-registry-server-url https://index.docker.io --docker-registry-server-user <DOCKERHUB_USERNAME> --docker-registry-server-password <DOCKERHUB_PASSWORD>
```

### 6. Get Your Azure Credentials for GitHub Actions
You will need the following secrets for your GitHub repository:
- `AZURE_CREDENTIALS` (Service Principal credentials in JSON format)
- `AZURE_APP_NAME` (your web app name, e.g., `my-web-app`)
- `DOCKERHUB_USERNAME` and `DOCKERHUB_PASSWORD` (already set up in previous steps)
- `AZURE_SUBSCRIPTION_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` (from your Service Principal)

#### a. Create a Service Principal for GitHub Actions
This allows GitHub Actions to deploy to your Azure resources securely.
```bash
az ad sp create-for-rbac --name "<ServicePrincipalName>" --role contributor --scopes /subscriptions/<SubscriptionID>/resourceGroups/<ResourceGroupName> --sdk-auth
```
Example:
```bash
az ad sp create-for-rbac --name "my-github-actions-sp" --role contributor --scopes /subscriptions/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/resourceGroups/MyResourceGroup --sdk-auth
```
- The output will be a JSON object. Copy this and save it as the value for the `AZURE_CREDENTIALS` secret in your GitHub repository.

#### b. Get Your Subscription ID, Tenant ID, Client ID, and Client Secret
- **Subscription ID:** Go to the Azure Portal → Subscriptions → select your subscription → Overview.
- **Tenant ID:** Go to Azure Portal → Microsoft Entra ID → Overview.
- **Client ID and Client Secret:** These are in the Service Principal output or in Azure Portal → App registrations → your app → Overview (for Client ID) and Certificates & secrets (for Client Secret).

From these, you can assemble the following JSON object:
```
{
	"subscriptionId": "<your_subscription_id>",
	"tenantId": "<your_tenant_id>",
	"clientId": "<your_client_id>",
	"clientSecret": "<your_client_secret>"
}
```

### 7. Add All Secrets to GitHub Actions
Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions** and add:
- `AZURE_CREDENTIALS` (the exact JSON object from the Service Principal, as shown above, including the curly brackets and the double quotation marks. Make sure to replace <your_subscription_id>, etc., with the actual values!)
- `AZURE_APP_NAME`
- `AZURE_SUBSCRIPTION_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` (if your workflow requires them)

### 8. Set Environment Variables in Azure Web App
After deployment, go to the [Azure Portal](https://portal.azure.com), find your Web App, and set the same environment variables (API keys, usernames, passwords) under **Settings > Environment variables**.

---

**Troubleshooting Tips:**
- If you get errors about missing images, make sure your image name in `docker-compose.yml` matches your DockerHub repository name.
- If the app fails to start, double-check your DockerHub credentials and environment variables in Azure.
- If you can't log in to the app, ensure the app username and password are set as environment variables in Azure.
- The first time you open a deployed app it takes 10 to 15 minutes. Open your app in a private browser window (or incognito mode) to ensure no cookies and no cache is used.

---

You are now ready to deploy your app to Azure using GitHub Actions and DockerHub! 🎉
