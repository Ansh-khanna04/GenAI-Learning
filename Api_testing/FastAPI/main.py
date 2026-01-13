from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

# we know the pythonic way to call a function but what if we want to expose this function to outer
#world and call it from any other language or platform?

# Then we need to create an API for this function so that it can be called over HTTP protocol. 

app = FastAPI()

@app.get("/")
def test():
    return {"message": "Hey bro welcome!"}

@app.get("/hello")
def sayhello():
    return {"message": "Hello World!"}

sample_data = {1:"ANSH",2:"YASH",3:"Anshika",4:"Ritik"}
# now if i want to get some input also from the user and then return the result
# we will need id of the student from sample-data as input and our function will return the name of the student
# lets see how that will work
# here {id} is a path parameter that we will get from the user and we will return corresponding name
# Remember in function we need to mention the type of id as int otherwise it will be treated as string by default

@app.get("/get_name/{id}")
def return_name(id:int):
    return {"Student name is": sample_data[id]}

class new_data(BaseModel):
    id:int
    name:str

@app.post("/add_student")
def add_student(new_data:new_data):
    sample_data[new_data.id] = new_data.name
    return sample_data



############              DAY - 2           #####################

class Student(BaseModel):
    id:int
    name:str
    age:int

def save_student_to_file_system(data):
    with open("students.txt","a") as f:
        f.write(f"{data.id}, {data.name}, {data.age}\n")

@app.post("/create_student")
def create_student(stud:Student):
    student_data = stud.dict()
    save_student_to_file_system(stud)
    return {"message":"Student created successfully", "student_data":student_data}

db_url = "postgresql://neondb_owner:npg_aYXRougf6vW5@ep-steep-rain-ahs6u70k-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def estabilish_db_connection():
    conn = psycopg2.connect(db_url, cursor_factory=RealDictCursor)
    return conn

@app.post("/store_student_db")
def store_student_to_db(student:Student):
    conn = estabilish_db_connection()
    cursor = conn.cursor()
    insert_query = "INSERT INTO student (id, name, age) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (student.id, student.name, student.age))
    conn.commit()
    cursor.close()
    conn.close()