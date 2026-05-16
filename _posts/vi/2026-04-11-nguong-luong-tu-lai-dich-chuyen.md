---
title: 'Ngưỡng lượng tử lại dịch chuyển'
subtitle: 'Shor có thể chạy trên 10.000 qubit — và điều đó thay đổi mọi thứ'
description: 'Một bài báo mới cho rằng thuật toán Shor có thể chạy với chỉ 10.000 qubit. Ngưỡng cho tính toán lượng tử liên quan đến mật mã đang giảm nhanh.'
date: 'April 11, 2026'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/quantum-thresholds-banner.webp'
banner_alt: 'Sơ đồ qubit và ngưỡng phá vỡ mật mã'
keywords: 'Shor, qubit, lượng tử, mật mã, RSA, hậu lượng tử, ngưỡng, 10000 qubit, Fujitsu, Riken'
---

![Ngưỡng lượng tử](https://cloudcdn.pro/stocks/images/quantum-thresholds-banner.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Một bài báo nghiên cứu năm 2026 cho rằng thuật toán Shor có thể chạy với chỉ 10.000 qubit nguyên tử trung tính có thể tái cấu hình — không phải các triệu qubit đã được giả định trong nhiều năm. Ngưỡng cho lượng tử liên quan đến mật mã đang giảm nhanh, và lộ trình PQC phải tăng tốc.
>
> **Điểm chính**
>
> - **Cách tiếp cận.** Các nguyên tử trung tính có thể tái cấu hình cho phép cánh cửa hai-qubit có tính kết nối cao.
> - **Phát hiện.** RSA-2048 có thể bị phá vỡ với 10.000 qubit logic — giảm 100x so với ước tính trước đó.
> - **Tác động.** Lộ trình PQC phải tăng tốc; mục tiêu 2030 không còn an toàn.
> - **Triển vọng.** Fujitsu và Riken đang xây dựng máy 10.000 qubit cho năm 2026; PsiQuantum nhắm vào triệu qubit vào 2027.

## Bối cảnh

### Lịch sử của các ước tính

Các ước tính sớm cho việc phá vỡ RSA-2048:

- **2012.** ~1 tỉ qubit (Beauregard).
- **2017.** ~20 triệu qubit (Gidney, Ekerå).
- **2021.** ~3 triệu qubit (các tối ưu hoá tiếp theo).
- **2024.** ~1 triệu qubit (Roetteler et al.).
- **2026.** ~10.000 qubit logic (bài báo mới).

Mỗi lần, các nhà nghiên cứu tìm ra các tối ưu hoá thuật toán hoặc kiến trúc làm giảm yêu cầu phần cứng.

## Bài báo mới

### Nguyên tử trung tính tái cấu hình

Bước đột phá năm 2026 đến từ sự kết hợp:

1. **Các nguyên tử trung tính** (như Ru hoặc Cs) được giữ trong các bẫy quang học.
2. **Khả năng tái cấu hình** vị trí của các nguyên tử trong quá trình tính toán.
3. **Cánh cửa hai-qubit chính xác cao** giữa các nguyên tử lân cận.

Khả năng tái cấu hình thay đổi cuộc chơi: thay vì cần một mạng cố định 2D với các kết nối giới hạn, các thuật toán có thể di chuyển các qubit để chúng tương tác trực tiếp, giảm đáng kể số lượng cánh cửa cần thiết.

## Tác động đến thuật toán Shor

### Tối ưu hoá

Thuật toán Shor cho RSA-2048 yêu cầu:

- **Số học modular** trên các số 2048-bit.
- **Biến đổi Fourier lượng tử** (QFT).
- **Sửa lỗi** cho các cánh cửa logic.

Bằng cách tận dụng tái cấu hình, các tác giả cho thấy rằng số qubit logic có thể giảm xuống còn vài nghìn — một cải thiện cấp độ.

## Phần cứng hiện tại

### Trạng thái 2026

- **Fujitsu + Riken.** Đang xây dựng một máy 10.000 qubit nguyên tử trung tính, dự kiến hoạt động vào cuối năm 2026.
- **QuEra.** Đã chứng minh các bộ xử lý 256 qubit với khả năng tái cấu hình.
- **Atom Computing.** Bộ xử lý 1.000 qubit đang được phát triển.
- **PsiQuantum.** Nhắm vào triệu qubit quang tử vào năm 2027-2028.

## Ý nghĩa với thanh toán

### Thời gian biểu thay đổi

Trước năm 2026, các ngân hàng dự kiến mối đe doạ lượng tử "vào cuối thập kỷ 2030". Với phát hiện mới:

- **2028-2030** trở thành một khung thời gian thực tế.
- **Thu thập ngay, giải mã sau** trở nên cấp bách hơn nữa.
- **Lộ trình PQC** phải được tăng tốc đáng kể.

### Hành động ngay

- **Thí điểm PQC** trong các môi trường sản xuất, không chỉ kiểm thử.
- **Loại bỏ RSA** cho các giao thức mới (chuyển sang Kyber + ECDH hybrid).
- **Đánh giá tài sản dài hạn** (hợp đồng 20 năm, hồ sơ pháp lý) cho rủi ro thu thập-trước.

## Triển vọng

### G7 và quy định

Tháng 1 năm 2026, G7 đã công bố một lộ trình chuyển đổi PQC chia sẻ. BIS Project Leap đã chứng minh khả năng tích hợp PQC vào các hệ thống thanh toán trực tiếp. Áp lực quy định đang tăng lên.

## Kết luận

Ngưỡng cho tính toán lượng tử liên quan đến mật mã không phải là một con số cố định — nó đang chuyển động xuống. Các tổ chức không tăng tốc lộ trình PQC năm 2026 có thể thấy mình thiếu chuẩn bị vào năm 2030. Thời gian an toàn không còn là một thập kỷ.
