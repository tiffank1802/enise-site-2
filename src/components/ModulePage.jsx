import { useEffect, useState } from 'react';
import { databases, Query, CONFIG } from '../appwrite';
import SectionList from './SectionList';

export default function ModulePage({ moduleCode }) {
  const [module, setModule] = useState(null);
  const [sections, setSections] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchModuleAndSections = async () => {
    try {
      const modulesRes = await databases.listDocuments(
        CONFIG.databaseId,
        CONFIG.modulesCollectionId,
        [Query.equal('code', moduleCode)]
      );

      if (modulesRes.total === 0) {
        setLoading(false);
        return;
      }

      const mod = modulesRes.documents[0];
      setModule(mod);

      const sectionsRes = await databases.listDocuments(
        CONFIG.databaseId,
        CONFIG.sectionsCollectionId,
        [Query.equal('moduleId', mod.$id), Query.orderAsc('order')]
      );

      setSections(sectionsRes.documents);
    } catch (err) {
      console.error('Erreur fetchModuleAndSections:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchModuleAndSections();
  }, [moduleCode]);

  if (loading) return <div className="loading">Chargement...</div>;
  if (!module) return <div className="error">Module introuvable.</div>;

  return (
    <div className="module-page">
      <header className="module-header">
        <h1>{module.title}</h1>
        <p className="module-meta">{module.year}A - {module.semester}</p>
        <p className="module-description">{module.description}</p>
      </header>
      <SectionList module={module} sections={sections} />
    </div>
  );
}