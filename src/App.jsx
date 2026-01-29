function App() {
  const moduleCode = '4A-S7-ET';

  return (
    <div className="app">
      <header className="site-header">
        <div className="site-logo">
          <div className="logo-icon">E</div>
          <h1>Énergétique - Thermique</h1>
        </div>
        <nav className="site-nav">
          <a href="#accueil">Accueil</a>
          <a href="#documents">Documents</a>
          <a href="#ressources">Ressources</a>
        </nav>
      </header>
      <main>
        <ModulePage moduleCode={moduleCode} />
      </main>
      <footer className="site-footer">
        <p>ENISE - École Nationale d'Ingénieurs de Saint-Étienne</p>
      </footer>
    </div>
  );
}

export default App;