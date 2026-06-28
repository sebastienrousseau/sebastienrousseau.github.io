---
title: 'Lỗi được phát hiện trong thuật toán lượng tử cho mật mã dựa trên mạng tinh thể'
subtitle: 'Cộng đồng mật mã phục hồi sau lo lắng Chen-LWE'
description: 'Một lỗi đã được phát hiện trong thuật toán lượng tử của Yilei Chen cho LWE, tạm thời bảo vệ mật mã dựa trên mạng tinh thể và nhấn mạnh nhu cầu nghiên cứu liên tục.'
date: 'April 22, 2024'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp'
banner_alt: 'Mạng tinh thể an toàn với khoá mật mã'
keywords: 'LWE, mạng tinh thể, mật mã, Chen, Kyber, PQC, hậu lượng tử, an toàn'
---

![Mạng tinh thể an toàn](https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Một tuần sau khi Yilei Chen công bố một thuật toán lượng tử có khả năng phá vỡ Lattice-LWE, các nhà mật mã đã tìm thấy một lỗi nghiêm trọng. Tuyên bố đã được rút lại; CRYSTALS-Kyber an toàn — bây giờ.
>
> **Điểm chính**
>
> - **Cách tiếp cận.** Đánh giá đồng cấp khẩn cấp của bài báo Chen từ các chuyên gia hàng đầu.
> - **Kết quả.** Một lỗi trong các bằng chứng đã được tìm thấy nhanh chóng.
> - **Tác động.** Tin cậy vào Lattice-LWE và Kyber được phục hồi tạm thời.
> - **Bài học.** Nhu cầu liên tục cho nghiên cứu, tính đa dạng và linh hoạt mật mã.

## Câu chuyện

### Tuần lo lắng

Vào ngày 10 tháng 4 năm 2024, Yilei Chen của Tsinghua University đã đăng tải một bản thảo trên IACR ePrint, tuyên bố một thuật toán lượng tử thời gian đa thức cho Lattice-LWE. Cộng đồng mật mã đã bùng nổ:

- **Cuộc tranh luận trên Twitter** giữa các chuyên gia hàng đầu.
- **Phân tích khẩn cấp** bởi các nhóm tại NIST, MIT, Stanford.
- **Câu hỏi từ ngành công nghiệp** về việc liệu lộ trình PQC có cần đánh giá lại.

### Phát hiện lỗi

Sau một tuần kiểm tra cẩn thận, các nhà mật mã — bao gồm Hongxun Wu (Berkeley) và những người khác — đã tìm thấy một lỗi trong các bằng chứng của Chen. Cụ thể, một bước trong các phân tích lấy mẫu Gaussian phụ thuộc vào một giả định không được biện minh.

Vào ngày 18 tháng 4, Chen đã thừa nhận lỗi và rút lại tuyên bố.

## Phản ứng

### Sự phục hồi của cộng đồng

Sự kiện đã minh hoạ điểm mạnh của khoa học mở trong mật mã:

- **Xem xét nhanh.** Trong vòng một tuần, lỗi đã được phát hiện.
- **Đối thoại lành mạnh.** Chen đã hợp tác với các nhà phê bình thay vì phòng thủ.
- **Tin cậy được phục hồi.** Cộng đồng quay lại với sự tự tin (tạm thời) vào Lattice-LWE.

## Bài học rộng hơn

### Nhu cầu liên tục cho nghiên cứu

Sự kiện này không có nghĩa là Lattice-LWE an toàn vĩnh viễn. Nó chỉ có nghĩa là cuộc tấn công cụ thể này không hoạt động. Các điểm cần lưu ý:

1. **Mật mã là một mục tiêu di động.** Các thuật toán mới có thể được phát hiện bất cứ lúc nào.
2. **Sự đa dạng quan trọng.** NIST đang chuẩn hoá các họ PQC khác nhau một phần để phòng vệ chiều sâu.
3. **Tính linh hoạt mật mã là chìa khoá.** Các tổ chức cần khả năng hoán đổi thuật toán nhanh chóng.
4. **Khoa học mở hoạt động.** Đăng tải sớm, xem xét sớm, sửa chữa sớm.

## Tác động với ngân hàng

### Hành động

Các ngân hàng triển khai PQC nên:

1. **Tiếp tục triển khai Kyber** — nó vẫn an toàn theo hiểu biết hiện tại.
2. **Sử dụng các sơ đồ hybrid** kết hợp Kyber với các giải pháp thay thế (ví dụ: McEliece dựa trên mã).
3. **Xây dựng tính linh hoạt mật mã** — đảm bảo các giao thức có thể đàm phán các bộ mật mã.
4. **Theo dõi nghiên cứu** thường xuyên, không phải hàng năm.

## Triển vọng

### NIST đang tiếp tục

NIST tiếp tục các vòng tiêu chuẩn hoá bổ sung. Vòng 4 đánh giá các sơ đồ KEM dựa trên mã (Classic McEliece, BIKE, HQC) là các phương án thay thế cho Kyber. Việc chuẩn hoá thêm một sơ đồ không dựa trên lattice sẽ cung cấp phòng vệ chiều sâu.

## Kết luận

Cảnh báo Chen-LWE là một bài tập về sự khiêm tốn cho ngành mật mã. Ngay cả các tiêu chuẩn mới nhất, được phân tích cẩn thận nhất cũng có thể bị thách thức. May mắn thay, cộng đồng mật mã đã đáp ứng nhanh chóng. Đối với các ngân hàng, bài học là: triển khai PQC bây giờ, nhưng xây dựng linh hoạt cho ngày mai.
