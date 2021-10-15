# Repository for Research Paper: Serverless Thumbnail Generation
Serverless deployment on Cloud Code Engine that uses the Lithops Framework to process images in parallel

**English Title:** Juxtaposition of thumbnail generation on IBM Cloud Code Engine with multiprocessing through the Lithops Framework and the traditional deployment on a virtual machine

**German Title:** Gegenüberstellung eines serverless Batch Jobs basierend auf dem Lithops Framework zur parallelen Generierung von Thumbnails auf IBM Cloud Code Engine und der Bereitstellung auf einem Virtual Server im Hinblick auf Performance, Skalierbarkeit und Kosten

(susceptible to change)

## Running the Thumbnail Generator

### Setting up requirements
- Create an IBM Cloud IAM Key [here](https://cloud.ibm.com/iam/apikeys)
- Create an IBM Cloud [COS Bucket](https://cloud.ibm.com/objectstorage/create) and store all images to be processed in a directory called "images"
- Create an IBM Cloud [Code Engine Namespace](https://cloud.ibm.com/codeengine/create/start)
- Add these keys with your values to the `.lithops_config`:

```
lithops:
    storage: ibm_cos
    storage_bucket: <YOUR BUCKET NAME>
    backend: code_engine
    mode: serverless
    
ibm:
    iam_api_key: <IAM_API_KEY>
   
code_engine:
    namespace: <NAMESPACE>
    region: <REGION>
    runtime: ibmfunctions/lithops-ce-v385:235
```
For more info, have a look [here](https://lithops-cloud.github.io/docs/source/compute_config/code_engine.html)


### 1. Sequential Thumbnail Generation

### 2. Multiprocessing Thumbnail Generation

### 3. Serverless Thumbnail Generation (Lithops)

## Architecture

### Thumbnail Generator System Context
<img src="./documentation/PA2-System-Context.png" width="30%" height="auto"/>

### Thumbnail Generator Architecture
<img src="./documentation/PA2-Architecture.png" width="30%" height="auto"/>


