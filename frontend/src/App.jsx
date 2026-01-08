function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col items-center justify-center p-8">
      <div className="text-6xl mb-8">🎮</div>
      <h1 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-neon-cyan via-blue-400 to-neon-purple bg-clip-text text-transparent drop-shadow-2xl mb-8 animate-pulse">
        TeamFinder
      </h1>
      <p className="text-xl text-slate-300 max-w-md text-center">
        TailwindCSS ✅ Fonctionne parfaitement !
      </p>
      <button className="mt-8 btn-primary px-8 py-4 text-lg">
        Lancer Matching
      </button>
    </div>
  )
}

export default App
