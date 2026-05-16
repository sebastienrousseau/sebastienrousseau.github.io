---
title: 'CRYSTALS-Kyber: thuật toán bảo vệ trong thời lượng tử'
subtitle: 'Tiêu chuẩn NIST FIPS 203 cho đóng gói khoá hậu lượng tử'
description: 'CRYSTALS-Kyber là thuật toán đóng gói khoá kháng lượng tử được NIST lựa chọn. Cách thức hoạt động, vì sao nó quan trọng, và cách nó định hình lại mật mã.'
date: 'November 19, 2023'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/kyber-banner.webp'
banner_alt: 'Sơ đồ trừu tượng của mạng tinh thể'
keywords: 'CRYSTALS-Kyber, NIST, FIPS 203, hậu lượng tử, mật mã, KEM, mạng tinh thể, ML-KEM'
---

![Mạng tinh thể](https://cloudcdn.pro/stocks/images/kyber-banner.webp).class=\"img-fluid clearfix\"

> **TL;DR.** CRYSTALS-Kyber (được tiêu chuẩn hoá thành ML-KEM trong FIPS 203) là cơ chế đóng gói khoá kháng lượng tử đầu tiên được NIST chuẩn hoá. Nó là sự thay thế cho việc trao đổi khoá RSA và Diffie-Hellman trong kỷ nguyên hậu lượng tử.
>
> **Điểm chính**
>
> - **Ý tưởng.** Dựa trên bài toán Module-LWE — khó cả với máy tính lượng tử.
> - **Đổi mới.** Nhanh, kích thước khoá hợp lý (1.184 byte cho Kyber-768).
> - **Tác động.** Thay thế cho RSA/ECDH trong TLS, SSH, VPN, các giao thức thanh toán.
> - **Lộ trình.** Đã được Cloudflare, Google, Apple áp dụng vào năm 2023-2024.

## Bối cảnh

### Vì sao chúng ta cần PQC

Thuật toán Shor có thể phá vỡ RSA và ECDH trên một máy tính lượng tử đủ lớn. NIST khởi động cuộc thi chuẩn hoá PQC năm 2016 để chọn các thuật toán thay thế. Sau bốn vòng đánh giá, CRYSTALS-Kyber được chọn làm tiêu chuẩn KEM năm 2022 và được công bố là FIPS 203 vào năm 2024.

## Cách thức hoạt động

### Bài toán cơ sở: Module-LWE

CRYSTALS-Kyber dựa trên bài toán Module Learning With Errors (Module-LWE). Tóm lược: cho một ma trận `A` và một vector `b = As + e` (với `e` là nhiễu nhỏ), khôi phục `s` được tin là khó — cho cả máy tính cổ điển và lượng tử.

### KEM (Cơ chế đóng gói khoá)

Một KEM cho phép hai bên thoả thuận về một khoá đối xứng dùng chung. Quy trình:

1. Bob tạo cặp khoá công khai/riêng tư.
2. Alice mã hoá một khoá ngẫu nhiên bằng khoá công khai của Bob.
3. Bob giải mã để có cùng khoá đối xứng.
4. Hai bên sử dụng khoá đối xứng (AES-256) cho mã hoá luồng dữ liệu.

## Đặc điểm hiệu suất

- **Kích thước khoá công khai Kyber-768:** 1.184 byte (so với 256 byte cho ECDH Curve25519).
- **Kích thước ciphertext:** 1.088 byte.
- **Tốc độ:** vài chục microgiây cho keygen, encaps và decaps trên CPU hiện đại.

## Áp dụng

### Triển khai sản xuất

- **Cloudflare** đã triển khai Kyber kết hợp với X25519 vào TLS 1.3 năm 2023.
- **Google Chrome** kích hoạt hybrid Kyber theo mặc định năm 2024.
- **Apple** thông báo PQ3 cho iMessage năm 2024, sử dụng Kyber kết hợp.
- **Signal** đã thêm PQXDH (sử dụng Kyber) vào năm 2023.

## Triển vọng

### Hậu lượng tử trong thanh toán

Các hệ thống thanh toán bán buôn (SWIFT, các sơ đồ thanh toán quốc gia) đang đánh giá việc tích hợp Kyber. Mối đe doạ "thu thập ngay, giải mã sau" — kẻ tấn công lưu trữ lưu lượng được mã hoá ngày nay để giải mã trong tương lai bằng máy tính lượng tử — khiến việc chuyển đổi sớm trở thành ưu tiên.

## Kết luận

CRYSTALS-Kyber không phải là tương lai xa của mật mã — nó là hiện tại. Các tổ chức xử lý dữ liệu nhạy cảm với thời gian sống dài (hồ sơ y tế, hợp đồng tài chính, bí mật quốc gia) phải lên kế hoạch chuyển đổi ngay bây giờ. Tiêu chuẩn đã có; câu hỏi là tốc độ triển khai.
