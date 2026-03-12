from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Simple UI Page
@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Grade Calculator</title>
        <style>
            body{
                font-family: Arial;
                background: linear-gradient(135deg,#4facfe,#00f2fe);
                height:100vh;
                display:flex;
                align-items:center;
                justify-content:center;
            }
            .card{
                background:white;
                padding:30px;
                border-radius:12px;
                width:320px;
                box-shadow:0 10px 25px rgba(0,0,0,0.2);
                text-align:center;
            }
            h2{margin-bottom:20px;}
            input{
                width:90%;
                padding:10px;
                margin:8px 0;
                border-radius:6px;
                border:1px solid #ccc;
            }
            button{
                background:#4facfe;
                color:white;
                border:none;
                padding:10px 15px;
                border-radius:6px;
                cursor:pointer;
                margin-top:10px;
            }
            button:hover{
                background:#007bff;
            }
            #result{
                margin-top:15px;
                font-weight:bold;
                color:#333;
            }
        </style>
    </head>
    <body>

        <div class="card">
            <h2>Grade Calculator</h2>

            <input type="number" id="score" placeholder="Enter Score">

            <br>
            <button onclick="getGrade()">Check Grade</button>

            <div id="result"></div>
        </div>

    <script>
    function getGrade(){
        let score = document.getElementById("score").value;

        fetch("/grade?score=" + score)
        .then(response => response.json())
        .then(data => {
            document.getElementById("result").innerHTML =
                "Grade: " + data.grade;
        });
    }
    </script>

    </body>
    </html>
    """)

# API Endpoint
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
