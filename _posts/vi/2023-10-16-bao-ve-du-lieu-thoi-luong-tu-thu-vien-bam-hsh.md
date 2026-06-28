---
title: 'Bảo vệ dữ liệu thời lượng tử: thư viện băm hsh'
subtitle: 'Một thư viện Rust cho mã hoá và xác thực mật khẩu kháng lượng tử'
description: 'hsh — thư viện Rust triển khai các thuật toán băm và digest an toàn, được thiết kế với tư thế kháng lượng tử cho kỷ nguyên xác thực hậu PQC.'
date: 'October 16, 2023'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/rustlogs.webp'
banner_alt: 'Hình ảnh trừu tượng của các hàm băm mật mã'
keywords: 'hsh, Rust, băm, mật khẩu, mật mã, hậu lượng tử, Argon2, bcrypt, scrypt, an toàn'
---

![Hàm băm mật mã](https://cloudcdn.pro/stocks/images/rustlogs.webp).class=\"img-fluid clearfix\"

> **TL;DR.** `hsh` là thư viện Rust triển khai các thuật toán băm và digest an toàn cho mã hoá và xác thực mật khẩu, được thiết kế với tư thế kháng lượng tử cho kỷ nguyên xác thực hậu PQC.
>
> **Điểm chính**
>
> - **Ý tưởng.** API thống nhất trên Argon2id, bcrypt và scrypt.
> - **Bảo mật.** Lựa chọn tham số mặc định theo khuyến nghị OWASP 2023.
> - **Hiệu năng.** Tận dụng song song và SIMD nơi có sẵn.
> - **Trường hợp sử dụng.** Hệ thống xác thực, lưu trữ mật khẩu, kiểm tra tính toàn vẹn.

## Bối cảnh

### Vì sao băm mật khẩu vẫn quan trọng

Hàng chục triệu mật khẩu bị rò rỉ mỗi năm. Lưu trữ chúng dưới dạng băm an toàn là tuyến phòng thủ cuối cùng giữa các vi phạm cơ sở dữ liệu và tài khoản người dùng bị xâm phạm. Tuy nhiên, các SHA-256 cũ không đủ — các thuật toán đặc biệt cho mật khẩu là cần thiết.

## API

```rust
use hsh::Hash;

// Băm mật khẩu
let hash = Hash::argon2id("mat_khau_cua_toi")?;

// Xác minh
let ok = Hash::verify("mat_khau_cua_toi", &hash)?;
```

## Thuật toán hỗ trợ

- **Argon2id** (khuyến nghị mặc định, người chiến thắng PHC).
- **bcrypt** (kế thừa, tương thích Unix).
- **scrypt** (yêu cầu bộ nhớ, kháng phần cứng tuỳ chỉnh).

## Tư thế kháng lượng tử

Băm mật mã là một trong số ít các nguyên thuỷ vẫn an toàn trước máy tính lượng tử. Thuật toán Grover giảm độ mạnh hiệu quả của băm bằng một nửa — SHA-256 trở thành 128 bit kháng cự lượng tử, vẫn đủ. `hsh` ưu tiên các thuật toán có biên độ an toàn dư cho kỷ nguyên hậu lượng tử.

## Cài đặt

```toml
[dependencies]
hsh = "0.0.8"
```

Mã nguồn trên [GitHub ⧉](https://github.com/sebastienrousseau/hsh "hsh trên GitHub") theo Apache-2.0.

## Kết luận

`hsh` là một thư viện Rust nhỏ, tập trung cho việc băm mật khẩu an toàn. Bằng cách đóng gói các lựa chọn mặc định tốt và đảm bảo biên độ kháng lượng tử, nó cho phép các nhà phát triển xây dựng các hệ thống xác thực mà không cần trở thành chuyên gia mật mã.
