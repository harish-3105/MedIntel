// Root shell that renders the primary MedIntel experience with navigation
import { useState } from 'react';
import ChatPage from './pages/ChatPage.jsx';
import NearbyPage from './pages/NearbyPage.jsx';

function App() {
  const [activeView, setActiveView] = useState('chat'); // 'chat' or 'nearby'

  return (
    <div className="flex h-screen flex-col">
      {/* Navigation Bar */}
      <nav className="flex items-center justify-between border-b border-white/10 bg-background/80 px-6 py-4 backdrop-blur-xl">
        <div className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-primary/60">
            <span className="text-xl">🏥</span>
          </div>
          <h1 className="text-xl font-bold text-white">MedIntel</h1>
        </div>

        <div className="flex gap-2 rounded-2xl border border-white/10 bg-white/5 p-1">
          <button
            onClick={() => setActiveView('chat')}
            className={`rounded-xl px-6 py-2 text-sm font-semibold transition ${
              activeView === 'chat'
                ? 'bg-primary text-background'
                : 'text-white/70 hover:text-white'
            }`}
          >
            💬 Chat
          </button>
          <button
            onClick={() => setActiveView('nearby')}
            className={`rounded-xl px-6 py-2 text-sm font-semibold transition ${
              activeView === 'nearby'
                ? 'bg-primary text-background'
                : 'text-white/70 hover:text-white'
            }`}
          >
            🗺️ Nearby
          </button>
        </div>
      </nav>

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        {activeView === 'chat' ? <ChatPage /> : <NearbyPage />}
      </div>
    </div>
  );
}

export default App;
