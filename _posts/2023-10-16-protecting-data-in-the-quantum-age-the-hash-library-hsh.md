---

# Front Matter (YAML)

author: "Sebastien Rousseau"
banner_alt: "A creative illustration on Quantum computing theme"
banner_height: "100vh"
banner_width: "100vw"
banner: "https://kura.pro/stock/images/banners/galina-nelyubova-7ej8VWfwFsg.webp"
cdn: "https://kura.pro"
changefreq: "weekly"
charset: "UTF-8"
cname: "sebastienrousseau.com"
copyright: "© Copyright 2024 - Sebastien Rousseau. All rights reserved."
date: "Oct 16, 2023"
description: "HSH uses quantum-resistant cryptographic primitives to protect your data, ensuring its security even in the face of future quantum computing advances."
format-detection: "telephone=no"
hreflang: "en"
icon: "https://kura.pro/sebastienrousseau/images/logos/sebastienrousseau.svg"
id: "https://sebastienrousseau.com/2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/index.html"
image_alt: "Black and White Portrait of Sebastien Rousseau"
image_height: "161.8"
image_width: "161.8"
image: "https://kura.pro/stock/images/banners/sebastien-rousseau.webp"
keywords: "quantum-resistant cryptography, post-quantum cryptography, hash library, HSH, password hashing, key derivation, Argon2i, Bcrypt, Scrypt, quantum computing"
language: "en-GB"
layout: "articles"
locale: "en_GB"
logo_alt: "Logo for Sebastien Rousseau"
logo_height: "44"
logo_width: "44"
logo: "https://kura.pro/sebastienrousseau/images/logos/sebastienrousseau.webp"
menu: "active"
measurementID: "G-169G4ET5HQ"
name: "Sebastien Rousseau"
permalink: "https://sebastienrousseau.com/2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/index.html"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "sebastienrousseau"
subtitle: "Open Source Software (OSS) Developer, Banking & Financial Service Professional"
tags: "quantum-resistant cryptography, post-quantum cryptography, hash library, HSH, password hashing, key derivation, Argon2i, Bcrypt, Scrypt, quantum computing"
theme-color: "0,102,204"
title: "Protecting Data in the Quantum Age: The Hash Library (HSH)"
url: "https://sebastienrousseau.com/2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/index.html"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"

# RSS - The RSS feed front matter (YAML).
atom_link: "https://sebastienrousseau.com/2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/rss.xml"
category: "Technology"
docs: "https://validator.w3.org/feed/docs/rss2.html"
generator: "Shokunin 🦀 (version 0.0.23)"
item_description: "Protecting Data in the Quantum Age: The Hash Library (HSH)"
item_guid: "https://sebastienrousseau.com/2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/rss.xml"
item_link: "https://sebastienrousseau.com/2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/rss.xml"
item_pub_date: "2023-10-27T06:13+01:00"
item_title: "Protecting Data in the Quantum Age: The Hash Library (HSH)"
last_build_date: "2023-10-27T06:13+01:00"
managing_editor: "contact@sebastienrousseau.com"
pub_date: "2023-10-27T06:13+01:00"
ttl: "60"
type: "website"
webmaster: "contact@sebastienrousseau.com"

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
twitter_creator: "@wwdseb"
twitter_description: "Protecting Data in the Quantum Age: The Hash Library (HSH)"
twitter_image: "https://kura.pro/sebastienrousseau/images/logos/sebastienrousseau.webp"
twitter_image_alt: "Logo of Sebastien Rousseau"
twitter_site: "@wwdseb"
twitter_title: "Protecting Data in the Quantum Age: The Hash Library (HSH)"
twitter_url: "https://sebastienrousseau.com/2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/index.html"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://sebastienrousseau.com/2023-10-16-protecting-data-in-the-quantum-age-the-hash-library-hsh/index.html"
author_twitter: "@wwdseb"
author_location: "London, UK"
thanks: "Thanks for reading!"
site_last_updated: "2023-11-27"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "Kaishi, Kaishi Builder, Kaishi CLI, Kaishi Templates, Kaishi Themes"
site_software: "Shokunin, Rust"

