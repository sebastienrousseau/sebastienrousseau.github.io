---
title: 'Cách mạng hoá nhận dạng giọng nói thời gian thực trên macOS với OpenAI Whisper'
subtitle: 'Tăng tốc bằng Metal Performance Shaders trên Apple Silicon'
description: 'Một hệ thống nhận dạng giọng nói thời gian thực trên macOS sử dụng OpenAI Whisper và Metal Performance Shaders để đạt độ trễ dưới một giây.'
date: 'March 12, 2024'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/circuit_board_cityscape.webp'
banner_alt: 'Sóng giọng nói với biểu tượng macOS'
keywords: 'Whisper, macOS, Metal, Apple Silicon, nhận dạng giọng nói, thời gian thực, OpenAI, M1, M2'
---

![Whisper trên macOS](https://cloudcdn.pro/stocks/images/circuit_board_cityscape.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Một hệ thống phiên âm giọng nói thành văn bản thời gian thực tận dụng OpenAI Whisper và tăng tốc GPU Metal Performance Shaders trên macOS để đạt được độ trễ dưới một giây, 8-12x tốc độ thời gian thực trên M1 Max.
>
> **Điểm chính**
>
> - **Cách tiếp cận.** Mô hình Whisper được chuyển sang Metal cho tăng tốc GPU trên Apple Silicon.
> - **Kết quả.** 8-12x thời gian thực trên M1 Max; độ trễ dưới một giây cho phiên âm trực tiếp.
> - **Trường hợp sử dụng.** Ghi chú họp, phụ đề trực tiếp, hỗ trợ tiếp cận.
> - **Hạn chế.** Đòi hỏi Apple Silicon (M1+); không có sẵn trên Intel Mac.

## Bối cảnh

### Whisper trên thiết bị

OpenAI Whisper là một mô hình ASR (nhận dạng giọng nói tự động) mã nguồn mở chất lượng cao. Chạy nó cục bộ thay vì gọi API mang lại các lợi ích về quyền riêng tư và độ trễ.

## Tăng tốc Metal

### Khai thác Apple Silicon

Apple Silicon (chip M1, M2, M3) tích hợp GPU mạnh mẽ. Metal Performance Shaders (MPS) là API tăng tốc GPU của Apple, được tối ưu hoá cho các phép toán tensor.

Bằng cách chuyển các phép toán Whisper sang MPS:

- **Tải mô hình** nhanh hơn nhờ chia sẻ bộ nhớ thống nhất.
- **Suy luận** tận dụng GPU và Neural Engine.
- **Sử dụng năng lượng thấp** so với việc chạy trên CPU.

## Hiệu suất đo được

### Kết quả M1 Max

- **Tốc độ:** 8-12x thời gian thực (1 giờ âm thanh được xử lý trong 5-7 phút).
- **Độ trễ:** dưới một giây cho luồng trực tiếp với kích thước cửa sổ 1 giây.
- **Độ chính xác:** ngang bằng với việc chạy Whisper trên đám mây.

## Pipeline thời gian thực

### Kiến trúc

1. **Bắt âm thanh** qua AVAudioEngine với độ trễ thấp.
2. **Cửa sổ trượt** thêm các đoạn âm thanh vào bộ đệm vòng.
3. **Suy luận liên tục** mỗi 500ms trên cửa sổ 1 giây gần đây.
4. **Xử lý hậu kỳ** loại bỏ trùng lặp giữa các cửa sổ chồng chéo.
5. **Đầu ra** đến giao diện người dùng hoặc bộ xử lý hạ nguồn.

## Trường hợp sử dụng

### Trên thiết bị

- **Ghi chú cuộc họp.** Phiên âm các cuộc họp Zoom hoặc Teams cục bộ.
- **Phụ đề trực tiếp.** Thêm phụ đề cho video phát trực tiếp.
- **Hỗ trợ tiếp cận.** Phụ đề thời gian thực cho người khiếm thính.
- **Lập trình bằng giọng nói.** Ra lệnh và viết mã bằng giọng nói.

## Quyền riêng tư

Mọi xử lý xảy ra trên thiết bị. Âm thanh không bao giờ rời khỏi máy Mac. Đối với các trường hợp sử dụng nhạy cảm (cuộc gọi luật sư, cuộc họp hội đồng quản trị), đây là một lợi thế đáng kể so với các giải pháp đám mây.

## Hạn chế

- **Chỉ Apple Silicon.** Yêu cầu M1 hoặc mới hơn.
- **Bộ nhớ.** Mô hình Whisper Large cần 10+ GB RAM.
- **Độ trễ.** Một bộ chuyển đổi trực tiếp đầu cuối có độ trễ tối thiểu 500ms-1s.

## Triển vọng

### Bài báo nghiên cứu

Tôi đã xuất bản một bài báo nghiên cứu chi tiết các tối ưu hoá ở mức thấp ([Papers ›](https://sebastienrousseau.com/papers/)).

## Kết luận

Whisper + Metal trên Apple Silicon mở khoá nhận dạng giọng nói thời gian thực cấp doanh nghiệp trên thiết bị tiêu dùng. Đối với các trường hợp sử dụng quan tâm về quyền riêng tư, đây là một sự thay thế hấp dẫn cho các API đám mây.
