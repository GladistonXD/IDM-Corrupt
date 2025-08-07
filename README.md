# 🛡️ CheckUpdtVMProtector

A Python service for Windows designed to **remove the corrupt IDM error pop-up** (Internet Download Manager) and **block automatic updates** that frequently reactivate the `CheckUpdtVM` key.

---

## ❗ What is this?

If your IDM shows the error:

```
IDM has been corrupted. Please install it again.
```

Or if you get an **unwanted pop-up every time your system starts**, it's because the `CheckUpdtVM` registry key is enabled or being re-enabled automatically.

This service permanently fixes that:

- ❌ **Removes the corrupted IDM pop-up**
- 🛑 **Disables IDM automatic updates**
- 🔄 **Prevents the value from being reactivated**

---

## 📍 Monitored Path

The service monitors and restores the value of this Windows registry key:

```
HKEY_USERS\<SID>\SOFTWARE\DownloadManager\CheckUpdtVM
```

Whenever it's different from `"0"`, the value will be automatically corrected every 5 seconds.

---

## ✅ Requirements

- Python 3 installed on the system
- pip installed
- Windows with administrator privileges
- `pywin32` package

Install with:

```bash
pip install pywin32
```

---

## ⚙️ Installation and Usage

**1. Install the service:**

```bash
python CheckUpdtVMProtectorService.py install
```

**2. Start the service:**

```bash
python CheckUpdtVMProtectorService.py start
```

**3. (Optional) Stop the service:**

```bash
python CheckUpdtVMProtectorService.py stop
```

**4. (Optional) Remove the service:**

```bash
python CheckUpdtVMProtectorService.py remove
```

---

## 🔎 How to check if it is running

Open the Start Menu and type:

```
services.msc
```

Look for:

```
CheckUpdtVM Registry Protection
```

You can start, stop, or configure the service from there as well.

---

## 🛠️ Technologies Used

- `pywin32` – for creating and managing Windows services
- `winreg` – for accessing and modifying the Windows registry
- `win32security`, `win32ts`, `win32api` – for retrieving the current user's SID
- `subprocess` – for configuring the service

---

## 💡 Notes

- The service does not interfere with other IDM functions.
- It only prevents the `CheckUpdtVM` value from being re-enabled, which causes the corruption error.
- The value is checked and corrected every **5 seconds**.

---

## 📄 License

Free to use. Feel free to use, modify, and distribute as you wish.