---

![A creative illustration on Quantum computing theme](https://kura.pro/stock/images/banners/galina-nelyubova-7ej8VWfwFsg.webp).class=\"img-fluid clearfix\"

In this article, I will examine the uses of quantum-resistant cryptography, specifically addressing the Rust Hash Library (HSH) that I developed. This library is fully optimised for cryptographic hashing and verification functions.

## Insight

### The Emerging Threat of Quantum Computing

As the digital landscape evolves, financial services organisations must embrace new technologies to remain competitive. Failure to do so could result in being left behind, as digital transformation is impacting every industry.

Quantum computing heralds a groundbreaking shift, offering the power to catalyse significant advancements across diverse sectors, including Banking and Financial Services. Yet, it is accompanied by a formidable risk to digital security, given its ability to decrypt even the most complex codes.

Quantum computing makes some traditional encryption techniques obsolete, as they can solve mathematical problems classical computers can't.

In today's context, Alice and Bob can communicate securely using cryptographic keys, preventing Eve from decoding the messages. But, the absolute security of key distribution and storage can never be entirely guaranteed. As a result, quantum computers pose a significant threat to encryption and digital security.

#### Secure Yet Vulnerable: Navigating Cryptographic Challenges in the Quantum Era

![Sequence Diagram][01].class=\"img-fluid clearfix\"

##### Legend

* *Alice to Eve - Alice sends encrypted message*
* *Eve intercepts - Eve intercepts Alice's message*
* *Eve attempts decryption - Eve tries but fails to decrypt*
* *Eve to Bob - Eve sends encrypted message to Bob*
* *Bob to Eve - Bob sends encrypted reply to Eve*
* *Eve intercepts - Eve intercepts Bob's reply*
* *Eve attempts decryption - Eve fails again to decrypt*
* *Eve to Alice - Eve sends encrypted message to Alice*

##### Explanation

###### Current encryption

The current encryption algorithms used by Alice and Bob are effective at preventing Eve from decrypting their messages. However, quantum computing poses a potential threat to the security of these algorithms.

###### Potential quantum risk

Quantum computers are much faster than traditional computers at performing certain types of calculations, including the calculations used to break some encryption algorithms. If Eve had access to a quantum computer, she could potentially break the encryption and read Alice and Bob's messages.

###### Key distribution and storage risks

Even if Alice and Bob are using strong encryption, their messages could still be compromised if the keys used to encrypt and decrypt the messages are compromised. Keys can be compromised in a number of ways, such as through theft, hacking, or social engineering attacks.

###### Need for post-quantum cryptography

Post-quantum cryptography is a new field of cryptography that is designed to be resistant to quantum attacks. Post-quantum encryption algorithms are still under development, but they have the potential to protect data from quantum attacks.

### Introducing Quantum-Resistant Cryptography

Quantum-resistant cryptography, also known as post-quantum cryptography (PQC) or quantum-safe cryptography, refers to cryptographic algorithms believed to be secure against quantum computer attacks.

Organisations must take the necessary precautions to protect their data from the dangers of quantum computing. Implementing quantum-resistant encryption and quantum entanglement strategies can provide financial services companies with an added layer of security.

* **Quantum-resistant cryptography** is a new type of encryption that can withstand attacks from quantum computers. Quantum-resistant encryption algorithms can speed up data processing and accuracy, making them a more efficient option.

* **Quantum entanglement** can be used to create quantum key distribution (QKD) systems, which can generate and distribute secure cryptographic keys over long distances. QKD systems are immune to attacks by quantum computers, making them ideal for protecting sensitive financial data.

## Idea

### The Hash Library (HSH): Pioneering Interoperability in Quantum-Resistant Cryptography

The Hash Library (HSH) provides a lightweight, efficient, and user-friendly solution for protecting data with quantum-resistant cryptography. It enables developers to use quantum-resistant algorithms in their applications without the need for a detailed understanding of the underlying cryptographic algorithms.

The library is built on the Rust programming language, renowned for its speed and efficiency, and ideally suited for cryptography, and long-term reliability.

## Impact

### The Benefits of the Quantum-Resistant Cryptographic Hash Library

The [Hash Library (HSH) ⧉][00] provides a wealth of modern cryptographic primitives, creating a strong barrier against the complexities of the quantum age. Its importance lies in protecting sensitive data in an age where quantum computing poses a significant risk to digital security.

The library offers organisations and financial institutions the highest level of protection available online with a selection of algorithms, including Argon2i, BScrypt, and Scrypt. These are password-based key derivation secure functions (PBKDFs). PBKDFs are used to convert passwords into cryptographic keys. They are designed to be slow and memory-intensive, making them difficult to crack using brute-force attacks.

Additionally, the library guarantees that not only are the results secure and efficient, but they are also perfectly suited for enterprise-level applications, extensible, and easy to use.

## Incentives

### Navigating the Quantum Computing Landscape Securely

* **Security Assurance**: Using the Hash Library (HSH), provides an assurance to organizations that their data remains secure.

* **Future-Proofing**: Adopting quantum-resistant algorithms now will safeguard organizations from potential future vulnerabilities.

* **Cost Efficiency**: The Hash Library (HSH) is open source and can be used without the need for expensive licenses or subscription fees. This makes it an attractive option to organizations that are looking to keep their costs low while still having access to secure quantum computing.

### Maintaining Consumer Trust

* **Protecting Customer Data**: Securing customer data from quantum computer attacks enhances trust in organizations' capabilities to safeguard information.

* **Compliance and Regulation Adherence**: Applying advanced cryptographic methods helps in adhering to stringent data protection laws and regulations, thereby avoiding legal consequences and fines.

### HSH: The Ultimate Quantum-Resistant Hash Library

* **Elevated Performance**: Leveraging the Rust-based [Hash Library (HSH) ⧉][00] provides security, efficiency, and performance.
Cross-Platform Consistency: The Hash Library (HSH) protects data across platforms and applications.

* **Ease of Implementation**: The Hash Library (HSH) provides developers with a tool that is easy to implement, reducing the barrier to adopting quantum-resistant algorithms.

## Conclusion

The [Hash Library (HSH) ⧉][00] provides a lightweight, efficient, and user-friendly solution for protecting data with quantum-resistant cryptography. It makes it easy for developers to upgrade their cryptographic protocols to be quantum-resistant without a deep understanding of the algorithms.

Quantum-resistant cryptography is a rapidly evolving field, and the HSH library is committed to staying ahead of the curve. The library is regularly updated with new algorithms and features to protect against emerging threats.

[The National Institute of Standards and Technology (NIST) ⧉][02] is currently defining a set of post-quantum cryptographic algorithms standards, through its [Post-Quantum Cryptography (PQC) project ⧉][03].

Protecting your data from quantum computing attacks is essential for any organisation that handles sensitive data. The [Hash Library (HSH) ⧉][00] is a powerful tool that can help you protect your data from this emerging threat.

![divider](https://kura.pro/common/images/elements/divider.svg).class=\"m-10 w-100\"

**That concludes our time together. Thank you for your time!**

If you have any questions, please don't hesitate to contact me via [LinkedIn ⧉][11] or via the [Contact page][10]. Thank you again for your time and I look forward to hearing from you.

[**❬ Back to Articles**][09]

[00]: https://crates.io/crates/hsh "The Hash Library (HSH) - Quantum-Resistant Cryptographic Hash Library for Password Hashing and Verification"
[01]: https://kura.pro/stock/diagrams/alice-bob-eve-encryption.svg "Secure Yet Vulnerable: Navigating Cryptographic Challenges in the Quantum Era"
[02]: https://www.nist.gov/ "National Institute of Standards and Technology"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography "Post-Quantum Cryptography PQC"
[09]: /articles/index.html "Back to Articles"
[10]: /contact/index.html "Contact Sebastien Rousseau"
[11]: https://www.linkedin.com/in/sebastienrousseau/ "Sebastien Rousseau on LinkedIn"
