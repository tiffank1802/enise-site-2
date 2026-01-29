import { useEffect, useState } from 'react';
import { databases, Query, CONFIG } from '../appwrite';

export default function ResourceList({ moduleId, sectionId }) {
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

  const getFileIcon = (type) => {
    switch (type) {
      case 'pdf': return '📄';
      case 'video': return '🎬';
      case 'link': return '🔗';
      case 'image': return '🖼️';
      case 'ppt':
      case 'pptx': return '📊';
      case 'doc':
      case 'docx': return '📝';
      case 'xls':
      case 'xlsx': return '📈';
      default: return '📎';
    }
  };

  const getFileSize = (url) => {
    return '';
  };

  return (
    <div className="file-list">
      {resources.length === 0 ? (
        <p className="no-resources">Aucun document disponible pour cette section.</p>
      ) : (
        resources.map((r) => (
          <a
            key={r.$id}
            href={r.url}
            target="_blank"
            rel="noopener noreferrer"
            className="file-item"
          >
            <div className="file-icon">{getFileIcon(r.type)}</div>
            <div className="file-info">
              <div className="file-name">{r.title}</div>
              {r.description && (
                <div className="file-meta">{r.description}</div>
              )}
            </div>
            <div className="file-download">↓</div>
          </a>
        ))
      )}
    </div>
  );
}