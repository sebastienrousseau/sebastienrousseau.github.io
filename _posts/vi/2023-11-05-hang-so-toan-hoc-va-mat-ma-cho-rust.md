---
title: 'Hằng số toán học và mật mã cho bảo mật Rust'
subtitle: 'Một thư viện Rust cho các hằng số có độ chính xác cao'
description: 'cmn — thư viện Rust cung cấp các hằng số toán học và mật mã với độ chính xác cao cho các ứng dụng tài chính và bảo mật.'
date: 'November 5, 2023'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/getty-images-dqHskSJDfe4.webp'
banner_alt: 'Hình ảnh trừu tượng của các hằng số toán học'
keywords: 'Rust, hằng số toán học, mật mã, cmn, độ chính xác cao, tài chính, bảo mật'
---

![Hằng số toán học](https://cloudcdn.pro/stocks/images/getty-images-dqHskSJDfe4.webp).class=\"img-fluid clearfix\"

> **TL;DR.** `cmn` là thư viện Rust tập trung các hằng số toán học và mật mã thường dùng — pi, e, các hằng số mật mã NIST, các giá trị tài chính — với độ chính xác và cách trình bày nhất quán.
>
> **Điểm chính**
>
> - **Ý tưởng.** Một nguồn duy nhất cho các hằng số được sử dụng trong tài chính và mật mã.
> - **Đổi mới.** Hỗ trợ cả `f64` cho hiệu năng và các loại số học có độ chính xác tuỳ ý.
> - **Trường hợp sử dụng.** Tính toán tài chính, mật mã, kỹ thuật khoa học.
> - **Tác động.** Giảm lỗi do hằng số sai lệch giữa các phần khác nhau của một dự án.

## Bối cảnh

Trong các dự án tài chính và mật mã, hằng số đúng là quan trọng. Một số sai lệch ở chữ số thứ 15 có thể trở thành lỗi quyết toán hàng triệu đô la khi nhân lên. `cmn` cung cấp các hằng số được trích từ các nguồn chính thức (NIST, IEEE, ISO).

## Hằng số được hỗ trợ

- **Toán học cơ bản.** π, e, φ (tỉ lệ vàng), √2.
- **Mật mã.** Các điểm generator NIST P-256/P-384/P-521, các số nguyên tố Curve25519.
- **Tài chính.** Năm tính toán theo ngày (365, 360, 365.25, ACT/ACT).
- **Vật lý.** Hằng số Planck, tốc độ ánh sáng (cho tính toán đồng hồ nguyên tử).

## Sử dụng

```rust
use cmn::constants::*;

let circumference = 2.0 * PI * radius;
let interest = principal * rate * days as f64 / DAY_COUNT_ACT_365;
```

## Cài đặt

```toml
[dependencies]
cmn = "0.0.1"
```

Mã nguồn trên [GitHub ⧉](https://github.com/sebastienrousseau/cmn) theo Apache-2.0.

## Kết luận

`cmn` là một thư viện nhỏ giải quyết một vấn đề nhỏ nhưng quan trọng. Bằng cách tập trung các hằng số vào một nguồn được kiểm chứng, nó loại bỏ một loại lỗi tinh tế nhưng nguy hiểm trong phần mềm tài chính và mật mã.
