---
title: 'Mã hoá hoàn toàn đồng cấu trong kỷ nguyên lượng tử ngân hàng'
subtitle: 'Tính toán trên dữ liệu được mã hoá mà không cần giải mã'
description: 'Cách mã hoá hoàn toàn đồng cấu (FHE) cách mạng hoá bảo mật dữ liệu trong ngân hàng và dịch vụ tài chính, bảo vệ quyền riêng tư trước các mối đe doạ thời lượng tử.'
date: 'March 25, 2024'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/circuit_board_cityscape.webp'
banner_alt: 'Sơ đồ trừu tượng của mã hoá hoàn toàn đồng cấu'
keywords: 'FHE, mã hoá đồng cấu, mật mã, ngân hàng, quyền riêng tư, lattice, mạng tinh thể, hậu lượng tử'
---

![Mã hoá hoàn toàn đồng cấu](https://cloudcdn.pro/stocks/images/circuit_board_cityscape.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Mã hoá hoàn toàn đồng cấu (FHE) cho phép tính toán trên dữ liệu được mã hoá mà không cần giải mã trước. Đối với các ngân hàng, đây là một sự thay đổi cấu trúc: dữ liệu khách hàng có thể được xử lý bởi các bên thứ ba mà vẫn được bảo vệ về mặt mật mã.
>
> **Điểm chính**
>
> - **Ý tưởng.** Mã hoá dữ liệu, tính toán trên ciphertext, trả về ciphertext kết quả. Chỉ chủ sở hữu khoá có thể giải mã.
> - **Đổi mới.** Các sơ đồ hiện đại (CKKS, BFV, BGV) dựa trên Module-LWE — cũng kháng lượng tử.
> - **Trường hợp sử dụng.** Phân tích đám mây trên dữ liệu nhạy cảm, tính toán đa bên, học máy bảo vệ quyền riêng tư.
> - **Hạn chế.** Chi phí tính toán cao (1000-10.000x so với tính toán cleartext); ngày càng cải thiện.

## Bối cảnh

### Vấn đề quyền riêng tư

Các ngân hàng có một bài toán cơ bản: họ muốn tận dụng các năng lực điện toán đám mây nhưng không thể tiết lộ dữ liệu khách hàng cho nhà cung cấp đám mây. Các phương pháp tiếp cận hiện tại (mã hoá khi lưu, mã hoá trong vận chuyển) yêu cầu giải mã trong bộ nhớ để xử lý.

## FHE: Cách thức hoạt động

### Nguyên lý

FHE cho phép các phép toán toán học trên ciphertext mà tương ứng với các phép toán trên cleartext:

```text
Enc(a) ⊕ Enc(b) = Enc(a + b)
Enc(a) ⊗ Enc(b) = Enc(a × b)
```

Một bên có thể tính toán hàm `f(a, b)` mà không bao giờ nhìn thấy `a` hoặc `b`. Chỉ chủ sở hữu khoá riêng có thể giải mã kết quả.

## Các sơ đồ FHE

### CKKS (Cheon-Kim-Kim-Song)

Hỗ trợ số học gần đúng trên số thực — lý tưởng cho học máy và phân tích.

### BFV / BGV

Hỗ trợ số học chính xác trên số nguyên — phù hợp với các trường hợp yêu cầu độ chính xác chính xác (kế toán, kiểm toán).

### Tất cả đều dựa trên lattice

Bảo mật của các sơ đồ FHE hiện đại đến từ tính khó của các bài toán Lattice — đặc biệt là Ring-LWE và Module-LWE. Đây là cùng các bài toán làm cơ sở cho CRYSTALS-Kyber. Điều này có nghĩa FHE cũng kháng lượng tử.

## Trường hợp sử dụng ngân hàng

### Phân tích đám mây bảo vệ quyền riêng tư

Ngân hàng A muốn chạy mô hình rủi ro tín dụng trên dữ liệu khách hàng bằng cách sử dụng cụm GPU của AWS:

1. Mã hoá dữ liệu khách hàng với khoá CKKS.
2. Gửi ciphertext đến AWS.
3. AWS chạy mô hình ML trên ciphertext.
4. AWS gửi ciphertext kết quả trở lại.
5. Ngân hàng giải mã cục bộ.

AWS không bao giờ nhìn thấy dữ liệu nhạy cảm.

### Tính toán đa bên (MPC)

Nhiều ngân hàng muốn tính tổng hợp một chỉ số ngành mà không tiết lộ dữ liệu cá nhân:

- Mỗi ngân hàng mã hoá dữ liệu của mình.
- Một bên trung gian tính toán trên các ciphertext.
- Kết quả được giải mã tập thể.

### Học máy bảo vệ quyền riêng tư

Huấn luyện một mô hình phát hiện gian lận trên dữ liệu kết hợp từ nhiều ngân hàng mà không có ngân hàng nào tiết lộ dữ liệu của riêng mình.

## Hạn chế

### Chi phí tính toán

FHE chậm hơn 1.000-10.000x so với tính toán cleartext. Các tối ưu hoá phần cứng (CPU GreenWaves, FPGA, ASIC) đang dần thu hẹp khoảng cách. Vào năm 2024, FHE trở nên khả thi cho các tác vụ với độ trễ chấp nhận được trên các pipeline ML.

## Triển vọng

### FHE trong sản xuất

Microsoft (SEAL), IBM (HElib), Inpher (TFHE-rs) và Zama (Concrete) đều có các thư viện FHE sẵn sàng sản xuất. Các thí điểm ngân hàng đầu tiên đang được triển khai.

## Kết luận

FHE không phải là lý thuyết — đó là một công nghệ đang trưởng thành với các trường hợp sử dụng thực tế trong dịch vụ tài chính. Đối với các ngân hàng đối mặt với cả mối đe doạ lượng tử và áp lực quyền riêng tư, FHE cung cấp một giải pháp kép thuyết phục.
