document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("bmiForm");
    const weightInput = document.getElementById("weight");
    const heightInput = document.getElementById("height");

    // Kiểm tra dữ liệu hợp lệ trước khi gửi form
    form.addEventListener("submit", function (event) {
        const weight = parseFloat(weightInput.value);
        const height = parseFloat(heightInput.value);

        if (weight <= 0 || weight > 300) {
            alert("Vui lòng nhập cân nặng hợp lệ (1 - 300 kg)!");
            event.preventDefault();
            return;
        }

        if (height <= 0 || height > 250) {
            alert("Vui lòng nhập chiều cao hợp lệ (1 - 250 cm)!");
            event.preventDefault();
            return;
        }
    });

    // Tạo hiệu ứng lắc nhẹ khung kết quả nếu có kết quả hiển thị
    const resultBox = document.getElementById("resultContainer");
    if (resultBox) {
        resultBox.style.opacity = "0";
        resultBox.style.transform = "translateY(10px)";
        resultBox.style.transition = "all 0.5s ease-out";

        setTimeout(() => {
            resultBox.style.opacity = "1";
            resultBox.style.transform = "translateY(0)";
        }, 100);
    }
});