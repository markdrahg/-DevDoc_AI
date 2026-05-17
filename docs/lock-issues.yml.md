# 📄 lock-issues.yml

---

## 📋 Overview
This file is a GitHub Actions workflow that locks closed issues and pull requests after a certain period of time.



---

## 📍 File Path
```
workspace/repository/.github/workflows/lock-issues.yml
```

---

## 🎯 Responsibilities
- Locks closed issues and pull requests after a certain period of time
- Uses the dessant/lock-threads action to achieve this



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
name: 'Lock Threads'

on:
  schedule:
    - cron: '0 0 * * *'

permissions:
  issues: write
  pull-requests: write

jobs:
  action:
    if: github.repository_owner == 'psf'
    runs-on: ubuntu-latest
    steps:
      - uses: dessant/lock-threads@7266a7ce5c1df01b1c6db85bf8cd86c737dadbe7 # v6.0.0
    
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
This file is a simple and effective way to manage inactive threads on GitHub. It ensures that old and unresolved issues and pull requests are locked, preventing further discussion or activity on them. The use of the dessant/lock-threads action makes it easy to implement this functionality without having to write complex code. Overall, this file is a valuable tool for maintaining a clean and organized issue tracker on GitHub.
