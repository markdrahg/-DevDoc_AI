# 📄 publish.yml

---

## 📋 Overview
N/A

---

## 📍 File Path
```
workspace/repository/.github/workflows/publish.yml
```

---

## 🎯 Responsibilities
N/A

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
name: Publish to PyPI

on:
  push:
    tags:
      - "v*"
  workflow_dispatch:
    inputs:
      test-pypi-only:
        description: "Publish to Test PyPI only"
        type: boolean
        default: true

permissions:
  contents: read

jobs:
  build:
    name: "Build dists"
    runs-on: "ubuntu-la
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
N/A