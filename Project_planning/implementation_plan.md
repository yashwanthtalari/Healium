# Enhance Healium GUI and Fix Connection Issues

The user reported that the GUI is refusing to connect and wants a better, more concise log display. I will recreate the missing API and GUI components with a premium design and improved logging.

## Proposed Changes

### Backend (API)

#### [NEW] [api.py](file:///c:/Users/yashw/Desktop/Healium/api.py)
- Implement a FastAPI app.
- Create a `LogStream` class to redirect `sys.stdout` to a WebSocket manager.
- Implement a `ConnectionManager` for WebSocket clients.
- Serve static files from the `gui` directory.

### Frontend (GUI)

#### [NEW] [gui/index.html](file:///c:/Users/yashw/Desktop/Healium/gui/index.html)
- Create a modern, dark-themed UI using a clean design.
- Include an input form for repository path and developer prompt.
- Add a dedicated log window for real-time updates.

#### [NEW] [gui/style.css](file:///c:/Users/yashw/Desktop/Healium/gui/style.css)
- Implement a premium design system (Glassmorphism, smooth gradients).
- Ensure responsiveness and high-quality typography.

#### [NEW] [gui/script.js](file:///c:/Users/yashw/Desktop/Healium/gui/script.js)
- Handle WebSocket connection to the backend.
- Filter and format logs to be "concise" (e.g., highlighting agent actions and tool results).
- Manage UI state (running/idle).

## Verification Plan

### Automated Tests
- Run `python main.py --gui` and check if the server starts on port 8000.
- Use the browser tool to navigate to `http://localhost:8000` and verify the UI.

### Manual Verification
- Test the "Start" button and observe the logs appearing in the GUI.
- Verify that the logs are concise and easy to read.
