# Site du cours Énergétique - Thermique

Site React déployé sur GitHub Pages avec Appwrite comme backend.

## Configuration Appwrite

### 1. Créer le projet

- Se connecter à [Appwrite Cloud](https://cloud.appwrite.io/)
- Créer un nouveau projet

### 2. Créer la base de données

- Aller dans **Databases** → **Create Database**
- Nommer la base `cours_enise`

### 3. Collections

Créer les 3 collections suivantes :

#### `modules`
| Attribut | Type |
|----------|------|
| title | string |
| code | string |
| description | string |
| year | integer |
| semester | string |

#### `sections`
| Attribut | Type |
|----------|------|
| moduleId | string |
| title | string |
| order | integer |

#### `resources`
| Attribut | Type |
|----------|------|
| moduleId | string |
| sectionId | string |
| title | string |
| type | string |
| url | string |
| description | string |
| order | integer |

### 4. Permissions

Pour chaque collection :
- Ouvrir l'onglet **Settings** → **Permissions**
- Ajouter le rôle `any` avec permission `read`

### 5. Données示例

**Module :**
- title: `Énergétique – Thermique`
- code: `4A-S7-ET`
- year: `4`
- semester: `S7`

**Sections :**
- Cours (order: 1)
- TD (order: 2)
- TP (order: 3)

**Resources :**
- Pointer vers PDF stockés dans Appwrite Storage ou Google Drive

## Variables d'environnement

Copier `.env.example` vers `.env` et remplir :

```bash
cp .env.example .env
```

## Installation

```bash
npm install
npm run dev
```

## Déploiement

Le site sera accessible à : `https://tiffank1802.github.io/enise-site-2/`

**Étapes finales pour activer le déploiement :**

1. Aller sur https://github.com/tiffank1802/enise-site-2/settings/pages
2. Sous "Build and deployment", sélectionner "GitHub Actions"
3. Le workflow se lancera automatiquement au prochain push

**Pour déclencher le premier déploiement :**

```bash
git add .
git commit -m "Trigger deployment"
git push origin main
```

## Structure du projet

```
src/
├── appwrite.js          # Configuration Appwrite
├── App.jsx              # Point d'entrée
├── main.jsx             # Mount React
├── index.css            # Styles
└── components/
    ├── ModulePage.jsx   # Page principale du module
    ├── SectionList.jsx  # Navigation par section
    └── ResourceList.jsx # Liste des ressources
```