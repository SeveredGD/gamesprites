const fs = require('fs');
const path = require('path');

const root = __dirname;
const sourcePath = process.argv[2];

if (!sourcePath) {
  throw new Error('Pass the reviewed pet/monster JSON path as the first argument.');
}

const review = JSON.parse(fs.readFileSync(sourcePath, 'utf8'));
const assets = Array.isArray(review.assets) ? review.assets : [];

const pets = assets
  .filter(asset => asset.type === 'pet' && asset.decision !== 'dont-use')
  .map(asset => ({
    name: asset.name,
    path: asset.path,
    notes: asset.notes || '',
    decision: asset.decision,
    found: false,
    frameCount: Math.max(1, Number(asset.frameCount) || 1),
    excludedFrameIndexes: Array.isArray(asset.excludedFrameIndexes)
      ? asset.excludedFrameIndexes
      : [],
    pixelSettings: asset.pixelSettings || {}
  }));

const missing = pets.filter(pet => !fs.existsSync(path.join(root, ...pet.path.split('/'))));
if (missing.length) {
  throw new Error(`Missing ${missing.length} pet sprites:\n${missing.map(pet => pet.path).join('\n')}`);
}

const json = `${JSON.stringify(pets, null, 2)}\n`;
fs.writeFileSync(path.join(root, 'pets.json'), json);
fs.writeFileSync(path.join(root, 'pets-data.js'), `window.EVERDEEP_PETS = ${json.trim()};\n`);

const counts = assets.reduce((result, asset) => {
  const key = `${asset.type}:${asset.decision}`;
  result[key] = (result[key] || 0) + 1;
  return result;
}, {});

console.log(JSON.stringify({ importedPets: pets.length, missing: missing.length, sourceCounts: counts }, null, 2));
