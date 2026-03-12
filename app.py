from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Grade Analyzer Dashboard</title>

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
}

.container{
width:400px;
padding:40px;
border-radius:20px;
background:rgba(255,255,255,0.15);
backdrop-filter:blur(10px);
box-shadow:0 8px 32px rgba(0,0,0,0.2);
text-align:center;
color:white;
}

h1{
margin-bottom:20px;
}

input{
width:100%;
padding:12px;
margin:10px 0;
border:none;
border-radius:8px;
outline:none;
font-size:16px;
}

button{
width:100%;
padding:12px;
margin-top:10px;
border:none;
border-radius:8px;
background:#00e1ff;
color:black;
font-weight:bold;
cursor:pointer;
transition:0.3s;
}

button:hover{
background:#00bcd4;
}

.result{
margin-top:20px;
font-size:20px;
font-weight:bold;
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

<h1>🎓 Grade Analyzer</h1>

<input type="number" id="score" placeholder="Enter your score">

<button onclick="checkGrade()">Check Grade</button>

<div class="result" id="result"></div>

<div class="footer">
API Powered by Flask
</div>

</div>

<script>

function checkGrade(){

let score = document.getElementById("score").value;

fetch("/grade?score=" + score)

.then(response => response.json())

.then(data => {

document.getElementById("result").innerHTML =
"Score: " + data.score + "<br>Grade: " + data.grade;

});

}

</script>

</body>
</html>
""")

@app.route("/grade")
def grade():

    score = int(request.args.get("score"))

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    return jsonify({
        "score": score,
        "grade": grade
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
