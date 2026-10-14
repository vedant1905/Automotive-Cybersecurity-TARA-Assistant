// Automotive Cybersecurity TARA Assistant - Frontend Client Logic

let allThreats = [];
let vehicleData = null;
let configData = null;

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  fetchInitialData();
  setupFilters();
  setupSimulator();
});

// 1. Navigation Tabs
function initTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      
      const target = tab.dataset.tab;
      document.querySelectorAll(".tab-content").forEach(content => {
        content.classList.remove("active");
      });
      document.getElementById(`tab-${target}`).classList.add("active");
    });
  });
}

// 2. Fetch Data from Local API
async function fetchInitialData() {
  try {
    const [threatsRes, vehicleRes, configRes] = await Promise.all([
      fetch("/api/threats"),
      fetch("/api/vehicle"),
      fetch("/api/config")
    ]);

    allThreats = await threatsRes.json();
    vehicleData = await vehicleRes.json();
    configData = await configRes.json();

    renderArchitecture(vehicleData);
    renderThreats(allThreats);
    populateCategoryDropdown(allThreats);
    populateSimulatorDropdowns(vehicleData, allThreats);
    renderAuditTable(allThreats);
    renderConfig(configData);
    updateRiskCalculation();
  } catch (err) {
    console.error("Failed to load local API data:", err);
  }
}

// 3. Render Vehicle Architecture
function renderArchitecture(data) {
  const container = document.getElementById("architecture-container");
  if (!container || !data.components) return;

  container.innerHTML = data.components.map(comp => `
    <div class="arch-card">
      <div class="arch-card-header">
        <span class="arch-id">${comp.id}</span>
        <span class="arch-zone">${comp.trust_zone}</span>
      </div>
      <h3>${comp.name}</h3>
      <p class="arch-desc">${comp.description}</p>
      
      <div class="arch-interfaces">
        ${comp.interfaces.map(i => `<span class="iface-badge">${i}</span>`).join("")}
      </div>
    </div>
  `).join("");
}

// 4. Render Threat Library
function renderThreats(threats) {
  const container = document.getElementById("threats-container");
  if (!container) return;

  if (threats.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding: 40px; color: var(--text-muted);">No threats match your search criteria.</div>`;
    return;
  }

  container.innerHTML = threats.map(t => {
    const capecBadges = t.capec.map(c => `
      <a href="https://capec.mitre.org/data/definitions/${c.id.replace('CAPEC-', '')}.html" target="_blank" class="tag-capec">
        ${c.id}: ${c.name} ↗
      </a>
    `).join("");

    const cweBadges = t.cwe.map(w => `
      <a href="https://cwe.mitre.org/data/definitions/${w.id.replace('CWE-', '')}.html" target="_blank" class="tag-cwe">
        ${w.id}: ${w.name} ↗
      </a>
    `).join("");

    const mitBadges = t.r155_mitigations.map(m => `
      <span class="tag-mitigation" title="${m.text_summary}">
        ${m.id}: ${m.text_summary.slice(0, 45)}...
      </span>
    `).join("");

    const confClass = t.mapping_confidence === "high" ? "badge-high" : (t.mapping_confidence === "medium" ? "badge-medium" : "badge-low");

    return `
      <div class="threat-card">
        <div class="threat-meta">
          <div>
            <span class="threat-id-pill">${t.id}</span>
            <span style="font-family: var(--font-mono); font-size: 11px; margin-left: 8px; color: #64748B;">UN R155: [${t.r155_threat_id}]</span>
          </div>
          <div>
            <span class="badge ${confClass}">CONFIDENCE: ${t.mapping_confidence.toUpperCase()}</span>
          </div>
        </div>
        <div class="threat-category-tag">${t.category}</div>
        <h4 class="threat-title">${t.title}</h4>
        <p class="threat-desc">${t.description}</p>
        <div class="threat-example">
          <strong>Concrete Attack Scenario:</strong> "${t.attack_example}"
        </div>
        <div class="threat-tags-row">
          ${capecBadges}
          ${cweBadges}
          ${mitBadges}
        </div>
      </div>
    `;
  }).join("");
}

