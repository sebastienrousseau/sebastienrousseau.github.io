---
title: 'libmake: bộ sinh mã giảm tác vụ lặp lại và xây dựng thư viện Rust chất lượng cao'
subtitle: 'Tự động hoá việc khởi tạo dự án Rust với cấu trúc tốt'
description: 'libmake — một CLI Rust tạo các thư viện Rust mới với cấu trúc tốt, kiểm thử, CI/CD và tài liệu sẵn sàng.'
date: 'October 26, 2023'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/rustlogs.webp'
banner_alt: 'Sơ đồ cấu trúc thư mục của một thư viện Rust'
keywords: 'libmake, Rust, scaffold, sinh mã, CLI, mã nguồn mở, năng suất, phát triển'
---

![Cấu trúc thư mục thư viện Rust](https://cloudcdn.pro/stocks/images/rustlogs.webp).class=\"img-fluid clearfix\"

> **TL;DR.** `libmake` là một CLI tạo các dự án thư viện Rust hoàn chỉnh — bao gồm bộ khung mã, các bài kiểm thử, cấu hình CI/CD GitHub Actions, tài liệu và mẫu README — bằng một lệnh duy nhất.
>
> **Điểm chính**
>
> - **Ý tưởng.** Loại bỏ công sức lặp đi lặp lại của việc khởi tạo dự án.
> - **Đổi mới.** Các mẫu được kiểm chứng theo thực hành tốt nhất của hệ sinh thái Rust.
> - **Tác động.** Giảm thời gian từ ý tưởng đến lần publish crates.io đầu tiên từ giờ xuống phút.
> - **Trường hợp sử dụng.** Các nhà phát triển khởi tạo nhiều thư viện, các đội cần chuẩn hoá cấu trúc.

## Vấn đề

### Khởi tạo dự án tốn công

`cargo new --lib` chỉ tạo bộ khung tối thiểu. Một thư viện Rust sẵn sàng xuất bản cần: README chi tiết, CHANGELOG, CI/CD, kiểm tra coverage, fuzz tests, benchmarks, ví dụ, tài liệu API và nhiều thứ khác. Việc thiết lập tất cả bằng tay tốn hàng giờ và thường bị bỏ qua.

## Giải pháp

```bash
libmake new my-library --author "Tên của bạn"
```

Một lệnh tạo:

- Cấu trúc thư mục đầy đủ.
- `Cargo.toml` với các trường metadata hoàn chỉnh.
- `README.md` với badges và phần được điền sẵn.
- `LICENSE` (Apache-2.0 hoặc MIT).
- `.github/workflows/` với CI/CD cho test, lint, coverage, release.
- `examples/`, `benches/`, `tests/` với mẫu khởi đầu.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`.

## Tính năng

- **Mẫu có thể tuỳ biến** cho các loại thư viện khác nhau (CLI, async, no_std).
- **Tích hợp Git** tự động khởi tạo kho lưu trữ và commit đầu tiên.
- **Tích hợp crates.io** với badges và metadata sẵn sàng cho việc xuất bản.

## Cài đặt

```bash
cargo install libmake
```

Mã nguồn trên [GitHub ⧉](https://github.com/sebastienrousseau/libmake) theo Apache-2.0.

## Kết luận

`libmake` không phải là một công nghệ phức tạp. Nó là một bộ sưu tập các mẫu tốt được đóng gói tiện lợi. Nhưng bằng cách loại bỏ hàng giờ công việc lặp đi lặp lại, nó cho phép các nhà phát triển dành nhiều thời gian hơn cho điều quan trọng: viết logic kinh doanh.
