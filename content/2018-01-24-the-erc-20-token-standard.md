---

# Front Matter (YAML)

author: "Sebastien Rousseau"
banner_alt: "Turned off laptop computer on top of brown wooden table"
banner_height: "571px"
banner_width: "1425px"
banner: "https://kura.pro/stock/images/banners/m-ZzOa5G8hSPI.webp"
cdn: "https://kura.pro"
charset: "UTF-8"
cname: "sebastienrousseau.co.uk"
copyright: "© Copyright 2023 - Sebastien Rousseau. All rights reserved."
date: "24 Jan 2018"
description: "An Ethereum's Standard Interface for Tokens"
format-detection: "telephone=no"
hreflang: "en"
icon: "https://kura.pro/sebastienrousseau/images/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.co.uk/payments/"
image_alt: "Black and White Portrait of Sebastien Rousseau"
image_height: "161.8"
image_width: "161.8"
image: "https://kura.pro/stock/images/banners/sebastien-rousseau.webp"
keywords: "ethereum, erc20, eip, tokens, contracts, blockchain, cryptocurrencies, smart-token, solidity"
language: "en-GB"
layout: "page"
locale: "en_GB"
logo_alt: "Logo for Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://kura.pro/sebastienrousseau/images/logos/sebastienrousseau.webp"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.co.uk/payments/"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "sebastienrousseau"
subtitle: "Open Source Software (OSS) Developer, Banking & Financial Service Professional"
tags: "ethereum, erc20, eip, tokens, contracts, blockchain, cryptocurrencies, smart-token, solidity"
theme_color: "rgb(0, 102, 204)"
title: "The ERC-20 Token Standard"
url: "https://sebastienrousseau.co.uk/payments/"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.co.uk/payments/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Shokunin 🦀 (version 0.0.15)"
item_description: "An Ethereum's Standard Interface for Tokens"
item_guid: "https://sebastienrousseau.co.uk/payments/rss.xml"
item_link: "https://sebastienrousseau.co.uk/payments/rss.xml"
item_pub_date: "Thu, 12 Jul 2023 20:20:20 GMT"
item_title: "The ERC-20 Token Standard"
last_build_date: "Thu, 12 Jul 2023 20:20:20 GMT"
managing_editor: "contact@sebastienrousseau.co.uk"
pub_date: "Thu, 12 Jul 2023 20:20:20 GMT"
ttl: "60"
type: "website"
webmaster: "contact@sebastienrousseau.co.uk"

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "Sebastien Rousseau"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).

msapplication-navbutton-color: "rgb(0, 102, 204)"

# Twitter Card - The Twitter Card front matter (YAML).

twitter_card: "summary"
twitter_creator: "wwdseb"
twitter_description: "An Ethereum's Standard Interface for Tokens"
twitter_image: "https://kura.pro/kaishi/images/logos/kaishi.svg"
twitter_image_alt: "Logo of Sebastien Rousseau"
twitter_site: "wwdseb"
twitter_title: "The ERC-20 Token Standard"
twitter_url: "https://sebastienrousseau.co.uk"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.co.uk"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2023-07-05"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
site_software: "Shokunin, Rust"

---

