from flask import Flask, render_template, request
from sklearn.linear_model import LogisticRegression
print('phạm gia khiêm')    
app = Flask(__name__)

# Dữ liệu huấn luyện
# Mở rộng tập dữ liệu X (Cân nặng, Chiều cao) chuẩn theo các mốc BMI
X = [[16.0], [17.5], [18.4], [18.5], [21.0], [22.9], [23.0], [26.0], [30.0]]
y = ["Gầy", "Gầy", "Gầy", "Cân đối", "Cân đối", "Cân đối", "Thừa cân", "Thừa cân", "Thừa cân"]

model = LogisticRegression()
model.fit(X, y)


# Tạo và huấn luyện AI
model = LogisticRegression()
model.fit(X, y)

@app.route("/", methods=["GET", "POST"])
def home():
    BODY_result = None
    BMI_result = None
    if request.method == "POST":
        user_name = request.form["name"]
        weight = float(request.form["weight"])
        height = float(request.form["height"])

       
        height_m=height/100
        bmi=weight/height_m**2
        # Mảng chứa các mốc ranh giới chuẩn BMI [Gầy, Cân đối, Thừa cân]
        # Các mốc: < 18.5 (Gầy), 18.5 - 22.9 (Cân đối), >= 23 (Béo/Lớn)
        prediction = model.predict([[bmi]])[0]
        bmi_thresholds = [18.5, 23.0]

        # Sau khi tính xong bmi = weight / (height_m ** 2)
        if bmi < bmi_thresholds[0]:
            danh_gia = " thiếu cân"
        elif bmi < bmi_thresholds[1]:
            danh_gia = " Cân đối"
        else:
            danh_gia = " Thừa cân"

        BODY_result = f"{user_name}'s BODY: {prediction}"
        BMI_result = f"{user_name}'s BMI: {round(bmi,1)}  ({danh_gia})"
       

    return render_template("index.html", BODY_result=BODY_result,BMI_result=BMI_result)

if __name__ == "__main__":
    app.run(debug=True)

