---
title: 'KyberLib: lá chắn Rust chống các mối đe doạ lượng tử'
subtitle: 'Triển khai Rust an toàn và nhanh của ML-KEM (FIPS 203)'
description: 'KyberLib — triển khai Rust thuần tuý của CRYSTALS-Kyber (ML-KEM/FIPS 203) được tối ưu hoá cho hiệu năng, tính di động và an toàn bộ nhớ.'
date: 'November 28, 2023'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/kyberlib-banner.webp'
banner_alt: 'Biểu ngữ KyberLib'
keywords: 'KyberLib, Rust, CRYSTALS-Kyber, ML-KEM, FIPS 203, hậu lượng tử, mật mã, mã nguồn mở'
---

![Biểu ngữ KyberLib](https://cloudcdn.pro/stocks/images/kyberlib-banner.webp).class=\"img-fluid clearfix\"

> **TL;DR.** `kyberlib` là triển khai Rust thuần tuý của CRYSTALS-Kyber (ML-KEM, FIPS 203). Nó cung cấp một API đơn giản, an toàn bộ nhớ cho mã hoá khoá kháng lượng tử, được thiết kế cho các ứng dụng tài chính và bảo mật.
>
> **Điểm chính**
>
> - **Ý tưởng.** Một triển khai Rust 100% (không có mã C hoặc unsafe) của ML-KEM.
> - **Đổi mới.** Hỗ trợ Kyber-512, Kyber-768 và Kyber-1024 — bao gồm cả các mức bảo mật khác nhau.
> - **Trường hợp sử dụng.** Tích hợp vào TLS, các giao thức thanh toán, VPN, các kênh truyền thông an toàn.
> - **Tác động.** Nền tảng cho xác thực thanh toán kháng lượng tử.

## Bối cảnh

### Vì sao Rust cho mật mã

Mật mã đòi hỏi hiệu năng cao và tuyệt đối không có lỗi bảo mật. Rust mang lại an toàn bộ nhớ mà không cần garbage collection và hiệu năng ngang với C. Các triển khai Rust đã trở thành tiêu chuẩn vàng cho thư viện mật mã mới.

## API

```rust
use kyberlib::*;

// Tạo cặp khoá
let mut rng = rand::thread_rng();
let keypair = keypair(&mut rng)?;

// Đóng gói (Alice ↔ Bob)
let (ciphertext, shared_secret_a) = encapsulate(&keypair.public, &mut rng)?;
let shared_secret_b = decapsulate(&ciphertext, &keypair.secret)?;

assert_eq!(shared_secret_a, shared_secret_b);
```

## Tính năng

- **Triển khai Rust 100%.** Không có mã C, không có unsafe.
- **Hỗ trợ tất cả các mức tham số** Kyber-512/768/1024.
- **Hằng số thời gian** để phòng chống tấn công kênh phụ.
- **`no_std`-tương thích** cho các môi trường nhúng.
- **Kiểm thử rộng rãi** chống lại các vector kiểm thử NIST.

## Tích hợp

`kyberlib` được thiết kế để dễ tích hợp:

```toml
[dependencies]
kyberlib = "0.0.3"
```

## Trường hợp sử dụng

- **TLS hybrid.** Kết hợp Kyber với X25519 cho phòng vệ chiều sâu.
- **Lưu trữ an toàn.** Mã hoá hồ sơ với khoá kháng lượng tử.
- **Giao tiếp ngang hàng.** Các kênh được mã hoá đầu cuối giữa các nút.
- **Thanh toán an toàn lượng tử.** Xác thực các yêu cầu thanh toán với khoá kháng lượng tử.

## Mã nguồn

Mã nguồn trên [GitHub ⧉](https://github.com/sebastienrousseau/kyberlib) theo Apache-2.0.

## Kết luận

`kyberlib` cung cấp một thư viện Rust nhỏ, tập trung cho CRYSTALS-Kyber. Bằng cách đóng gói tiêu chuẩn NIST trong một API Rust sạch sẽ, nó cho phép các nhà phát triển tích hợp mật mã kháng lượng tử vào các ứng dụng của họ mà không cần trở thành chuyên gia về mạng tinh thể.
