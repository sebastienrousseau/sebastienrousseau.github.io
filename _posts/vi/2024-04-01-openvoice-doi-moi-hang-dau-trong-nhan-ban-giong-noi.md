---
title: 'OpenVoice: đổi mới hàng đầu trong công nghệ nhân bản giọng nói'
subtitle: 'Tổng hợp giọng nói tức thì từ một mẫu vài giây'
description: 'OpenVoice của MyShell mở khoá việc nhân bản giọng nói chất lượng cao từ một mẫu ngắn. Cách nó hoạt động, các trường hợp sử dụng và các vấn đề đạo đức.'
date: 'April 1, 2024'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/rustlogs.webp'
banner_alt: 'Sóng giọng nói và biểu tượng AI'
keywords: 'OpenVoice, nhân bản giọng nói, TTS, MyShell, AI, deepfake, đạo đức, hỗ trợ tiếp cận'
---

![Nhân bản giọng nói AI](https://cloudcdn.pro/stocks/images/rustlogs.webp).class=\"img-fluid clearfix\"

> **TL;DR.** OpenVoice là một hệ thống nhân bản giọng nói mã nguồn mở của MyShell có khả năng sao chép giọng nói của một người từ chỉ một mẫu vài giây và tổng hợp lời nói mới với giọng đó.
>
> **Điểm chính**
>
> - **Ý tưởng.** Học các đặc điểm giọng nói (timbre, ngữ điệu) một cách độc lập, cho phép kiểm soát chính xác.
> - **Đổi mới.** Hỗ trợ đa ngôn ngữ và kiểm soát cảm xúc trong giọng nói tổng hợp.
> - **Trường hợp sử dụng.** Hỗ trợ tiếp cận, lồng tiếng, sách nói, hỗ trợ khách hàng.
> - **Rủi ro.** Deepfake giọng nói, lừa đảo, vi phạm bản quyền nghệ sĩ.

## Bối cảnh

### Sự ra đời của nhân bản giọng nói

Cho đến gần đây, nhân bản giọng nói chất lượng yêu cầu hàng giờ ghi âm và tính toán mạnh mẽ. OpenVoice (và các sản phẩm tương tự như ElevenLabs) đã giảm điều này xuống còn vài giây và một laptop.

## Kiến trúc

### Học đặc điểm tách rời

OpenVoice tách giọng nói thành các thành phần:

- **Timbre.** "Âm sắc" của giọng nói — danh tính.
- **Nội dung.** Văn bản được nói.
- **Ngữ điệu/Cảm xúc.** Tốc độ, cao độ, năng lượng.
- **Ngôn ngữ.** Tiếng Anh, tiếng Việt, tiếng Pháp, v.v.

Mỗi thành phần có thể được kiểm soát độc lập, cho phép tổng hợp một câu mới với giọng của Alice, ngữ điệu vui vẻ và bằng tiếng Việt.

## Trường hợp sử dụng

### Hỗ trợ tiếp cận

- **Hỗ trợ giao tiếp.** Cho người bị mất giọng nói (ví dụ bệnh nhân ALS) duy trì giọng nói của họ.
- **Sách nói.** Tạo sách nói với một loạt các giọng nói mà không cần đến diễn viên lồng tiếng.
- **Học ngôn ngữ.** Nghe phát âm trong nhiều giọng vùng miền.

### Doanh nghiệp

- **Tin nhắn cá nhân hoá.** Mỗi khách hàng nhận được tin nhắn marketing trong giọng nói có vẻ riêng cho mình.
- **Trợ lý ảo.** Tạo nhiều "nhân vật" trợ lý với các giọng nói khác nhau.
- **Tạo nội dung.** Lồng tiếng video không cần phòng thu.

## Vấn đề đạo đức

### Rủi ro

- **Lừa đảo.** Kẻ tấn công sao chép giọng CEO để uỷ quyền chuyển tiền giả.
- **Tin giả.** Tạo các tuyên bố giả mạo từ chính trị gia.
- **Vi phạm bản quyền.** Sao chép giọng diễn viên hoặc ca sĩ mà không có sự đồng ý.

### Phòng vệ

- **Watermarking.** Nhúng các tín hiệu không thể nghe vào âm thanh tổng hợp để phát hiện.
- **Quy định.** EU và California đang xem xét các luật yêu cầu tiết lộ.
- **Sự đồng ý.** Yêu cầu cho phép rõ ràng để nhân bản giọng nói.

## Tác động với ngân hàng

### Phòng chống lừa đảo

Các ngân hàng phải nâng cấp xác minh giọng nói. Mật khẩu giọng nói tĩnh không còn an toàn — kẻ tấn công có thể tổng hợp chúng. Các phương pháp tiếp cận mới:

- **Xác thực hành vi.** Phân tích các mẫu nói chung, không chỉ giọng nói.
- **Câu hỏi thử thách.** Yêu cầu khách hàng phản hồi các câu hỏi không thể chuẩn bị trước.
- **Liveness detection.** Đảm bảo người nói đang nói trực tiếp.

## Kết luận

OpenVoice là một bước nhảy vọt công nghệ với những hậu quả đạo đức sâu sắc. Đối với các ứng dụng hợp pháp (hỗ trợ tiếp cận, sách nói), đó là một phước lành. Đối với các ứng dụng độc hại (lừa đảo, tin giả), nó tăng cường các mối đe doạ hiện có. Các ngân hàng phải lên kế hoạch cho cả hai.
