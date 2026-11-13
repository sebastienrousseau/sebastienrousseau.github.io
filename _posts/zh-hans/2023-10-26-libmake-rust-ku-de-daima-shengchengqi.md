---
title: "LibMake：减少重复任务、构建高质量 Rust 库的代码生成器"
subtitle: "LibMake 通过强制最佳实践与生成初始代码加速 Rust 库开发，节省开发者时间与精力"
description: "LibMake 是一款 Rust 库代码生成工具，通过模板化生成减少重复劳动，强制最佳实践。"
date: "October 26, 2023"
language: "zh-Hans"
locale: "zh_CN"
banner: "https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp"
banner_alt: "巨大的白色柱子"
keywords: "LibMake, Rust 库, 代码生成器, 模板, 脚手架, 最佳实践, GitHub Actions, 开源, Cargo, CLI"
---

![巨大的白色柱子](https://cloudcdn.pro/stocks/images/tarik-haiga-3637943.webp).class=\"img-fluid clearfix\"

## 洞察

### Rust 库开发的挑战

开发 Rust 库可能颇具挑战，尤其对初学者而言。最大的挑战之一是设置高效的项目结构并编写所有必要的样板代码。这既耗时又重复，会让开发者无暇专注于库开发中更具创造性与战略性的方面。

### 使用代码生成器的好处

使用代码生成器可以通过自动生成样板代码及其他重复任务，精简 Rust 库的开发流程。这能为开发者节省大量时间与精力，让他们专注于库开发中更重要的方面——设计、实现与测试。

## 理念

### LibMake：Rust 库的代码生成器

[LibMake ⧉][00] 是一款代码生成工具，旨在通过生成一组预填写、预定义的模板文件，快速帮助创建高质量的 Rust 库。这个有主张的脚手架工具旨在大幅缩短开发时间并最小化重复任务，让你专注于业务逻辑，同时强制规范、最佳实践、一致性，并为你的库提供风格指南。

LibMake 灵活且可扩展，适用于任何规模或复杂度的库。它还支持多种配置选项，开发者可根据具体需求自定义。

### 使用 LibMake 的示例

要使用 LibMake，开发者只需运行以下命令：

```bash
libmake \
    --author "John Smith" \
    --build "build.rs" \
    --categories "['category 1', 'category 2', 'category 3']" \
    --description "A Rust library for doing cool things" \
    --documentation "https://docs.rs/my_library" \
    --edition "2021" \
    --email "john.smith@example.com" \
    --homepage "https://my_library.rs" \
    --keywords "['rust', 'library', 'cool']" \
    --license "MIT" \
    --name "my_library" \
    --output "my_library" \
    --readme "README.md" \
    --repository "https://github.com/example/my_library" \
    --rustversion "1.69.0" \
    --version "0.1.0" \
    --website "https://example.com/john-smith"
```

这会创建库的新目录，LibMake 将生成必要的样板代码与文档结构。开发者随后可向库添加自己的代码并开始开发。

## 影响

### 缩短开发时间与精力

LibMake 通过自动生成代码与其他任务，减少了开发 Rust 库所需的时间与精力。这让开发者节省时间精力，专注于设计、实现与测试等关键部分。

### 提升库的质量与可靠性

LibMake 还能通过提供遵循最佳实践的预定义模板，帮助开发者提升库的质量与可靠性。这有助于减少库中的 bug 与错误，使其更稳健可靠。

## 激励

### 强制最佳实践并生成初始代码

LibMake 可通过提供遵循最佳实践的预定义模板，帮助开发者强制最佳实践。它还能为常见库功能生成初始代码，为开发者节省大量时间。

LibMake 提供以下特性与好处：

- 通过命令行界面或提供 CSV、JSON、TOML、YAML 格式的配置文件，轻松创建 Rust 库。
- 快速生成具有预定义结构和样板代码的新库项目，可使用你自己的模板自定义。
- 生成预定义的 GitHub Actions 工作流，帮助你自动化库的开发与测试。
- 自动生成基本函数、方法与宏，让你的 Rust 库快速起步。
- 通过启动文档、测试套件和基准套件强制最佳实践与规范，让你迅速上手。

借助 LibMake，你可以在几秒钟内轻松生成新的 Rust 库代码库结构，包括所有必要的文件、布局、构建配置、代码、测试、基准、文档等。

### 立即试用 LibMake

如果你是开发者，鼓励你试用 [LibMake ⧉][00]，看看它如何帮助你简化库开发流程。LibMake 是一个免费的开源工具，可从 [GitHub 仓库 ⧉][00] 下载。

[00]: https://github.com/sebastienrousseau/libmake "LibMake：减少重复任务、构建高质量 Rust 库的代码生成器"
