---
title: 'Tiêu chuẩn token ERC-20'
subtitle: 'Giao diện token Ethereum đã thay đổi thế giới'
description: 'ERC-20 đã chuẩn hoá việc tạo token trên Ethereum, mở khoá hàng nghìn dự án và nền tảng cho stablecoin, DeFi và token hoá tài sản thực.'
date: 'January 24, 2018'
language: 'vi-VN'
locale: 'vi_VN'
banner: 'https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp'
banner_alt: 'Một chiếc máy tính xách tay tắt nguồn trên bàn gỗ nâu'
keywords: 'ERC-20, Ethereum, token, hợp đồng thông minh, DeFi, stablecoin, USDC, token hoá tài sản'
---

![Máy tính xách tay trên bàn gỗ](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

> **TL;DR.** ERC-20 là tiêu chuẩn token có thể thay thế trên Ethereum. Bằng cách định nghĩa một giao diện chung (transfer, approve, balanceOf...), nó đã mở khoá hàng chục nghìn dự án token, tạo nền tảng cho stablecoin, DeFi và token hoá tài sản thực.
>
> **Điểm chính**
>
> - **Ý tưởng.** Một bộ sáu hàm bắt buộc và ba sự kiện cho phép bất kỳ token nào tương tác với ví, sàn giao dịch và hợp đồng khác.
> - **Tác động.** USDC, USDT, UNI và phần lớn các token DeFi tuân theo ERC-20. Khả năng tương tác đã trở thành tài sản chiến lược.
> - **Đổi mới.** ERC-20 mở đường cho ERC-721 (NFT), ERC-1155 (token đa loại) và ERC-4626 (kho lưu trữ token hoá).
> - **Hạn chế.** Không hỗ trợ giao dịch gốc; chuyển token đòi hỏi ETH cho phí gas. Các biến thể như ERC-777 cố gắng cải thiện điều này.

## Phân tích

### Vì sao chuẩn hoá quan trọng

Trước ERC-20, mỗi token trên Ethereum có giao diện riêng. Một ví hỗ trợ Token A không nhất thiết hỗ trợ Token B. Một sàn giao dịch phải viết mã tích hợp riêng cho từng token. ERC-20 đã giải quyết điều này bằng một giao diện chung.

## Đặc tả

### Sáu hàm bắt buộc

```solidity
function totalSupply() external view returns (uint256);
function balanceOf(address account) external view returns (uint256);
function transfer(address to, uint256 amount) external returns (bool);
function allowance(address owner, address spender) external view returns (uint256);
function approve(address spender, uint256 amount) external returns (bool);
function transferFrom(address from, address to, uint256 amount) external returns (bool);
```

### Hai sự kiện

```solidity
event Transfer(address indexed from, address indexed to, uint256 value);
event Approval(address indexed owner, address indexed spender, uint256 value);
```

Đó là toàn bộ tiêu chuẩn. Sự đơn giản này chính là điểm mạnh.

## Tác động

### Hệ sinh thái mà ERC-20 đã tạo ra

- **Stablecoin.** USDC và USDT — hai token được giao dịch nhiều nhất theo khối lượng trên toàn bộ thị trường tiền mã hoá — đều là ERC-20.
- **DeFi.** Các giao thức như Uniswap, Aave và Compound xây dựng trên giả định rằng các token tuân thủ ERC-20.
- **Token hoá tài sản.** Cổ phần công ty, bất động sản, hàng hoá — tất cả đều có thể được đại diện bằng token ERC-20.

## Đổi mới

### Tiêu chuẩn kế thừa

- **ERC-721** chuẩn hoá token không thể thay thế (NFT), cho phép nghệ thuật số duy nhất và sưu tập.
- **ERC-1155** kết hợp token có thể thay thế và không thể thay thế trong một hợp đồng duy nhất, tiết kiệm gas.
- **ERC-4626** chuẩn hoá kho lưu trữ token hoá cho các giao thức lợi suất.

## Hạn chế

### Những gì ERC-20 không giải quyết được

Chuyển token ERC-20 đòi hỏi ETH cho phí gas, ngay cả khi người dùng chỉ giữ stablecoin. Một số biến thể (như ERC-777) cố gắng giải quyết điều này nhưng chưa đạt được sự áp dụng rộng rãi. Lỗi lập trình trong các hợp đồng ERC-20 có thể dẫn đến mất tiền — ví dụ vụ Parity bug năm 2017.

## Kết luận

ERC-20 là một ví dụ kinh điển về việc một tiêu chuẩn đơn giản tạo ra hiệu ứng mạng khổng lồ. Sáu hàm và ba sự kiện đã định nghĩa cách các token số hoạt động trên Ethereum trong gần một thập kỷ, và bài học của nó — khả năng tương tác là tài sản chiến lược — áp dụng vượt ra ngoài blockchain.