![A very tall building that has a lot of holes in it](https://kura.pro/stock/images/banners/m-ZzOa5G8hSPI.webp).class=\"img-fluid clearfix\"

## Insight

### The need for a standardized token interface

Before the advent of the ERC-20 (Ethereum Request for Comments 20) standard, the Ethereum blockchain was like the Wild West of token architectures. Each newly minted token had its own unique set of rules, functions, and interfaces. This not only presented developers with a daunting learning curve but also impeded the interoperability of tokens. Essentially, each new token was like a new language that needed to be learned, understood, and implemented. This fragmentation hindered scalability and broad adoption of tokens on the Ethereum platform.

The introduction of the ERC-20 standard acted like a unifying language, setting forth a common set of rules and functions that all Ethereum tokens must adhere to. Now, developers had a consistent interface to work with, regardless of the token in question. This standardization streamlined the token interaction processes, allowing for more seamless integration into various applications and services. As a result, developers could engage more meaningfully with tokens, fostering an environment conducive to innovation and growth within the Ethereum ecosystem.

#### The Wild West of token architectures

The Ethereum blockchain was initially designed to support a single type of token: ETH. However, as the platform grew in popularity, developers began to create their own tokens to represent a variety of assets and concepts. This led to a proliferation of different token architectures, each with its own unique set of rules and functions.

This fragmentation made it difficult for developers to create applications that could interact with multiple tokens. It also made it difficult for users to manage their token assets across different platforms.

#### The ERC-20 standard

The ERC-20 standard was introduced in 2015 to address the challenges posed by the Wild West of token architectures. The standard defines a common set of rules and functions that all Ethereum tokens must adhere to. This standardization makes it easier for developers to create applications that can interact with any ERC-20 token, and it also makes it easier for users to manage their token assets.

The ERC-20 standard has been widely adopted by the Ethereum community. Today, there are over 200,000 ERC-20 tokens in existence, and the standard is used by a wide variety of applications, including decentralized exchanges, lending platforms, and gaming dapps.

## Idea

### A common set of functions and properties for all tokens

The ERC-20 standard defines a set of six essential functions that all ERC-20 compliant tokens must implement. These functions are:

- `transfer(address to, uint256 amount)`: Transfers an amount of tokens from the caller's address to the specified address.
- `approve(address spender, uint256 amount)`: Approves the specified address to spend an amount of tokens on behalf of the caller.
- `allowance(address owner, address spender)`: Returns the amount of tokens that the specified spender is approved to spend on behalf of the specified owner.
- `totalSupply()`: Returns the total number of tokens in circulation.
- `balanceOf(address owner)`: Returns the number of tokens owned by the specified address.
- `name()`: Returns the name of the token.
- `symbol()`: Returns the symbol of the token.

The ERC-20 standard also defines two events that must be emitted upon the successful execution of corresponding functions. These events are:

- `Transfer(address from, address to, uint256 amount)`: Emitted when an amount of tokens is transferred from one address to another.
- `Approval(address owner, address spender, uint256 amount)`: Emitted when the specified address is approved to spend an amount of tokens on behalf of the specified owner.

## Impact

### The growth of DeFi and Ethereum adoption

The ERC-20 standard has had a significant impact on the Ethereum ecosystem. It has been a key enabler of the DeFi (Decentralized Finance) movement, and it has also helped to increase the adoption of Ethereum.

DeFi platforms, which offer a range of financial services from lending to asset management, heavily rely on tokens to facilitate transactions. With ERC-20 acting as a universal adapter, it has been far easier for DeFi applications to incorporate a wide array of tokens without having to tailor their code for each one.

The ERC-20 standard has also made it easier for users to manage their token assets. With tokens adhering to the same basic rules, users find it easier to transfer, spend, and manage their token assets across multiple platforms. This heightened user experience has been a driving factor in Ethereum's increased adoption rates.

## Incentive

### Reduced development costs and improved security

The standardization brought about by the ERC-20 protocol has had a direct economic impact as well. By providing a tested and community-approved blueprint for token creation, it has significantly reduced the barriers to entry for developers. They can now create a new token with reduced developmental costs and a faster time-to-market, as they no longer have to reinvent the wheel. The standard also indirectly encourages the creation of DApps (Decentralized Applications) and services that can universally interact with any ERC-20 token, thereby fostering a more vibrant ecosystem.

Another notable benefit is that of enhanced security. The ERC-20 standard has undergone rigorous scrutiny by the Ethereum community, making it a robust and secure model for token implementation. Adherence to this standard implies that the fundamental aspects of the token's smart contract adhere to community-accepted best practices. This minimizes the risk of security vulnerabilities that could otherwise result from an improperly designed token model. While it is not a guarantee against all types of vulnerabilities, it is a significant step toward ensuring the overall security of tokens and by extension, the projects that utilize them.