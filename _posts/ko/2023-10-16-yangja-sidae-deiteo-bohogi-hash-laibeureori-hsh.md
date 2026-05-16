---
title: "양자 시대 데이터 보호: 해시 라이브러리 hsh"
subtitle: "포스트 양자 시대를 위하여 설계된 Rust 해시·다이제스트 라이브러리"
description: "hsh는 양자 내성 자세로 설계된 Rust 해시 라이브러리로, 비밀번호 암호화와 검증을 위한 것입니다."
date: "October 16, 2023"
language: "ko-KR"
locale: "ko_KR"
banner: "https://cloudcdn.pro/stocks/images/markus-spiske-iar-afB0QQw-unsplash.webp"
banner_alt: "암호화된 바이너리 데이터"
keywords: "해시, 다이제스트, 비밀번호, Rust, hsh, 양자 내성, 포스트 양자 암호, 보안"
last_reviewed: "2026-05-16"
---

![암호화된 바이너리 데이터](https://cloudcdn.pro/stocks/images/markus-spiske-iar-afB0QQw-unsplash.webp).class=\"img-fluid clearfix\"

## 통찰

### 오래된 해시는 양자 시대에 취약해진다

해시는 현대 인증의 기반입니다. MD5, SHA-1, 나아가 약한 SHA-2 변종은 고전 컴퓨터에서도 더 이상 안전하지 않습니다. 양자 컴퓨터는 현대의 모든 해시 함수의 보안 마진을 더욱 깎아 내립니다.

## 아이디어

### 감사를 거친 프리미티브만 사용하는 Rust 라이브러리

`hsh`는 신중히 선정되고 감사가 이루어진 암호 프리미티브만을 사용하는 Rust 라이브러리입니다: Argon2, bcrypt, scrypt, SHA-2, SHA-3, BLAKE3. 레거시 알고리즘은 선택할 수 없습니다.

## 혁신

### 기본값으로 메모리 하드

비밀번호 해싱에 대하여 `hsh`는 Argon2id를 기본으로 하며, 메모리 하드 방식으로 GPU와 ASIC 기반 공격에 내성을 갖습니다. 이는 양자 가속 무차별 대입 공격에 대한 미래의 방어선입니다.

## 접근 방식

### 단순, 명시적, Rust 네이티브

```rust
use hsh::password::{hash_password, verify_password};

let hash = hash_password("secret123")?;
assert!(verify_password("secret123", &hash)?);
```

## 활용 사례

### 인증과 완전성

`hsh`는 다음에 사용됩니다: 비밀번호 해싱, API 키 보관, 메시지 인증 코드, 트랜잭션 완전성 검사. 포스트 양자 시대 인증 스택의 핵심 요소입니다.

## 보안

### 감사와 투명성

라이브러리는 GitHub에 있으며, 모든 의존성을 확인하실 수 있습니다. 암호 프리미티브는 Rust 생태계의 일반적으로 감사된 크레이트(`argon2`, `bcrypt`, `sha2` 등)에서 가져오며, 자체 구현이 아닙니다.

## 결론

### 포스트 양자 인증으로의 이행

`hsh`는 인증 스택을 양자 내성 자세로 재설정할 기회를 제공합니다. 지금 이행을 시작하시기 바랍니다 — 양자 컴퓨터가 가용 상태가 될 때까지 기다리지 마십시오.
