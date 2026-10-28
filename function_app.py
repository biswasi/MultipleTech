import azure.funcions as func
import json
from db import get_container
from models import CustomerCreate

app = func.FunctionApp()

@app.route(route="customers", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def create_customer(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        customer = CustomerCreate(**req_body)
        container = get_container()
        
        # Insert or upsert item into Cosmos DB
        container.upsert_item(customer.model_dump())
        
        return func.HttpResponse(
            body=json.dumps({"message": "Customer created successfully", "data": customer.model_dump()}),
            status_code=201,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            body=json.dumps({"error": str(e)}),
            status_code=400,
            mimetype="application/json"
        )

@app.route(route="customers/{id}", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
def get_customer(req: func.HttpRequest) -> func.HttpResponse:
    customer_id = req.route_params.get("id")
    try:
        container = get_container()
        # Point read is more efficient than a SQL query if you have the id and partition key
        item = container.read_item(item=customer_id, partition_key=customer_id)
        return func.HttpResponse(
            body=json.dumps(item),
            status_code=200,
            mimetype="application/json"
        )
    except Exception:
        return func.HttpResponse(
            body=json.dumps({"error": "Customer not found"}),
            status_code=404,
            mimetype="application/json"
        )
