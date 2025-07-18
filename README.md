# 🤖 Robot Camera Commissioning Tool

This project provides a Python-based command-line tool to configure scanning cameras installed on warehouse robots.
The tool reads a list of serial numbers from a JSON file, asks the user for camera type, and sends a formatted configuration payload to a local test API.

---

## 📦 Features

- Interactive CLI for selecting camera type and loading camera serial numbers
- Constructs a valid API configuration based on provided camera type
- Sends a `PUT` request to a mock server endpoint to simulate robot configuration
- Includes automated unit testing for key functionality

---

## 🛠 Requirements

- Python 3.7+
- Standard libraries only: `json`, `requests`, `http.server`, `unittest`, etc.

---

## 🚀 How to Run

### 1. Start the Mock Server

In terminal 1:

```bash
python server.py
```

> This starts a server at `http://localhost:8888/api/v1/config/cameras`

### 2. Run the CLI Tool

In terminal 2:

```bash
python Task2_Commision_tool.py
```

Follow the prompt to:

- Select camera type (TYPE_A or TYPE_B)
- Enter the path to the serial number file (e.g. `serial_numbers.json`)

If successful, you’ll see:

```bash
✅ Cameras successfully configured!
```

---

## 🧪 Run Unit Tests

To validate logic and API structure, use:

```bash
python Unit_Testing.py
```

Expected output:

```bash
......
----------------------------------------------------------------------
Ran 6 tests in 0.01s

OK
```

---

## 📁 Project Structure

```text
.
├── Task2_Commision_tool.py     # CLI tool
├── serial_numbers.json         # Sample serial number file
├── server.py                   # Mock API server (port 8888)
├── Unit_Testing.py             # Unit tests
├── README.md                   # This file
```

---

## 📄 Example JSON Input

`serial_numbers.json`:

```json
{
  "A": "DA2352466",
  "B": "DA2352453",
  "C": "DA2352580",
  "D": "DA2471547"
}
```

---

## 📬 API Details

- Method: `PUT`
- Endpoint: `/api/v1/config/cameras`
- Content-Type: `application/json`
- Success Response: `204 No Content`

---

## 🧠 Notes

- Ensure the mock server is running before executing the CLI tool
- IDs and serial numbers must be unique or the server will reject the request
