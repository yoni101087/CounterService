# Counter Service Python App

The Counter Service Python App is a lightweight web application designed to maintain a counter of the number of POST requests it receives. Built using the Flask web framework, this application offers simplicity, flexibility, and robustness for tracking incoming requests.

# Usage 

To check the app counter simply run:
curl -X POST http://localhost:80



# Pipeline Explanation

This document outlines the steps of the deployment pipeline:

## Step 1: Build Docker Image
Build a Docker image from the selected branch using its associated SHA-1 hash. This ensures that a specific version of the code is used for the deployment.

## Step 2: Promote to Production
Promote the Docker image to the production environment by tagging and pushing it to Docker Hub.

## Step 3: Deploy to Production
Deploy the newly built Docker image to the production environment using Docker Swarm. If the deployment fails, an automated rollback to the previous version is triggered to maintain system stability.

## Step 4: Tag as Stable
If the deployment is successful, mark the Docker image as stable on the production host. Additionally, append the `-stable` tag to the image on Docker Hub. This practice helps track and identify stable versions of the application.

Feel free to modify and adapt these steps based on your project's specific requirements.





