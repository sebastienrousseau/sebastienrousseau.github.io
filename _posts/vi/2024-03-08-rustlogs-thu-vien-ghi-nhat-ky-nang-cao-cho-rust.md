---
title: 'RustLogs: thư viện ghi nhật ký nâng cao cho ứng dụng Rust'
subtitle: 'Ghi nhật ký có cấu trúc, hiệu năng cao cho các hệ thống tài chính'
description: 'RustLogs — thư viện ghi nhật ký Rust cho ứng dụng cấp doanh nghiệp với ghi nhật ký có cấu trúc, đa kênh và an toàn về thread.'
date: 'March 8, 2024'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/rustlogs.webp'
banner_alt: 'Sơ đồ trừu tượng của một hệ thống ghi nhật ký'
keywords: 'RustLogs, Rust, ghi nhật ký, có cấu trúc, JSON, hiệu năng, doanh nghiệp, quan sát'
---

![Hệ thống ghi nhật ký](https://cloudcdn.pro/stocks/images/rustlogs.webp).class=\"img-fluid clearfix\"

> **TL;DR.** `rustlogs` là thư viện ghi nhật ký Rust được thiết kế cho các ứng dụng cấp doanh nghiệp: ghi nhật ký có cấu trúc, nhiều mức độ ưu tiên, hỗ trợ nhiều kênh và an toàn thread.
>
> **Điểm chính**
>
> - **Ý tưởng.** Ghi nhật ký có cấu trúc theo mặc định để dễ dàng truy vấn trong ELK, Splunk hoặc Datadog.
> - **Đổi mới.** Định dạng đầu ra linh hoạt (JSON, văn bản, CEF, GELF).
> - **Trường hợp sử dụng.** Các dịch vụ tài chính, hệ thống thanh toán, microservices.
> - **Hiệu năng.** Bộ đệm và ghi không đồng bộ để giảm thiểu chi phí.

## Vấn đề

### Vì sao ghi nhật ký có cấu trúc

Ghi nhật ký dạng văn bản truyền thống khó tìm kiếm. Một dòng như `[ERROR] failed to charge user 12345 amount 99.99` đòi hỏi biểu thức chính quy để truy vấn. Ghi nhật ký có cấu trúc xuất ra JSON:

```json
{
  "level": "error",
  "event": "charge_failed",
  "user_id": 12345,
  "amount": 99.99,
  "currency": "USD",
  "timestamp": "2024-03-08T10:30:00Z"
}
```

Dữ liệu này có thể được lập chỉ mục, truy vấn và biểu đồ hoá.

## API

```rust
use rustlogs::{Logger, Level};

let logger = Logger::new()
    .with_format(Format::Json)
    .with_output(Output::Stdout);

logger.info("user_login", json!({
    "user_id": 12345,
    "ip": "192.168.1.1",
}));

logger.error("charge_failed", json!({
    "user_id": 12345,
    "amount": 99.99,
    "error": "insufficient_funds",
}));
```

## Tính năng

- **Nhiều mức độ.** Trace, Debug, Info, Warn, Error, Critical.
- **Nhiều kênh.** Đồng thời ghi đến stdout, tệp, syslog, mạng.
- **Định dạng linh hoạt.** JSON, văn bản, CEF (Common Event Format), GELF (Graylog).
- **Async-first.** Ghi không đồng bộ để tránh chặn luồng chính.
- **An toàn thread.** Sử dụng từ nhiều luồng mà không cần khoá.

## Tích hợp với hệ sinh thái

### Tương thích với `tracing`

`rustlogs` tích hợp với hệ sinh thái `tracing` được sử dụng rộng rãi của Rust, cho phép tích hợp dễ dàng với các công cụ quan sát hiện có (Jaeger, OpenTelemetry).

## Trường hợp sử dụng ngân hàng

- **Tuân thủ.** Ghi nhật ký kiểm toán đầy đủ của tất cả các thay đổi cấu hình.
- **Phát hiện gian lận.** Sự kiện có cấu trúc cho phép phát hiện mẫu thời gian thực.
- **Đối soát.** Mỗi bước của một giao dịch được ghi với cùng correlation_id để dễ dàng theo dõi.
- **SLO.** Các chỉ số dựa trên nhật ký có cấu trúc cấp cho biểu đồ và cảnh báo.

## Cài đặt

```toml
[dependencies]
rustlogs = "0.0.1"
```

Mã nguồn trên [GitHub ⧉](https://github.com/sebastienrousseau/rustlogs) theo Apache-2.0.

## Kết luận

`rustlogs` là một thư viện ghi nhật ký tập trung vào việc giải quyết các nhu cầu của các hệ thống tài chính: cấu trúc, hiệu năng, đa kênh. Bằng cách xây dựng quan sát từ đầu, nó tiết kiệm hàng giờ điều tra khi có sự cố.