// 5. Setup Search and Filtering
function setupFilters() {
  const searchInput = document.getElementById("search-input");
  const categoryFilter = document.getElementById("category-filter");
  const confidenceFilter = document.getElementById("confidence-filter");

  function applyFilters() {
    const q = searchInput.value.toLowerCase();
    const cat = categoryFilter.value;
    const conf = confidenceFilter.value;

    const filtered = allThreats.filter(t => {
      const matchQuery = !q || 
        t.title.toLowerCase().includes(q) || 
        t.description.toLowerCase().includes(q) || 
        t.r155_threat_id.toLowerCase().includes(q) ||
        t.affected_components.some(c => c.toLowerCase().includes(q)) ||
        t.affected_interfaces.some(i => i.toLowerCase().includes(q));

      const matchCat = cat === "all" || t.category === cat;
      const matchConf = conf === "all" || t.mapping_confidence === conf;

      return matchQuery && matchCat && matchConf;
    });

    renderThreats(filtered);
  }

  searchInput.addEventListener("input", applyFilters);
  categoryFilter.addEventListener("change", applyFilters);
  confidenceFilter.addEventListener("change", applyFilters);
}

function populateCategoryDropdown(threats) {
  const select = document.getElementById("category-filter");
  const categories = [...new Set(threats.map(t => t.category))];
  categories.forEach(cat => {
    const opt = document.createElement("option");
    opt.value = cat;
    opt.textContent = cat.length > 55 ? cat.slice(0, 52) + "..." : cat;
    select.appendChild(opt);
  });
}

// 6. ISO/SAE 21434 Simulator Logic
const TIME_SCORES = [0, 1, 4, 10, 19];
const TIME_LABELS = ["<= 1 day (0 pts)", "<= 1 week (1 pt)", "<= 1 month (4 pts)", "<= 6 months (10 pts)", "> 6 months (19 pts)"];

const EXP_SCORES = [0, 3, 6, 8];
const EXP_LABELS = ["Layman (0 pts)", "Proficient (3 pts)", "Expert (6 pts)", "Multiple Experts (8 pts)"];

const KNOW_SCORES = [0, 3, 7, 11];
const KNOW_LABELS = ["Public (0 pts)", "Restricted (3 pts)", "Confidential (7 pts)", "Strictly Confidential (11 pts)"];

const WIN_SCORES = [0, 1, 4, 10];
const WIN_LABELS = ["Unlimited (0 pts)", "Easy (1 pt)", "Moderate (4 pts)", "Difficult (10 pts)"];

const EQUIP_SCORES = [0, 4, 7];
const EQUIP_LABELS = ["Standard (0 pts)", "Specialized (4 pts)", "Bespoke (7 pts)"];

// ISO/SAE 21434 5x5 Matrix Definition: [Impact: Severe, Major, Moderate, Negligible] x [Feas: High, Medium, Low, Very Low]
const MATRIX_TABLE = [
  // Feasibility: High(0), Medium(1), Low(2), Very Low(3)
  [5, 4, 3, 2], // Impact: Severe (0)
  [4, 4, 3, 1], // Impact: Major (1)
  [3, 3, 2, 1], // Impact: Moderate (2)
  [1, 1, 1, 1]  // Impact: Negligible (3)
];

function populateSimulatorDropdowns(vehicle, threats) {
  const compSelect = document.getElementById("sim-component-select");
  const threatSelect = document.getElementById("sim-threat-select");

  compSelect.innerHTML = vehicle.components.map(c => `<option value="${c.name}">${c.name} (${c.trust_zone})</option>`).join("");
  threatSelect.innerHTML = threats.map(t => `<option value="${t.id}">[${t.r155_threat_id}] ${t.title}</option>`).join("");

  compSelect.addEventListener("change", () => {
    const selectedComp = compSelect.value;
    const matching = threats.filter(t => t.affected_components.includes(selectedComp));
    if (matching.length > 0) {
      threatSelect.innerHTML = matching.map(t => `<option value="${t.id}">[${t.r155_threat_id}] ${t.title}</option>`).join("");
    } else {
      threatSelect.innerHTML = threats.map(t => `<option value="${t.id}">[${t.r155_threat_id}] ${t.title}</option>`).join("");
    }
    updateRiskCalculation();
  });

  threatSelect.addEventListener("change", updateRiskCalculation);
}

