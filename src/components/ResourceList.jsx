import { useEffect, useState } from 'react';
import { databases, Query, CONFIG } from '../appwrite';

export default function ResourceList({ moduleId, sectionId, sectionTitle }) {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchResources = async () => {
    try {
      const res = await databases.listDocuments(
        CONFIG.databaseId,
        CONFIG.resourcesCollectionId,
        [
          Query.equal('moduleId', moduleId),
          Query.equal('sectionId', sectionId),
          Query.orderAsc('order'),
        ]
      );
      setResources(res.documents);
    } catch (err) {
      console.error('Erreur fetchResources:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);
    fetchResources();
  }, [moduleId, sectionId]);

  if (loading) return <div className="loading">Chargement des ressources...</div>;

  return (
    <div className="resources-container">
      <h2>{sectionTitle}</h2>
      {resources.length === 0 ? (
        <p className="no-resources">Aucune ressource pour cette section.</p>
      ) : (
        <ul className="resources-list">
          {resources.map((r) => (
            <li key={r.$id} className="resource-item">
              <a
                href={r.url}
                target="_blank"
                rel="noopener noreferrer"
                className="resource-link"
              >
                <span className="resource-icon">{getIcon(r.type)}</span>
                <span className="resource-title">{r.title}</span>
              </a>
              {r.description && (
                <p className="resource-description">{r.description}</p>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function getIcon(type) {
  switch (type) {
    case 'pdf': return '📄';
    case 'video': return '🎬';
    case 'link': return '🔗';
    case 'image': return '🖼️';
    default: return '📎';
  }
}