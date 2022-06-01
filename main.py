from typing import Union
from fastapi import FastAPI, HTTPException
from uuid import UUID
from uuid import uuid4
from kubernetes import client, config
import json
import yaml
from os import path

app = FastAPI()

config.load_kube_config()

@app.get("/questdb/{instance_id}")
def questdb_status(instance_id: UUID):
    instance_id_str = str(instance_id)
    v1 = client.AppsV1Api()
    try:
        ret = v1.read_namespaced_stateful_set_status(name="questdb", namespace=instance_id_str)
    except:
        raise HTTPException(status_code=404, detail="QuestDB instance not found")    
    return json.dump(ret)

@app.post("/questdb")
def questdb_create():
    instance_id: UUID = uuid4()
    instance_id_str = str(instance_id)
    client.CoreV1Api().create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name=instance_id_str)))
    v1 = client.AppsV1Api()
    with open(path.join(path.dirname(__file__), "questdb_config_map.yml")) as f:
        dep = yaml.safe_load(f)
        ret = client.CoreV1Api().create_namespaced_config_map(namespace=instance_id_str, body=dep)
    with open(path.join(path.dirname(__file__), "questdb_service.yml")) as f:
        dep = yaml.safe_load(f)
        ret = client.CoreV1Api().create_namespaced_service(namespace=instance_id_str, body=dep)
    with open(path.join(path.dirname(__file__), "questdb_headless_svc.yml")) as f:
        dep = yaml.safe_load(f)
        ret = client.CoreV1Api().create_namespaced_service(namespace=instance_id_str, body=dep)
    with open(path.join(path.dirname(__file__), "questdb_stateful_set.yml")) as f:
        dep = yaml.safe_load(f)
        ret = v1.create_namespaced_stateful_set(namespace=instance_id_str, body=dep)
    return {"id": instance_id}

@app.delete("/questdb/{instance_id}")
def questdb_delete(instance_id: UUID):
    instance_id_str = str(instance_id)
    v1 = client.AppsV1Api()
    try:
        ret = v1.read_namespaced_stateful_set(name="questdb", namespace=instance_id_str)
    except:
        raise HTTPException(status_code=404, detail="QuestDB instance not found")
    v1.delete_namespaced_stateful_set(name="questdb", namespace=instance_id_str)
    client.CoreV1Api().delete_namespace(name=instance_id_str)
    return {"ok": True}