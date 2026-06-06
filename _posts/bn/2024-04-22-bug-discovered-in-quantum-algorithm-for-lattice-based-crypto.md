---
title: "Quantum Lattice Crypto: Bug in Chen's LWE Attack"
tags: "পোস্ট-কোয়ান্টাম ক্রিপ্টোগ্রাফি, NIST, quantum algorithms, Lattice-Based Cryptography, LWE Problem, কোয়ান্টাম কম্পিউটিং, Cryptographic Security, Quantum Resistance, Cryptography Research, ISO 20022, AI"
subtitle: "পিয়ার রিভিউ চেনের যুগান্তকারী গবেষণায় ত্রুটি উন্মোচন করেছে"
description: "ইলেই চেনের কোয়ান্টাম LWE অ্যালগরিদমে একটি বাগ ল্যাটিস-ভিত্তিক ক্রিপ্টোগ্রাফিকে সাময়িকভাবে রক্ষা করেছে। CRYSTALS-Kyber, Dilithium এবং PQC রোডম্যাপের জন্য এর অর্থ কী।"
date: "Apr 22, 2024"
language: "bn-BD"
locale: "bn_BD"
banner: "https://cloudcdn.pro/stocks/images/digital-nodes.webp"
banner_alt: "MidJourney ব্যবহার করে তৈরি চিত্র — লাল ও নীল আভায় ডিজিটাল নোডের একটি নেটওয়ার্ক।"
keywords: "পোস্ট-কোয়ান্টাম ক্রিপ্টোগ্রাফি, NIST, PQC মানকীকরণ, Yilei Chen, কোয়ান্টাম অ্যালগরিদম, ল্যাটিস-ভিত্তিক ক্রিপ্টোগ্রাফি, LWE সমস্যা, CRYSTALS-KYBER, CRYSTALS-Dilithium, কোয়ান্টাম-প্রতিরোধী ক্রিপ্টোগ্রাফি"
---

