# FastAPI

## Setup (Recommended: Use a Virtual Environment)

1. **Create and activate a virtual environment** (Windows):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
   On macOS/Linux:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Start the server:**
   ```sh
   uvicorn app.main:app --reload
   ```

4. **Visit** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API docs