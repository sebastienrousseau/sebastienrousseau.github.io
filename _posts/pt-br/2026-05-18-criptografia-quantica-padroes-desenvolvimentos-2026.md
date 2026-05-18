---
title: "O reset da criptografia quântica em 2026: padrões PQC, garantia de QKD e o trabalho de migração que os bancos não podem adiar"
subtitle: "A criptografia quântica passou da prospecção à disciplina de implementação: os padrões NIST PQC estão prontos, a orientação do NCSC britânico estreitou as escolhas de algoritmos, o trabalho protocolar do IETF ainda amadurece, e a garantia de QKD passa da confiança de laboratório para a linguagem de certificação."
description: "A criptografia quântica em 2026 não é mais um debate sobre a iminência dos computadores quânticos. É um programa de migração que atravessa criptografia pós-quântica, cripto-agilidade, garantia de distribuição quântica de chaves, padrões de protocolo, prontidão de fornecedores e dados financeiros de longa duração já expostos ao risco «harvest-now-decrypt-later»."
date: "May 18, 2026"
language: "pt-BR"
locale: "pt_BR"
banner: "https://cloudcdn.pro/stock/images/alex-shuper-YYZnrK8NrSw-unsplash.webp"
banner_alt: "Mapa de migração para criptografia resistente ao quântico em 2026 — padrões NIST PQC, trabalho sobre protocolos híbridos, garantia de QKD, cripto-agilidade e níveis de risco de dados bancários"
keywords: "criptografia quântica 2026, criptografia pós-quântica, NIST FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC PQC, IETF TLS, IPsec, RFC 9794, troca de chaves híbrida, QKD, ETSI QKD, ISO IEC 23837, cripto-agilidade, harvest now decrypt later, HNDL, criptografia para serviços financeiros, segurança bancária"
tags: "criptografia quântica, criptografia pós-quântica, PQC, NIST, FIPS 203, FIPS 204, FIPS 205, ML-KEM, ML-DSA, SLH-DSA, NCSC, IETF, TLS, IPsec, QKD, ETSI, cripto-agilidade, HNDL, segurança bancária"
item_title: "O reset da criptografia quântica em 2026: padrões PQC, garantia de QKD e o trabalho de migração que os bancos não podem adiar"
item_description: "O reset da criptografia quântica 2026 — padrões NIST PQC, recomendações de migração do NCSC, prontidão protocolar do IETF, garantia de QKD, cripto-agilidade e o que os bancos devem priorizar esta semana."
twitter_title: "Criptografia quântica 2026: padrões PQC e migração bancária"
twitter_description: "O reset da criptografia quântica 2026 — padrões NIST PQC, recomendações de migração do NCSC, prontidão protocolar do IETF, garantia de QKD, cripto-agilidade e o que os bancos devem priorizar esta semana."
---

# O reset da criptografia quântica em 2026: padrões PQC, garantia de QKD e o trabalho de migração que os bancos não podem adiar

A criptografia quântica em 2026 dividiu-se em duas trilhas práticas. A criptografia pós-quântica é agora um programa de implementação, porque o NIST afirma que três padrões pós-quânticos estão prontos para uso e que os sistemas federais devem tratá-los como padrões FIPS ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")); a distribuição quântica de chaves está se tornando um problema de garantia e certificação, porque as implantações de QKD precisam de linguagem de avaliação, perfis de proteção e padrões operacionais, e não apenas de demonstrações de laboratório ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publica perfil de proteção QKD")).

---

> **Resumo executivo / Principais conclusões**
>
> - **O NIST levou a PQC à fase de implementação.** Os padrões atuais são FIPS 203 para estabelecimento de chaves ML-KEM, FIPS 204 para assinaturas ML-DSA e FIPS 205 para assinaturas SLH-DSA; o NIST insta as organizações a identificar a criptografia vulnerável e iniciar a migração já ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")).
> - **O NCSC britânico estreitou as escolhas práticas.** Recomenda ML-KEM-768 e ML-DSA-65 para a maioria dos casos de uso, alertando que os sistemas devem se apoiar em implementações robustas dos padrões finais em vez de experimentos compatíveis com rascunhos ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos passos para preparar a PQC")).
> - **A prontidão protocolar é desigual.** O IETF está atualizando TLS e IPsec para PQC e troca de chaves híbrida, mas o NCSC adverte que sistemas operacionais devem preferir RFCs publicados em vez de Internet Drafts em movimento ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos passos para preparar a PQC")).
> - **O híbrido é um mecanismo de transição, não um estado-final.** Esquemas híbridos de chave pública mais pós-quântico ajudam a faseamento da migração e cobrem risco de implementação, mas adicionam complexidade e podem exigir uma segunda migração para somente-PQC mais tarde ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos passos para preparar a PQC")).
> - **QKD não é substituto da PQC.** QKD pode servir para enlaces especializados de alta garantia, mas sua relevância bancária depende de certificação, interoperabilidade, custo operacional e integração com sistemas existentes de gestão de chaves, não da física isolada ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publica perfil de proteção QKD")).
> - **A pergunta no nível do banco é o inventário.** Uma instituição financeira que não localiza RSA, ECDH, ECDSA, EdDSA, criptografia proprietária de VPN, templates HSM, tempos de vida de certificados e criptografia gerenciada por fornecedores não pode migrar, sejam quais forem os padrões disponíveis.
> - **O risco já está vivo.** Ataques harvest-now-decrypt-later tornam dados financeiros de longa duração vulneráveis antes da existência de computadores quânticos criptograficamente relevantes, porque o adversário só precisa coletar o cifrado hoje.
> - **A cripto-agilidade é o controle duradouro.** A arquitetura vencedora não é uma troca pontual de RSA para ML-KEM; é uma capacidade da plataforma de rotacionar algoritmos, parâmetros, bibliotecas, certificados, políticas de hardware e modos de protocolo sem reconstruir o banco.
>
---

