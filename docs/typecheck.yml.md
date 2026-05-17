# 📄 typecheck.yml

---

## 📋 Overview
This file is a GitHub Workflow that runs a type check on the code.



---

## 📍 File Path
```
workspace/repository/.github/workflows/typecheck.yml
```

---

## 🎯 Responsibilities
- Runs the type check on the code



---

## 🔑 Key Components

### 🏗️ Classes
None



---

### ⚙️ Functions
None



---

## 💻 Code Snippet
```python
name: Type Check

on: [push, pull_request]

permissions:
  contents: read

jobs:
  typecheck:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    strategy:
      matrix:
        python-version: ["3.10", "3.14"]

    steps:
    - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.
```

---

## 📝 Additional Notes

### 📦 Dependencies
N/A

---

### ▶️ Usage Example
```python
# example
```

---

### 🔗 Related Files
N/A

---

## 🧠 Summary
This file is a GitHub Workflow that runs a type check on the code.
