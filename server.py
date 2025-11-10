from fastapi import FastAPI, File, UploadFile
from typing_extensions import Annotated
import uvicorn
from utils import *
from dijkstra import dijkstra
import json

# create FastAPI app
app = FastAPI()

# global variable for active graph
active_graph = None

@app.get("/")
async def root():
    return {"message": "Welcome to the Shortest Path Solver!"}


@app.post("/upload_graph_json/")
async def create_upload_file(file: UploadFile):
    global active_graph

    # Check file type
    if not file.filename.endswith(".json"):
        return {"Upload Error": "Invalid file type. Please upload a JSON file."}

    try:
        active_graph = create_graph_from_json(file)
        return {"Upload Success": file.filename}
    except Exception:
        return {"Error: File failed to process"}
        

@app.get("/solve_shortest_path/start_node_id={start_node_id}&end_node_id={end_node_id}")
async def solve_shortest_path(start_node_id: str, end_node_id: str):
    if not active_graph:
        return {"Solver Error": "No active graph uploaded."}

    try:
        start = active_graph.nodes.get(start_node_id)
        end = active_graph.nodes.get(end_node_id)
        if not start or not end:
            return {"Solver Error": "Invalid start or end node ID."}

        dijkstra(active_graph, start)

        # Rebuild path from end to start
        path = []
        current = end
        while current:
            path.append(current.id)
            current = current.prev
            
        path.reverse()

        if not path or path[0] != start_node_id:
            return {"Solver Error": "No path found."}

        return {"shortest_path": path, "total_distance": end.dist}

    except Exception as e:
        return {"Solver Error": f"{e}"}
    #TODO: implement this function
    raise NotImplementedError("/solve_shortest_path not yet implemented.")

if __name__ == "__main__":
    print("Server is running at http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)



