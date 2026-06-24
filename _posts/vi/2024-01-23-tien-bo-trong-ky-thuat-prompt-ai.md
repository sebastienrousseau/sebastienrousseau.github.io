---
title: 'Tiến bộ trong kỹ thuật prompt AI'
subtitle: 'Khoa học của việc giao tiếp với các mô hình ngôn ngữ lớn'
description: 'Kỹ thuật prompt đã trưởng thành thành một ngành kỹ thuật riêng. Các kỹ thuật mới — CoT, ReAct, RAG — giúp tối đa hoá giá trị từ các LLM.'
date: 'January 23, 2024'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/circuit_board_cityscape.webp'
banner_alt: 'Sơ đồ trừu tượng của các kỹ thuật prompt'
keywords: 'kỹ thuật prompt, LLM, chain of thought, ReAct, RAG, few-shot, GPT, Claude'
---

![Kỹ thuật prompt](https://cloudcdn.pro/stocks/images/circuit_board_cityscape.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Kỹ thuật prompt đã chuyển từ thử-và-sai sang một ngành kỹ thuật có phương pháp. Các kỹ thuật mới — Chain-of-Thought, ReAct, Retrieval-Augmented Generation — cải thiện đáng kể hiệu quả của LLM cho các tác vụ phức tạp.
>
> **Điểm chính**
>
> - **Chain-of-Thought (CoT).** Yêu cầu mô hình "suy nghĩ từng bước" cải thiện độ chính xác trên các bài toán nhiều bước.
> - **ReAct.** Kết hợp lý luận và hành động — gọi công cụ, tra cứu thông tin.
> - **RAG.** Tăng cường LLM bằng tài liệu cụ thể của miền để giảm hallucination.
> - **Few-shot.** Cung cấp ví dụ trong prompt cho mô hình học mô hình.

## Bối cảnh

### Vì sao prompt quan trọng

Cùng một LLM có thể đưa ra các câu trả lời khác nhau đáng kể tuỳ thuộc vào cách đặt câu hỏi. Kỹ thuật prompt là nghệ thuật và khoa học của việc tạo ra các đầu vào tối đa hoá khả năng của mô hình.

## Các kỹ thuật cốt lõi

### Chain-of-Thought (CoT)

Yêu cầu mô hình suy luận từng bước trước khi trả lời:

```
Hỏi: Nếu tôi có 23 quả táo và ăn 7, sau đó mua thêm 12, tôi có bao nhiêu quả?

Hãy suy nghĩ từng bước:
```

CoT cải thiện đáng kể độ chính xác trên các bài toán nhiều bước, đặc biệt là toán và lập luận.

### Few-Shot Learning

Cung cấp các ví dụ trong prompt:

```
Phân loại các đánh giá:

"Sản phẩm tuyệt vời!" → Tích cực
"Thất vọng nặng nề." → Tiêu cực
"Bình thường, không có gì đặc biệt." → Trung tính
"Vượt quá mong đợi!" → ?
```

### ReAct (Reason + Act)

Kết hợp lý luận và hành động, ví dụ gọi công cụ:

```
Suy nghĩ: Tôi cần biết tỉ giá hiện tại.
Hành động: search("USD to EUR exchange rate")
Quan sát: 0.92 EUR/USD
Suy nghĩ: 100 USD = 92 EUR
Trả lời: 92 EUR
```

### Retrieval-Augmented Generation (RAG)

Tăng cường LLM bằng tài liệu được lấy động:

1. Người dùng đặt câu hỏi.
2. Hệ thống lấy các tài liệu liên quan từ cơ sở tri thức.
3. Tài liệu được chèn vào prompt cùng với câu hỏi.
4. LLM trả lời dựa trên các tài liệu được cung cấp.

RAG giảm đáng kể hallucination cho các câu hỏi cụ thể của miền.

## Các kỹ thuật nâng cao

### Self-Consistency

Hỏi LLM cùng câu hỏi nhiều lần và lấy phiếu đa số. Cải thiện độ chính xác trên các tác vụ lập luận.

### Tree-of-Thoughts (ToT)

Mở rộng CoT bằng cách khám phá nhiều nhánh suy luận và chọn nhánh tốt nhất.

### Prompt Chaining

Phân chia một tác vụ phức tạp thành nhiều prompt nhỏ, đầu ra của một prompt là đầu vào của prompt tiếp theo.

## Trường hợp sử dụng ngân hàng

- **Phân loại tài liệu.** Phân loại email khách hàng vào các danh mục.
- **Trích xuất thực thể.** Trích xuất các điều khoản chính từ hợp đồng.
- **Tóm tắt.** Tóm tắt các báo cáo dài thành các điểm nổi bật.
- **Hỗ trợ khách hàng.** Trả lời các câu hỏi với RAG trên cơ sở kiến thức nội bộ.

## Kết luận

Kỹ thuật prompt là một kỹ năng quan trọng cho năm 2024 và xa hơn. Cùng một LLM có thể là một công cụ tầm thường hoặc một đối tác mạnh mẽ tuỳ thuộc vào cách bạn giao tiếp với nó. Đầu tư vào năng lực này — qua đào tạo, công cụ và quy trình — sẽ phân biệt các tổ chức áp dụng AI thành công với những tổ chức thất bại.