## Por que esta semana importa

A conversa sobre padrões passou do ponto da abstração. A orientação pública do NIST diz que as organizações devem começar a aplicar os novos padrões agora, identificar onde algoritmos vulneráveis são usados e planejar atualizações de produtos, serviços e protocolos ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Essa linguagem importa porque transforma a PQC de um tema de pesquisa em uma dependência de renovação tecnológica.

O calendário também importa porque os dados financeiros têm uma meia-vida de confidencialidade longa. Materiais de M&A, fluxos de tesouraria, investigações de sanções, documentos de identidade de clientes, metadados de roteamento de pagamentos e registros de liquidação wholesale podem permanecer sensíveis por anos. O computador quântico que quebra a criptografia clássica de chave pública não precisa existir hoje para que a exposição seja racional hoje.

## A base criptográfica 2026: quatro frentes de trabalho

### 1. Os padrões PQC estão prontos o suficiente para se planejar

A primeira base é algorítmica. O programa PQC do NIST oferece agora aos líderes de tecnologia alvos nomeados: ML-KEM para estabelecimento de chaves, ML-DSA para assinaturas digitais gerais e SLH-DSA para assinaturas baseadas em hash ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos passos para preparar a PQC")). O impacto prático é que as equipes de compras, arquitetura e gestão de fornecedores podem parar de perguntar se padrões PQC existirão e começar a perguntar quando cada sistema os apoiará.

O ponto mais delicado é a compatibilidade. O NCSC adverte que implementações baseadas em rascunhos podem não ser compatíveis com os padrões finais, exatamente o tipo de detalhe que descarrila migrações em grandes bancos se ignorado ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos passos para preparar a PQC")). Os bancos devem, portanto, separar pilotos experimentais de trajetórias de migração em produção.

### 2. Os protocolos são o gargalo

Os algoritmos por si só não protegem o tráfego bancário. TLS, IPsec, SSH, S/MIME, APIs de pagamentos, integrações HSM e pilhas de gestão de certificados precisam de suporte em nível de protocolo. O NCSC afirma que o IETF está atualizando protocolos amplamente usados como TLS e IPsec para que algoritmos PQC possam ser incorporados aos mecanismos de troca de chaves e assinatura ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos passos para preparar a PQC")).

Isso cria um problema de implementação faseada. Um banco pode inventariar criptografia imediatamente, exigir roadmaps de fornecedores imediatamente e projetar cripto-agilidade imediatamente, mas pode ainda precisar aguardar implementações protocolares estáveis antes de mover canais de produção de alta criticidade.

### 3. QKD torna-se disciplina de garantia

A distribuição quântica de chaves permanece relevante para enlaces altamente especializados, particularmente quando a instituição controla os terminais e as rotas de rede. O desenvolvimento importante de 2026 não é uma nova caixa QKD; é o surgimento de uma linguagem de certificação, com o ETSI GS QKD 016 descrito como um marco de perfil de proteção para avaliação de produtos QKD ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publica perfil de proteção QKD")).

Para os bancos, isso desloca a conversa de aquisição. A pergunta correta não é mais se QKD é quanticamente seguro em princípio. A pergunta correta é se o dispositivo, a integração, o processo de gestão de chaves, o ambiente operacional e a evidência de certificação atendem ao modelo de ameaça do banco.

### 4. A cripto-agilidade é a arquitetura

A cripto-agilidade é a capacidade de mudar algoritmos sem mudar o sistema inteiro. Cobre bibliotecas de software, negociação de protocolo, política HSM, perfis de certificados, tempos de vida de chaves, serviços de assinatura, evidência de auditoria e caminhos de rollback. Sem ela, cada migração criptográfica vira projeto sob medida.

