---
title: 'Làm chủ ngày và giờ trong Rust với thư viện DTT'
subtitle: 'Một thư viện Rust toàn diện cho xử lý ngày, giờ và múi giờ'
description: 'DTT — thư viện Rust cho ngày, giờ, múi giờ, định dạng và parsing. Được thiết kế cho các ứng dụng tài chính và backend nghiêm túc về dữ liệu thời gian.'
date: 'December 4, 2023'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/rustlogs.webp'
banner_alt: 'Đồng hồ và lịch trên nền trừu tượng'
keywords: 'DTT, Rust, ngày, giờ, múi giờ, parsing, định dạng, tài chính, ISO 8601, RFC 3339'
---

![Đồng hồ và lịch](https://cloudcdn.pro/stocks/images/rustlogs.webp).class=\"img-fluid clearfix\"

> **TL;DR.** `dtt` là thư viện Rust để xử lý ngày, giờ và múi giờ. Nó cung cấp một API đơn giản trên đỉnh các tiêu chuẩn ISO 8601 và RFC 3339, với hỗ trợ chuyên biệt cho các trường hợp sử dụng tài chính (ngày làm việc, lịch ngày nghỉ).
>
> **Điểm chính**
>
> - **Ý tưởng.** API đơn giản, an toàn về loại cho các thao tác ngày/giờ phổ biến.
> - **Đổi mới.** Hỗ trợ ngày làm việc và lịch ngày nghỉ tích hợp.
> - **Trường hợp sử dụng.** Tính toán quyết toán T+1/T+2, ngày tới hạn, kế hoạch chu kỳ.
> - **Tác động.** Loại bỏ một lớp lỗi tinh tế trong logic kinh doanh tài chính.

## Vấn đề

### Tại sao ngày khó

Ngày và giờ trông đơn giản nhưng đầy rẫy các trường hợp biên: múi giờ, ngày DST, năm nhuận, định dạng văn hoá, ngày làm việc và ngày nghỉ. Trong tài chính, một lỗi tính ngày quyết toán có thể có ý nghĩa hàng tỉ đô la (ví dụ vụ Knight Capital năm 2012).

## API

```rust
use dtt::*;

// Phân tích và định dạng
let date = Date::parse("2023-12-04", Format::Iso8601)?;
let formatted = date.format(Format::Rfc3339);

// Số học ngày làm việc
let settlement = date.add_business_days(2)?; // T+2
let next_friday = date.next_weekday(Weekday::Fri);

// Múi giờ
let utc = date.to_timezone(Timezone::Utc);
let london = utc.to_timezone(Timezone::Europe_London);
```

## Tính năng

- **Hỗ trợ múi giờ đầy đủ** thông qua tích hợp `chrono-tz`.
- **Lịch ngày nghỉ** cho các thị trường tài chính lớn (NYSE, LSE, TYO, HKG).
- **Số học ngày làm việc** cho T+1, T+2, T+3.
- **Parsing linh hoạt** với nhiều định dạng đầu vào.
- **Hằng số thời gian** cho các tính toán nhạy cảm về bảo mật (ví dụ: hết hạn JWT).

## Cài đặt

```toml
[dependencies]
dtt = "0.0.5"
```

Mã nguồn trên [GitHub ⧉](https://github.com/sebastienrousseau/dtt) theo Apache-2.0.

## Kết luận

`dtt` giải quyết một vấn đề nhàm chán nhưng quan trọng. Bằng cách đóng gói các thực hành tốt nhất cho xử lý ngày trong một API Rust sạch sẽ, nó giảm rủi ro các lỗi tốn kém trong các ứng dụng tài chính nhạy cảm với thời gian.