function setupSimulator() {
  // Bind sliders
  const sTime = document.getElementById("slider-time");
  const sExp = document.getElementById("slider-exp");
  const sKnow = document.getElementById("slider-know");
  const sWin = document.getElementById("slider-win");
  const sEquip = document.getElementById("slider-equip");

  sTime.addEventListener("input", (e) => {
    document.getElementById("val-time").textContent = TIME_LABELS[e.target.value];
    updateRiskCalculation();
  });
  sExp.addEventListener("input", (e) => {
    document.getElementById("val-exp").textContent = EXP_LABELS[e.target.value];
    updateRiskCalculation();
  });
  sKnow.addEventListener("input", (e) => {
    document.getElementById("val-know").textContent = KNOW_LABELS[e.target.value];
    updateRiskCalculation();
  });
  sWin.addEventListener("input", (e) => {
    document.getElementById("val-win").textContent = WIN_LABELS[e.target.value];
    updateRiskCalculation();
  });
  sEquip.addEventListener("input", (e) => {
    document.getElementById("val-equip").textContent = EQUIP_LABELS[e.target.value];
    updateRiskCalculation();
  });

  document.getElementById("sim-impact-s").addEventListener("change", updateRiskCalculation);
  document.getElementById("sim-impact-fo").addEventListener("change", updateRiskCalculation);
  document.getElementById("sim-impact-p").addEventListener("change", updateRiskCalculation);

  buildMatrixGrid();
}

function buildMatrixGrid() {
  const container = document.getElementById("matrix-grid");
  const impacts = ["Severe", "Major", "Mod", "Negl"];
  const feas = ["High", "Med", "Low", "V.Low"];

  let html = "";
  for (let r = 0; r < 4; r++) {
    for (let c = 0; c < 4; c++) {
      const riskVal = MATRIX_TABLE[r][c];
      html += `<div class="matrix-cell risk-${riskVal}" id="cell-${r}-${c}">R${riskVal}</div>`;
    }
  }
  container.innerHTML = html;
}

function updateRiskCalculation() {
  const tVal = TIME_SCORES[parseInt(document.getElementById("slider-time").value)];
  const eVal = EXP_SCORES[parseInt(document.getElementById("slider-exp").value)];
  const kVal = KNOW_SCORES[parseInt(document.getElementById("slider-know").value)];
  const wVal = WIN_SCORES[parseInt(document.getElementById("slider-win").value)];
  const eqVal = EQUIP_SCORES[parseInt(document.getElementById("slider-equip").value)];

  const totalPoints = tVal + eVal + kVal + wVal + eqVal;
  document.getElementById("res-feasibility-score").textContent = `${totalPoints} pts`;

  // Feasibility mapping (ISO/SAE 21434 Section 15)
  // 0-13: High, 14-19: Medium, 20-24: Low, >=25: Very Low
  let feasIdx = 0;
  let feasLabel = "FEASIBILITY: HIGH";
  let feasClass = "badge-high";

  if (totalPoints <= 13) {
    feasIdx = 0;
    feasLabel = "FEASIBILITY: HIGH";
    feasClass = "badge-high";
  } else if (totalPoints <= 19) {
    feasIdx = 1;
    feasLabel = "FEASIBILITY: MEDIUM";
    feasClass = "badge-medium";
  } else if (totalPoints <= 24) {
    feasIdx = 2;
    feasLabel = "FEASIBILITY: LOW";
    feasClass = "badge-low";
  } else {
    feasIdx = 3;
    feasLabel = "FEASIBILITY: VERY LOW";
    feasClass = "badge-low";
  }

  const fBadge = document.getElementById("res-feasibility-badge");
  fBadge.textContent = feasLabel;
  fBadge.className = `badge ${feasClass}`;

  // Highest SFOP impact
  const impS = document.getElementById("sim-impact-s").value;
  const impFO = document.getElementById("sim-impact-fo").value;
  const impP = document.getElementById("sim-impact-p").value;

  const severityOrder = ["Severe", "Major", "Moderate", "Negligible"];
  const severities = [impS, impFO, impP];
  let highestImp = "Negligible";
  let impactIdx = 3;

  for (let s of severityOrder) {
    if (severities.includes(s)) {
      highestImp = s;
      impactIdx = severityOrder.indexOf(s);
      break;
    }
  }

  document.getElementById("res-impact-level").textContent = highestImp.toUpperCase();
  const iBadge = document.getElementById("res-impact-badge");
  iBadge.textContent = `SEVERITY: ${highestImp.toUpperCase()}`;
  iBadge.className = `badge ${highestImp === 'Severe' || highestImp === 'Major' ? 'badge-low' : 'badge-high'}`;

  // Update Matrix Active Cell
  document.querySelectorAll(".matrix-cell").forEach(cell => cell.classList.remove("active"));
  const activeCell = document.getElementById(`cell-${impactIdx}-${feasIdx}`);
  if (activeCell) activeCell.classList.add("active");

  const riskValue = MATRIX_TABLE[impactIdx][feasIdx];
  const riskVerdictBox = document.getElementById("risk-verdict-box");
  const verdictTitle = document.getElementById("res-risk-value");
  const verdictDesc = document.getElementById("res-risk-desc");

  verdictTitle.textContent = `${riskValue} / 5 (${getRiskTitle(riskValue)})`;
  verdictDesc.textContent = getRiskDescription(riskValue);

  // Update Mitigation text from currently selected threat
  const threatSelect = document.getElementById("sim-threat-select");
  const selectedThreat = allThreats.find(t => t.id === threatSelect.value);
  const mitEl = document.getElementById("res-mitigation-text");
  if (selectedThreat && selectedThreat.r155_mitigations.length > 0) {
    mitEl.innerHTML = selectedThreat.r155_mitigations.map(m => `<strong>${m.id}:</strong> ${m.text_summary}`).join("<br>");
  } else {
    mitEl.textContent = "Architectural network isolation (M22) and SecOC frame authentication (M10) recommended.";
  }
}

