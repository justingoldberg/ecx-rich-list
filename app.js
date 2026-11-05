/**
 * eCash (ECX) Drivechain Whale Index & Top 500 UTXO Rich List
 * Snapshot at Hard Fork Block #973,728
 */

(function () {
  "use strict";

  // Application State
  const state = {
    utxos: [],
    filtered: [],
    currentPage: 1,
    pageSize: 50,
    sortField: "rank",
    sortDir: "asc",
    currency: "ECX",
    ecxPriceUsd: 100000,
    searchQuery: "",
    selectedCategory: "ALL",
    selectedType: "ALL",
    selectedTier: "ALL",
    selectedUtxo: null
  };

  const TOTAL_ESTIMATED_SUPPLY = 19780000; // ~19.78M ECX at fork block 973,728

  // DOM Elements
  const elements = {
    priceSlider: document.getElementById("price-slider"),
    priceDisplay: document.getElementById("price-display"),
    btnCurrEcx: document.getElementById("btn-curr-ecx"),
    btnCurrUsd: document.getElementById("btn-curr-usd"),
    statTotalAmount: document.getElementById("stat-total-amount"),
    statSupplyPct: document.getElementById("stat-supply-pct"),
    statLargestUtxo: document.getElementById("stat-largest-utxo"),
    statLargestEntity: document.getElementById("stat-largest-entity"),
    statCutoffUtxo: document.getElementById("stat-cutoff-utxo"),
    statAvgUtxo: document.getElementById("stat-avg-utxo"),
    statAvgUsd: document.getElementById("stat-avg-usd"),
    heroTotalTracked: document.getElementById("hero-total-tracked"),
    scriptDistContainer: document.getElementById("script-distribution-container"),
    canvasChart: document.getElementById("concentration-chart"),
    searchInput: document.getElementById("search-input"),
    filterCategory: document.getElementById("filter-category"),
    filterType: document.getElementById("filter-type"),
    filterTier: document.getElementById("filter-tier"),
    resultsCount: document.getElementById("results-count"),
    activeFiltersContainer: document.getElementById("active-filters-container"),
    utxoTbody: document.getElementById("utxo-tbody"),
    pageSizeSelect: document.getElementById("page-size-select"),
    paginationControls: document.getElementById("pagination-controls"),
    tableHeaders: document.querySelectorAll("th.sortable"),
    btnExportCsv: document.getElementById("btn-export-csv"),
    btnQuickExportCsv: document.getElementById("btn-quick-export-csv"),
    btnExportJson: document.getElementById("btn-export-json"),
    modal: document.getElementById("utxo-modal"),
    modalCloseBtn: document.getElementById("modal-close-btn"),
    toast: document.getElementById("toast"),
    toastMsg: document.getElementById("toast-msg")
  };

  // Helper Formatters
  function formatEcx(val) {
    return new Intl.NumberFormat("en-US", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 4
    }).format(val) + " ECX";
  }

  function formatUsd(val) {
    const usdVal = val * state.ecxPriceUsd;
    if (usdVal >= 1e9) {
      return "$" + (usdVal / 1e9).toFixed(2) + "B";
    }
    if (usdVal >= 1e6) {
      return "$" + (usdVal / 1e6).toFixed(2) + "M";
    }
    return "$" + new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(usdVal);
  }

  function formatDisplayAmount(val) {
    return state.currency === "USD" ? formatUsd(val) : formatEcx(val);
  }

  function truncateAddress(addr) {
    if (!addr || addr.length <= 16) return addr;
    return addr.substring(0, 8) + "..." + addr.substring(addr.length - 8);
  }

  function showToast(message) {
    if (!elements.toast) return;
    elements.toastMsg.textContent = message;
    elements.toast.classList.add("show");
    setTimeout(() => {
      elements.toast.classList.remove("show");
    }, 2400);
  }

  function copyToClipboard(text, label = "Item") {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => {
        showToast(`${label} copied to clipboard!`);
      }).catch(() => {
        fallbackCopy(text, label);
      });
    } else {
      fallbackCopy(text, label);
    }
  }

  function fallbackCopy(text, label) {
    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.left = "-9999px";
    document.body.appendChild(textarea);
    textarea.select();
    try {
      document.execCommand("copy");
      showToast(`${label} copied to clipboard!`);
    } catch (e) {
      showToast("Unable to copy");
    }
    document.body.removeChild(textarea);
  }

  // Load Data
  async function loadData() {
    if (window.ECX_TOP_500_UTXOS && Array.isArray(window.ECX_TOP_500_UTXOS)) {
      state.utxos = window.ECX_TOP_500_UTXOS;
      initApp();
      return;
    }

    try {
      const res = await fetch("data/utxos.json");
      if (!res.ok) throw new Error("Failed to load utxos.json");
      state.utxos = await res.json();
      initApp();
    } catch (err) {
      console.error("Error loading UTXO dataset:", err);
      elements.resultsCount.textContent = "Error loading UTXO dataset. Check console.";
    }
  }

  // Initialize Application
  function initApp() {
    applyFilters();
    updateKpis();
    renderScriptDistribution();
    setupCanvasChart();
    attachEvents();
  }

  // Calculate & Update Metrics
  function updateKpis() {
    if (!state.utxos.length) return;

    const totalTrackedAmount = state.utxos.reduce((sum, u) => sum + u.amount, 0);
    const largest = state.utxos[0];
    const cutoff = state.utxos[state.utxos.length - 1];
    const avg = totalTrackedAmount / state.utxos.length;
    const supplyPct = ((totalTrackedAmount / TOTAL_ESTIMATED_SUPPLY) * 100).toFixed(2);

    elements.statTotalAmount.textContent = formatDisplayAmount(totalTrackedAmount);
    elements.statSupplyPct.textContent = `~${supplyPct}% of Circulating Supply (${formatEcx(totalTrackedAmount)})`;
    elements.statLargestUtxo.textContent = formatDisplayAmount(largest.amount);
    elements.statLargestEntity.textContent = `${largest.entity} (${formatEcx(largest.amount)})`;
    elements.statCutoffUtxo.textContent = formatDisplayAmount(cutoff.amount);
    elements.statAvgUtxo.textContent = formatDisplayAmount(avg);
    elements.statAvgUsd.textContent = state.currency === "USD" ? formatEcx(avg) : formatUsd(avg);
    elements.heroTotalTracked.textContent = `${state.utxos.length} UTXOs (${(totalTrackedAmount / 1e6).toFixed(2)}M ECX)`;
  }

  // Script Type Distribution Card
  function renderScriptDistribution() {
    const counts = { P2WPKH: 0, P2TR: 0, P2SH: 0, P2PKH: 0 };
    const amounts = { P2WPKH: 0, P2TR: 0, P2SH: 0, P2PKH: 0 };
    const colors = {
      P2WPKH: "var(--accent-cyan)",
      P2TR: "var(--accent-emerald)",
      P2SH: "var(--accent-purple)",
      P2PKH: "var(--accent-amber)"
    };
    const labels = {
      P2WPKH: "P2WPKH (Native SegWit)",
      P2TR: "P2TR (Taproot BIP-341)",
      P2SH: "P2SH (Legacy Multi-Sig)",
      P2PKH: "P2PKH (Legacy P2PKH)"
    };

    state.utxos.forEach(u => {
      if (counts[u.type] !== undefined) {
        counts[u.type]++;
        amounts[u.type] += u.amount;
      }
    });

    const total = state.utxos.length;
    let html = "";

    for (const [type, count] of Object.entries(counts)) {
      const pct = ((count / total) * 100).toFixed(1);
      html += `
        <div class="script-row">
          <div class="script-row-header">
            <span style="color: ${colors[type]}; font-weight: 600;">${labels[type]}</span>
            <span style="font-family: var(--font-mono);">${count} UTXOs (${pct}%)</span>
          </div>
          <div class="script-progress-bg">
            <div class="script-progress-bar" style="width: ${pct}%; background: ${colors[type]};"></div>
          </div>
        </div>
      `;
    }

    elements.scriptDistContainer.innerHTML = html;
  }

  // Responsive Concentration Curve Chart
  function setupCanvasChart() {
    const canvas = elements.canvasChart;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");

    function drawChart() {
      const rect = canvas.parentElement.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);

      const width = rect.width;
      const height = rect.height;
      const padding = { top: 20, right: 20, bottom: 30, left: 60 };
      const chartWidth = width - padding.left - padding.right;
      const chartHeight = height - padding.top - padding.bottom;

      ctx.clearRect(0, 0, width, height);

      if (!state.utxos.length) return;

      const maxVal = state.utxos[0].amount;
      const minVal = state.utxos[state.utxos.length - 1].amount;

      // Draw Grid Lines & Y-axis labels
      ctx.strokeStyle = "rgba(255, 255, 255, 0.06)";
      ctx.fillStyle = "#64748b";
      ctx.font = "10px monospace";
      ctx.lineWidth = 1;

      const yTicks = 4;
      for (let i = 0; i <= yTicks; i++) {
        const val = minVal + (maxVal - minVal) * (1 - i / yTicks);
        const y = padding.top + (chartHeight * (i / yTicks));
        
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(width - padding.right, y);
        ctx.stroke();

        ctx.textAlign = "right";
        ctx.fillText((val / 1000).toFixed(0) + "k ECX", padding.left - 8, y + 3);
      }

      // Build Curve Points
      const points = [];
      const n = state.utxos.length;
      for (let i = 0; i < n; i++) {
        const x = padding.left + (i / (n - 1)) * chartWidth;
        const normalizedY = (state.utxos[i].amount - minVal) / (maxVal - minVal);
        const y = padding.top + chartHeight * (1 - normalizedY);
        points.push({ x, y, u: state.utxos[i] });
      }

      // Draw Gradient Area
      const grad = ctx.createLinearGradient(0, padding.top, 0, padding.top + chartHeight);
      grad.addColorStop(0, "rgba(6, 182, 212, 0.35)");
      grad.addColorStop(1, "rgba(6, 182, 212, 0.0)");

      ctx.beginPath();
      ctx.moveTo(points[0].x, padding.top + chartHeight);
      for (let i = 0; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
      }
      ctx.lineTo(points[points.length - 1].x, padding.top + chartHeight);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();

      // Draw Line
      ctx.beginPath();
      ctx.moveTo(points[0].x, points[0].y);
      for (let i = 1; i < points.length; i++) {
        ctx.lineTo(points[i].x, points[i].y);
      }
      ctx.strokeStyle = "#06b6d4";
      ctx.lineWidth = 2.5;
      ctx.stroke();

      // X-axis labels
      ctx.fillStyle = "#64748b";
      ctx.textAlign = "center";
      ctx.fillText("#1 (Whale Apex)", padding.left + 40, height - 10);
      ctx.fillText("#250 (Mid)", padding.left + chartWidth / 2, height - 10);
      ctx.fillText("#500 (Cutoff)", width - padding.right - 35, height - 10);
    }

    drawChart();
    window.addEventListener("resize", drawChart);
  }

  // Apply Filter, Search & Sort
  function applyFilters() {
    let result = [...state.utxos];

    // Search query
    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase().trim();
      result = result.filter(u => 
        u.address.toLowerCase().includes(q) ||
        u.entity.toLowerCase().includes(q) ||
        u.txid.toLowerCase().includes(q) ||
        String(u.rank) === q ||
        String(u.block_height).includes(q)
      );
    }

    // Category filter
    if (state.selectedCategory !== "ALL") {
      result = result.filter(u => u.category.includes(state.selectedCategory));
    }

    // Script type filter
    if (state.selectedType !== "ALL") {
      result = result.filter(u => u.type === state.selectedType);
    }

    // Tier filter
    if (state.selectedTier !== "ALL") {
      if (state.selectedTier === "MEGA") {
        result = result.filter(u => u.amount >= 50000);
      } else if (state.selectedTier === "LARGE") {
        result = result.filter(u => u.amount >= 10000 && u.amount < 50000);
      } else if (state.selectedTier === "MID") {
        result = result.filter(u => u.amount >= 5000 && u.amount < 10000);
      } else if (state.selectedTier === "SMALL") {
        result = result.filter(u => u.amount < 5000);
      }
    }

    // Sort
    result.sort((a, b) => {
      let valA = a[state.sortField];
      let valB = b[state.sortField];

      if (typeof valA === "string") {
        return state.sortDir === "asc"
          ? valA.localeCompare(valB)
          : valB.localeCompare(valA);
      }

      return state.sortDir === "asc" ? valA - valB : valB - valA;
    });

    state.filtered = result;
    state.currentPage = 1;
    renderTable();
    renderPagination();
    renderActiveFilterBadges();
  }

  // Active filter badge pills
  function renderActiveFilterBadges() {
    const pills = [];

    if (state.searchQuery) {
      pills.push({ label: `Search: "${state.searchQuery}"`, action: () => { state.searchQuery = ""; elements.searchInput.value = ""; applyFilters(); } });
    }
    if (state.selectedCategory !== "ALL") {
      pills.push({ label: `Category: ${state.selectedCategory}`, action: () => { state.selectedCategory = "ALL"; elements.filterCategory.value = "ALL"; applyFilters(); } });
    }
    if (state.selectedType !== "ALL") {
      pills.push({ label: `Type: ${state.selectedType}`, action: () => { state.selectedType = "ALL"; elements.filterType.value = "ALL"; applyFilters(); } });
    }
    if (state.selectedTier !== "ALL") {
      pills.push({ label: `Tier: ${state.selectedTier}`, action: () => { state.selectedTier = "ALL"; elements.filterTier.value = "ALL"; applyFilters(); } });
    }

    elements.activeFiltersContainer.innerHTML = pills.map((p, idx) => `
      <div class="filter-pill">
        <span>${p.label}</span>
        <button data-pill-idx="${idx}">&times;</button>
      </div>
    `).join("");

    elements.activeFiltersContainer.querySelectorAll("button").forEach(btn => {
      btn.addEventListener("click", () => {
        const idx = Number(btn.getAttribute("data-pill-idx"));
        pills[idx].action();
      });
    });

    elements.resultsCount.textContent = `Showing ${state.filtered.length} of ${state.utxos.length} UTXOs`;
  }

  // Category Tag CSS helper
  function getCategoryTagClass(cat) {
    if (cat.includes("Exchange")) return "tag-exchange";
    if (cat.includes("Institutional")) return "tag-institutional";
    if (cat.includes("Dormant")) return "tag-dormant";
    if (cat.includes("Protocol") || cat.includes("Drivechain")) return "tag-protocol";
    return "tag-defi";
  }

  // Render Table
  function renderTable() {
    const tbody = elements.utxoTbody;
    tbody.innerHTML = "";

    if (!state.filtered.length) {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" style="text-align: center; padding: 40px; color: var(--text-muted);">
            No UTXOs match the current filter criteria.
          </td>
        </tr>
      `;
      return;
    }

    const startIdx = (state.currentPage - 1) * state.pageSize;
    const endIdx = Math.min(startIdx + state.pageSize, state.filtered.length);
    const pageItems = state.filtered.slice(startIdx, endIdx);

    const maxAmountInSet = state.utxos[0] ? state.utxos[0].amount : 1;

    const rows = pageItems.map(u => {
      const barPct = Math.max(3, (u.amount / maxAmountInSet) * 100).toFixed(1);
      const rankClass = u.rank <= 3 ? "top-3" : (u.rank <= 10 ? "top-10" : "");
      const tagClass = getCategoryTagClass(u.category);
      const typeClass = u.type.toLowerCase();

      return `
        <tr data-rank="${u.rank}">
          <td>
            <span class="rank-badge ${rankClass}">#${u.rank}</span>
          </td>
          <td>
            <div class="entity-cell">
              <span class="entity-name">${escapeHtml(u.entity)}</span>
              <span class="category-tag ${tagClass}">${escapeHtml(u.category)}</span>
            </div>
          </td>
          <td>
            <div class="address-cell">
              <a href="javascript:void(0)" class="address-text" data-action="inspect" data-rank="${u.rank}" title="${u.address}">
                ${truncateAddress(u.address)}
              </a>
              <button class="btn-copy" data-copy="${u.address}" title="Copy Address">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              </button>
            </div>
          </td>
          <td class="amount-cell">
            <div class="amount-main">${formatDisplayAmount(u.amount)}</div>
            <div class="amount-sub">${state.currency === "USD" ? formatEcx(u.amount) : formatUsd(u.amount)}</div>
            <div class="amount-bar-container">
              <div class="amount-bar-fill" style="width: ${barPct}%;"></div>
            </div>
          </td>
          <td style="text-align: center;">
            <span class="type-badge ${typeClass}">${u.type}</span>
          </td>
          <td>
            <div style="font-family: var(--font-mono); font-size: 0.8rem; color: #fff;">#${u.block_height.toLocaleString()}</div>
            <div style="font-size: 0.72rem; color: var(--text-muted);">${u.date}</div>
          </td>
          <td style="text-align: center;">
            <span style="display: inline-flex; align-items: center; gap: 4px; font-size: 0.75rem; color: var(--accent-emerald); font-weight: 600;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Ready
            </span>
          </td>
          <td style="text-align: center;">
            <button class="btn-inspect" data-action="inspect" data-rank="${u.rank}">
              Inspect
            </button>
          </td>
        </tr>
      `;
    }).join("");

    tbody.innerHTML = rows;
  }

  // Render Pagination
  function renderPagination() {
    const totalPages = Math.ceil(state.filtered.length / state.pageSize) || 1;
    const controls = elements.paginationControls;

    let html = `
      <button class="page-btn" id="page-prev" ${state.currentPage === 1 ? "disabled" : ""}>&larr;</button>
    `;

    // Window logic for page buttons
    const maxBtns = 5;
    let startPage = Math.max(1, state.currentPage - 2);
    let endPage = Math.min(totalPages, startPage + maxBtns - 1);
    if (endPage - startPage < maxBtns - 1) {
      startPage = Math.max(1, endPage - maxBtns + 1);
    }

    if (startPage > 1) {
      html += `<button class="page-btn" data-page="1">1</button>`;
      if (startPage > 2) html += `<span style="color: var(--text-muted); padding: 0 4px;">...</span>`;
    }

    for (let p = startPage; p <= endPage; p++) {
      html += `
        <button class="page-btn ${p === state.currentPage ? "active" : ""}" data-page="${p}">${p}</button>
      `;
    }

    if (endPage < totalPages) {
      if (endPage < totalPages - 1) html += `<span style="color: var(--text-muted); padding: 0 4px;">...</span>`;
      html += `<button class="page-btn" data-page="${totalPages}">${totalPages}</button>`;
    }

    html += `
      <button class="page-btn" id="page-next" ${state.currentPage === totalPages ? "disabled" : ""}>&rarr;</button>
    `;

    controls.innerHTML = html;

    // Attach listeners
    controls.querySelectorAll(".page-btn[data-page]").forEach(btn => {
      btn.addEventListener("click", () => {
        state.currentPage = Number(btn.getAttribute("data-page"));
        renderTable();
        renderPagination();
      });
    });

    const prevBtn = document.getElementById("page-prev");
    if (prevBtn) {
      prevBtn.addEventListener("click", () => {
        if (state.currentPage > 1) {
          state.currentPage--;
          renderTable();
          renderPagination();
        }
      });
    }

    const nextBtn = document.getElementById("page-next");
    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        if (state.currentPage < totalPages) {
          state.currentPage++;
          renderTable();
          renderPagination();
        }
      });
    }
  }

  // Open Modal
  function openModal(utxo) {
    if (!utxo) return;
    state.selectedUtxo = utxo;

    document.getElementById("modal-rank-badge").textContent = `Rank #${utxo.rank}`;
    const catTag = document.getElementById("modal-category-tag");
    catTag.textContent = utxo.category;
    catTag.className = "category-tag " + getCategoryTagClass(utxo.category);
    document.getElementById("modal-entity-title").textContent = utxo.entity;
    document.getElementById("modal-amount-ecx").textContent = formatEcx(utxo.amount);
    document.getElementById("modal-amount-usd").textContent = formatUsd(utxo.amount);
    document.getElementById("modal-address").textContent = utxo.address;
    document.getElementById("modal-txid").textContent = utxo.txid;
    document.getElementById("modal-vout").textContent = utxo.vout;
    document.getElementById("modal-block").textContent = `Block #${utxo.block_height.toLocaleString()}`;
    document.getElementById("modal-date").textContent = `Confirmed ~${utxo.date}`;
    document.getElementById("modal-script-hex").textContent = utxo.script_hex || "0014...";

    elements.modal.classList.add("active");
  }

  function closeModal() {
    elements.modal.classList.remove("active");
    state.selectedUtxo = null;
  }

  // Attach Event Handlers
  function attachEvents() {
    // Price Slider
    elements.priceSlider.addEventListener("input", (e) => {
      state.ecxPriceUsd = Number(e.target.value);
      elements.priceDisplay.textContent = "$" + state.ecxPriceUsd.toLocaleString();
      updateKpis();
      renderTable();
      if (state.selectedUtxo) openModal(state.selectedUtxo);
    });

    // Currency Switcher
    elements.btnCurrEcx.addEventListener("click", () => {
      state.currency = "ECX";
      elements.btnCurrEcx.classList.add("active");
      elements.btnCurrUsd.classList.remove("active");
      updateKpis();
      renderTable();
    });

    elements.btnCurrUsd.addEventListener("click", () => {
      state.currency = "USD";
      elements.btnCurrUsd.classList.add("active");
      elements.btnCurrEcx.classList.remove("active");
      updateKpis();
      renderTable();
    });

    // Search input (debounced)
    let searchDebounce;
    elements.searchInput.addEventListener("input", (e) => {
      clearTimeout(searchDebounce);
      searchDebounce = setTimeout(() => {
        state.searchQuery = e.target.value;
        applyFilters();
      }, 180);
    });

    // Category filter
    elements.filterCategory.addEventListener("change", (e) => {
      state.selectedCategory = e.target.value;
      applyFilters();
    });

    // Script type filter
    elements.filterType.addEventListener("change", (e) => {
      state.selectedType = e.target.value;
      applyFilters();
    });

    // Tier filter
    elements.filterTier.addEventListener("change", (e) => {
      state.selectedTier = e.target.value;
      applyFilters();
    });

    // Page size select
    elements.pageSizeSelect.addEventListener("change", (e) => {
      state.pageSize = Number(e.target.value);
      state.currentPage = 1;
      renderTable();
      renderPagination();
    });

    // Sortable Headers
    elements.tableHeaders.forEach(th => {
      th.addEventListener("click", () => {
        const field = th.getAttribute("data-sort");
        if (state.sortField === field) {
          state.sortDir = state.sortDir === "asc" ? "desc" : "asc";
        } else {
          state.sortField = field;
          state.sortDir = field === "amount" ? "desc" : "asc";
        }

        // Update indicator arrows
        elements.tableHeaders.forEach(h => {
          const arrow = h.querySelector(".sort-arrow");
          if (h === th) {
            arrow.textContent = state.sortDir === "asc" ? "▲" : "▼";
          } else {
            arrow.textContent = "";
          }
        });

        applyFilters();
      });
    });

    // Table Clicks (delegated)
    elements.utxoTbody.addEventListener("click", (e) => {
      const inspectBtn = e.target.closest("[data-action='inspect']");
      if (inspectBtn) {
        const rank = Number(inspectBtn.getAttribute("data-rank"));
        const item = state.utxos.find(u => u.rank === rank);
        if (item) openModal(item);
        return;
      }

      const copyBtn = e.target.closest("[data-copy]");
      if (copyBtn) {
        const text = copyBtn.getAttribute("data-copy");
        copyToClipboard(text, "Address");
      }
    });

    // Modal Close
    elements.modalCloseBtn.addEventListener("click", closeModal);
    elements.modal.addEventListener("click", (e) => {
      if (e.target === elements.modal) closeModal();
    });
    window.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && elements.modal.classList.contains("active")) {
        closeModal();
      }
    });

    // Modal Copy Buttons
    document.getElementById("btn-modal-copy-addr").addEventListener("click", () => {
      if (state.selectedUtxo) copyToClipboard(state.selectedUtxo.address, "Address");
    });
    document.getElementById("btn-modal-copy-txid").addEventListener("click", () => {
      if (state.selectedUtxo) copyToClipboard(state.selectedUtxo.txid, "Transaction Hash");
    });

    // Export CSV
    const triggerCsvExport = () => {
      exportToCsv(state.filtered);
    };
    elements.btnExportCsv.addEventListener("click", triggerCsvExport);
    elements.btnQuickExportCsv.addEventListener("click", triggerCsvExport);

    // Export JSON
    elements.btnExportJson.addEventListener("click", () => {
      exportToJson(state.filtered);
    });
  }

  // CSV Exporter
  function exportToCsv(data) {
    if (!data.length) {
      showToast("No data to export");
      return;
    }

    const headers = [
      "Rank",
      "Entity",
      "Category",
      "Address",
      "Amount_ECX",
      "Amount_USD",
      "Script_Type",
      "Block_Height",
      "Confirmed_Date",
      "TXID",
      "Vout",
      "BIP300_Eligible"
    ];

    const rows = data.map(u => [
      u.rank,
      `"${(u.entity || "").replace(/"/g, '""')}"`,
      `"${(u.category || "").replace(/"/g, '""')}"`,
      u.address,
      u.amount.toFixed(4),
      (u.amount * state.ecxPriceUsd).toFixed(2),
      u.type,
      u.block_height,
      u.date,
      u.txid,
      u.vout,
      "TRUE"
    ]);

    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(r => r.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `ECX_Drivechain_Top_${data.length}_UTXOs.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast(`Exported ${data.length} UTXOs to CSV!`);
  }

  // JSON Exporter
  function exportToJson(data) {
    if (!data.length) {
      showToast("No data to export");
      return;
    }
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `ECX_Drivechain_Top_${data.length}_UTXOs.json`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    showToast(`Exported ${data.length} UTXOs to JSON!`);
  }

  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Launch on DOM ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", loadData);
  } else {
    loadData();
  }
})();
