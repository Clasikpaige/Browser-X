# Browser-X 

_A Python tool to inspect **browser cookies and autofill data** for cybersecurity research. Use responsibly!_

---

## 🚀 What Does This Do?
- Extracts **Chrome cookies** (decrypted!) and **autofill entries** from your local system.
- Helps you understand how credential theft works (for defensive purposes).
- **⚠️ WARNING**: Only run this on systems you own or have explicit written permission to test!

---

## 🛠️ Installation
1. **Install Python 3.10+** (if you haven’t already).
2. Clone this repo:
   ```
   git clone https://github.clasikpaige/browser-X.git
   cd Broswee-X
    ```
```
pip install -r requirements.txt
```
# Usage
```
python3 hijack.py
```
### � What Happens?
1. **Copies Chrome Data**: Temporarily duplicates `Cookies` and `Web Data` files (to avoid locking the browser).
2. **Decrypts Cookies**: Uses Windows DPAPI and AES-GCM to decrypt stored cookies.
3. **Shows Autofill**: Lists saved names, emails, and other autofill entries.
