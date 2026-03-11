from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from ask_enterprise_ai import retrieve_context, ask_llama
from query_parser import extract_filters

app = FastAPI()

# serve static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


class QueryRequest(BaseModel):
    org_id: str
    query: str


# homepage → load chat UI
@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/ask")
def ask_ai(request: QueryRequest):

    org_id = request.org_id
    user_query = request.query

    # extract filters
    query, brand, price_limit = extract_filters(user_query)

    context = retrieve_context(query, org_id, brand, price_limit)

    if context.strip() == "":
        return {"answer": "No matching records found."}

    answer = ask_llama(query, context)

    return {
        "query": user_query,
        "parsed_query": query,
        "brand": brand,
        "price_limit": price_limit,
        "answer": answer
    }