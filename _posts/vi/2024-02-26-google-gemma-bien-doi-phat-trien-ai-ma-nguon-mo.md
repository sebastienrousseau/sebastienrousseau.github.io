---
title: 'Google Gemma: biến đổi phát triển AI mã nguồn mở'
subtitle: 'Mô hình ngôn ngữ mở của Google cho các nhà phát triển'
description: 'Gemma là họ mô hình ngôn ngữ mở của Google, được xây dựng từ cùng nghiên cứu với Gemini. Cách nó thay đổi bối cảnh AI mã nguồn mở.'
date: 'February 26, 2024'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/gemma-banner.webp'
banner_alt: 'Logo Gemma của Google'
keywords: 'Gemma, Google, AI mã nguồn mở, LLM, Llama, Mistral, mô hình mở, phát triển'
---

![Logo Gemma](https://cloudcdn.pro/stocks/images/gemma-banner.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Gemma là họ mô hình ngôn ngữ mở của Google (2B và 7B tham số), được xây dựng từ cùng nghiên cứu và công nghệ với Gemini. Nó cho phép các nhà phát triển chạy AI cấp doanh nghiệp tại chỗ với giấy phép thân thiện với thương mại.
>
> **Điểm chính**
>
> - **Ý tưởng.** Mô hình mở chất lượng cao cho phép triển khai tại chỗ và tuỳ biến.
> - **Đổi mới.** Hiệu suất cạnh tranh với các mô hình lớn hơn nhiều.
> - **Trường hợp sử dụng.** Triển khai trên thiết bị, tinh chỉnh cụ thể của miền, xử lý dữ liệu nhạy cảm.
> - **Tác động.** Đẩy nhanh cuộc đua AI mã nguồn mở (Llama 3, Mistral, Gemma).

## Bối cảnh

### Cuộc đua AI mở

Năm 2023, Meta phát hành Llama 2 dưới giấy phép thân thiện với thương mại, khởi đầu một cuộc đua AI mã nguồn mở. Mistral của Pháp tiếp nối với các mô hình hiệu quả. Google trả lời với Gemma vào tháng 2 năm 2024.

## Các mô hình

### Gemma 2B và 7B

- **Gemma 2B.** 2 tỉ tham số, có thể chạy trên một laptop hiện đại.
- **Gemma 7B.** 7 tỉ tham số, cần một GPU 16 GB cho suy luận.

Cả hai đều có sẵn các phiên bản pre-trained và instruction-tuned.

## Hiệu suất

### Cạnh tranh trong phạm vi tham số

Gemma 7B cạnh tranh với Llama 2 13B và Mistral 7B trên hầu hết các điểm chuẩn — đạt được hiệu suất tương đương với một nửa số tham số trong một số trường hợp.

## Trường hợp sử dụng

### Triển khai cục bộ

- **Trên thiết bị.** Gemma 2B có thể chạy trên các thiết bị di động cao cấp.
- **Lưu trữ riêng.** Doanh nghiệp có thể chạy Gemma trên hạ tầng của riêng họ, đảm bảo quyền riêng tư dữ liệu.

### Tinh chỉnh

- **Cụ thể của miền.** Tinh chỉnh trên dữ liệu pháp lý, y tế, tài chính để có hiệu suất tốt hơn các mô hình đa năng.
- **Tinh chỉnh tham số hiệu quả (LoRA, QLoRA).** Tinh chỉnh trên một GPU duy nhất.

## Giấy phép

### Thân thiện với thương mại

Giấy phép Gemma cho phép sử dụng thương mại với các hạn chế hợp lý (cấm vũ khí, lạm dụng, v.v.). Đây là một lợi thế so với các mô hình có hạn chế nặng hơn.

## Cài đặt

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b-it")
model = AutoModelForCausalLM.from_pretrained("google/gemma-7b-it")

input_text = "Giải thích cơ học lượng tử cho người mới bắt đầu."
inputs = tokenizer(input_text, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0]))
```

## Tác động với ngân hàng

### Quyền riêng tư và tuỳ biến

Đối với các ngân hàng, các mô hình mở như Gemma có sức hấp dẫn đặc biệt:

- **Dữ liệu khách hàng không cần rời cơ sở.**
- **Tuỳ biến cho thuật ngữ và quy trình cụ thể.**
- **Không phụ thuộc vào nhà cung cấp** — tránh khoá nhà cung cấp.

## Triển vọng

### AI mã nguồn mở trong 2024

Khoảng cách giữa các mô hình đóng và mở đang thu hẹp. Đến cuối năm 2024, các mô hình mở 70B+ tham số có khả năng cạnh tranh với GPT-4 trên nhiều tác vụ. Đây là tin tốt cho doanh nghiệp và phát triển AI có chủ quyền.

## Kết luận

Gemma là một động thái chiến lược: Google nhận ra rằng phát triển AI mở là một mặt trận quan trọng và không muốn nhường nó cho Meta và Mistral. Đối với các tổ chức tìm kiếm các lựa chọn AI riêng tư và có thể tuỳ biến, Gemma là một bổ sung được đón chào cho hệ sinh thái.
