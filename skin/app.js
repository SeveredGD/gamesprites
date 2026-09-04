(() => {
  const pets = Array.isArray(window.EVERDEEP_PETS) ? window.EVERDEEP_PETS : [];
  const elements = {
    grid: document.getElementById('petGrid'),
    empty: document.getElementById('emptyState'),
    count: document.getElementById('petCount'),
    search: document.getElementById('searchInput'),
    sprite: document.getElementById('activeSprite'),
    name: document.getElementById('petName'),
    kind: document.getElementById('petKind'),
    discovery: document.getElementById('discoveryState'),
    flavor: document.getElementById('petFlavor'),
    effect: document.getElementById('petEffect'),
    acquisition: document.getElementById('petAcquisition'),
    equip: document.getElementById('equipButton'),
    phonePet: document.getElementById('phonePetSprite'),
    phoneGrid: document.getElementById('phonePetGrid'),
    phoneEmpty: document.getElementById('phoneEmptyState'),
    phoneCount: document.getElementById('phonePetCount'),
    phoneSearch: document.getElementById('phoneSearchInput'),
    phoneName: document.getElementById('phonePetName'),
    phoneDiscovery: document.getElementById('phoneDiscoveryState'),
    phoneFlavor: document.getElementById('phonePetFlavor'),
    phoneEffect: document.getElementById('phonePetEffect'),
    phoneEquip: document.getElementById('phoneEquipButton')
  };

  let selected = pets.find(p => /longhaired-black-cat/.test(p.path)) || pets[0];
  let equippedPath = selected?.path || '';

  const isFound = pet => pet?.found === true;

  const parseNotes = notes => {
    const result = { name: '', acquisition: '', effect: '', flavor: '' };
    for (const line of String(notes || '').split(/\r?\n/)) {
      const match = line.match(/^(Name|Acquisition|Effect|Flavor):\s*(.*)$/i);
      if (!match) continue;
      result[match[1].toLowerCase()] = match[2].replace(/^"|"$/g, '');
    }
    return result;
  };

  const assetUrl = pet => pet.path.replace(/^assets\/pets\//, 'assets/pets/');

  function setupSprite(node, pet, active = false) {
    const frames = Math.max(1, Number(pet.frameCount) || 1);
    const excluded = new Set(pet.excludedFrameIndexes || []);
    const firstAllowed = Array.from({ length: frames }, (_, index) => index).find(index => !excluded.has(index)) || 0;
    node.style.backgroundImage = 'none';
    node.style.aspectRatio = '1';
    node.dataset.frames = String(frames);
    let canvas = node.querySelector('canvas');
    if (!canvas) {
      canvas = document.createElement('canvas');
      canvas.width = active ? 256 : 160;
      canvas.height = active ? 256 : 160;
      canvas.setAttribute('aria-hidden', 'true');
      node.replaceChildren(canvas);
    }
    const probe = new Image();
    probe.onload = () => {
      const frameWidth = Math.floor(probe.naturalWidth / frames);
      const frameHeight = probe.naturalHeight;
      const sourceX = firstAllowed * frameWidth;
      const sample = document.createElement('canvas');
      sample.width = frameWidth;
      sample.height = frameHeight;
      const sampleContext = sample.getContext('2d', { willReadFrequently: true });
      sampleContext.drawImage(probe, sourceX, 0, frameWidth, frameHeight, 0, 0, frameWidth, frameHeight);
      const pixels = sampleContext.getImageData(0, 0, frameWidth, frameHeight).data;
      let minX = frameWidth;
      let maxX = -1;
      let minY = frameHeight;
      let maxY = -1;
      for (let y = 0; y < frameHeight; y += 1) {
        for (let x = 0; x < frameWidth; x += 1) {
          if (pixels[((y * frameWidth + x) * 4) + 3] < 16) continue;
          minX = Math.min(minX, x);
          maxX = Math.max(maxX, x);
          minY = Math.min(minY, y);
          maxY = Math.max(maxY, y);
        }
      }
      const context = canvas.getContext('2d');
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.imageSmoothingEnabled = false;
      if (maxY < 0) return;

      // Keep the authored frame scale, but register the lowest visible pixel
      // to one shared floor. Transparent source padding no longer affects height.
      const fullFrameScale = Math.min(
        (canvas.width * .9) / frameWidth,
        (canvas.height * .9) / frameHeight
      );
      const visibleCenterX = (minX + maxX + 1) / 2;
      const floorY = canvas.height * (active ? .86 : .83);
      const drawX = (canvas.width / 2) - (visibleCenterX * fullFrameScale);
      const drawY = floorY - ((maxY + 1) * fullFrameScale);
      context.drawImage(
        probe,
        sourceX, 0, frameWidth, frameHeight,
        drawX, drawY, frameWidth * fullFrameScale, frameHeight * fullFrameScale
      );
    };
    probe.src = assetUrl(pet);
    node.setAttribute('aria-label', active ? `${parseNotes(pet.notes).name || pet.name} companion portrait` : '');
  }

  function selectPet(pet) {
    selected = pet;
    const copy = parseNotes(pet.notes);
    const found = isFound(pet);
    setupSprite(elements.sprite, pet, true);
    setupSprite(elements.phonePet, pet, false);
    elements.sprite.classList.toggle('unknown-silhouette', !found);
    elements.sprite.parentElement.classList.toggle('unknown', !found);
    elements.name.textContent = found ? (copy.name || pet.name) : 'Unknown Companion';
    elements.kind.textContent = found
      ? (/combat-/.test(pet.path) ? 'Combat companion' : 'Idle companion')
      : 'Undiscovered';
    elements.discovery.textContent = found ? 'Found' : 'Not Found';
    elements.discovery.classList.toggle('found', found);
    elements.flavor.textContent = found && copy.flavor ? `“${copy.flavor}”` : 'Its identity has not been discovered.';
    elements.effect.textContent = found ? (copy.effect || 'Cosmetic companion.') : 'Unknown';
    elements.acquisition.textContent = found ? (copy.acquisition || 'Acquisition not assigned.') : 'Keep exploring to find this companion.';
    elements.equip.disabled = !found;
    elements.equip.textContent = !found ? 'Not Yet Found' : (equippedPath === pet.path ? 'Equipped' : 'Equip Companion');
    elements.equip.classList.toggle('equipped', found && equippedPath === pet.path);
    elements.phoneName.textContent = found ? (copy.name || pet.name) : 'Unknown Companion';
    elements.phoneDiscovery.textContent = found ? 'Found' : 'Not Found';
    elements.phoneDiscovery.classList.toggle('found', found);
    elements.phoneFlavor.textContent = found && copy.flavor ? `“${copy.flavor}”` : 'Its identity has not been discovered.';
    elements.phoneEffect.textContent = found ? (copy.effect || 'Cosmetic companion.') : 'Unknown';
    elements.phoneEquip.disabled = !found;
    elements.phoneEquip.textContent = !found ? 'Not Found' : (equippedPath === pet.path ? 'Equipped' : 'Equip');
    elements.phoneEquip.classList.toggle('equipped', found && equippedPath === pet.path);
    document.querySelectorAll('.pet-card').forEach(card => {
      const current = card.dataset.path === pet.path;
      card.classList.toggle('selected', current);
      card.setAttribute('aria-pressed', String(current));
    });
  }

  function makeCard(pet, compact = false) {
    const copy = parseNotes(pet.notes);
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'pet-card' + (compact ? ' compact-pet-card' : '');
    button.dataset.path = pet.path;
    const found = isFound(pet);
    button.classList.add(found ? 'found-card' : 'unknown-card');
    button.title = found ? (copy.name || pet.name) : 'Unknown companion';
    button.setAttribute('aria-label', found ? `Inspect ${copy.name || pet.name}` : 'Inspect unknown companion');
    button.innerHTML = found
      ? '<span class="thumb-stage"><span class="pet-sprite thumb-sprite"></span></span><span class="card-frame" aria-hidden="true"></span>'
      : '<span class="thumb-stage"><span class="unknown-mark" aria-hidden="true">???</span></span><span class="card-frame" aria-hidden="true"></span>';
    if (found) setupSprite(button.querySelector('.thumb-sprite'), pet);
    button.addEventListener('click', () => selectPet(pet));
    return button;
  }

  function renderGrid(query = '') {
    const needle = query.trim().toLowerCase();
    const filtered = pets.filter(pet => {
      const copy = parseNotes(pet.notes);
      return [copy.name, pet.name, copy.effect, copy.acquisition].join(' ').toLowerCase().includes(needle);
    });
    elements.grid.replaceChildren(...filtered.map(makeCard));
    elements.phoneGrid.replaceChildren(...filtered.map(pet => makeCard(pet, true)));
    elements.empty.hidden = filtered.length > 0;
    elements.phoneEmpty.hidden = filtered.length > 0;
    elements.count.textContent = `${pets.filter(isFound).length} / ${pets.length}`;
    elements.phoneCount.textContent = `${pets.filter(isFound).length} / ${pets.length}`;
    if (selected) selectPet(selected);
  }

  elements.search.addEventListener('input', event => {
    elements.phoneSearch.value = event.target.value;
    renderGrid(event.target.value);
  });
  elements.phoneSearch.addEventListener('input', event => {
    elements.search.value = event.target.value;
    renderGrid(event.target.value);
  });
  document.querySelectorAll('.view-button').forEach(button => button.addEventListener('click', () => {
    const compact = button.dataset.view === 'compact';
    document.getElementById('menagerieView').hidden = compact;
    document.getElementById('phoneView').hidden = !compact;
    document.querySelectorAll('.view-button').forEach(item => item.classList.toggle('active', item === button));
  }));
  elements.equip.addEventListener('click', () => {
    if (!selected || !isFound(selected)) return;
    equippedPath = selected.path;
    selectPet(selected);
  });
  elements.phoneEquip.addEventListener('click', () => {
    if (!selected || !isFound(selected)) return;
    equippedPath = selected.path;
    selectPet(selected);
  });
  renderGrid();
})();
