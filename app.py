import re
import random
import unicodedata
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==========================================
# ĐƯỜNG DẪN AVATAR VÀ ẢNH NỀN GIA ĐÌNH
# ==========================================
AVATAR_MAP = {
    "me": "/static/avatars/me.jpg",
    "di": "/static/avatars/di.jpg",
    "bac": "/static/avatars/bac.jpg",
    "ba": "/static/avatars/ba.jpg",
    "em": "/static/avatars/em.jpg"
}

DEFAULT_BG_URL = "/static/backgrounds/family_bg.jpg"

def remove_accents(input_str):
    """Hàm loại bỏ toàn bộ dấu tiếng Việt và chuyển thành chữ thường để so sánh chính xác 100%"""
    if not input_str:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower().strip()

# ==========================================
# DANH SÁCH LỜI CHÚC DÀNH RIÊNG CHO MẸ, DÌ, BÁC, BÀ, EM GÁI
# ==========================================
WISHES_ME_THAO = [
    "Gửi Mẹ Ngô Thị Thảo yêu thương nhân ngày Phụ nữ Việt Nam 20/10!\n\n"
    "Con chúc Mẹ luôn xinh đẹp, trẻ trung, dồi dào sức khỏe và luôn tràn ngập nụ cười trên môi. "
    "Cảm ơn Mẹ vì những vất vả, hi sinh thầm lặng và tình yêu thương vô bờ bến Mẹ đã dành cho con. Mong Mẹ luôn hạnh phúc mỗi ngày! 💐❤️\n\n"
    "From: Con trai quang minh 💫",

    "Chúc mừng ngày 20/10 gửi tới Mẹ Ngô Thị Thảo - người Mẹ tuyệt vời nhất trên đời!\n\n"
    "Nhân ngày Phụ nữ Việt Nam, con mong Mẹ luôn vạn sự như ý, bớt đi những lo toan vất vả và lúc nào cũng bình an, vui vẻ. "
    "Con yêu Mẹ thật nhiều! 🌹✨\n\n"
    "From: Con trai quang minh 💫",

    "Kính gửi Mẹ Thảo nhân dịp đặc biệt 20/10!\n\n"
    "Chúc Mẹ mỗi ngày trôi qua đều là một ngày thật nhiều niềm vui, luôn giữ trọn ngọn lửa ấm áp cho gia đình mình. "
    "Con hứa sẽ luôn cố gắng học tập và trưởng thành để Mẹ luôn tự hào! 💕🌸\n\n"
    "From: Con trai quang minh 💫"
]

WISHES_DI_THANH = [
    "Gửi Dì Ngô Thị Thanh yêu quý nhân ngày 20/10!\n\n"
    "Cháu chúc Dì ngày càng trẻ trung, xinh đẹp, luôn giữ trọn ngọn lửa năng lượng tích cực và thành công trong mọi dự định. "
    "Chúc Dì có một ngày 20/10 ngập tràn hoa, quà và những lời chúc ngọt ngào nhất! 💐✨\n\n"
    "From: Cháu minh 💫",

    "Chúc mừng ngày Phụ nữ Việt Nam 20/10 gửi tới Dì Ngô Thị Thanh!\n\n"
    "Cảm ơn Dì vì đã luôn dịu dàng, tâm lý và mang đến nhiều niềm vui cho cả nhà. "
    "Cháu chúc Dì luôn hạnh phúc, bình an và vạn sự như ý! 💕🌸\n\n"
    "From: Cháu minh💫"
]

WISHES_BAC_LUA = [
    "Kính gửi Bác Ngô Thị Lụa nhân ngày Phụ nữ Việt Nam 20/10!\n\n"
    "Cháu chúc Bác luôn luôn dồi dào sức khỏe, gia đình êm ấm, hạnh phúc và gặp thật nhiều may mắn trong cuộc sống. "
    "Cảm ơn Bác đã luôn quan tâm, yêu thương và chỉ bảo chúng cháu! 🌸💖\n\n"
    "From: Cháu Đắc Việt Dũng 💫",

    "Chúc mừng ngày 20/10 gửi tới Bác Ngô Thị Lụa!\n\n"
    "Nhân ngày Phụ nữ Việt Nam, cháu chúc Bác luôn trẻ trung, tươi tắn, công việc suôn sẻ và luôn tràn ngập tiếng cười trong ngôi nhà của mình! ✨🌷\n\n"
    "From: Cháu minh 💫"
]

