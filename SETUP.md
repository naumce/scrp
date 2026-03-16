# Local Business Intelligence Scraper

A desktop app for finding local businesses, enriching them with contact info, and exporting lead lists.

**No API keys needed** — uses free OpenStreetMap data.

---

## Quick Start (Use Pre-Built App)

### macOS (Apple Silicon — M1/M2/M3/M4)

1. Download `Local Biz Scraper_0.1.0_aarch64.dmg`
2. Double-click the `.dmg` file
3. Drag **Local Biz Scraper** into Applications
4. Open from Applications (you may need to right-click → Open the first time due to Gatekeeper)
5. The app starts automatically — no setup needed

### macOS (Intel)

An Intel build must be compiled on an Intel Mac (or cross-compiled). See "Build from Source" below.

### Windows

A Windows `.msi` installer must be built on a Windows machine. See "Build from Source" below.

---

## Build from Source

### Prerequisites (All Platforms)

| Tool | Version | Install |
|------|---------|---------|
| Node.js | 18+ | https://nodejs.org |
| Rust | 1.77+ | https://rustup.rs |
| Python | 3.9+ | https://python.org |
| uv | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` (macOS/Linux) or `powershell -c "irm https://astral.sh/uv/install.ps1 \| iex"` (Windows) |

### macOS

```bash
# 1. Install system dependencies
xcode-select --install
brew install node rust python3

# 2. Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Clone and enter the project
cd local-biz-scraper

# 4. Install frontend dependencies
npm install

# 5. Install backend dependencies
cd backend
uv sync
cd ..

# 6. Build the Python backend binary
cd backend
uv run pyinstaller --onefile --name backend-$(rustc -vV | grep host | cut -d' ' -f2) main.py
cp dist/backend-* ../src-tauri/binaries/
cd ..

# 7. Build the desktop app
npm run tauri:build
```

The `.dmg` installer will be at:
```
src-tauri/target/release/bundle/dmg/Local Biz Scraper_0.1.0_aarch64.dmg
```

### Windows

```powershell
# 1. Install prerequisites
# - Node.js: https://nodejs.org (LTS)
# - Rust: https://rustup.rs
# - Python 3.9+: https://python.org (check "Add to PATH")
# - Visual Studio Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/
#   (select "Desktop development with C++")

# 2. Install uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 3. Enter the project directory
cd local-biz-scraper

# 4. Install frontend dependencies
npm install

# 5. Install backend dependencies
cd backend
uv sync
cd ..

# 6. Build the Python backend binary
cd backend
uv run pyinstaller --onefile --name backend-x86_64-pc-windows-msvc.exe main.py
copy dist\backend-x86_64-pc-windows-msvc.exe ..\src-tauri\binaries\
cd ..

# 7. Build the desktop app
npm run tauri:build
```

The `.msi` installer will be at:
```
src-tauri\target\release\bundle\msi\Local Biz Scraper_0.1.0_x64_en-US.msi
```

### Linux (Debian/Ubuntu)

```bash
# 1. Install system dependencies
sudo apt update
sudo apt install -y libwebkit2gtk-4.1-dev build-essential curl wget file \
  libssl-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev \
  nodejs npm python3 python3-pip

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Enter the project directory
cd local-biz-scraper

# 3. Install frontend dependencies
npm install

# 4. Install backend dependencies
cd backend
uv sync
cd ..

# 5. Build the Python backend binary
cd backend
uv run pyinstaller --onefile --name backend-$(rustc -vV | grep host | cut -d' ' -f2) main.py
cp dist/backend-* ../src-tauri/binaries/
cd ..

# 6. Build the desktop app
npm run tauri:build
```

The `.deb` and `.AppImage` will be at:
```
src-tauri/target/release/bundle/deb/
src-tauri/target/release/bundle/appimage/
```

---

## Development Mode (Run Without Building)

For developers who want to run the app locally without packaging:

### Terminal 1 — Backend
```bash
cd backend
uv run uvicorn main:app --host 127.0.0.1 --port 8742
```

### Terminal 2 — Frontend (browser)
```bash
npm run dev
# Opens at http://localhost:5173
```

### Or run as desktop app in dev mode
```bash
npm run tauri:dev
```

---

## How to Use

1. **Create a Project** — Click "New Project", give it a name and description
2. **Search Businesses** — Enter a keyword and location:
   - Keywords that work well: `restaurant`, `cafe`, `hotel`, `dentist`, `pharmacy`, `supermarket`, `bakery`, `bar`, `bank`, `hospital`, `hairdresser`, `car_repair`
   - Any keyword also searches by business name (e.g., "manufacturing", "consulting")
   - Set radius (km) and max results
3. **Review Results** — Browse the table, star favorites, click rows for details
4. **Enrich** — Click "Enrich" to scrape business websites for emails, phone numbers, and social media links
5. **Export** — Download your leads as CSV or Excel

---

## Troubleshooting

### App won't open on macOS
Right-click the app → Open → click "Open" in the dialog. This bypasses Gatekeeper for unsigned apps.

### "Starting backend service..." stuck
The Python sidecar may have failed to start. Check Console.app for logs, or run in dev mode to see errors.

### Search returns 0 results
- Try common keywords: `restaurant`, `hotel`, `pharmacy`
- Some keywords only work as name searches (e.g., "manufacturing") — these search business names
- Increase the radius
- OpenStreetMap coverage varies by region — major cities have better data

### Backend won't start (dev mode)
```bash
cd backend
uv sync                    # reinstall dependencies
uv run uvicorn main:app --host 127.0.0.1 --port 8742
```
