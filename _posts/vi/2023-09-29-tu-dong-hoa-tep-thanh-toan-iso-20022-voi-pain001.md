---
title: 'Tự động hoá tạo tệp thanh toán tuân thủ ISO 20022 với pain001'
subtitle: 'Một thư viện Python cho chuyển đổi thanh toán toàn cầu'
description: 'pain001 — thư viện Python tự động hoá việc tạo tệp thanh toán ISO 20022 pain.001 từ CSV hoặc SQLite, hỗ trợ chuyển đổi MT/MX trên SWIFT, SEPA và các sơ đồ lớn.'
date: 'September 29, 2023'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/pain001-banner.webp'
banner_alt: 'Sơ đồ luồng dữ liệu thanh toán từ CSV đến XML ISO 20022'
keywords: 'ISO 20022, pain.001, Python, thanh toán, SWIFT, SEPA, mã nguồn mở, tự động hoá, MT/MX'
---

![Luồng dữ liệu từ CSV đến XML ISO 20022](https://cloudcdn.pro/stocks/images/pain001-banner.webp).class=\"img-fluid clearfix\"

> **TL;DR.** `pain001` là một thư viện Python mã nguồn mở tự động hoá việc tạo tệp thanh toán ISO 20022 pain.001 từ CSV hoặc SQLite. Được thiết kế cho cuộc chuyển đổi toàn cầu từ MT/MX sang tin nhắn có cấu trúc trên SWIFT, SEPA và các sơ đồ thanh toán lớn.
>
> **Điểm chính**
>
> - **Ý tưởng.** Một thư viện duy nhất xử lý xác thực, ánh xạ và tạo XML pain.001 với chữ ký rõ ràng.
> - **Tác động.** Giảm đáng kể chi phí phát triển cho các doanh nghiệp di chuyển sang ISO 20022.
> - **Đổi mới.** Hỗ trợ nhiều biến thể quốc gia của tiêu chuẩn (Đức, Pháp, Vương quốc Anh, v.v.).
> - **Trường hợp sử dụng.** Hệ thống ERP, treasury management và các nền tảng thanh toán doanh nghiệp.

## Bối cảnh

### Vì sao ISO 20022 quan trọng

ISO 20022 là tiêu chuẩn nhắn tin tài chính được áp dụng toàn cầu, thay thế cho các định dạng MT của SWIFT đã tồn tại từ thập niên 1970. SWIFT CBPR+ đặt mục tiêu chuyển đổi hoàn toàn vào tháng 11 năm 2025. Các sơ đồ SEPA, FedNow và các hệ thống thanh toán quốc gia khác cũng đã hoặc đang áp dụng nó.

## Vấn đề

### Sự phức tạp của ISO 20022

Tin nhắn pain.001 (Customer Credit Transfer Initiation) là tin nhắn cốt lõi để khởi tạo thanh toán. XML của nó có thể chứa hàng trăm trường, với các quy tắc xác thực và yêu cầu cấu trúc khác nhau giữa các quốc gia và sơ đồ. Viết một trình tạo từ đầu là tốn kém và dễ lỗi.

## Giải pháp

### pain001 hoạt động ra sao

```python
from pain001 import generate_pain001

generate_pain001(
    input_csv="payments.csv",
    output_xml="pain001.xml",
    schema="pain.001.001.09",
)
```

Thư viện:

1. **Đọc** dữ liệu thanh toán từ CSV hoặc SQLite.
2. **Xác thực** mỗi bản ghi theo các quy tắc của biến thể được chọn.
3. **Tạo** XML pain.001 tuân thủ.
4. **Xác minh** XML đầu ra theo XSD chính thức.

## Đổi mới

### Hỗ trợ nhiều biến thể

`pain001` hỗ trợ:

- **pain.001.001.03** (di sản, vẫn được sử dụng rộng rãi).
- **pain.001.001.09** (phiên bản hiện tại của CBPR+).
- **DIN 16645** (biến thể Đức).
- **CFONB 320** (biến thể Pháp).
- **Bacs** (biến thể Vương quốc Anh).

## Trường hợp sử dụng

### Ứng dụng thực tế

- **Hệ thống ERP** cần xuất tệp thanh toán hàng loạt cho ngân hàng.
- **Bộ phận treasury doanh nghiệp** quản lý thanh toán đa ngân hàng.
- **Fintech** xây dựng các API thanh toán cho khách hàng kinh doanh.
- **Tích hợp ngân hàng** thay thế các định dạng độc quyền bằng tiêu chuẩn.

## Cài đặt

```bash
pip install pain001
```

Mã nguồn có sẵn trên [GitHub ⧉](https://github.com/sebastienrousseau/pain001 "pain001 trên GitHub") theo giấy phép Apache-2.0.

## Kết luận

`pain001` giảm rào cản gia nhập cho việc tuân thủ ISO 20022. Bằng cách đóng gói sự phức tạp của tiêu chuẩn vào một thư viện đơn giản, nó cho phép các đội phát triển tập trung vào logic kinh doanh thay vì cấu trúc XML — đặc biệt quan trọng khi thời hạn CBPR+ đang đến gần.