WISHES_BA_NHAN = [
    "Kính gửi Bà Trần Thị Nhàn kính yêu nhân ngày 20/10!\n\n"
    "Cháu chúc Bà luôn thật nhiều sức khỏe, bình an, tâm hồn luôn vui vẻ và sống thật lâu bên con cháu. "
    "Cảm ơn Bà đã luôn yêu thương, bao bọc và dành những điều tốt đẹp nhất cho cả gia đình mình! 👵🌸\n\n"
    "From: Cháu minh 💖",
    
    "Chúc mừng ngày Phụ nữ Việt Nam 20/10 gửi tới Bà Trần Thị Nhàn!\n\n"
    "Nhân ngày đặc biệt hôm nay, cháu kính chúc Bà luôn mạnh khỏe, mỉm cười mỗi ngày và có thật nhiều niềm vui. "
    "Bà chính là điểm tựa ấm áp nhất của cả gia đình mình! ✨❤️\n\n"
    "From: Cháu minh 💖"
]

WISHES_EM_LINH = [
    "Gửi em gái Lê Phương Linh nhân ngày Phụ nữ Việt Nam 20/10!\n\n"
    "Anh chúc em gái luôn xinh đẹp, đáng yêu, chăm ngoan học giỏi và luôn tràn đầy năng lượng tích cực. "
    "Chúc em ngày 20/10 nhận được thật nhiều quà, luôn mỉm cười rạng rỡ và đạt được mọi ước mơ của mình nhé! 🎀✨\n\n"
    "From: Anh minh 💫",

    "Chúc mừng ngày 20/10 gửi tới cô em gái Lê Phương Linh!\n\n"
    "Chúc em ngày càng lớn khôn, thông minh, học tập ngày càng tiến bộ và luôn là niềm tự hào của cả gia đình. "
    "Có gì vướng bận hay khó khăn cứ bảo anh nhé! Chúc em luôn vui tươi và hạnh phúc! 🌸💖\n\n"
    "From: Anh minh 💫"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-card', methods=['POST'])
def get_card():
    data = request.get_json()
    input_name = data.get('name', '').strip()
    
    if not input_name:
        return jsonify({'success': False, 'message': 'Vui lòng nhập tên người nhận nhé!'}), 400

    clean_name = remove_accents(input_name)

    # ==========================================
    # NHẬN DIỆN THÔNG MINH VÀ PHÂN LOẠI AVATAR
    # ==========================================
    
    # 1. MẸ NGÔ THỊ THẢO
    if any(k in clean_name for k in ["ngo thi thao", "thi thao", "thao", "me thao", "me"]):
        display_name = "Mẹ Ngô Thị Thảo"
        wishes = random.choice(WISHES_ME_THAO)
        avatar_url = AVATAR_MAP["me"]

    # 2. DÌ NGÔ THỊ THANH
    elif any(k in clean_name for k in ["ngo thi thanh", "thi thanh", "thanh", "di thanh", "di"]):
        display_name = "Dì Ngô Thị Thanh"
        wishes = random.choice(WISHES_DI_THANH)
        avatar_url = AVATAR_MAP["di"]

    # 3. BÁC NGÔ THỊ LỤA
    elif any(k in clean_name for k in ["ngo thi lua", "thi lua", "lua", "bac lua", "bac"]):
        display_name = "Bác Ngô Thị Lụa"
        wishes = random.choice(WISHES_BAC_LUA)
        avatar_url = AVATAR_MAP["bac"]

    # 4. BÀ TRẦN THỊ NHÀN
    elif any(k in clean_name for k in ["tran thi nhan", "thi nhan", "nhan", "ba nhan", "ba"]):
        display_name = "Bà Trần Thị Nhàn"
        wishes = random.choice(WISHES_BA_NHAN)
        avatar_url = AVATAR_MAP["ba"]

    # 5. EM GÁI LÊ PHƯƠNG LINH
    elif any(k in clean_name for k in ["le phuong linh", "phuong linh", "linh", "em linh", "em gai"]):
        display_name = "Em Gái Lê Phương Linh"
        wishes = random.choice(WISHES_EM_LINH)
        avatar_url = AVATAR_MAP["em"]

    else:
        return jsonify({
            'success': False,
            'message': 'ai vậy??? ❤️'
        })

    return jsonify({
        'success': True,
        'name': display_name,
        'image_url': avatar_url,
        'bg_url': DEFAULT_BG_URL,
        'wishes': wishes
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)