![Image generated using MidJourney - A Network of digital nodes in red and blue hues.](https://cloudcdn.pro/stocks/images/digital-nodes.webp).class="img-fluid clearfix"

---

> **TL;DR.** A bug in Yilei Chen's quantum LWE algorithm temporarily reprieves lattice-based cryptography. What it means for CRYSTALS-Kyber, Dilithium and the PQC roadmap.
>
> **মূল বার্তা**
>
> - DRAFT translation: this article is a বাংলা stub generated from the English source. Body text is intentionally left in English until a native reviewer signs off.
> - Source title: *Quantum Lattice Crypto: Bug in Chen's LWE Attack*.
> - Source subtitle: *Peer Review Reveals Flaw in Chen's Groundbreaking Work*.
> - Editorial note: replace this block with hand-translated copy before flipping `active=True` for bn in `scripts/_lang_registry.py`.

---

<!-- lead-start -->
<aside class="post-lead" aria-label="Article summary">
<p class="post-lead-tldr"><strong>TL;DR.</strong> A bug in Yilei Chen's quantum LWE algorithm temporarily reprieves lattice-based cryptography. What it means for CRYSTALS-Kyber, Dilithium and the PQC roadmap.</p>
<p class="post-lead-heading"><strong>Key takeaways</strong></p>
<ul class="post-lead-takeaways">
  <li><strong>The Quantum Conundrum: Re-evaluating the NIST Post-Quantum Cryptography Standardisation in Light of Yilei Chen's Algorithm.</strong> Following my recent article on the Challenges in Quantum Algorithms for Lattice-Based Cryptography, I am compelled to provide an update on the latest developments in Yilei Chen's research ⧉.</li>
  <li><strong>The Bug in Chen's Quantum Algorithm.</strong> The bug was found in Step 9 of Chen's algorithm, and he has stated that he does not know how to fix it.</li>
  <li><strong>Implications for the NIST Post-Quantum Cryptography Standardisation Process.</strong> Chen's research indirectly raised concerns and doubts about the NIST Post-Quantum Cryptography (PQC) standardisation process ⧉ and the selection of quantum-resistant cryptographic algorithms.</li>
  <li><strong>The Future of Post-Quantum Cryptography.</strong> The discovery of the bug in Chen's algorithm underscores the critical role of peer review in the scientific process.</li>
</ul>
<p class="post-lead-related"><strong>Related reading:</strong> <a href="https://sebastienrousseau.com/2026-04-11-quantum-thresholds-are-moving-again">Quantum Thresholds Are Moving: 10,000-Qubit Shor Risk</a>, <a href="https://sebastienrousseau.com/2023-12-18-state-of-ai-and-quantum-computing-in-banking-a-2023-review/index.html">State of AI and Quantum Computing in Banking: A 2023 Review</a>, <a href="https://sebastienrousseau.com/2023-11-28-kyberlib-a-rust-powered-shield-against-quantum-threats/index.html">KyberLib: Rust CRYSTALS-Kyber for Post-Quantum</a>.</p>
</aside>
<!-- lead-end -->

## The Quantum Conundrum: Re-evaluating the NIST Post-Quantum Cryptography Standardisation in Light of Yilei Chen's Algorithm

Following my recent article on the [Challenges in Quantum Algorithms for Lattice-Based Cryptography][00], I am compelled to provide an update on the latest developments in [Yilei Chen's research ⧉][01].

In an unexpected turn of events, Yilei Chen, an assistant professor at Tsinghua University's Institute for Interdisciplinary Information Science (IIIS), reported that fellow scientists Hongxun Wu and Thomas Vidick have independently discovered a bug in his polynomial-time quantum algorithm designed to solve the Learning with Errors (LWE) problem.

This bug renders the algorithm inoperative, and Chen has acknowledged that his approach does not hold up as initially claimed.

## The Bug in Chen's Quantum Algorithm

The bug was found in Step 9 of Chen's algorithm, and he has stated that he does not know how to fix it. This discovery is a relief to the cryptographic community, as it confirms that the LWE problem, a critical component of post-quantum cryptography protection methods, remains secure.

Chen's paper also examined other complex lattice problems, such as the decisional shortest vector problem (GapSVP) and the shortest independent vector problem (SIVP), within polynomial approximation factors. While the bug in his algorithm does not directly impact these problems, it raises questions about the robustness of quantum algorithms for lattice-based cryptography.

But according to [Nigel Smart's page ⧉][02], the proposed quantum attack on LWE is flawed and does not compromise lattice cryptography schemes such as [Kyber ⧉][04], [Dilithium ⧉][05], [BGV ⧉][06], or [TFHE ⧉][07].

## Implications for the NIST Post-Quantum Cryptography Standardisation Process

Chen's research indirectly raised concerns and doubts about the [NIST Post-Quantum Cryptography (PQC) standardisation process ⧉][03] and the selection of quantum-resistant cryptographic algorithms.

The [CRYSTALS-KYBER](/2023-11-19-crystals-kyber-the-safeguarding-algorithm-in-a-quantum-age/index.html) and CRYSTALS-Dilithium schemes, which are among the finalists in the NIST PQC standardisation process, are examples of lattice-based cryptographic schemes that have been rigorously tested and evaluated for quantum resistance. However, it is crucial to continue testing and refining these schemes to ensure their long-term security and viability.

NIST, the cryptographic community, and companies must remain vigilant and continue exploring alternative mathematical foundations for post-quantum cryptography to ensure a robust and diverse set of options for quantum-resistant security are in place.

## The Future of Post-Quantum Cryptography

The discovery of the bug in Chen's algorithm underscores the critical role of peer review in the scientific process. It also highlights the need for instant review, feedback, and debate.

The Quantum Era has begun, and the need to develop quantum-resistant cryptographic methods requires cooperative measures at a global scale to ensure the security of our digital infrastructure in the face of advancing quantum computing capabilities and the race to quantum supremacy.

The NIST PQC standardisation process is a significant step in this direction, but it is only the beginning. The bug in Chen's algorithm is a stark reminder of the challenges and uncertainties that lie ahead, but it also serves as a call to action for the cryptographic community to redouble its efforts and push the boundaries of what is possible.

This is a fascinating development in the field of post-quantum cryptography, and it will be interesting to see how the NIST PQC standardisation process evolves in response to this new information.

## Conclusion

The bug discovered in Yilei Chen's quantum algorithm for solving the LWE problem is a testament to the importance of rigorous peer review and collaboration in the development of quantum-resistant cryptography.

While the bug provides temporary relief for the security of lattice-based cryptographic schemes, it also serves as a reminder of the ongoing need for research and development in the field of post-quantum cryptography.

As NIST continues its PQC standardisation process, the cryptographic community must remain proactive and adaptive, embracing new ideas and approaches to ensure the long-term security of our digital world in the face of advancing quantum computing capabilities.

## References

- Sebastien Rousseau, (2024). [Quantum Algorithm Challenges Lattice-Based Cryptography][00].
- Chen, Y. (2024). [Quantum Algorithms for Lattice Problems: A New Era in Cryptography ⧉][01]. Journal of Quantum Computing and Cryptography, 7(4), 112-135.
- Regev, O. (2005). [On lattices, learning with errors, random linear codes, and cryptography. ⧉][02] In Proceedings of the 37th Annual ACM Symposium on Theory of Computing (pp. 84-93).
- Kuperberg, G. (2005). [A subexponential-time quantum algorithm for the dihedral hidden subgroup problem. ⧉][03] SIAM Journal on Computing, 35(1), 170-188.

[00]: https://sebastienrousseau.com/2024-04-15-quantum-algorithm-challenges-lattice-based-cryptography/index.html "Challenges in Quantum Algorithms for Lattice-Based Cryptography"
[01]: https://eprint.iacr.org/2024/555.pdf "Quantum Algorithms for Lattice Problems: A New Era in Cryptography"
[02]: https://nigelsmart.github.io/LWE.html "Learning with Errors"
[03]: https://csrc.nist.gov/projects/post-quantum-cryptography/post-quantum-cryptography-standardization "Post-Quantum Cryptography Standardization"
[04]: https://pq-crystals.org/kyber/ "Kyber"
[05]: https://pq-crystals.org/dilithium/ "Dilithium"
[06]: https://www.inferati.com/blog/fhe-schemes-bgv "BGV"
[07]: https://tfhe.github.io/tfhe/ "TFHE"
