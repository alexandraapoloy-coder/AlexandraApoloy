from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Temporary storage
student_data = {
    "name": "Alexa",
    "grade": 10,
    "section": "Zechariah"
}

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

.card{
margin-top:20px;
padding:15px;
border-radius:10px;
background:rgba(255,255,255,0.25);
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
<button onclick="loadStudent()">Load Student</button>

<div class="card" id="result">
Student info will appear here
</div>

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
document.getElementById("result").innerHTML="Student Saved ✅"
})

}

function loadStudent(){

fetch("/student")
.then(res=>res.json())
.then(data=>{

document.getElementById("result").innerHTML=
"<h3>"+data.name+"</h3>"+
"Grade: "+data.grade+"<br>"+
"Section: "+data.section

})

}

</script>

</body>
</html>
""")

@app.route("/student", methods=["GET","POST"])
def student():

    global student_data

    if request.method == "POST":
        student_data = request.json
        return jsonify({"message":"Student saved","data":student_data})

    return jsonify(student_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
