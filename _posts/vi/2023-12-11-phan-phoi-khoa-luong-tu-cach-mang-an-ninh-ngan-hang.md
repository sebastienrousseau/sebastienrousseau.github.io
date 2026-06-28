---
title: 'Phân phối Khoá Lượng tử: cách mạng an ninh trong ngân hàng'
subtitle: 'Khi máy tính lượng tử đe doạ mã hoá truyền thống, QKD nổi lên như câu trả lời cấu trúc'
description: 'Quantum Key Distribution (QKD) cung cấp bảo mật được đảm bảo về mặt vật lý cho phân phối khoá. Cách nó hoạt động, đâu là giới hạn, và tại sao các ngân hàng nên quan tâm.'
date: 'December 11, 2023'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp'
banner_alt: 'Sơ đồ giao thoa photon trong một hệ thống QKD'
keywords: 'QKD, phân phối khoá lượng tử, BB84, mật mã lượng tử, ngân hàng, an ninh tài chính, photon'
---

![Sơ đồ QKD](https://cloudcdn.pro/stocks/images/getty-images-LaU3HadwEeE-unsplash.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Phân phối Khoá Lượng tử (QKD) sử dụng các tính chất của cơ học lượng tử để phân phối khoá mã hoá với bảo mật được đảm bảo về mặt vật lý. Đối với các ngân hàng, nó là một câu trả lời cấu trúc — bổ sung cho PQC — đối với mối đe doạ lượng tử.
>
> **Điểm chính**
>
> - **Ý tưởng.** Bảo mật QKD đến từ các định luật vật lý, không phải giả thiết tính toán.
> - **Đổi mới.** Bất kỳ nỗ lực nghe lén nào cũng làm xáo trộn các photon và bị phát hiện.
> - **Trường hợp sử dụng.** Liên kết liên ngân hàng, dữ liệu trung tâm dữ liệu, các tuyến cáp dài.
> - **Hạn chế.** Khoảng cách hạn chế (~100 km không repeater), chi phí phần cứng cao.

## Bối cảnh

### Bảo mật mật mã so với bảo mật vật lý

Mật mã hiện đại (RSA, ECDH) dựa trên các giả định tính toán: chúng ta tin rằng một số bài toán nhất định là khó. Máy tính lượng tử thách thức một số giả định này. QKD đề xuất một mô hình bảo mật khác: bảo mật đến từ các định luật vật lý, không phải các giả định.

## Cách thức hoạt động

### Giao thức BB84

Giao thức BB84 (Bennett & Brassard, 1984) là QKD đầu tiên và vẫn được áp dụng rộng rãi nhất:

1. Alice gửi một dãy các photon được phân cực ngẫu nhiên (ngang, dọc, chéo).
2. Bob đo từng photon bằng cách chọn ngẫu nhiên một trong hai bộ lọc.
3. Họ trao đổi công khai các bộ lọc đã sử dụng (không phải kết quả).
4. Họ giữ lại chỉ các bit nơi cả hai sử dụng cùng bộ lọc.

Nếu Eve cố gắng đo các photon trên đường, định lý không nhân bản (no-cloning) đảm bảo cô ấy gây nhiễu — và Alice và Bob phát hiện qua tỉ lệ lỗi.

## Triển khai thực tế

### Đã có các mạng QKD

- **Trung Quốc.** Mạng QKD quốc gia kết nối Bắc Kinh và Thượng Hải qua 2.000 km, sử dụng vệ tinh và cáp sợi.
- **Châu Âu.** EuroQCI đang triển khai một backbone QKD châu Âu.
- **Tài chính.** ID Quantique cung cấp các tuyến QKD cho các trung tâm dữ liệu của các ngân hàng lớn ở Geneva và Tokyo.

## Hạn chế

### Đâu là giới hạn

- **Khoảng cách.** Tín hiệu photon yếu nhanh chóng theo khoảng cách. Hiện tại giới hạn khoảng 100 km không có repeater lượng tử.
- **Chi phí.** Phần cứng QKD chuyên dụng tốn hàng trăm nghìn đô la cho mỗi tuyến.
- **Khả năng tương tác.** Không có tiêu chuẩn rộng rãi; mỗi nhà cung cấp có thiết kế riêng.
- **Bổ sung, không thay thế.** QKD chỉ phân phối khoá; bạn vẫn cần mã hoá đối xứng (AES) cho dữ liệu.

## Triển vọng

### QKD và PQC

QKD và PQC không loại trừ nhau. PQC mở rộng được cho phần mềm (cập nhật thư viện); QKD cung cấp bảo mật dựa trên vật lý cho các liên kết cao giá trị. Một chiến lược phòng thủ chiều sâu sẽ kết hợp cả hai.

## Kết luận

QKD không phải là viên đạn bạc. Nhưng đối với các tuyến liên kết quan trọng giữa các trung tâm dữ liệu của ngân hàng, các sàn giao dịch hoặc các cơ sở quốc phòng, nó cung cấp một đảm bảo bảo mật mà không có công nghệ nào khác cung cấp. Khi máy tính lượng tử trở nên có khả năng hơn, các ngân hàng nên đánh giá QKD là một phần của chiến lược hậu lượng tử của họ.
