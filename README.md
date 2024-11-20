# Multi-turn Conversation Dataset for E-Commerce Customer Support

This repository contains the code and resources for generating a synthetic dataset of multi-turn conversations for e-commerce customer support using Large Language Model (LLM) agents. This dataset is designed to train and fine-tune customer support systems effectively by simulating realistic interactions between customers and support agents.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Installing Dependencies](#installing-dependencies)
  - [Reproducing the Dataset](#reproducing-the-dataset)
- [Dataset Details](#dataset-details) (TODO: add numbers - queries, conversations, etc.)
- [Augmentation Techniques](#augmentation-techniques)
- [Directory Structure](#directory-structure)

---

## Overview

This project demonstrates the potential of synthetic data generation to enhance customer support systems. Conversations are simulated between two LLM agents, representing a **Customer** and a **Customer Support Agent**, across various intents and product categories. Techniques like **product substitution**, **tone augmentation**, and **language style variations** are applied to ensure dataset diversity and realism.

---

## Features

- **Multi-turn Conversations**: Simulates back-and-forth interactions between customers and agents.
- **Product-Specific Queries**: Augments generic queries to make them product-focused (e.g., cameras, smartphones).
- **Tone Variations**: Adds emotional diversity with cheerful, neutral, and annoyed tones.
- **Scalable and Modular Design**: Easily generate and scale datasets using provided augmentation modules.
- **Grounded on Real Help Content**: Uses help content sourced from Amazon to ensure conversations are realistic and meaningful.

---

## Getting Started

### Installing Dependencies

1. Clone this repository:
   ```bash
   git clone https://github.com/suchitg-nw/asynth_amazon.git
   cd asynth_amazon
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Reproducing the Dataset

1. Set up the help content directory as described in the [Appendix](https://docs.google.com/document/d/1CSPYUnLAQtJHqrinShTxA57aBRPOjC4ikApfiLxizL8/edit?tab=t.0#heading=h.g2fra7gshhoh) and replace the paths to the help content folder in notebooks under `query_gen/generation_nbs`.
   You can also find the help content in [this repository](https://github.com/suchitg-nw/amazon_help) under the `leafdirs/` folder.
2. Run the notebooks in `query_gen/generation_nbs` to generate seed queries and apply augmentations.
3. Run the individual commands in `agentic_convo/data_gen_cmds.txt` to generate conversations.
---

## Augmentation Techniques

1. **Product Substitution**: Augments queries to refer to specific products.
2. **Tone Augmentation**: Adds emotional diversity (cheerful, neutral, annoyed).
3. **Language Style Variations**:
   - Colloquial English
   - Non-native English (with intentional typos or grammatical errors)
4. **Typographic Errors**: Adds misspellings and incorrect punctuation for realism.

---

## Directory Structure

```
├── agentic_convo
│   ├── agent_prompts.py
│   ├── conversation_data
│   ├── data_gen_cmds.txt
│   ├── parallel_data_gen.py
│   └── test_nbs
├── query_gen
│   ├── generation_nbs
│   └── queries_data
├── README.md
└── requirements.txt
```

---

For more details, refer to the [design document](https://docs.google.com/document/d/1CSPYUnLAQtJHqrinShTxA57aBRPOjC4ikApfiLxizL8/edit?usp=sharing).  
