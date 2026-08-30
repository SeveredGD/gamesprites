(function () {
  const AVAILABLE_SIZES = [16, 20, 24, 28, 32, 40, 48];

  function nearestSize(requested) {
    return AVAILABLE_SIZES.reduce((best, size) =>
      Math.abs(size - requested) < Math.abs(best - requested) ? size : best
    );
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function renderReservoir(root) {
    const chambers = Math.max(2, Number(root.dataset.chambers) || 2);
    const maxSips = chambers * 2;
    const sips = clamp(Number(root.dataset.sips) || 0, 0, maxSips);
    const size = nearestSize(Number(root.dataset.size) || 20);
    const assetRoot = root.dataset.assetRoot || "assets";

    root.dataset.sips = String(sips);
    root.dataset.size = String(size);
    root.setAttribute("role", "img");
    root.setAttribute("aria-label", `${sips} of ${maxSips} relic sips`);
    root.innerHTML = "";

    for (let index = 0; index < chambers; index += 1) {
      const part = index === 0 ? "left" : index === chambers - 1 ? "right" : "center";
      const state = clamp(sips - index * 2, 0, 2);
      const image = document.createElement("img");
      image.className = "relic-reservoir__module";
      image.alt = "";
      image.draggable = false;
      image.height = size;
      image.src = `${assetRoot}/${size}px/${part}-${state}.png`;
      root.appendChild(image);
    }
  }

  function renderAll(scope = document) {
    scope.querySelectorAll(".relic-reservoir").forEach(renderReservoir);
  }

  window.EverdeepRelicReservoir = {
    render: renderReservoir,
    renderAll,
    set(root, { chambers, sips, size } = {}) {
      if (chambers != null) root.dataset.chambers = chambers;
      if (sips != null) root.dataset.sips = sips;
      if (size != null) root.dataset.size = size;
      renderReservoir(root);
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => renderAll());
  } else {
    renderAll();
  }
}());
