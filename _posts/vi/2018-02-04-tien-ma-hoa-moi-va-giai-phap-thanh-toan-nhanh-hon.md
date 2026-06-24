---
title: 'Hé lộ một đồng tiền mã hoá mới và giải pháp thanh toán nhanh hơn cho tương lai'
subtitle: 'Tổng quan thiết kế của Express Transaction Credits (ETC)'
description: 'Hé lộ Express Transaction Credits — một đồng tiền mã hoá mới được thiết kế để giải quyết các giới hạn tốc độ của Bitcoin và Ethereum.'
date: 'February 4, 2018'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/sebastienrousseau.webp'
banner_alt: 'Một sơ đồ trừu tượng về một mạng thanh toán nhanh'
keywords: 'tiền mã hoá, thanh toán nhanh, Express Transaction Credits, ETC, blockchain, giao dịch tức thời, Layer 2'
---

![Sơ đồ trừu tượng của mạng thanh toán nhanh](https://cloudcdn.pro/stocks/images/sebastienrousseau.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Express Transaction Credits (ETC) là một đề xuất tiền mã hoá tập trung vào tốc độ giao dịch và chi phí thấp, được thiết kế để giải quyết các giới hạn thông lượng của các blockchain công khai thế hệ đầu tiên.
>
> **Điểm chính**
>
> - **Ý tưởng.** Một blockchain được tối ưu hoá cho thanh toán bán lẻ và vi giao dịch, không phải lưu trữ giá trị.
> - **Đổi mới.** Cơ chế đồng thuận lai và kênh trạng thái Layer 2 để xử lý ngoài chuỗi.
> - **Tác động.** Khả năng xử lý vài nghìn TPS so với 7 TPS của Bitcoin.
> - **Hạn chế.** Đánh đổi giữa thông lượng và phi tập trung; cần kiểm thử dài hạn.

## Phân tích

### Vì sao tốc độ quan trọng

Bitcoin và Ethereum được thiết kế ưu tiên bảo mật và phi tập trung, không phải tốc độ. Kết quả: 7 TPS cho Bitcoin, ~15 TPS cho Ethereum (trước Merge). Visa xử lý 24.000 TPS. Để tiền mã hoá trở thành phương tiện thanh toán đại trà, khoảng cách này phải được thu hẹp.

## Ý tưởng

### Express Transaction Credits

ETC đề xuất một blockchain mới được tối ưu hoá đặc biệt cho thanh toán:

- **Thời gian khối ngắn** (1-2 giây thay vì 10 phút của Bitcoin).
- **Cơ chế đồng thuận lai** kết hợp các trình xác thực được uỷ quyền và xác minh ngẫu nhiên.
- **Kênh trạng thái** cho thanh toán lặp lại giữa hai bên (như Lightning Network).
- **Phí thấp** đủ để vi giao dịch (dưới một xu) trở nên thực tế.

## Đổi mới

### Các đánh đổi thiết kế

ETC chấp nhận một mức độ tập trung nhất định để đạt được hiệu suất. Số lượng trình xác thực hữu hạn (vài chục thay vì hàng nghìn) cho phép đồng thuận nhanh hơn nhưng yêu cầu tin cậy nhiều hơn vào tập hợp trình xác thực. Mô hình quản trị bù đắp điều này thông qua quay vòng trình xác thực và yêu cầu cổ phần.

## Tác động

### Các trường hợp sử dụng

- **Thanh toán bán lẻ.** Quẹt thẻ ảo tại quầy thanh toán.
- **Vi giao dịch.** Trả tiền theo bài hoặc theo phút cho nội dung.
- **Chuyển tiền xuyên biên giới.** Quyết toán dưới một phút với chi phí gần bằng không.
- **IoT.** Các thiết bị tự thanh toán cho dịch vụ (điện, băng thông) theo thời gian thực.

## Hạn chế

### Câu hỏi mở

ETC vẫn ở giai đoạn đề xuất. Các câu hỏi mở gồm: liệu mô hình đồng thuận có vẫn an toàn dưới tải thực tế? Quản trị sẽ phát triển ra sao khi mạng mở rộng? Khả năng tương tác với các blockchain khác và với hạ tầng thanh toán truyền thống sẽ được giải quyết thế nào?

## Triển vọng

### Bài học rộng hơn

Cho dù ETC có thành công hay không, đề xuất này phản ánh một xu hướng quan trọng năm 2018: nhận thức rằng các blockchain công khai thế hệ đầu tiên không đủ cho thanh toán đại trà, và rằng các blockchain chuyên biệt cho từng trường hợp sử dụng có thể là tương lai.

## Kết luận

Express Transaction Credits là một thử nghiệm trong việc tối ưu hoá blockchain cho thanh toán. Liệu nó có trở thành chuẩn mực hay không sẽ phụ thuộc vào việc thực thi và sự áp dụng — nhưng câu hỏi mà nó đặt ra (làm thế nào để tiền mã hoá trở thành phương tiện thanh toán thực tế) sẽ định hình thập kỷ tiếp theo của ngành.