Essa é a lição arquitetônica central. A transição pós-quântica não será a última transição criptográfica que o sistema financeiro enfrentará. Os bancos que construírem cripto-agilidade agora obtêm um plano de controle reutilizável para atualizações de algoritmos, risco de fornecedores, revogação emergencial e evidência para o regulador.

## O que os bancos devem fazer agora

### Construir o inventário de ativos criptográficos

O primeiro entregável é uma lista de materiais criptográfica. Deve incluir algoritmos de chave pública, tamanhos de chave, autoridades de certificação, templates HSM, versões de TLS, produtos VPN, gateways de pagamento, APIs de terceiros, SDKs móveis, wrappers de criptografia de dados em repouso, chaves de assinatura, processos de assinatura de firmware e criptografia gerida por fornecedores.

O inventário deve distinguir confidencialidade e autenticidade. Dados cifrados de longa duração estão expostos ao risco harvest-now-decrypt-later, enquanto chaves de assinatura de longa duração criam risco futuro de falsificação se permanecerem ancoradas em algoritmos de chave pública vulneráveis.

### Segmentar pela meia-vida dos dados

Nem todos os dados precisam da mesma ordem de migração. Uma mensagem de autorização de cartão em tempo real pode ter uma meia-vida de confidencialidade diferente da de uma investigação de sanções, de um arquivo de aquisição corporativa, de um pacote de identidade de private banking ou de um documento de emissão de dívida soberana. Por isso a migração quântica pertence à classificação de dados tanto quanto à segurança de rede.

A prioridade devem ser os sistemas que protegem dados de longa duração com estabelecimento de chaves vulnerável. Esses são os sistemas em que a coleta de hoje cria a exposição de amanhã.

### Forçar roadmaps de fornecedores nos contratos

O NIST diz que produtos, serviços e protocolos precisam de atualizações para a transição ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")). Isso significa que a linguagem de aquisição precisa mudar. Os fornecedores devem divulgar prazos de suporte PQC, compatibilidade com padrões finais, comportamento em modo híbrido, restrições de módulos de hardware, impactos de desempenho, suporte a perfis de certificados e controles de fallback.

Um fornecedor que diz apenas «roadmap quantum-safe» não respondeu à pergunta. O banco precisa de datas, algoritmos, fronteiras de integração e evidência.

## PQC, QKD e híbrido: uma tabela prática de decisão

