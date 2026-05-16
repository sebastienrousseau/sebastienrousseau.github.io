---
title: 'Shokunin: bộ tạo trang tĩnh dựa trên Rust nhanh nhất'
subtitle: 'Tốc độ, an toàn và đơn giản cho web hiện đại'
description: 'Shokunin là bộ tạo trang tĩnh viết bằng Rust, được tối ưu hoá cho hiệu năng, khả năng tiếp cận và SEO. Builds cực nhanh với hỗ trợ JSON-LD hạng nhất.'
date: 'October 9, 2023'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/clients/shokunin/v1/banners/banner-shokunin.svg'
banner_alt: 'Biểu ngữ Shokunin Static Site Generator'
keywords: 'Shokunin, SSG, Rust, bộ tạo trang tĩnh, hiệu năng, SEO, JSON-LD, mã nguồn mở'
---

![Biểu ngữ Shokunin](https://cloudcdn.pro/clients/shokunin/v1/banners/banner-shokunin.svg).class=\"img-fluid clearfix\"

> **TL;DR.** Shokunin là bộ tạo trang tĩnh (SSG) viết bằng Rust, được thiết kế để mang lại tốc độ build cực nhanh, an toàn bộ nhớ và hỗ trợ tích hợp cho SEO, khả năng tiếp cận và JSON-LD.
>
> **Điểm chính**
>
> - **Ý tưởng.** Một SSG đơn nhị phân, không cần Node.js, không cần dependency runtime.
> - **Đổi mới.** Tự động sinh JSON-LD, sitemap, RSS/Atom và metadata SEO từ frontmatter.
> - **Trường hợp sử dụng.** Blog, trang doanh nghiệp, tài liệu, microsite cần xếp hạng tốt và tải nhanh.
> - **Tác động.** Builds 10-100x nhanh hơn các SSG dựa trên Node phổ biến.

## Bối cảnh

### Vì sao một SSG khác

Có hàng chục SSG đã tồn tại — Jekyll, Hugo, Eleventy, Next.js, Gatsby. Hầu hết đều có vấn đề: phụ thuộc nặng nề, builds chậm hoặc thiếu SEO tích hợp. Shokunin được sinh ra từ mong muốn có một công cụ làm tốt một việc: tạo các trang tĩnh nhanh chóng và sạch sẽ.

## Triết lý

### Tên gọi

*Shokunin* (職人) trong tiếng Nhật có nghĩa là "thợ thủ công" — một người dành cuộc đời để hoàn thiện một nghề. Tên gọi phản ánh triết lý: làm một việc, làm tốt.

## Tính năng

### Những gì Shokunin mang lại

- **Tốc độ.** Build các trang web 1.000 trang trong vài giây.
- **Đơn nhị phân.** Không cần Node.js, không cần dependency runtime.
- **SEO tích hợp.** Tự động tạo metadata, OG tags, JSON-LD, sitemap.
- **Khả năng tiếp cận.** Tuân thủ WCAG 2.1 AA mặc định.
- **Frontmatter linh hoạt.** YAML, TOML hoặc JSON.
- **Markdown mở rộng.** GitHub Flavored Markdown + ghi chú bên lề + bảng nâng cao.

## Đổi mới

### Hỗ trợ JSON-LD hạng nhất

Khác với hầu hết SSG, Shokunin tạo ra schema.org JSON-LD tự động từ frontmatter. Điều này có nghĩa các kết quả tìm kiếm phong phú (rich results) trên Google không yêu cầu cấu hình thêm.

## Sử dụng

```bash
# Cài đặt
cargo install shokunin

# Khởi tạo dự án
ssg new my-site

# Xây dựng
ssg build
```

Cấu trúc dự án đơn giản:

```text
my-site/
├── _data/
├── _layouts/
├── _posts/
├── _site/      ← đầu ra
└── config.toml
```

## Trường hợp sử dụng

- **Blog kỹ thuật** cần tải nhanh và SEO tốt.
- **Trang tài liệu** cho các thư viện mã nguồn mở.
- **Microsite chiến dịch** với chu kỳ xuất bản nhanh.
- **Trang cá nhân** muốn đơn giản và bền vững.

## Mã nguồn

Shokunin được phát hành theo giấy phép Apache-2.0. Mã nguồn có sẵn trên [GitHub ⧉](https://github.com/sebastienrousseau/shokunin "Shokunin trên GitHub").

## Kết luận

Shokunin không cố gắng làm mọi thứ. Nó cố gắng làm tốt một việc: tạo các trang tĩnh nhanh, sạch và thân thiện với SEO. Đó là triết lý *shokunin* — sự thuần thục thông qua sự tập trung.
