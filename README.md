# File Uploader Web App

This is a small web application that allows users to upload files, which are then stored in Google Cloud Storage (GCS) using a Python Flask backend deployed on Google Cloud Run. The frontend is a simple HTML form served by the same Flask application.

## Features

*   **File Upload**: Users can select and upload files through a web interface.
*   **Google Cloud Storage Integration**: Uploaded files are securely stored in a specified GCS bucket.
*   **Public URL Return**: A direct link to the uploaded file is returned upon successful upload.
*   **File Size Limit**: Configurable file size limit to prevent large uploads.
*   **Serverless Deployment**: The entire application is designed for deployment on Google Cloud Run, offering scalability and cost-efficiency.

## Project Structure

```
.
├── app.py                  # Flask backend application
├── requirements.txt        # Python dependencies
├── Dockerfile              # Used to containerize the Flask app
├── .dockerignore           # Specifies files to ignore when building Docker image
└── templates/
    └── index.html          # Frontend HTML file with upload form
```

## Setup and Deployment on Google Cloud Platform (GCP)

Follow these steps to deploy and run your file uploader application on Google Cloud.

### Prerequisites

1.  **Google Cloud Project**:
    *   Create a new Google Cloud Project or select an existing one.
    *   Make sure billing is enabled for your project.
2.  **Enable GCP APIs**: Ensure the following APIs are enabled for your project:
    *   Cloud Run API
    *   Cloud Storage API
    *   Cloud Build API
3.  **Google Cloud CLI (`gcloud`)**:
    *   Install the `gcloud` CLI tool on your local machine if you haven't already. Follow the official installation guide: [Install Google Cloud CLI](https://cloud.google.com/sdk/docs/install).
    *   Authenticate and set your project:
        ```bash
        gcloud auth login
        gcloud config set project YOUR_PROJECT_ID
        ```
        Replace `YOUR_PROJECT_ID` with your actual Google Cloud Project ID.
4.  **Local Project**: Ensure you are in the root directory of this project (`task2/` in your local setup).

### Deployment Steps

#### 1. Create a Google Cloud Storage Bucket for Uploaded Files

This bucket will be used by your Flask backend to store the files uploaded by users.

```bash
gsutil mb -p YOUR_PROJECT_ID -l YOUR_REGION gs://your-backend-gcs-bucket-name
```

*   Replace `YOUR_PROJECT_ID` with your Google Cloud Project ID.
*   Replace `YOUR_REGION` with your desired GCP region (e.g., `us-central1`, `europe-west1`).
*   Replace `your-backend-gcs-bucket-name` with a globally unique name for your GCS bucket. This name will be used in your Cloud Run environment variables.

#### 2. Build and Deploy the Flask Backend to Google Cloud Run

Your Flask application serves both the frontend HTML and handles file uploads.

```bash
# Navigate to the root directory of your project (e.g., cd /path/to/task2)

# Build the Docker image using Cloud Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/file-uploader-app

# Deploy the Docker image to Cloud Run
gcloud run deploy file-uploader-app \
  --image gcr.io/YOUR_PROJECT_ID/file-uploader-app \
  --platform managed \
  --region YOUR_REGION \
  --allow-unauthenticated \
  --set-env-vars GCS_BUCKET_NAME=your-backend-gcs-bucket-name \
  --port 8080
```

*   Replace `YOUR_PROJECT_ID` with your Google Cloud Project ID.
*   Replace `YOUR_REGION` with the same region you used for your GCS bucket.
*   Ensure `your-backend-gcs-bucket-name` matches the bucket name you created in the previous step.
*   The `--allow-unauthenticated` flag makes your Cloud Run service publicly accessible. For production, consider implementing more robust authentication.
*   `--port 8080` specifies that your Flask application listens on port 8080 within the container.

#### 3. Grant Cloud Run Service Account Permissions to Google Cloud Storage

Your Cloud Run service needs permissions to write (and make public) objects in your GCS bucket.

*   **Find your Cloud Run service account email**:
    ```bash
    gcloud run services describe file-uploader-app \
      --platform managed \
      --region YOUR_REGION \
      --format "value(spec.template.spec.serviceAccountName)"
    ```
    This command will output an email address, typically in the format `YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com`.

*   **Grant `Storage Object Admin` role**:
    ```bash
    gsutil iam ch serviceAccount:YOUR_SERVICE_ACCOUNT_EMAIL:objectAdmin gs://your-backend-gcs-bucket-name
    ```
    Replace `YOUR_SERVICE_ACCOUNT_EMAIL` with the email address obtained in the previous step, and `your-backend-gcs-bucket-name` with your GCS bucket name.

### Accessing the Application

After successful deployment, Google Cloud Run will provide a `Service URL`. You can find this URL in the Cloud Run console or by running:

```bash
gcloud run services describe file-uploader-app \
  --platform managed \
  --region YOUR_REGION \
  --format "value(status.url)"
```

Open this `Service URL` in your web browser. You should see the file upload form. Upload a file, and upon success, you'll receive a link to the file stored in your GCS bucket.

### Bonus: File Size Limit Configuration

You can configure the maximum allowed file size by setting an environment variable when deploying to Cloud Run:

```bash
gcloud run deploy file-uploader-app \
  --image gcr.io/YOUR_PROJECT_ID/file-uploader-app \
  --platform managed \
  --region YOUR_REGION \
  --allow-unauthenticated \
  --set-env-vars GCS_BUCKET_NAME=your-backend-gcs-bucket-name,MAX_FILE_SIZE_MB=10 \
  --port 8080
```

In this example, `MAX_FILE_SIZE_MB=10` would set the limit to 10 MB. The default is 5 MB if this environment variable is not set.

## Result
http://127.0.0.1:5000/







