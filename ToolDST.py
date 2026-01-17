import fitz  # PyMuPDF
import os

def xu_ly_pdf_tong_hop():
    input_folder = os.getcwd()
    output_folder = os.path.join(input_folder, "KET_QUA_CUOI_CUNG")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    # Sắp xếp để file A4 được đánh số trước
    files.sort(key=lambda x: "(A4)" not in x)

    page_counter = 1
    blue = (0, 0, 1)

    for filename in files:
        doc = fitz.open(os.path.join(input_folder, filename))
        is_a4_file = "(A4)" in filename
        
        for page in doc:
            # 1. XỬ LÝ XOAY (Chỉ áp dụng cho file A4)
            # Nếu là file A4 và đang nằm ngang -> Xoay ngược chiều kim đồng hồ (90 độ)
            if is_a4_file and page.rect.width > page.rect.height:
                page.set_rotation((page.rotation + 90) % 360)
            
            # Lấy lại thông số trang sau khi xoay
            rect = page.rect
            w, h = rect.width, rect.height

            # 2. LOGIC NHẬN DIỆN SIZE VÀ ĐẶT VỊ TRÍ (A, B, C)
            # A4 chuẩn: ~595x842 | A3 chuẩn: ~842x1191
            
            if w < 600 and h > 800:  # Khổ A4 Dọc (Vị trí A)
                pos = fitz.Point(w - 60, h - 35)
                f_size = 11
            elif w < 900 and h > 1100:  # Khổ A3 Dọc (Vị trí B)
                pos = fitz.Point(w - 80, h - 45)
                f_size = 13
            elif w > 1100 and w > h:  # Khổ A3 Ngang (Vị trí C)
                pos = fitz.Point(w - 120, h - 60)
                f_size = 14
            else:  # Khổ bất kỳ hoặc bản vẽ lớn A2, A1, A0 (Vị trí D)
                # Tự động tính: Cách lề phải 5%, lề dưới 3%
                pos = fitz.Point(w * 0.94, h * 0.97)
                f_size = h * 0.015  # Font chiếm 1.5% chiều cao trang

            # 3. GHI SỐ TRANG
            page.insert_text(
                pos,
                f"Page {page_counter}",
                fontsize=f_size,
                fontname="helv",
                color=blue,
                align=fitz.TEXT_ALIGN_RIGHT,
                overlay=True
            )
            page_counter += 1

        doc.save(os.path.join(output_folder, f"Fixed_{filename}"))
        doc.close()
        print(f"Xong file: {filename}")

if __name__ == "__main__":
    xu_ly_pdf_tong_hop()
