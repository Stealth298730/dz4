from typing import Optional,List,Union

from fastapi import FastAPI,HTTPException,status
import uvicorn 
from pydantic import BaseModel
from To_Do_tasks import To_Do_list

app = FastAPI()

class To_Do_listModel(BaseModel):
    id:int 
    name:str
    complexity:Optional[str] = None


@app.get("/tasks/{task_id}/",response_model = To_Do_listModel,status_code = status.HTTP_200_OK)
async def get_tasks(task_id:int):
    task = [task for task in To_Do_list if task.get("id") == task_id] 
    if task:
        return task[0]
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="task not found")

@app.get("/tasks/",response_model = List[To_Do_listModel],status_code= status.HTTP_200_OK)
async def get_tasks():
    return To_Do_list

@app.post("/tasks/",status_code=status.HTTP_201_CREATED)
async def create_task(task:To_Do_listModel):
    To_Do_list.append(task.dict())
    return dict(msg ="Created")


@app.put("/tasks/{tasks_id}/",response_model = To_Do_listModel,status_code=status.HTTP_202_ACCEPTED)
async def update_task(task_id:int,To_Do_list_model:To_Do_listModel):
    for task in To_Do_list:
        if task.get("id") == task_id:
            task["id"]= To_Do_list_model.model_dump()["id"]
            task["name"]= To_Do_list_model.model_dump()["name"]
            task["complexity"]= To_Do_list_model.model_dump()["complexity"]
            return task
        
@app.patch("/tasks/{param}/{tasks_id}/",status_code=status.HTTP_202_ACCEPTED)
async def update_param_task(param :str ,task_id:int,value:Union[str,int,str]):
    for task in To_Do_list:
        if task.get("id") == task_id:
            if param in task:
                task[param] = value

            else:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,parametr = "Parametr invalid")

@app.delete("/tasks/",status_code=status.HTTP_200_OK)
async def delete_task(task:To_Do_listModel):
    To_Do_list.remove(task.dict())
    return dict(msg = "Deleted" )


@app.delete("/tasks/{task_id}/", response_model=To_Do_listModel, status_code=status.HTTP_200_OK)
async def delete_task(task_id: int):
    task = next((task for task in To_Do_list if task["id"] == task_id), None)
    if task:
        To_Do_list.remove(task) 
        return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


if __name__ == "__main__":
    uvicorn.run("main:app" ,port = 3000)