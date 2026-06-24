---
title: 'Tối ưu phân tích tỉ lệ tín dụng với IBM Qiskit và biến đổi Fourier lượng tử'
subtitle: 'Một thuật toán lượng tử cho rủi ro tín dụng nhanh hơn'
description: 'Cách IBM Qiskit và biến đổi Fourier lượng tử định hình lại phân tích tỉ lệ tín dụng trong tài chính, mang lại độ chính xác và tốc độ chưa từng có.'
date: 'January 8, 2024'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/rustlogs.webp'
banner_alt: 'Sơ đồ mạch lượng tử với cửa Fourier'
keywords: 'IBM Qiskit, QFT, biến đổi Fourier lượng tử, tỉ lệ tín dụng, rủi ro, tài chính, lượng tử'
---

![Mạch lượng tử với QFT](https://cloudcdn.pro/stocks/images/rustlogs.webp).class=\"img-fluid clearfix\"

> **TL;DR.** Biến đổi Fourier Lượng tử (QFT) là nền tảng của nhiều thuật toán lượng tử mạnh mẽ. Trong tài chính, nó có thể tăng tốc các tính toán xác suất quan trọng cho phân tích rủi ro tín dụng.
>
> **Điểm chính**
>
> - **Cách tiếp cận.** Sử dụng QFT để ước lượng các tích phân xác suất hiệu quả.
> - **Đổi mới.** Quantum Amplitude Estimation cung cấp tăng tốc quadratically so với Monte Carlo.
> - **Trường hợp sử dụng.** Tính toán PD (xác suất vỡ nợ), Expected Loss, CVaR.
> - **Trạng thái.** Trình diễn ý tưởng trên Qiskit; lợi thế thực tế còn vài năm nữa.

## Bối cảnh

### Rủi ro tín dụng và Monte Carlo

Các ngân hàng dành phần lớn năng lực tính toán để mô phỏng Monte Carlo cho rủi ro tín dụng. Sai số của Monte Carlo cổ điển giảm như `1/√N` (N = số mẫu). QFT cho phép giảm như `1/N` — một sự tăng tốc bậc hai.

## Thuật toán

### Quantum Amplitude Estimation

Để ước lượng một xác suất `p`:

1. Mã hoá phân phối xác suất vào một thanh ghi lượng tử.
2. Áp dụng các phép quay tham số hoá kết hợp với QFT.
3. Đo và rút ra ước lượng cho `p`.

Sai số giảm theo `1/N` thay vì `1/√N` của Monte Carlo cổ điển.

## Triển khai Qiskit

```python
from qiskit_finance.applications.estimation import EuropeanCallPricing
from qiskit_algorithms import IterativeAmplitudeEstimation
from qiskit_aer.primitives import Sampler

# Cấu hình bài toán
problem = EuropeanCallPricing(
    num_state_qubits=3,
    strike_price=1.5,
    rescaling_factor=0.25,
    bounds=(0, 7),
    uncertainty_model=...,
)

# Thực thi
ae = IterativeAmplitudeEstimation(
    epsilon_target=0.01,
    alpha=0.05,
    sampler=Sampler(),
)
result = problem.evaluate(ae)
```

## Trường hợp sử dụng

### Xác suất vỡ nợ (PD)

Ước lượng PD cho một danh mục lớn liên quan đến việc tích hợp một phân phối nhiều chiều. QFT cung cấp một con đường để tăng tốc.

### Expected Loss và CVaR

Các chỉ số rủi ro phụ thuộc vào việc tích hợp các phân phối tổn thất. Quantum Amplitude Estimation áp dụng trực tiếp.

## Hạn chế

### Phần cứng hiện tại

Trên các bộ xử lý lượng tử hiện tại (NISQ), nhiễu hạn chế độ sâu mạch khả thi. Các bộ ước lượng amplitude lặp đi lặp lại cố gắng giảm thiểu điều này nhưng chưa cung cấp lợi thế lượng tử rõ ràng. FTQC (sửa lỗi đầy đủ) sẽ cần thiết cho lợi thế thực tế.

## Triển vọng

### Lộ trình

- **2024-2026.** Các trình diễn lớn hơn trên các bộ xử lý lượng tử với nhiều qubit hơn.
- **2026-2028.** Các bộ xử lý đầu tiên có sửa lỗi một phần có thể bắt đầu mang lại lợi thế cho các bài toán hẹp.
- **2028+.** FTQC có thể mở khoá lợi thế chuyển đổi cho rủi ro tín dụng.

## Kết luận

QFT và Quantum Amplitude Estimation là các công cụ mạnh mẽ trong hộp công cụ lượng tử. Chúng không sẵn sàng cho sản xuất hôm nay, nhưng các ngân hàng xây dựng năng lực trong các kỹ thuật này hôm nay sẽ ở vị trí dẫn đầu khi phần cứng trưởng thành.