function getRiskTitle(val) {
  switch(val) {
    case 5: return "Critical Risk";
    case 4: return "High Risk";
    case 3: return "Medium Risk";
    case 2: return "Low Risk";
    case 1: return "Negligible Risk";
  }
}

function getRiskDescription(val) {
  switch(val) {
    case 5: return "Critical Safety/Security Hazard: Vehicle deployment is strictly unacceptable under UN R155. Urgent architectural overhaul and high-assurance hardware countermeasures required.";
    case 4: return "Mandatory Cybersecurity Treatment Required: High risk level requiring cryptographic protection, gateway filtering, and Type Approval evidence.";
    case 3: return "Substantial Risk: Cybersecurity goals must be specified and verified during vehicle integration.";
    case 2: return "Low Risk: Mitigation is recommended if cost-effective, or risk may be formally retained with engineering justification.";
    case 1: return "Negligible Risk: Residual risk is within acceptable operational tolerance. No mandatory controls required.";
  }
}

// 7. Render Compliance Audit Table
function renderAuditTable(threats) {
  const tbody = document.getElementById("audit-table-body");
  if (!tbody) return;

  tbody.innerHTML = threats.map(t => {
    const capecLink = t.capec.length > 0 
      ? `<a href="https://capec.mitre.org/data/definitions/${t.capec[0].id.replace('CAPEC-', '')}.html" target="_blank">${t.capec[0].id}</a>`
      : `<span style="color:var(--text-subtle)">N/A</span>`;

    const cweLink = t.cwe.length > 0
      ? `<a href="https://cwe.mitre.org/data/definitions/${t.cwe[0].id.replace('CWE-', '')}.html" target="_blank">${t.cwe[0].id}</a>`
      : `<span style="color:var(--text-subtle)">N/A</span>`;

    const mits = t.r155_mitigations.map(m => m.id).join(", ") || "None";
    const confClass = t.mapping_confidence === "high" ? "badge-high" : (t.mapping_confidence === "medium" ? "badge-medium" : "badge-low");

    return `
      <tr>
        <td style="font-family: var(--font-mono); font-weight: 600; color: #60A5FA;">${t.id}</td>
        <td><a href="https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf" target="_blank">R155 [${t.r155_threat_id}]</a></td>
        <td><strong>${t.title}</strong></td>
        <td><span class="badge ${confClass}">${t.mapping_confidence.toUpperCase()}</span></td>
        <td>${capecLink}</td>
        <td>${cweLink}</td>
        <td>${mits}</td>
      </tr>
    `;
  }).join("");
}

// 8. Render AI Config Inspector
function renderConfig(cfg) {
  const paramsBox = document.getElementById("config-params-box");
  const promptBox = document.getElementById("config-system-prompt");

  if (paramsBox && cfg.model_configuration) {
    paramsBox.textContent = JSON.stringify(cfg.model_configuration, null, 2);
  }
  if (promptBox && cfg.prompts_configuration) {
    promptBox.textContent = cfg.prompts_configuration.system_prompt;
  }
}
