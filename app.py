from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

students = []

# ---------------------------
# LANDING PAGE
# ---------------------------
@app.route("/")
def landing():
    return render_template_string("""

<!DOCTYPE html>
<html>
<head>
<title>Student Management API</title>

<style>

body{
margin:0;
font-family:Segoe UI;
height:100vh;
display:flex;
justify-content:center;
align-items:center;
background:linear-gradient(135deg,#667eea,#764ba2);
color:white;
text-align:center;
}

.container{
background:rgba(255,255,255,0.15);
padding:60px;
border-radius:20px;
backdrop-filter:blur(10px);
width:520px;
}

h1{
font-size:36px;
margin-bottom:15px;
}

p{
opacity:0.9;
margin-bottom:30px;
}

button{
padding:14px 30px;
border:none;
border-radius:10px;
background:#00e1ff;
font-size:16px;
font-weight:bold;
cursor:pointer;
}

button:hover{
background:#00bcd4;
}

</style>

</head>

<body>

<div class="container">

<h1>🎓 Student Management System</h1>

<p>
This project demonstrates a Flask API integrated with a modern
web interface. Users can add students, view all records,
search students, and manage the list.
</p>

<button onclick="start()">Start System</button>

</div>

<script>

function start(){
window.location="/form"
}

</script>

</body>
</html>

""")

# ---------------------------
# STUDENT FORM
# ---------------------------
@app.route("/form")
def form():
    return render_template_string("""

<!DOCTYPE html>
<html>
<head>
<title>Add Student</title>

<style>

body{
font-family:Segoe UI;
background:linear-gradient(135deg,#667eea,#764ba2);
display:flex;
justify-content:center;
align-items:center;
height:100vh;
color:white;
}

.container{
background:rgba(255,255,255,0.15);
padding:40px;
border-radius:20px;
backdrop-filter:blur(10px);
width:400px;
text-align:center;
}

input{
width:100%;
padding:10px;
margin:10px 0;
border:none;
border-radius:6px;
}

button{
width:100%;
padding:12px;
margin-top:10px;
border:none;
border-radius:8px;
background:#00e1ff;
font-weight:bold;
cursor:pointer;
}

button:hover{
background:#00bcd4;
}

</style>

</head>

<body>

<div class="container">

<h2>➕ Add Student</h2>

<input id="name" placeholder="Student Name">
<input id="grade" placeholder="Grade">
<input id="section" placeholder="Section">

<button onclick="saveStudent()">Save Student</button>

<button onclick="viewStudents()">View Student List</button>

<button onclick="goHome()">Back to Home</button>

</div>

<script>

function saveStudent(){

let name=document.getElementById("name").value
let grade=document.getElementById("grade").value
let section=document.getElementById("section").value

fetch("/student",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
name:name,
grade:grade,
section:section
})
})
.then(res=>res.json())
.then(data=>{
alert("Student Saved ✅")
})

}

function viewStudents(){
window.location="/students"
}

function goHome(){
window.location="/"
}

</script>

</body>
</html>

""")

# ---------------------------
# STUDENT LIST
# ---------------------------
@app.route("/students")
def students_page():
    return render_template_string("""

<!DOCTYPE html>
<html>
<head>
<title>Student List</title>

<style>

body{
font-family:Segoe UI;
background:linear-gradient(135deg,#667eea,#764ba2);
padding:40px;
color:white;
text-align:center;
}

.search{
margin-bottom:20px;
}

input{
padding:10px;
border:none;
border-radius:6px;
width:250px;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
gap:20px;
margin-top:30px;
}

.card{
background:rgba(255,255,255,0.2);
padding:20px;
border-radius:12px;
backdrop-filter:blur(8px);
}

button{
margin-top:10px;
padding:8px 15px;
border:none;
border-radius:6px;
background:#ff5c5c;
color:white;
cursor:pointer;
}

.nav{
margin-top:30px;
}

.nav button{
background:#00e1ff;
color:black;
margin:5px;
}

</style>

</head>

<body>

<h1>📚 Student List</h1>

<div class="search">
<input id="search" placeholder="Search student..." onkeyup="searchStudent()">
</div>

<div class="grid" id="students"></div>

<div class="nav">
<button onclick="goForm()">Add Student</button>
<button onclick="goHome()">Back to Home</button>
</div>

<script>

let allStudents=[]

fetch("/student")
.then(res=>res.json())
.then(data=>{
allStudents=data
displayStudents(data)
})

function displayStudents(data){

let container=document.getElementById("students")
container.innerHTML=""

data.forEach((student,index)=>{

container.innerHTML+=
"<div class='card'>"+
"<h3>"+student.name+"</h3>"+
"<p>Grade: "+student.grade+"</p>"+
"<p>Section: "+student.section+"</p>"+
"<button onclick='deleteStudent("+index+")'>Delete</button>"+
"</div>"

})

}

function searchStudent(){

let keyword=document.getElementById("search").value.toLowerCase()

let filtered=allStudents.filter(s =>
s.name.toLowerCase().includes(keyword)
)

displayStudents(filtered)

}

function deleteStudent(index){

fetch("/delete/"+index,{method:"DELETE"})
.then(res=>res.json())
.then(data=>{
location.reload()
})

}

function goForm(){
window.location="/form"
}

function goHome(){
window.location="/"
}

</script>

</body>
</html>

""")

# ---------------------------
# API ROUTES
# ---------------------------
@app.route("/student", methods=["GET","POST"])
def student():

    global students

    if request.method == "POST":
        data=request.json
        students.append(data)
        return jsonify({"message":"Student saved","students":students})

    return jsonify(students)


@app.route("/delete/<int:index>", methods=["DELETE"])
def delete_student(index):

    if index < len(students):
        students.pop(index)

    return jsonify({"message":"Student deleted"})


# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
