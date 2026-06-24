---
title: 'Hiểu về công nghệ đằng sau blockchain'
subtitle: 'Mật mã, đồng thuận và sổ cái phân tán — các khối xây dựng của tin cậy số'
description: 'Cách blockchain hoạt động: băm mật mã, cây Merkle, cơ chế đồng thuận và mô hình kinh tế đảm bảo tính bất biến.'
date: 'January 9, 2018'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/digital-nodes.webp'
banner_alt: 'Sơ đồ kỹ thuật của một sổ cái phân tán với các khối được liên kết'
keywords: 'blockchain, băm mật mã, cây Merkle, đồng thuận, proof-of-work, sổ cái phân tán, mật mã, tài chính'
---

![Sơ đồ kỹ thuật của một sổ cái phân tán](https://cloudcdn.pro/stocks/images/digital-nodes.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Blockchain dựa trên ba khối xây dựng kỹ thuật: hàm băm mật mã, cây Merkle để tổng hợp giao dịch và cơ chế đồng thuận để các nút phân tán đồng ý về trạng thái sổ cái.
>
> **Điểm chính**
>
> - **Cách tiếp cận.** Các giao dịch được nhóm thành khối, được băm và liên kết với khối trước bằng con trỏ băm.
> - **Bối cảnh.** Hàm băm SHA-256 và mật mã khoá công khai tạo ra tính bất biến và xác thực không cần tin cậy.
> - **Phương pháp.** Proof-of-work, proof-of-stake và các biến thể giải quyết bài toán đồng thuận giữa các nút không tin cậy lẫn nhau.
> - **Triển vọng.** Sự hiểu biết về các nguyên thuỷ này là điều kiện tiên quyết để đánh giá các thiết kế blockchain mới một cách có hiểu biết.

## Phân tích

### Vì sao kiến trúc kỹ thuật quan trọng

Nhiều người nói về blockchain nhưng ít người hiểu các cơ chế bên dưới. Bài viết này giải thích các thành phần cốt lõi: cách các khối được liên kết, cách các giao dịch được xác thực và cách các nút đạt đến đồng thuận mà không cần một bên trung gian tin cậy.

## Băm mật mã

### Nền tảng của tính bất biến

Một hàm băm mật mã như SHA-256 lấy một đầu vào có độ dài tuỳ ý và tạo ra một đầu ra cố định 256 bit. Ba thuộc tính quan trọng:

1. **Tính một chiều.** Không thể tính ngược đầu vào từ đầu ra.
2. **Kháng va chạm.** Không thể tìm hai đầu vào khác nhau cho cùng một đầu ra.
3. **Hiệu ứng tuyết lở.** Thay đổi một bit của đầu vào thay đổi hoàn toàn đầu ra.

Mỗi khối trong blockchain chứa băm của khối trước, tạo thành một chuỗi liên kết. Sửa đổi bất kỳ khối nào sẽ phá vỡ chuỗi và bị mạng phát hiện ngay lập tức.

## Cây Merkle

### Tổng hợp giao dịch hiệu quả

Trong một khối có hàng nghìn giao dịch, không thực tế khi băm tất cả cùng nhau. Cây Merkle giải quyết điều này: các giao dịch được băm theo cặp, sau đó các băm cặp được băm lại, lặp đi lặp lại cho đến khi chỉ còn một băm gốc Merkle duy nhất. Băm gốc này được lưu trong tiêu đề khối, cho phép xác minh nhanh chóng một giao dịch riêng lẻ thuộc về khối nào.

## Đồng thuận

### Đồng ý về trạng thái sổ cái

Đây là vấn đề khó nhất. Trong một mạng phân tán không có trung gian tin cậy, làm thế nào các nút đồng ý về thứ tự và tính hợp lệ của các giao dịch?

- **Proof-of-Work (PoW).** Thợ đào cạnh tranh giải một câu đố tính toán đắt đỏ. Người thắng đề xuất khối tiếp theo và nhận phần thưởng. Bitcoin sử dụng PoW.
- **Proof-of-Stake (PoS).** Các trình xác thực được chọn ngẫu nhiên dựa trên lượng cổ phần họ nắm giữ. Tiết kiệm năng lượng hơn nhiều so với PoW. Ethereum đã chuyển sang PoS năm 2022.
- **Các biến thể.** Practical Byzantine Fault Tolerance (PBFT), Proof-of-Authority (PoA), Delegated Proof-of-Stake (DPoS) — mỗi cái cân nhắc khác nhau giữa phi tập trung, hiệu suất và bảo mật.

## Mật mã khoá công khai

### Sở hữu và uỷ quyền

Mỗi người dùng sở hữu một cặp khoá: khoá công khai (địa chỉ ví) và khoá riêng (chữ ký). Khoá riêng được dùng để ký giao dịch; khoá công khai xác minh chữ ký mà không tiết lộ khoá riêng. Mất khoá riêng đồng nghĩa với mất tài sản — không có cơ chế khôi phục trung tâm.

## Kết luận

Blockchain không phải là phép màu. Đó là sự kết hợp tinh tế của các nguyên thuỷ mật mã đã biết, được kết nối theo cách tạo ra một sổ cái không thể sửa đổi mà không cần bên trung gian tin cậy. Hiểu các thành phần này giúp đánh giá các thiết kế mới một cách có hiểu biết — và phân biệt sự đổi mới thực sự với tiếp thị.
