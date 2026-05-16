---
title: 'Thuật toán lượng tử thách thức mật mã dựa trên mạng tinh thể'
subtitle: 'Bài báo của Yilei Chen làm rung chuyển nền tảng PQC'
description: 'Một thuật toán lượng tử mới giải quyết vấn đề Lattice-LWE — cơ sở của CRYSTALS-Kyber. Điều này có ý nghĩa gì cho mật mã hậu lượng tử?'
date: 'April 15, 2024'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/lattice-quantum-banner.webp'
banner_alt: 'Sơ đồ trừu tượng của mạng tinh thể bị tấn công'
keywords: 'mạng tinh thể, LWE, lượng tử, Yilei Chen, PQC, Kyber, mật mã, hậu lượng tử'
---

![Mạng tinh thể bị tấn công](https://cloudcdn.pro/stocks/images/lattice-quantum-banner.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Bài báo của Yilei Chen công bố tháng 4 năm 2024 đề xuất một thuật toán lượng tử có thể giải Lattice-LWE — bài toán cơ sở cho CRYSTALS-Kyber và phần lớn mật mã hậu lượng tử. Nếu đúng, đây sẽ là một cú đánh nghiêm trọng cho NIST PQC.
>
> **Điểm chính**
>
> - **Cách tiếp cận.** Một thuật toán lượng tử sử dụng các kỹ thuật mới trong việc lấy mẫu Gaussian.
> - **Bối cảnh.** Lattice-LWE được cho là khó cho cả tính toán cổ điển và lượng tử.
> - **Nếu đúng.** Buộc phải đánh giá lại lộ trình PQC; quay lại các thiết kế dựa trên hash hoặc isogeny.
> - **Trạng thái.** Bài báo đang được xem xét bởi cộng đồng mật mã; chưa được xác nhận.

## Bối cảnh

### CRYSTALS-Kyber và Lattice-LWE

CRYSTALS-Kyber, tiêu chuẩn KEM hậu lượng tử mới của NIST (FIPS 203), dựa trên độ khó của bài toán Module-Lattice-LWE. Trong nhiều năm, các nhà mật mã đã tin rằng Lattice-LWE là khó ngay cả với máy tính lượng tử.

## Tuyên bố của Chen

### Một bước đột phá

Vào ngày 10 tháng 4 năm 2024, Yilei Chen của Tsinghua University đã đăng tải một bản thảo sơ bộ trên IACR ePrint Archive khẳng định một thuật toán lượng tử thời gian đa thức cho Lattice-LWE với một số tham số.

Nếu chính xác, điều này sẽ:

- **Phá vỡ** CRYSTALS-Kyber và một loạt các sơ đồ PQC liên quan.
- **Buộc** NIST đánh giá lại lộ trình tiêu chuẩn hoá.
- **Khôi phục** sự không chắc chắn trong cộng đồng mật mã.

## Phản ứng cộng đồng

### Sự thận trọng

Sau khi đăng tải, các chuyên gia hàng đầu đã đánh giá khẩn cấp bài báo. Phản hồi ban đầu:

- **Daniel Apon (NIST)** và những người khác đã tìm thấy các vấn đề trong các bằng chứng.
- **Vinod Vaikuntanathan (MIT)** ghi nhận các thách thức kỹ thuật.
- Vào tháng 5, Chen đã thừa nhận một lỗi và rút lại tuyên bố.

## Bài học

### Tại sao điều này quan trọng dù đã rút lại

Sự kiện này nhấn mạnh nhiều bài học:

1. **Mật mã hậu lượng tử chưa "đã giải quyết".** Bất kỳ giả thuyết về độ khó nào cũng có thể được thử thách.
2. **Sự đa dạng là quan trọng.** NIST đang khám phá các họ PQC khác nhau (lattice, hash-based, code-based, isogeny-based) một phần để phòng vệ chiều sâu.
3. **Tốc độ xem xét.** Phản ứng nhanh chóng của cộng đồng minh hoạ tầm quan trọng của khoa học mở trong mật mã.
4. **Tính linh hoạt mật mã.** Các tổ chức nên có khả năng chuyển đổi giữa các thuật toán nhanh chóng.

## Tác động dài hạn

### Lộ trình PQC

Sự kiện Chen, dù đã rút lại, nhắc nhở rằng:

- **Kyber không bất khả xâm phạm.** NIST tiêu chuẩn hoá nó nhưng tiếp tục nghiên cứu các phương án thay thế.
- **Hybrid là khôn ngoan.** Chiến lược kết hợp Kyber với một sơ đồ không dựa trên lattice (ví dụ: McEliece dựa trên mã, hoặc Falcon dựa trên hash) cung cấp phòng thủ chiều sâu.
- **Tính linh hoạt mật mã không đàm phán được.** Hệ thống thanh toán phải hỗ trợ các thuật toán có thể hoán đổi.

## Trường hợp với ngân hàng

### Tại sao quan tâm

Các ngân hàng đang chuyển sang PQC nên:

1. **Theo dõi** các phát triển trong mã hoá lattice.
2. **Xây dựng tính linh hoạt mật mã** vào hạ tầng — không hard-code Kyber.
3. **Xem xét các sơ đồ hybrid** kết hợp Kyber với một bộ thay thế.
4. **Giám sát** các nghiên cứu trên các họ PQC khác.

## Kết luận

Bài báo của Chen, dù đã được rút lại, là một cú gọi tỉnh táo. Mật mã hậu lượng tử không phải là một đích đến — đó là một hành trình. Các tổ chức phải xây dựng hệ thống linh hoạt cho phép cập nhật mật mã khi nghiên cứu phát triển.
