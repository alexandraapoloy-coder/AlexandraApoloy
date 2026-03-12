from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

students = []

# -----------------------------
# LANDING PAGE
# -----------------------------
@app.route("/")
def landing():
    return render_template_string("""
<html>
<head>
<title>Student Management System</title>

<style>

body{
font-family:Segoe UI;
margin:0;
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
width:500px;
}

button{
padding:12px 25px;
border:none;
border-radius:8px;
background:#00e1ff;
font-weight:bold;
cursor:pointer;
}

</style>

</head>

<body>

<div class="container">

<h1>🎓 Student Management System</h1>

<p>A Flask API project with dashboard, student records, and management tools.</p>

<button onclick="enter()">Enter System</button>

</div>

<script>

function enter(){
window.location="/dashboard"
}

</script>

</body>
</html>
""")

# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/dashboard")
def dashboard():
    return render_template_string("""
<html>

<head>
<title>Dashboard</title>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
font-family:Segoe UI;
background:linear-gradient(135deg,#667eea,#764ba2);
color:white;
text-align:center;
padding:40px;
}

.nav{
margin-bottom:30px;
}

.nav button{
margin:5px;
padding:10px 20px;
border:none;
border-radius:6px;
background:#00e1ff;
font-weight:bold;
cursor:pointer;
}

.card{
background:rgba(255,255,255,0.2);
padding:20px;
border-radius:12px;
width:300px;
margin:auto;
margin-bottom:30px;
}

canvas{
background:white;
border-radius:10px;
padding:10px;
}

</style>

</head>

<body>

<div class="nav">
<button onclick="goForm()">Add Student</button>
<button onclick="goStudents()">Student List</button>
<button onclick="goHome()">Home</button>
</div>

<h1>📊 Dashboard</h1>

<div class="card">
<h2>Total Students</h2>
<h1 id="total">0</h1>
</div>

<canvas id="chart" width="400" height="200"></canvas>

<script>

fetch("/student")
.then(res=>res.json())
.then(data=>{

document.getElementById("total").innerText=data.length

let grades={}

data.forEach(s=>{
if(!grades[s.grade]){
grades[s.grade]=0
}
grades[s.grade]++
})

let labels=Object.keys(grades)
let values=Object.values(grades)

new Chart(document.getElementById("chart"),{

type:"bar",

data:{
labels:labels,
datasets:[{
label:"Students per Grade",
data:values
}]
}

})

})

function goForm(){
window.location="/form"
}

function goStudents(){
window.location="/students"
}

function goHome(){
window.location="/"
}

</script>

</body>
</html>
""")

# -----------------------------
# ADD STUDENT FORM
# -----------------------------
@app.route("/form")
def form():
    return render_template_string("""

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
margin:8px 0;
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

</style>

</head>

<body>

<div class="container">

<h2>Add Student</h2>

<input id="name" placeholder="Student Name">
<input id="grade" placeholder="Grade">
<input id="section" placeholder="Section">

<button onclick="saveStudent()">Save Student</button>
<button onclick="dashboard()">Dashboard</button>

</div>

<script>

function saveStudent(){

let name=document.getElementById("name").value
let grade=document.getElementById("grade").value
let section=document.getElementById("section").value

fetch("/student",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({name:name,grade:grade,section:section})
})
.then(res=>res.json())
.then(data=>{
alert("Student Saved")
})

}

function dashboard(){
window.location="/dashboard"
}

</script>

</body>
</html>
""")

# -----------------------------
# STUDENT LIST
# -----------------------------
@app.route("/students")
def students_page():
    return render_template_string("""

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

table{
width:80%;
margin:auto;
border-collapse:collapse;
background:rgba(255,255,255,0.2);
}

th,td{
padding:12px;
border:1px solid white;
}

th{
background:#00e1ff;
color:black;
}

button{
padding:6px 10px;
border:none;
border-radius:6px;
cursor:pointer;
}

.edit{
background:#ffc107;
}

.delete{
background:#ff5c5c;
color:white;
}

.nav{
margin-bottom:20px;
}

</style>

</head>

<body>

<div class="nav">
<button onclick="goDashboard()">Dashboard</button>
<button onclick="goForm()">Add Student</button>
</div>

<h1>📋 Student Records</h1>

<input id="search" placeholder="Search Student" onkeyup="searchStudent()">

<br><br>

<table>

<thead>
<tr>
<th>Name</th>
<th>Grade</th>
<th>Section</th>
<th>Actions</th>
</tr>
</thead>

<tbody id="table"></tbody>

</table>

<script>

let students=[]

fetch("/student")
.then(res=>res.json())
.then(data=>{

students=data.sort((a,b)=>a.name.localeCompare(b.name))

display(students)

})

function display(data){

let table=document.getElementById("table")

table.innerHTML=""

data.forEach((s,i)=>{

table.innerHTML+=`
<tr>
<td>${s.name}</td>
<td>${s.grade}</td>
<td>${s.section}</td>
<td>
<button class="edit" onclick="editStudent(${i})">Edit</button>
<button class="delete" onclick="deleteStudent(${i})">Delete</button>
</td>
</tr>
`

})

}

function searchStudent(){

let keyword=document.getElementById("search").value.toLowerCase()

let filtered=students.filter(s=>s.name.toLowerCase().includes(keyword))

display(filtered)

}

function deleteStudent(index){

fetch("/delete/"+index,{method:"DELETE"})
.then(res=>res.json())
.then(data=>{
location.reload()
})

}

function editStudent(index){

let name=prompt("New Name")
let grade=prompt("New Grade")
let section=prompt("New Section")

fetch("/edit/"+index,{
method:"PUT",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({name:name,grade:grade,section:section})
})
.then(res=>res.json())
.then(data=>{
location.reload()
})

}

function goDashboard(){
window.location="/dashboard"
}

function goForm(){
window.location="/form"
}

</script>

</body>
</html>
""")

# -----------------------------
# API
# -----------------------------
@app.route("/student", methods=["GET","POST"])
def student():

    if request.method=="POST":
        students.append(request.json)
        return jsonify({"message":"saved"})

    return jsonify(students)


@app.route("/delete/<int:index>", methods=["DELETE"])
def delete_student(index):

    if index<len(students):
        students.pop(index)

    return jsonify({"message":"deleted"})


@app.route("/edit/<int:index>", methods=["PUT"])
def edit_student(index):

    if index<len(students):
        students[index]=request.json

    return jsonify({"message":"updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
