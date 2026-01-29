import { useState } from 'react';
import ResourceList from './ResourceList';

export default function SectionList({ module, sections }) {
  const [activeSectionId, setActiveSectionId] = useState(
    sections[0]?.$id || null
  );

  const activeSection = sections.find(s => s.$id === activeSectionId);

  return (
    <div className="section-layout">
      <nav className="section-nav">
        <h3>Contents</h3>
        <ul className="nav-list">
          {sections.map((sec) => (
            <li key={sec.$id}>
              <button
                className={`nav-button ${sec.$id === activeSectionId ? 'active' : ''}`}
                onClick={() => setActiveSectionId(sec.$id)}
              >
                {sec.title}
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <main className="section-content">
        {activeSectionId && activeSection && (
          <ResourceList
            moduleId={module.$id}
            sectionId={activeSectionId}
            sectionTitle={activeSection.title}
          />
        )}
      </main>
    </div>
  );
}