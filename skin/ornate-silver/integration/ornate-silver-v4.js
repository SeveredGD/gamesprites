(function () {
  'use strict';

  /* Border geometry belongs to the skin and never changes between states. */
  var SKINS = Object.freeze({
    classic:          { image: 'skins/ornate-silver/assets/ornate-silver/classic/ButtonMediumDark.png', slice: '30', y: 7, x: 12, safe: 4, minHeight: 36 },
    chainBracket:     { image: 'skins/ornate-silver/assets/ornate-silver/buttons/button-chain-bracket.png', slice: '68 180 68 180', y: 9, x: 25, safe: 8, minHeight: 40 },
    wingedPlaque:     { image: 'skins/ornate-silver/assets/ornate-silver/buttons/button-winged-plaque.png', slice: '72 205 72 205', y: 12, x: 34, safe: 10, minHeight: 48 },
    splitBevel:       { image: 'skins/ornate-silver/assets/ornate-silver/buttons/button-minimal-split-bevel.png', slice: '145 205 145 205', y: 7, x: 19, safe: 4, minHeight: 38 },
    pinRivet:         { image: 'skins/ornate-silver/assets/ornate-silver/buttons/button-minimal-pin-rivet.png', slice: '150 175 150 175', y: 7, x: 17, safe: 4, minHeight: 34 },
    needleClamp:      { image: 'skins/ornate-silver/assets/ornate-silver/buttons/button-needle-clamp.png', slice: '58 200 58 200', y: 7, x: 18, safe: 5, minHeight: 36 },
    slimChain:        { image: 'skins/ornate-silver/assets/ornate-silver/buttons/button-slim-chain.png', slice: '54 190 54 190', y: 7, x: 18, safe: 8, minHeight: 34 },
    knifeWing:        { image: 'skins/ornate-silver/assets/ornate-silver/buttons/button-knife-wing.png', slice: '58 220 58 220', y: 7, x: 20, safe: 5, minHeight: 34 },
    diamondBrace:     { image: 'skins/ornate-silver/assets/ornate-silver/buttons/button-diamond-brace.png', slice: '58 205 58 205', y: 7, x: 19, safe: 5, minHeight: 34 },
    cathedralTabs:    { image: 'skins/ornate-silver/assets/ornate-silver/plaques/plaque-cathedral-tabs.png', slice: '100 240 100 240', y: 18, x: 42, safe: 10, minHeight: 58 },
    chainSeal:        { image: 'skins/ornate-silver/assets/ornate-silver/plaques/plaque-chain-seal.png', slice: '100 230 100 230', y: 18, x: 40, safe: 10, minHeight: 58 },
    thornCorners:     { image: 'skins/ornate-silver/assets/ornate-silver/plaques/plaque-thorn-corners.png', slice: '105 210 105 210', y: 19, x: 38, safe: 10, minHeight: 60 },
    crescentAcanthus: { image: 'skins/ornate-silver/assets/ornate-silver/plaques/plaque-crescent-acanthus.png', slice: '105 220 105 220', y: 19, x: 40, safe: 10, minHeight: 60 },
    laurelSentinel:   { image: 'skins/ornate-silver/assets/ornate-silver/plaques/plaque-laurel-sentinel.png', slice: '100 240 100 240', y: 18, x: 42, safe: 10, minHeight: 58 }
  });

  /* Content sizes are independent from skins. Effective height is the larger
     of these tokens and the chosen skin's safe minimum. */
  var SIZES = Object.freeze({
    compact:  { minHeight: 32, fontSize: 12.5, lineHeight: 1.15, py: 1, px: 6 },
    standard: { minHeight: 38, fontSize: 14, lineHeight: 1.2, py: 2, px: 10 },
    wide:     { minHeight: 42, fontSize: 14, lineHeight: 1.25, py: 3, px: 14 },
    action:   { minHeight: 52, fontSize: 15, lineHeight: 1.2, py: 6, px: 16 },
    multiline:{ minHeight: 66, fontSize: 14, lineHeight: 1.2, py: 7, px: 16 },
    large:    { minHeight: 52, fontSize: 14, lineHeight: 1.2, py: 2, px: 14 }
  });

  /* Broad-to-specific. Later matches win. This replaces scattered CSS ownership. */
  var RULES = [
    { selector: '.fm-btn', skin: 'classic' },
    { selector: '.sk-btn', skin: 'cathedralTabs' },
    { selector: '.rpr-btn', skin: 'needleClamp' },
    { selector: '.overlay-btn', skin: 'slimChain', size: 'wide' },
    { selector: '#shop-choice-continue-btn', skin: 'slimChain', size: 'multiline' },
    { selector: '.blessing-buy-btn', skin: 'slimChain', size: 'action' },
    { selector: '.relic-mode-btn, .relic-use-btn', skin: 'classic', size: 'compact' },
    { selector: '.relic-stash-open-btn', skin: 'slimChain', size: 'wide' },
    { selector: '.step-btn, .ui-step, .tab-btn, .skill-tab, .drops-tab', skin: 'splitBevel', size: 'compact' },
    { selector: '.stree-add', skin: 'pinRivet', size: 'compact' },
    { selector: '.pro-xbtn, .b4-chain-button, .unique-review-action, .discard-btn', skin: 'chainBracket', size: 'wide' },
    { selector: '#bloodpit-menu .bp-frame > div button', skin: 'knifeWing', size: 'compact' },
    { selector: '#speed-controls .step-btn', skin: 'speedCap', size: 'compact' },
    { selector: '#pause-btn, #class-switch-btn', skin: 'chainBracket', size: 'compact' },
    { selector: '.shop-pause-btn', skin: 'chainBracket', size: 'action' },
    { selector: '#pc-arcade, #pc-epoch', skin: 'splitBevel', size: 'large' },
    { selector: '#pc-begin-btn, #journey-chip, #xm-run, #xm-rn-go, #bloodpit-claim-btn, #bloodpit-discard-btn', skin: 'wingedPlaque', size: 'large' },
    { selector: '#bloodpit-end-btn, #bloodpit-btn, #delve-extract-continue-btn, #mdlv-lv, #delve-extract-panel button, #idle-queue-btn, #xm-queue, #xm-view-queue, #boss-loop-btn, #farm-loop-btn, #quiver-mode-boss', skin: 'chainSeal', size: 'large' },
    { selector: '#delve-extract-pause-btn, #delve-death-btn, #mdlv-ex, #xm-rn-stop, #queue-stop-btn', skin: 'chainBracket', size: 'wide' },
    { selector: '#xm-rn-bless', skin: 'crescentAcanthus', size: 'large' },
    { selector: '#xm-bar .xm-abtn', skin: 'wingedPlaque', size: 'large' },
    { selector: '#xm-bar .xm-dbtn, #xm-bar .xm-pbtn', skin: 'diamondBrace', size: 'compact' },
    { selector: '#more-sheet .more-btn', skin: 'thornCorners', size: 'large' },
    { selector: '#zone-picker button', skin: 'native', size: 'layout' },
    { selector: '#log-tab-combat, #log-tab-event, #log-tab-item', skin: 'native', size: 'layout' }
  ];

  /* Panels use the same single-owner model. Rules are grouped by reusable
     treatment so changing an asset or border metric is a one-line edit. */
  var FRAME_SKINS = Object.freeze({
    thornedReliquary: { image: 'skins/ornate-silver/assets/ornate-silver/frames/frame-thorned-reliquary.png', slice: '190', y: 26, x: 26, surface: 0.96 },
    crownSpire:       { image: 'skins/ornate-silver/assets/ornate-silver/frames/frame-crown-spire-subtle.png', slice: '170', y: 20, x: 20, surface: 0.96 },
    fleurSubtle:      { image: 'skins/ornate-silver/assets/ornate-silver/frames/frame-fleur-sentinel-subtle.png', slice: '120', y: 38, x: 38, surface: 0.96 },
    acanthusHalo:     { image: 'skins/ornate-silver/assets/ornate-silver/frames/frame-acanthus-halo-subtle.png', slice: '120', y: 44, x: 44, surface: 0.96 },
    fleurSentinel:    { image: 'skins/ornate-silver/assets/ornate-silver/frames/frame-fleur-sentinel.png', slice: '180', y: 58, x: 58, surface: 0.96 },
    cathedral:        { image: 'skins/ornate-silver/assets/ornate-silver/frames/frame-cathedral.png', slice: '210', y: 52, x: 52, surface: 0.96 },
    widowLace:        { image: 'skins/ornate-silver/assets/ornate-silver/frames/frame-widow-lace.png', slice: '220', y: 72, x: 72, surface: 0.96 },
    thornPlaque:      { image: 'skins/ornate-silver/assets/ornate-silver/plaques/plaque-thorn-corners.png', slice: '105 210 105 210', y: 19, x: 38, surface: 0 },
    chainPlaque:      { image: 'skins/ornate-silver/assets/ornate-silver/plaques/plaque-chain-seal.png', slice: '100 230 100 230', y: 18, x: 40, surface: 0 }
  });
  var FRAME_RULES = [
    { selector: '#left-bottom, #bloodpit-timer, .pro-modal, #stats-overlay > div, #auto-equip-pop, #xm-overlay, #idle-queue-box, #stats-help-overlay, #class-help-overlay, #last-recap-overlay, #bossgift-overlay, #journey-list-overlay, #welcome-back-overlay > div, #wc-modal, #text-prompt-overlay > div, #text-prompt-box, #relic-stash-panel, #mastery-overlay > div, #mastery-box, #sessm-box, #ach-box', skin: 'thornedReliquary', type: 'modal' },
    { selector: '#tooltip, .tooltip, .item-tooltip, #overlay-box, #settings-overlay > div, #help-overlay > div, #stats-help-overlay > div, #drops-help-overlay > div, #item-help-modal, #cm-ren-box, #help-relic-section, #bank-overlay, #xm-help', skin: 'crownSpire', type: 'popup' },
    { selector: '#bloodpit-menu, #rn-bless-popup .pro-modal, #loadout-panel, #loadout-section', skin: 'fleurSubtle', type: 'modal' },
    { selector: '#gamble-result-overlay > div', skin: 'acanthusHalo', type: 'modal' },
    { selector: '#delve-death > div', skin: 'fleurSentinel', type: 'popup' },
    { selector: '#stats-sheet, #more-sheet, #skill-tree-overlay-box, #ascendancy-overlay > #asc-box, #asc-box', skin: 'cathedral', type: 'modal' },
    { selector: '#pet-overlay > div', skin: 'widowLace', type: 'modal' },
    { selector: '#floating-gold-readout, #combat-gold-box', skin: 'thornPlaque', type: 'bar' },
    { selector: '#queue-status-strip', skin: 'chainPlaque', type: 'bar' }
  ];

  var ICON_ONLY_SELECTOR = [
    '#skills-icon-tiles > button',
    '#rpanel-skills .sorc-cell',
    '#rpanel-skills .skill-btn',
    '#rpanel-skills [data-skill]',
    '#top-right-bar .tb-btn',
    '.act-shop-icon-btn',
    '.vf-chip', '.x-icon', '.pair-x', '.vault-trash-btn', '.bank-sc', '.gr-lock',
    '[data-ui-icon-only="true"]'
  ].join(', ');
  var FIT_CONTENT_SELECTOR = [
    '.fm-btn', '.sk-btn', '.rpr-btn', '.overlay-btn', '.pro-xbtn',
    '.b4-chain-button', '.unique-review-action', '.discard-btn', '.shop-pause-btn',
    '#pc-cancel-btn', '#pc-begin-btn', '#journey-chip',
    '#bloodpit-claim-btn', '#bloodpit-discard-btn', '#bloodpit-end-btn',
    '#delve-extract-continue-btn', '#delve-extract-pause-btn', '#delve-death-btn',
    '#xm-run', '#xm-rn-go', '#xm-rn-stop', '#queue-stop-btn'
  ].join(', ');

  function labelOf(button) {
    return String(button.textContent || '').replace(/[\u200B-\u200D\uFEFF]/g, '').replace(/\s+/g, ' ').trim();
  }
  function safeMatches(element, selector) {
    try { return element.matches(selector); } catch (error) { return false; }
  }
  function ownsIconArtwork(button) {
    if (button.getAttribute('data-ui-icon-only') === 'false' || button.getAttribute('data-ui-force-skin') === 'true') return false;
    if (safeMatches(button, ICON_ONLY_SELECTOR)) return true;
    var artwork = button.querySelectorAll('img, picture, svg, canvas, [data-ui-icon-artwork="true"], [class*="sprite"], [class*="-icon-art"]');
    for (var i = 0; i < artwork.length; i++) {
      var node = artwork[i];
      var style = window.getComputedStyle(node);
      var width = parseFloat(style.width) || node.width || node.naturalWidth || 0;
      var height = parseFloat(style.height) || node.height || node.naturalHeight || 0;
      var hasImage = node.matches('img, picture, svg, canvas, [data-ui-icon-artwork="true"]') || (style.backgroundImage && style.backgroundImage !== 'none');
      /* A small inline glyph may sit inside a framed text action. Large artwork
         is already the control silhouette and must not receive a second skin. */
      if (hasImage && width >= 32 && height >= 32) return true;
    }
    return false;
  }
  function resolveContract(button) {
    var label = labelOf(button);
    var result = { skin: 'classic', size: 'standard', explicit: false };
    RULES.forEach(function (rule) {
      if (!safeMatches(button, rule.selector)) return;
      if (rule.skin) result.skin = rule.skin;
      if (rule.size) result.size = rule.size;
      result.explicit = true;
    });
    if (!result.explicit) {
      if (button.classList.contains('sm') || label.length <= 3) result.size = 'compact';
      else if (label.length > 20 || button.children.length > 0) result.size = 'wide';
      if (button.closest('.pro-modal, #overlay-box, [role="dialog"]')) result.size = 'wide';
    }
    if (/^(close|cancel|discard all)$/i.test(label)) {
      result.skin = 'chainBracket'; result.size = 'wide'; result.explicit = true;
    } else if (/^begin$/i.test(label)) {
      result.skin = 'wingedPlaque'; result.size = 'large'; result.explicit = true;
    }
    var singleGlyph = label.length <= 2 && !result.explicit;
    if (ownsIconArtwork(button) || singleGlyph || (!label && button.getAttribute('aria-label'))) {
      result.skin = 'none'; result.size = 'icon';
    }
    if (button.dataset.uiSkinOverride) result.skin = button.dataset.uiSkinOverride;
    if (button.dataset.uiSizeOverride) result.size = button.dataset.uiSizeOverride;
    return result;
  }
  function setImportant(style, property, value) {
    if (style.getPropertyValue(property) === value && style.getPropertyPriority(property) === 'important') return;
    style.setProperty(property, value, 'important');
  }
  function setData(element, name, value) {
    if (element.getAttribute(name) !== value) element.setAttribute(name, value);
  }
  function isSelected(button) {
    if (button.getAttribute('aria-pressed') === 'true' || button.getAttribute('aria-selected') === 'true') return true;
    return ['active', 'selected', 'on', 'pc-mode-selected', 'tree-open'].some(function (name) { return button.classList.contains(name); });
  }
  function updateVisualState(button) {
    if (!button || button.dataset.uiV4 !== 'button') return;
    var filter = 'none';
    if (button.disabled || button.getAttribute('aria-disabled') === 'true') filter = 'brightness(.68) saturate(.55)';
    else if (safeMatches(button, ':active')) filter = 'brightness(.82)';
    else if (safeMatches(button, ':hover') || safeMatches(button, ':focus-visible')) {
      filter = isSelected(button) ? 'brightness(1.18) drop-shadow(0 0 5px rgba(222,208,178,.34))' : 'brightness(1.13)';
    } else if (isSelected(button)) filter = 'brightness(1.12) drop-shadow(0 0 5px rgba(222,208,178,.28))';
    setImportant(button.style, 'filter', filter);
    setImportant(button.style, 'transform', 'none');
    setImportant(button.style, 'transition', 'filter .12s ease');
  }
  function normalizeButton(button) {
    if (!button || button.tagName !== 'BUTTON') return;
    var contract = resolveContract(button);
    setData(button, 'data-ui-skin', contract.skin);
    setData(button, 'data-ui-size', contract.size);
    if (contract.skin === 'native') {
      setData(button, 'data-ui-v4', 'native');
      setData(button, 'data-ui-fit', 'layout');
      button.removeAttribute('data-ui-measured-min-height');
      /* The picker already owns its card, pill, and zone-row geometry. Remove
         only properties previously written by v4 so its native CSS can win. */
      ['border-style', 'border-color', 'border-width', 'border-image', 'border-radius',
       'background-image', 'background-color', 'box-shadow', 'box-sizing', 'height',
       'min-height', 'min-width', 'max-width', 'padding', 'font-size', 'line-height',
       'white-space', 'overflow-wrap', 'word-break', 'text-overflow', 'overflow',
       'filter', 'transform', 'transition'].forEach(function (property) {
        button.style.removeProperty(property);
      });
      return;
    }
    if (contract.skin === 'speedCap') {
      setData(button, 'data-ui-v4', 'native');
      setData(button, 'data-ui-fit', 'layout');
      return;
    }
    if (contract.skin === 'none') {
      setData(button, 'data-ui-v4', 'icon');
      setImportant(button.style, 'border', '0px');
      setImportant(button.style, 'border-image', 'none');
      setImportant(button.style, 'border-radius', '0px');
      setImportant(button.style, 'background-color', 'transparent');
      setImportant(button.style, 'box-shadow', 'none');
      return;
    }
    var skin = SKINS[contract.skin] || SKINS.classic;
    var size = SIZES[contract.size] || SIZES.standard;
    var mobile = document.body.classList.contains('mmode') || window.innerWidth <= 700;
    var measuredMinHeight = Math.max(0, parseInt(button.dataset.uiMeasuredMinHeight || '0', 10) || 0);
    var minHeight = Math.max(skin.minHeight, size.minHeight, mobile ? 40 : 0, measuredMinHeight);
    var contentFit = safeMatches(button, FIT_CONTENT_SELECTOR) && labelOf(button).length <= 24;
    var skillTab = safeMatches(button, '#rpanel-skills .skill-tab');
    var borderX = skillTab ? 10 : skin.x;
    var paddingX = skillTab ? 4 : (size.px + (skin.safe || 0));
    setData(button, 'data-ui-v4', 'button');
    setImportant(button.style, 'border-style', 'solid');
    setImportant(button.style, 'border-color', 'transparent');
    setImportant(button.style, 'border-width', skin.y + 'px ' + borderX + 'px');
    setImportant(button.style, 'border-image', 'url("' + skin.image + '") ' + skin.slice + ' fill / ' + skin.y + 'px ' + borderX + 'px stretch');
    setImportant(button.style, 'border-radius', '0px');
    setImportant(button.style, 'background-image', 'none');
    setImportant(button.style, 'background-color', 'transparent');
    setImportant(button.style, 'box-shadow', 'none');
    setImportant(button.style, 'box-sizing', 'border-box');
    setImportant(button.style, 'height', 'auto');
    setImportant(button.style, 'min-height', minHeight + 'px');
    setData(button, 'data-ui-fit', contentFit ? 'content' : 'layout');
    setImportant(button.style, 'min-width', contentFit ? 'max-content' : '0px');
    setImportant(button.style, 'max-width', '100%');
    setImportant(button.style, 'padding', size.py + 'px ' + paddingX + 'px');
    setImportant(button.style, 'font-size', size.fontSize + 'px');
    setImportant(button.style, 'line-height', String(size.lineHeight));
    setImportant(button.style, 'white-space', (contentFit || skillTab) ? 'nowrap' : 'normal');
    setImportant(button.style, 'overflow-wrap', button.dataset.uiHardWrap === 'true' ? 'anywhere' : 'normal');
    setImportant(button.style, 'word-break', skillTab ? 'keep-all' : 'normal');
    setImportant(button.style, 'text-overflow', 'clip');
    setImportant(button.style, 'overflow', 'visible');
    updateVisualState(button);
  }
  function normalizeFrame(element, rule) {
    if (!element || !rule) return;
    var override = element.dataset.uiFrameSkinOverride;
    var skinName = override || rule.skin;
    var skin = FRAME_SKINS[skinName];
    if (!skin) return;
    var mobile = document.body.classList.contains('mmode') || window.innerWidth <= 700;
    var y = mobile ? Math.min(skin.y, 26) : skin.y;
    var x = mobile ? Math.min(skin.x, 26) : skin.x;
    setData(element, 'data-ui-frame-v4', rule.type || 'panel');
    setData(element, 'data-ui-frame-skin', skinName);
    setImportant(element.style, 'border-style', 'solid');
    setImportant(element.style, 'border-color', 'transparent');
    setImportant(element.style, 'border-width', y + 'px ' + x + 'px');
    setImportant(element.style, 'border-image', 'url("' + skin.image + '") ' + skin.slice + ' fill / ' + y + 'px ' + x + 'px stretch');
    setImportant(element.style, 'border-radius', '0px');
    setImportant(element.style, 'box-sizing', 'border-box');
    if (skin.surface) setImportant(element.style, 'background-color', 'rgba(9, 8, 8, ' + skin.surface + ')');
  }
  var FRAMELESS_FRAME_SELECTOR = '#zone-title-col, #boss-announce, #unique-flash-overlay';
  function normalizeFrames(root) {
    FRAME_RULES.forEach(function (rule) {
      if (root.nodeType === 1 && safeMatches(root, rule.selector)) normalizeFrame(root, rule);
      var found = root.querySelectorAll ? root.querySelectorAll(rule.selector) : [];
      Array.prototype.forEach.call(found, function (element) { normalizeFrame(element, rule); });
    });
    var frameless = [];
    if (root.nodeType === 1 && safeMatches(root, FRAMELESS_FRAME_SELECTOR)) frameless.push(root);
    if (root.querySelectorAll) frameless = frameless.concat(Array.prototype.slice.call(root.querySelectorAll(FRAMELESS_FRAME_SELECTOR)));
    frameless.forEach(function (element) {
      setData(element, 'data-ui-frame-v4', 'none');
      setData(element, 'data-ui-frame-skin', 'none');
      setImportant(element.style, 'border', '0px');
      setImportant(element.style, 'border-image', 'none');
      setImportant(element.style, 'border-radius', '0px');
      setImportant(element.style, 'background', 'transparent');
      setImportant(element.style, 'box-shadow', 'none');
    });
  }
  function normalizeTree(root) {
    if (!root) return;
    if (root.nodeType === 1 && root.tagName === 'BUTTON') normalizeButton(root);
    var list = root.querySelectorAll ? root.querySelectorAll('button') : [];
    Array.prototype.forEach.call(list, normalizeButton);
    normalizeFrames(root);
  }
  function syncSkillPointsBadge() {
    var source = document.getElementById('skill-pts-label');
    var tile = document.getElementById('skill-tree-toggle');
    if (!source || !tile) return;
    var match = String(source.textContent || '').match(/\d+/);
    var points = match ? Number(match[0]) : 0;
    setData(tile, 'data-sp', points > 0 ? 'SP ' + points : '');
    tile.setAttribute('aria-label', points > 0 ? 'Skill Levels, ' + points + ' skill points available' : 'Skill Levels');
  }
  function auditButtons() {
    var results = [];
    Array.prototype.forEach.call(document.querySelectorAll('button[data-ui-v4]'), function (button) {
      if (button.dataset.uiV4 !== 'button') { button.removeAttribute('data-ui-overflow'); return; }
      var rect = button.getBoundingClientRect();
      if (rect.width < 1 || rect.height < 1) { button.removeAttribute('data-ui-overflow'); return; }
      var overflowX = button.scrollWidth > button.clientWidth + 1;
      var overflowY = button.scrollHeight > button.clientHeight + 1;
      if (overflowY && button.dataset.uiV4 === 'button' && safeMatches(button, FIT_CONTENT_SELECTOR)) {
        /* A few legacy layouts impose a smaller box after the button is built.
           Measure the real text instead of guessing from its character count,
           then persist the repair so later normalizations cannot shrink it. */
        var repairedHeight = Math.min(160, Math.ceil(rect.height + (button.scrollHeight - button.clientHeight) + 6));
        var priorRepair = parseInt(button.dataset.uiMeasuredMinHeight || '0', 10) || 0;
        if (repairedHeight > priorRepair) {
          setData(button, 'data-ui-measured-min-height', String(repairedHeight));
          setImportant(button.style, 'min-height', repairedHeight + 'px');
          rect = button.getBoundingClientRect();
          overflowY = button.scrollHeight > button.clientHeight + 1;
        }
      }
      if (overflowX || overflowY) {
        button.setAttribute('data-ui-overflow', 'true');
        results.push({ id: button.id || '', classes: button.className || '', label: labelOf(button), overflowX: overflowX, overflowY: overflowY, client: [button.clientWidth, button.clientHeight], scroll: [button.scrollWidth, button.scrollHeight], skin: button.dataset.uiSkin, size: button.dataset.uiSize });
      } else button.removeAttribute('data-ui-overflow');
    });
    return results;
  }
  var auditTimer = 0;
  function scheduleAudit() { window.clearTimeout(auditTimer); auditTimer = window.setTimeout(auditButtons, 80); }
  function handleMutations(records) {
    records.forEach(function (record) {
      if (record.type === 'childList') Array.prototype.forEach.call(record.addedNodes, normalizeTree);
      else if (record.target === document.body && record.attributeName === 'class') normalizeTree(document);
      else if (record.target && record.target.tagName === 'BUTTON') normalizeButton(record.target);
    });
    syncSkillPointsBadge();
    scheduleAudit();
  }
  function boot() {
    document.body.classList.add('v4-button-system');
    normalizeTree(document);
    syncSkillPointsBadge();
    new MutationObserver(handleMutations).observe(document.documentElement, { childList: true, subtree: true, attributes: true, attributeFilter: ['class', 'style', 'disabled', 'aria-disabled', 'aria-pressed', 'aria-selected'] });
    ['pointerover', 'pointerout', 'pointerdown', 'pointerup', 'focusin', 'focusout'].forEach(function (name) {
      document.addEventListener(name, function (event) {
        var button = event.target && event.target.closest ? event.target.closest('button[data-ui-v4="button"]') : null;
        if (button) window.requestAnimationFrame(function () { updateVisualState(button); });
      }, true);
    });
    window.addEventListener('resize', function () { normalizeTree(document); scheduleAudit(); }, { passive: true });
    window.setTimeout(scheduleAudit, 250);
    window.setTimeout(scheduleAudit, 1200);
  }

  window.EverdeepV4Buttons = {
    version: '4.0.1', skins: SKINS, sizes: SIZES, rules: RULES, frameSkins: FRAME_SKINS, frameRules: FRAME_RULES,
    normalize: function () { normalizeTree(document); return auditButtons(); },
    audit: auditButtons,
    setDebug: function (enabled) { document.body.classList.toggle('v4-button-debug', Boolean(enabled)); return auditButtons(); },
    setSkin: function (selector, skin, size) {
      Array.prototype.forEach.call(document.querySelectorAll(selector), function (button) {
        button.dataset.uiSkinOverride = skin;
        if (size) button.dataset.uiSizeOverride = size;
        normalizeButton(button);
      });
      return auditButtons();
    },
    setFrame: function (selector, skin) {
      Array.prototype.forEach.call(document.querySelectorAll(selector), function (element) {
        element.dataset.uiFrameSkinOverride = skin;
      });
      normalizeFrames(document); return true;
    },
    exportConfig: function () {
      return {
        format: 'everdeep-v4-skin-config', version: 1,
        iconOnlySelector: ICON_ONLY_SELECTOR,
        buttons: RULES.map(function (rule) { return { selector: rule.selector, skin: rule.skin, size: rule.size || null }; }),
        frames: FRAME_RULES.map(function (rule) { return { selector: rule.selector, skin: rule.skin, type: rule.type }; })
      };
    },
    importConfig: function (config) {
      if (!config || config.format !== 'everdeep-v4-skin-config') throw new Error('Unsupported v4 skin config.');
      (config.buttons || []).forEach(function (rule) { if (rule.selector) RULES.push(rule); });
      (config.frames || []).forEach(function (rule) { if (rule.selector) FRAME_RULES.push(rule); });
      normalizeTree(document); return auditButtons();
    },
    registerRule: function (rule) {
      if (!rule || !rule.selector) throw new Error('A selector is required.');
      RULES.push(rule); normalizeTree(document); return RULES.length;
    }
  };
  window.EverdeepV4Skins = window.EverdeepV4Buttons;
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, { once: true });
  else boot();
})();
