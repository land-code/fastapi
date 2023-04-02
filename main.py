from fastapi import FastAPI

app = FastAPI()

employees_list = ["Andrés", "Juan Luis"]

@app.get(path="/employees")
def employees():
    return {"employees_list": employees_list}


@app.post(path="/employees")
def add_employee(name):
    employees_list.append(name)
    return "Appended successful"
