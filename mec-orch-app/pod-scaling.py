from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from kubernetes import client, config

app = FastAPI()

class DeploymentUpdate(BaseModel):
    name: str
    namespace: str
    replicas: int

@app.post("/update_deployment_replicas")
async def update_deployment_replicas(deployment_update: DeploymentUpdate):
    try:
        config.load_kube_config()

        api_instance = client.AppsV1Api()

        deployment = api_instance.read_namespaced_deployment(
            name=deployment_update.name,
            namespace=deployment_update.namespace
        )

        deployment.spec.replicas = deployment_update.replicas

        api_instance.patch_namespaced_deployment(
            name=deployment_update.name,
            namespace=deployment_update.namespace,
            body=deployment
        )

        return {"message": f"Replica count for deployment {deployment_update.name} in namespace {deployment_update.namespace} successfully updated."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
