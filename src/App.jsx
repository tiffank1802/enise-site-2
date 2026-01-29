import ModulePage from './components/ModulePage';

function App() {
  const moduleCode = '4A-S7-ET';

  return (
    <div className="app">
      <ModulePage moduleCode={moduleCode} />
    </div>
  );
}

export default App;