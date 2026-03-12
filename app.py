from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Store multiple students
students = []

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Student API Dashboard</title>

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:Segoe UI;
}

body{
height:100vh;
display:flex;
justify-content:center;
align-items:center;
background:linear-gradient(135deg,#667eea,#764ba2);
color:white;
}

.container{
width:420px;
padding:35px;
border-radius:20px;
background:rgba(255,255,255,0.15);
backdrop-filter:blur(10px);
box-shadow:0 10px 40px rgba(0,0,0,0.3);
text-align:center;
}

h1{
margin-bottom:15px;
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
border:none;
border-radius:8px;
background:#00e1ff;
color:black;
font-weight:bold;
cursor:pointer;
margin-top:10px;
}

button:hover{
background:#00bcd4;
}

.footer{
margin-top:15px;
font-size:12px;
opacity:0.7;
}

</style>

</head>

<body>

<div class="container">

<h1>🎓 Student Dashboard</h1>

<input id="name" placeholder="Student Name">
<input id="grade" placeholder="Grade">
<input id="section" placeholder="Section">

<button onclick="saveStudent()">Save Student</button>

<button onclick="viewStudents()">View All Students</button>

<div class="footer">
Flask API Project
</div>

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

</script>

</body>
</html>
""")

@app.route("/students")
def students_page():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Saved Students</title>

<style>

body{
font-family:Segoe UI;
background:linear-gradient(135deg,#667eea,#764ba2);
padding:40px;
color:white;
text-align:center;
}

h1{
margin-bottom:30px;
}

.grid{
display:grid;
grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
gap:20px;
}

.card{
background:rgba(255,255,255,0.2);
padding:20px;
border-radius:12px;
backdrop-filter:blur(8px);
}

button{
margin-top:30px;
padding:10px 20px;
border:none;
border-radius:8px;
background:#00e1ff;
cursor:pointer;
font-weight:bold;
}

</style>

</head>

<body>

<h1>📚 Saved Students</h1>

<div class="grid" id="students"></div>

<button onclick="goBack()">⬅ Back to Home</button>

<script>

fetch("/student")
.then(res=>res.json())
.then(data=>{

let container=document.getElementById("students")

data.forEach(student=>{

container.innerHTML+=
"<div class='card'>"+
"<h3>"+student.name+"</h3>"+
"<p>Grade: "+student.grade+"</p>"+
"<p>Section: "+student.section+"</p>"+
"</div>"

})

})

function goBack(){
window.location="/"
}

</script>

</body>
</html>
""")

@app.route("/student", methods=["GET","POST"])
def student():

    global students

    if request.method == "POST":
        data = request.json
        students.append(data)
        return jsonify({"message":"Student saved","students":students})

    return jsonify(students)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
