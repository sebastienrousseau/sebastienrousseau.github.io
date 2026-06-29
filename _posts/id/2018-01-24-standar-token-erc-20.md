---
title: "ERC-20: antarmuka token Ethereum yang mengubah dunia"
subtitle: "Token ERC-20, smart contract Ethereum dan standardisasi aset digital."
description: "ERC-20 adalah jenis token paling umum di blockchain Ethereum, sering disebut kontrak digital smart contract yang merevolusi cara aset digital diperdagangkan."
date: "Jan 24, 2018"
language: "id-ID"
locale: "id_ID"
banner: "https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp"
banner_alt: "Laptop yang dimatikan di atas meja kayu berwarna coklat"
keywords: "ethereum, erc20, eip, token, kontrak, blockchain, mata uang kripto, smart-token, solidity"
---

![Laptop yang dimatikan di atas meja kayu berwarna coklat](https://cloudcdn.pro/stocks/images/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

> **TL;DR.** ERC-20 adalah standard token paling umum di Ethereum: sebuah antarmuka smart contract yang membuat wallet, exchange, dan aplikasi dapat memahami aset digital dengan cara yang konsisten.
>
> **Kesimpulan utama**
>
> - **Wawasan.** ERC-20 mengubah token dari implementasi khusus menjadi antarmuka bersama yang dapat diintegrasikan oleh ekosistem.
> - **Gagasan.** Fungsi seperti `transfer`, `balanceOf`, `approve`, dan `allowance` menciptakan bahasa umum untuk token Ethereum.
> - **Dampak.** Standard ini mempercepat ICO, DeFi, stablecoin, governance token, dan integrasi exchange.
> - **Insentif.** Developer, pengguna, wallet, dan marketplace mendapat manfaat dari interoperabilitas yang sama.

## Wawasan

ERC-20 penting karena menyederhanakan cara aset digital dibuat dan digunakan di Ethereum. Sebelum ada standard bersama, setiap token dapat memiliki fungsi dan perilaku berbeda, sehingga wallet dan exchange harus membangun integrasi khusus untuk setiap proyek.

Dengan ERC-20, token memiliki antarmuka yang dapat diprediksi. Aplikasi dapat membaca saldo, mengirim token, dan memberi izin pengeluaran tanpa memahami seluruh logika internal smart contract. Inilah yang membuat token Ethereum mudah dipakai ulang di banyak layanan.

## Gagasan

ERC-20 mendefinisikan sekumpulan fungsi dan event dasar. `totalSupply` menunjukkan jumlah token beredar, `balanceOf` membaca saldo alamat, `transfer` memindahkan token, sedangkan `approve` dan `allowance` memungkinkan aplikasi pihak ketiga memindahkan token atas izin pemilik.

Model izin ini menjadi dasar banyak aplikasi DeFi. Pengguna dapat memberi smart contract hak untuk menggunakan sejumlah token tertentu, misalnya untuk swap, lending, staking, atau pembayaran otomatis. Namun desain ini juga menuntut kehati-hatian karena approval yang terlalu luas dapat menjadi risiko keamanan.

## Dampak

ERC-20 mempercepat lahirnya ekonomi token. Proyek dapat menerbitkan aset digital yang langsung kompatibel dengan wallet, block explorer, exchange, dan aplikasi. Efek jaringan ini membuat Ethereum menjadi platform utama untuk eksperimen tokenisasi.

Dampaknya terlihat pada ICO, stablecoin, governance token, dan protokol DeFi. Banyak inovasi keuangan on-chain menjadi mungkin karena token dapat dipindahkan, disimpan, dan digabungkan secara konsisten di berbagai smart contract.

## Insentif

ERC-20 menciptakan insentif kuat untuk standardisasi. Developer token mendapat akses langsung ke infrastruktur Ethereum. Wallet dan exchange dapat mendukung ribuan token tanpa menulis integrasi dari nol. Pengguna mendapat pengalaman yang lebih konsisten ketika mengelola aset.

Standard ini juga memberi dasar bagi komposabilitas: satu token dapat digunakan sebagai jaminan, alat governance, reward, atau unit pembayaran di banyak aplikasi. Semakin banyak layanan yang mendukung ERC-20, semakin besar nilai mengikuti standard tersebut.

ERC-20 bukan standard sempurna. Masalah seperti approval risk, transaksi yang gagal karena alamat kontrak, dan phishing tetap ada. Namun sebagai antarmuka bersama, ERC-20 menjadi salah satu kontribusi paling penting Ethereum terhadap ekosistem aset digital.
