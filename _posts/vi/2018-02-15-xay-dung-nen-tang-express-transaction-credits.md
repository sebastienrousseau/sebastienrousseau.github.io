---
title: 'Xây dựng nền tảng Express Transaction Credits'
subtitle: 'Hành trình kỹ thuật từ ý tưởng đến triển khai'
description: 'Quá trình thiết kế và xây dựng Express Transaction Credits — các quyết định kỹ thuật, các trade-off và bài học rút ra.'
date: 'February 15, 2018'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/etc-build.webp'
banner_alt: 'Một sơ đồ kiến trúc của một nền tảng blockchain'
keywords: 'Express Transaction Credits, blockchain, kiến trúc, đồng thuận, phát triển, kỹ thuật, fintech'
---

![Sơ đồ kiến trúc nền tảng blockchain](https://cloudcdn.pro/stocks/images/etc-build.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Xây dựng một nền tảng blockchain cho thanh toán đòi hỏi đánh đổi cẩn thận giữa thông lượng, độ trễ, bảo mật và phi tập trung. Bài viết này ghi lại các quyết định thiết kế đằng sau Express Transaction Credits.
>
> **Điểm chính**
>
> - **Cách tiếp cận.** Bắt đầu từ các trường hợp sử dụng thực tế (thanh toán bán lẻ, vi giao dịch) chứ không từ công nghệ.
> - **Phương pháp.** Lựa chọn cơ chế đồng thuận, mô hình dữ liệu và lớp ứng dụng dựa trên các yêu cầu cụ thể.
> - **Kết quả.** Một prototype có thể xử lý vài nghìn TPS với thời gian xác nhận dưới hai giây.
> - **Bài học.** Phi tập trung và hiệu suất là một phổ liên tục, không phải đối lập nhị phân.

## Bối cảnh

### Tại sao xây dựng một blockchain mới

Năm 2018, các blockchain công khai hiện có không đáp ứng được yêu cầu thanh toán thực tế. Forking một blockchain hiện có sẽ kế thừa các giả định thiết kế của nó. Bắt đầu mới cho phép định nghĩa lại các đánh đổi từ đầu.

## Phương pháp

### Các quyết định kiến trúc

**Đồng thuận.** Chúng tôi đánh giá PoW, PoS thuần tuý, DPoS và PBFT. Đã chọn một biến thể PBFT lai với rotation trình xác thực để cân bằng giữa hiệu suất và phi tập trung.

**Mô hình dữ liệu.** Account-based (như Ethereum) thay vì UTXO (như Bitcoin) vì đơn giản hơn cho các nhà phát triển và phù hợp hơn với hợp đồng thông minh.

**Lưu trữ.** Trie Merkle Patricia cho trạng thái toàn cầu. RocksDB làm cơ sở dữ liệu key-value bên dưới.

**Mạng.** libp2p cho peer-to-peer; gRPC cho API máy khách.

## Quá trình

### Các giai đoạn phát triển

1. **Prototype lõi.** Triển khai khối, giao dịch, băm và chữ ký. Một nút duy nhất.
2. **Đồng thuận.** Thêm các trình xác thực, vòng đồng thuận, xử lý phân nhánh.
3. **Mạng.** Kết nối nhiều nút, gossip giao dịch và khối.
4. **API và SDK.** REST/gRPC cho khách hàng, thư viện JavaScript và Python.
5. **Kiểm thử tải.** Mô phỏng các kịch bản thanh toán thực tế.

## Kết quả

### Hiệu suất đo được

Prototype đạt được:

- **3.500 TPS** ổn định trong kiểm thử tải.
- **Thời gian xác nhận trung bình 1,8 giây.**
- **Phí giao dịch dưới 0,001 $.**

Đây là một cải thiện đáng kể so với Bitcoin và Ethereum nhưng vẫn dưới mức 24.000 TPS của Visa. Layer 2 và sharding sẽ là các bước tiếp theo.

## Bài học

### Những gì chúng tôi học được

1. **Phi tập trung là một phổ.** Không có giải pháp đúng cho mọi trường hợp sử dụng.
2. **Đồng thuận khó hơn dự kiến.** Các trường hợp biên (mạng phân vùng, các nút độc hại) tiêu thụ phần lớn thời gian phát triển.
3. **Trải nghiệm nhà phát triển quan trọng.** Một blockchain với SDK kém sẽ không được áp dụng dù hiệu suất tốt đến đâu.
4. **Khả năng tương tác là chìa khoá.** Không blockchain nào tồn tại trong sự cô lập; cầu nối và tiêu chuẩn là thiết yếu.

## Triển vọng

### Các bước tiếp theo

Các giai đoạn tiếp theo gồm: triển khai testnet công khai, kiểm toán bảo mật của bên thứ ba, các thí điểm với đối tác thanh toán và lộ trình mainnet.

## Kết luận

Xây dựng Express Transaction Credits là một bài tập trong việc cân bằng các đánh đổi kỹ thuật. Không có giải pháp hoàn hảo — chỉ có những lựa chọn được thông tin phù hợp với các trường hợp sử dụng cụ thể. Đó là bài học áp dụng cho mọi dự án blockchain.