| Controle | Melhor uso | Status 2026 | Ressalva bancária |
|---|---|---|---|
| **ML-KEM / FIPS 203** | Estabelecimento de chaves para confidencialidade duradoura | Padronizado e pronto para planejamento de implementação ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography")) | Precisa de suporte de protocolo e bibliotecas antes do rollout crítico em produção |
| **ML-DSA / FIPS 204** | Assinaturas digitais gerais | Recomendado pelo NCSC para a maioria dos casos gerais de assinatura ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos passos para preparar a PQC")) | Cadeias de certificados e migração de PKI são operacionalmente difíceis |
| **SLH-DSA / FIPS 205** | Assinaturas baseadas em hash para assinatura de firmware e software | Padrão NIST final referenciado pelo NCSC ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos passos para preparar a PQC")) | Assinaturas maiores podem afetar ambientes restritos |
| **Esquemas híbridos PQ/T** | Migração intermediária e interoperabilidade | Útil como medida de transição ([NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos passos para preparar a PQC")) | Adiciona complexidade e pode exigir uma segunda migração |
| **QKD** | Enlaces especializados de alta garantia | O trabalho de garantia amadurece via atividade de perfil de proteção da ETSI ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publica perfil de proteção QKD")) | Não resolve autenticação em escala de internet nem inventário criptográfico empresarial |

## O que isso significa por tipo de instituição

### Bancos universais de primeira linha

Os bancos de primeira linha precisam de um escritório de programa, não de uma prova de conceito. O modelo operacional-alvo deve combinar inventário criptográfico, imposição a fornecedores, gestão do roadmap de HSMs, ambientes de teste para TLS/IPsec híbridos e evidência pronta para o regulador. O trabalho inicial de maior valor não é trocar imediatamente toda a cifra; é construir o plano de controle que torna a mudança segura.

### Bancos de médio porte e regionais

Os bancos médios devem tratar a PQC como exercício de gestão de fornecedores e padronização de plataforma. Podem evitar trabalho sob medida caro concentrando os sistemas em bibliotecas suportadas, pilhas TLS padrão, serviços de certificados gerenciados e prazos claros para fornecedores. O risco-chave é a criptografia oculta dentro de appliances, gateways de pagamento e middleware legado.

### Fintechs, PSPs e instituições cripto-adjacentes

As fintechs podem se mover mais rápido porque costumam ter menos âncoras de confiança herdadas. O risco é a complacência em APIs de terceiros, padrões de KMS em nuvem, infraestrutura de wallets e integrações de custódia. Firmas cripto-adjacentes devem tomar cuidado especial para não confundir narrativas de segurança nativas de blockchain com prontidão pós-quântica.

### Engenheiros e arquitetos de segurança

A disciplina de engenharia é concreta: adicionar metadados de algoritmo aos inventários de serviços, registrar modos de protocolo negociados, criar feature flags seguros para testes híbridos, encurtar tempos de vida de certificados onde possível, remover suposições de algoritmo hard-coded e tornar a política criptográfica entregável por configuração em vez de forks de código.

## Conclusão

O reset da criptografia quântica não é uma compra única de tecnologia. É um modelo operacional criptográfico. O NIST deu à indústria uma linha de base de padrões, o NCSC estreitou a orientação prática, os corpos de protocolos ainda se movem e a garantia de QKD está se formalizando. As instituições bancárias que vencerão essa transição não serão as que anunciarem o maior piloto. Serão as que sabem onde vive sua criptografia, sabem quais dados precisam de proteção primeiro e podem trocar primitivas criptográficas sem reconstruir o banco.

## Perguntas frequentes

**A criptografia pós-quântica está pronta para os bancos usarem?**

Está pronta para planejamento, engajamento de fornecedores, pilotos e trabalho de implementação selecionado. O NIST diz que três padrões estão prontos para implementação, enquanto o NCSC adverte que o uso operacional deve se apoiar em implementações robustas de padrões finais e em protocolos estáveis ([NIST](https://www.nist.gov/pqc "NIST Post-Quantum Cryptography"), [NCSC](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "Próximos passos para preparar a PQC")).

**QKD elimina a necessidade de PQC?**

Não. QKD pode ser útil para enlaces controlados especializados, mas a PQC é a trajetória de migração escalável para software geral, protocolos de Internet, APIs, certificados e sistemas corporativos. QKD também depende de frameworks de garantia e certificação antes de poder ser tratado como infraestrutura de qualidade bancária ([ID Quantique / ETSI QKD 016](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI publica perfil de proteção QKD")).

**O que deve ser migrado primeiro?**

Os sistemas que protegem dados sensíveis de longa duração devem ser priorizados. Isso inclui criptografia de arquivos, investigações de pagamentos, documentos de tesouraria e mercados de capitais, registros de identidade de private banking, arquivos de deals estratégicos, autoridades certificadoras raiz, assinatura de firmware e canais interbancários.

**Qual a maior armadilha de implementação?**

A maior armadilha é tratar a PQC como simples troca de algoritmos. A migração toca em protocolos, certificados, HSMs, fornecedores, testes de desempenho, resposta a incidentes, monitoramento e governança. Sem cripto-agilidade, a instituição simplesmente recria o mesmo problema de migração para a próxima mudança de algoritmo.

## Referências

- NIST, (2025). [Criptografia pós-quântica ⧉](https://www.nist.gov/pqc "Post-quantum cryptography").
- NCSC, (2024). [Próximos passos para preparar a criptografia pós-quântica ⧉](https://www.ncsc.gov.uk/paper/next-steps-in-preparing-for-post-quantum-cryptography "NCSC PQC guidance").
- NIST CSRC, (2026). [The NIST Post-Quantum Cryptography Project ⧉](https://csrc.nist.gov/presentations/2026/mpts2026-3b1 "The NIST PQC Project").
- ID Quantique, (2024). [ETSI publica o primeiro perfil de proteção mundial para QKD ⧉](https://www.idquantique.com/etsi-releases-qkd-protection-profile/ "ETSI QKD 016").
<!-- enrich-start -->
<aside class="author-card" aria-label="Sobre o autor"><img alt="Retrato de Sebastien Rousseau" src="https://cloudcdn.pro/stocks/images/sebastien-rousseau.png" width="64" height="64" loading="lazy" decoding="async" /><span class="author-card-body"><strong class="author-card-name"><a href="/about/index.html">Sebastien Rousseau</a></strong><span class="author-card-bio">Tecnólogo bancário sênior, escreve sobre IA aplicada, migração para ISO 20022, criptografia pós-quântica para serviços financeiros e a transformação estrutural dos pagamentos wholesale.</span><span class="author-credentials">Mais de 20 anos no HSBC Commercial &amp; Investment Bank, PayPal, Barclays, Shazam, AKQA, Virgin Group. <a href="/about/index.html">Perfil completo</a> &middot; <a href="https://www.linkedin.com/in/sebastienrousseau/" rel="external noopener">LinkedIn</a> &middot; <a href="https://github.com/sebastienrousseau" rel="external noopener">GitHub</a></span></span></aside>
<p class="post-reviewed">Última revisão <time datetime="2026-05-18">2026-05-18</time>.</p>
<!-- enrich-end -->
