import { useState } from 'react';
import ResourceList from './ResourceList';

const getIcon = (title) => {
  const t = title.toLowerCase();
  if (t.includes('cours')) return '📚';
  if (t.includes('td')) return '✏️';
  if (t.includes('tp')) return '🔧';
  if (t.includes('projet')) return '🛠️';
  if (t.includes('examen')) return '📝';
  return '📁';
};

export default function SectionList({ module, sections }) {
  const [activeSectionId, setActiveSectionId] = useState(
    sections[0]?.$id || null
  );

  const activeSection = sections.find(s => s.$id === activeSectionId);

  return (
    <div>
      {sections.length > 0 ? (
        <>
          <section className="content-section">
            <div className="section-container">
              <h2 className="section-title">Contenu du cours</h2>
              <div className="content-grid">
                {sections.map((sec) => (
                  <div
                    key={sec.$id}
                    className="content-card"
                    onClick={() => setActiveSectionId(sec.$id)}
                  >
                    <div className="card-header">
                      <div className="card-icon">{getIcon(sec.title)}</div>
                      <h3 className="card-title">{sec.title}</h3>
                    </div>
                    <p className="card-description">
                      Cliquez pour voir les documents et ressources
                    </p>
                    <span className="card-link">
                      Accéder →
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section className="files-section" id="documents">
            <div className="section-container">
              <h2 className="section-title">
                {activeSection ? activeSection.title : 'Documents'}
              </h2>
              {activeSectionId && (
                <ResourceList
                  moduleId={module.$id}
                  sectionId={activeSectionId}
                />
              )}
            </div>
          </section>
        </>
      ) : (
        <section className="content-section">
          <div className="section-container">
            <div className="error">Aucune section disponible.</div>
          </div>
        </section>
      )}
    </div>
  );
}