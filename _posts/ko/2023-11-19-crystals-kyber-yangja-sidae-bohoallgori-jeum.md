---
title: "CRYSTALS-Kyber: 양자 시대의 방어 알고리즘"
subtitle: "NIST 선정 양자 내성 키 캡슐화 메커니즘"
description: "CRYSTALS-Kyber, NIST FIPS 203 표준, 양자 시대 암호 통신의 기반."
date: "November 19, 2023"
language: "ko-KR"
locale: "ko_KR"
banner: "https://cloudcdn.pro/stocks/images/markus-spiske-FXFz-sW0uwo-unsplash.webp"
banner_alt: "암호 키를 표현하는 매트릭스의 코드"
keywords: "CRYSTALS-Kyber, 양자 내성, 키 캡슐화, KEM, NIST PQC, 격자 기반 암호, ML-KEM, FIPS 203"
last_reviewed: "2026-05-16"
---

![암호 키를 표현하는 매트릭스의 코드](https://cloudcdn.pro/stocks/images/markus-spiske-FXFz-sW0uwo-unsplash.webp).class=\"img-fluid clearfix\"

## 통찰

### NIST가 양자 내성 KEM을 선정하다

2022년 7월, NIST는 CRYSTALS-Kyber를 최초의 표준화 양자 내성 키 캡슐화 메커니즘(KEM)으로 선정하였습니다. 2024년에는 FIPS 203 (ML-KEM)으로 최종 확정되었습니다. 이는 포스트 양자 암호의 표준화된 출발입니다.

## 아이디어

### 격자 문제의 난해함에 의존

CRYSTALS-Kyber는 Module-LWE (Learning With Errors) 문제의 난해함에 의존합니다. 이는 양자 컴퓨터와 고전 컴퓨터 모두에 대하여 안전한 것으로 여겨집니다. Shor의 알고리즘을 사용하더라도 효율적으로 해결할 수 없습니다.

## 접근 방식

### 공개키 KEM: 캡슐화와 캡슐화 해제

```rust
// 키 쌍 생성
let (pk, sk) = kem.keypair();

// 캡슐화(공개키 사용)
let (ciphertext, shared_secret_a) = kem.encapsulate(&pk);

// 캡슐화 해제(비공개키 사용)
let shared_secret_b = kem.decapsulate(&ciphertext, &sk);
assert_eq!(shared_secret_a, shared_secret_b);
```

공유된 비밀은 대칭 암호 키로 사용될 수 있습니다.

## 혁신

### 효율적 연산

Kyber-768 (NIST 보안 레벨 3)은 약 1.1 KB의 공개키, 약 1.1 KB의 암호문, 약 32바이트의 공유 비밀을 제공합니다. 연산은 고전 ECC와 동등하게 빠릅니다.

## 활용 사례

### TLS, 메시징, 결제 인증

Kyber는 TLS 1.3, Signal 메시징(하이브리드 ECC + Kyber), 결제 인증, PQC 이행을 계획 중인 기업 VPN에 이미 통합되어 있습니다.

## 규제와 정책

### 글로벌 PQC 로드맵

NIST 표준화에 따라 모든 주요 정부(미국 CNSA 2.0, 영국 NCSC, 유럽 ENISA, 호주 ASD, 중국 OSCCA)가 국가 PQC 이행 로드맵을 발표하였습니다. Kyber는 중심적 선택입니다.

## 과제

### 사이드 채널 공격

모든 암호와 마찬가지로 Kyber는 사이드 채널 공격에 대비하여 주의 깊게 구현하여야 합니다. NIST FIPS 203은 이 위험에 대응하는 표준 구현 지침을 포함하고 있습니다.

## 결론

### 양자 내성의 첫 진정한 패키지

CRYSTALS-Kyber는 양자 내성 KEM에 대한 규제와 산업의 합의를 처음으로 진정하게 구현한 결과물입니다. 모든 은행과 클라우드 제공자는 Kyber 이행 계획을 보유하여야 합니다 — 더 이상 기다릴 이유가 없습니다.
