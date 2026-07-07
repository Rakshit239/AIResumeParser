# AI Resume Parser — Setup Guide

This project has two parts that both need to be running at the same time:

1. **API** — a Python backend that reads resume/job description files (PDF, DOCX, TXT) and extracts text.
2. **UI** — an Angular website where you upload a file and see the extracted text.

This guide assumes you have never used the terminal before. Follow the steps in order, top to bottom.

---

## Before you start: install the required tools

You need three tools installed on your computer. Install them in this order.

### 1. Install Python (version 3.9 or newer)

- Go to https://www.python.org/downloads/
- Download and install the latest version for your operating system.
- **Windows users:** during installation, make sure you check the box that says **"Add Python to PATH"**.
- To check it worked, open a terminal (see below) and type:
  ```
  python3 --version
  ```
  You should see something like `Python 3.11.4`.

### 2. Install Node.js (version 20 or newer)

- Go to https://nodejs.org/
- Download and install the **LTS** version.
- To check it worked, open a terminal and type:
  ```
  node -v
  ```
  You should see something like `v20.11.0`.

### 3. Open a terminal

- **Mac:** Press `Cmd + Space`, type `Terminal`, press Enter.
- **Windows:** Press the Start key, type `Command Prompt` (or `PowerShell`), press Enter.

You will run all the commands below inside this terminal window.

---

## Step 1: Get the project folder

Make sure you have the `AIResumeParser` project folder on your computer (for example, downloaded or copied to your Desktop). Everything below assumes you `cd` (change directory) into that folder.

For example, if it's on your Desktop:
```
cd Desktop/AIResumeParser
```

---

## Step 2: Run the API (backend)

Keep this terminal window open for the entire time you're using the app — closing it will stop the API.

1. Move into the API folder:
   ```
   cd API
   ```

2. Create a virtual environment (an isolated space for this project's Python packages). You only need to do this once:
   ```
   python3 -m venv .venv
   ```

3. Activate the virtual environment:
   - **Mac / Linux:**
     ```
     source .venv/bin/activate
     ```
   - **Windows:**
     ```
     .venv\Scripts\activate
     ```
   You'll know it worked because your terminal line now starts with `(.venv)`.

   > You must repeat this "activate" step every time you open a new terminal window to work on the API.

4. Install the required Python packages (only needed once, or whenever `requirements.txt` changes):
   ```
   pip install -r requirements.txt
   ```

5. Move into the `backend` folder and start the API server:
   ```
   cd backend
   python3 app.py
   ```

6. You should see output that includes something like:
   ```
   * Running on http://127.0.0.1:9000
   ```
   This means the API is running. **Leave this terminal window open.**

7. To check it's working, open a web browser and go to:
   ```
   http://127.0.0.1:9000/api/health
   ```
   You should see `{"status": "ok"}` on the page.

---

## Step 3: Run the UI (frontend)

Open a **new** terminal window (leave the API one running from Step 2) and follow these steps.

1. Move into the UI folder from the project root:
   ```
   cd UI
   ```

2. Install the required packages (only needed once, or whenever `package.json` changes):
   ```
   npm install
   ```

3. Start the UI:
   ```
   npm start
   ```

4. Wait until you see a message like:
   ```
   Local:   http://localhost:4200/
   ```

5. Open your web browser and go to:
   ```
   http://localhost:4200
   ```
   You should see the Job Description / Resume Parser website.

---

## Step 4: Use the app

1. With both the API (Step 2) and UI (Step 3) running, go to `http://localhost:4200` in your browser.
2. Upload a resume or job description file (`.pdf`, `.docx`, or `.txt`).
3. The extracted text should appear on the page.

---

## Stopping the app

In each terminal window, press `Ctrl + C` to stop the server.

## Running it again later

Once everything is installed, you don't need to repeat the install steps. Each time you want to use the app:

**Terminal 1 (API):**
```
cd API
source .venv/bin/activate      # Windows: .venv\Scripts\activate
cd backend
python3 app.py
```

**Terminal 2 (UI):**
```
cd UI
npm start
```

Then open `http://localhost:4200` in your browser.

---

## Troubleshooting

- **"command not found: python3" or "python3 is not recognized"** — Python isn't installed correctly, or wasn't added to PATH. Reinstall it and make sure to check the "Add to PATH" option (Windows).
- **"command not found: npm" or "npm is not recognized"** — Node.js isn't installed correctly. Reinstall it from https://nodejs.org/.
- **The website loads but uploading a file does nothing / shows an error** — Make sure the API terminal (Step 2) is still running and shows no errors. The UI needs the API running at `http://127.0.0.1:9000` to work.
- **Port already in use** — Close any other terminal windows that might already be running the API or UI, then try again.
