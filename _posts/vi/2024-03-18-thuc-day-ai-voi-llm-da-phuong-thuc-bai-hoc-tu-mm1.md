---
title: 'Thúc đẩy AI với LLM đa phương thức: bài học từ MM1'
subtitle: 'Phân tích bài báo MM1 của Apple về các mô hình ngôn ngữ lớn đa phương thức'
description: 'Phân tích bài báo MM1 của Apple — kiến trúc, chiến lược huấn luyện trước và các khả năng mới nổi của LLM đa phương thức.'
date: 'March 18, 2024'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/mm1-banner.webp'
banner_alt: 'Sơ đồ trừu tượng của một LLM đa phương thức'
keywords: 'MM1, Apple, LLM, đa phương thức, hình ảnh, văn bản, học máy, kiến trúc, huấn luyện trước'
---

![MM1 LLM đa phương thức](https://cloudcdn.pro/stocks/images/mm1-banner.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Bài báo MM1 của Apple cung cấp một phân tích chi tiết về việc xây dựng các mô hình ngôn ngữ lớn đa phương thức (MLLM). Các bài học chính: trộn lẫn các loại dữ liệu là quan trọng, các bộ mã hoá hình ảnh nhỏ hoạt động tốt và các khả năng mới nổi xuất hiện ở quy mô.
>
> **Điểm chính**
>
> - **Cách tiếp cận.** Trộn lẫn các caption hình ảnh-văn bản, văn bản xen kẽ và văn bản thuần tuý cho huấn luyện trước.
> - **Bối cảnh.** Apple xuất bản bài báo này như một phần của chiến lược AI trên thiết bị.
> - **Kết quả.** MM1 30B cạnh tranh với các mô hình lớn hơn nhiều trên các điểm chuẩn đa phương thức.
> - **Bài học.** Hỗn hợp dữ liệu quan trọng hơn kiến trúc cụ thể.

## Bối cảnh

### Apple và AI

Apple được biết đến với việc giữ kín các nỗ lực AI. Việc xuất bản MM1 vào tháng 3 năm 2024 báo hiệu một sự thay đổi: Apple muốn thiết lập sự hiện diện trong cộng đồng nghiên cứu AI, có khả năng để hỗ trợ các tính năng AI sắp tới của iOS 18.

## Kiến trúc

### Các thành phần

MM1 tuân theo kiến trúc chuẩn của một MLLM hiện đại:

- **Bộ mã hoá hình ảnh** (ViT) chuyển đổi hình ảnh thành các embedding.
- **Cầu nối Q-Former hoặc MLP** chuyển embedding sang không gian LLM.
- **Mô hình ngôn ngữ** (decoder transformer) tạo văn bản.

## Bài học chính

### 1. Hỗn hợp dữ liệu là quan trọng

Apple thử nghiệm các tỉ lệ khác nhau của các loại dữ liệu:

- **Caption hình ảnh-văn bản:** Hình ảnh với mô tả ngắn.
- **Văn bản xen kẽ:** Web pages với hình ảnh xen kẽ trong văn bản.
- **Văn bản thuần tuý:** Sách, bài báo, mã.

Kết quả: tất cả ba đều cần thiết. Văn bản xen kẽ đặc biệt quan trọng cho khả năng học few-shot.

### 2. Bộ mã hoá hình ảnh nhỏ hoạt động tốt

Trái với mong đợi, sử dụng bộ mã hoá hình ảnh lớn hơn không cải thiện hiệu suất đáng kể. Các bộ mã hoá nhỏ và hiệu quả là đủ.

### 3. Quy mô tạo ra các khả năng

Ở quy mô 30B tham số, MM1 cho thấy khả năng nổi bật trong các tác vụ ít ví dụ — học các nhiệm vụ mới từ chỉ vài ví dụ trong prompt.

## So sánh

### MM1 so với các mô hình khác

- **GPT-4V** vẫn vượt trội trên hầu hết các điểm chuẩn.
- **MM1** cạnh tranh trên các tác vụ chú thích hình ảnh và VQA.
- **LLaVA, Gemini** đều có hiệu suất tương đương trong phạm vi tham số tương tự.

## Ý nghĩa với Apple

### AI trên thiết bị

Bài báo gợi ý rằng Apple đang chuẩn bị các tính năng AI cho iOS 18 và sau đó:

- **Mô tả ảnh** cho hỗ trợ tiếp cận.
- **Tìm kiếm hình ảnh** trong ứng dụng Photos.
- **Phụ đề tự động** cho video.

## Trường hợp sử dụng

### Doanh nghiệp

- **Phân loại tài liệu.** Đọc hình thức và phân loại tự động.
- **Kiểm tra chất lượng.** Phát hiện khiếm khuyết trong hình ảnh sản phẩm.
- **Hỗ trợ khách hàng.** Khách hàng tải lên ảnh sản phẩm hỏng, AI chẩn đoán.

## Triển vọng

### Tương lai MLLM

Đa phương thức (hình ảnh + âm thanh + video + văn bản) sẽ là tiêu chuẩn vào năm 2025. MM1 cung cấp một sách hướng dẫn cho việc xây dựng các mô hình như vậy.

## Kết luận

MM1 không phải là mô hình mạnh nhất, nhưng bài báo đi kèm là một trong những bản tóm tắt rõ ràng nhất về cách xây dựng các MLLM hiện đại. Đối với các nhà nghiên cứu và kỹ sư xây dựng các hệ thống đa phương thức, đây là tài liệu đọc bắt buộc.
