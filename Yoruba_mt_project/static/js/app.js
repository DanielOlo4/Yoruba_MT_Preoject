/**
 * ═══════════════════════════════════════════════════
 * YORUBA-ENGLISH TRANSLATOR — FRONTEND APPLICATION
 * ═══════════════════════════════════════════════════
 */

(function () {
    "use strict";

    // ── State ──
    let currentDirection = "en_to_yo";
    let isTranslating = false;
    let examplesCache = null;

    // ── DOM References ──
    const sourceText = document.getElementById("source-text");
    const outputPlaceholder = document.getElementById("output-placeholder");
    const translationText = document.getElementById("translation-text");
    const charCount = document.getElementById("char-count");
    const btnTranslate = document.getElementById("btn-translate");
    const btnText = document.querySelector(".btn-text");
    const loader = document.getElementById("loader");
    const detailsCard = document.getElementById("details-card");
    const examplesGrid = document.getElementById("examples-grid");

    // Direction buttons
    const dirEnYo = document.getElementById("dir-en-yo");
    const dirYoEn = document.getElementById("dir-yo-en");
    const btnSwap = document.getElementById("btn-swap");

    // Labels
    const sourceLabel = document.getElementById("source-label");
    const targetLabel = document.getElementById("target-label");
    const sourceFlag = document.getElementById("source-flag");
    const targetFlag = document.getElementById("target-flag");

    // ══════════════════════════════════
    //  TRANSLATION
    // ══════════════════════════════════

    async function translate() {
        const text = sourceText.value.trim();
        if (!text) {
            showToast("⚠️", "Please enter text to translate");
            sourceText.focus();
            return;
        }

        if (isTranslating) return;
        isTranslating = true;
        showLoading(true);

        try {
            const response = await fetch("/api/translate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    text: text,
                    direction: currentDirection,
                }),
            });

            const data = await response.json();

            if (!response.ok || data.error) {
                showToast("❌", data.error || "Translation failed");
                return;
            }

            displayResult(data);
            showToast("✅", "Translation complete");
        } catch (err) {
            console.error("Translation error:", err);
            showToast("❌", "Network error. Is the server running?");
        } finally {
            isTranslating = false;
            showLoading(false);
        }
    }

    function displayResult(data) {
        // Show translation text
        outputPlaceholder.style.display = "none";
        translationText.style.display = "block";
        translationText.textContent = data.translation;

        // Show details card
        detailsCard.style.display = "block";

        // Confidence bar
        const confBar = document.getElementById("conf-bar");
        const confValue = document.getElementById("conf-value");
        const confidence = data.confidence;

        confBar.style.width = Math.max(confidence, 8) + "%";
        confValue.textContent = confidence + "%";

        if (confidence >= 80) {
            confBar.style.background = "linear-gradient(90deg, #22c55e, #16a34a)";
        } else if (confidence >= 50) {
            confBar.style.background = "linear-gradient(90deg, #f59e0b, #d97706)";
        } else {
            confBar.style.background = "linear-gradient(90deg, #ef4444, #dc2626)";
        }

        // Match type badge
        const matchEl = document.getElementById("detail-match");
        matchEl.textContent = data.match_type;
        matchEl.className = "detail-value badge badge-" + data.match_type;

        // Other details
        document.getElementById("detail-section").textContent =
            formatSectionName(data.section);
        document.getElementById("detail-tokens").textContent =
            data.tokens_processed;
        document.getElementById("detail-time").textContent =
            data.processing_time + "s";
        document.getElementById("detail-rules").textContent =
            data.rules_applied.join(", ") || "—";

        // Alternatives
        const altSection = document.getElementById("alternatives-section");
        const altList = document.getElementById("alternatives-list");

        if (data.alternatives && data.alternatives.length > 0) {
            altSection.style.display = "block";
            altList.innerHTML = "";
            data.alternatives.forEach(function (alt) {
                const li = document.createElement("li");
                li.textContent = alt;
                li.addEventListener("click", function () {
                    translationText.textContent = alt;
                    showToast("✅", "Alternative selected");
                });
                altList.appendChild(li);
            });
        } else {
            altSection.style.display = "none";
        }
    }

    // ══════════════════════════════════
    //  DIRECTION SWITCHING
    // ══════════════════════════════════

    function setDirection(dir) {
        currentDirection = dir;

        if (dir === "en_to_yo") {
            dirEnYo.classList.add("active");
            dirYoEn.classList.remove("active");
            sourceLabel.textContent = "English";
            targetLabel.textContent = "Yorùbá";
            sourceFlag.textContent = "🇬🇧";
            targetFlag.textContent = "🇳🇬";
            sourceText.placeholder = "Type English text here...";
        } else {
            dirYoEn.classList.add("active");
            dirEnYo.classList.remove("active");
            sourceLabel.textContent = "Yorùbá";
            targetLabel.textContent = "English";
            sourceFlag.textContent = "🇳🇬";
            targetFlag.textContent = "🇬🇧";
            sourceText.placeholder = "Kọ ọ̀rọ̀ Yorùbá sí ibí...";
        }

        clearOutput();
        loadExamples();
    }

    function swapDirection() {
        // Swap text content too
        const currentOutput = translationText.textContent;
        const currentInput = sourceText.value;

        const newDir = currentDirection === "en_to_yo" ? "yo_to_en" : "en_to_yo";
        setDirection(newDir);

        if (currentOutput &&
            translationText.style.display !== "none" &&
            currentOutput !== "Translation will appear here...") {
            sourceText.value = currentOutput;
            updateCharCount();
        }
    }

    // ══════════════════════════════════
    //  EXAMPLES
    // ══════════════════════════════════

    async function loadExamples() {
        try {
            if (!examplesCache) {
                const res = await fetch("/api/examples");
                const data = await res.json();
                if (data.success) {
                    examplesCache = data.examples;
                }
            }

            if (!examplesCache) return;

            const examples = examplesCache[currentDirection] || [];
            examplesGrid.innerHTML = "";

            examples.forEach(function (ex) {
                const chip = document.createElement("button");
                chip.className = "example-chip";
                chip.textContent = ex;
                chip.addEventListener("click", function () {
                    sourceText.value = ex;
                    updateCharCount();
                    translate();
                    window.scrollTo({ top: 0, behavior: "smooth" });
                });
                examplesGrid.appendChild(chip);
            });
        } catch (err) {
            console.error("Failed to load examples:", err);
        }
    }

    // ══════════════════════════════════
    //  BATCH TRANSLATION
    // ══════════════════════════════════

    async function batchTranslate() {
        const input = document.getElementById("batch-input").value.trim();
        if (!input) {
            showToast("⚠️", "Enter sentences to translate");
            return;
        }

        const lines = input
            .split("\n")
            .map(function (l) { return l.trim(); })
            .filter(function (l) { return l.length > 0; });

        if (lines.length === 0) {
            showToast("⚠️", "No valid sentences found");
            return;
        }

        if (lines.length > 50) {
            showToast("⚠️", "Maximum 50 sentences allowed");
            return;
        }

        try {
            const res = await fetch("/api/translate/batch", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    texts: lines,
                    direction: currentDirection,
                }),
            });

            const data = await res.json();

            if (!data.success) {
                showToast("❌", data.error || "Batch translation failed");
                return;
            }

            displayBatchResults(data);
            showToast("✅", data.count + " sentences translated");
        } catch (err) {
            console.error("Batch error:", err);
            showToast("❌", "Batch translation failed");
        }
    }

    function displayBatchResults(data) {
        const container = document.getElementById("batch-results");
        const tbody = document.getElementById("batch-table-body");
        tbody.innerHTML = "";

        data.translations.forEach(function (item, i) {
            var confClass = "conf-low";
            if (item.confidence >= 80) confClass = "conf-high";
            else if (item.confidence >= 50) confClass = "conf-med";

            const row = document.createElement("tr");
            row.innerHTML =
                "<td>" + (i + 1) + "</td>" +
                "<td>" + escapeHTML(item.source) + "</td>" +
                "<td><strong>" + escapeHTML(item.translation) + "</strong></td>" +
                '<td><span class="conf-badge ' + confClass + '">' +
                    item.confidence + '%</span></td>';
            tbody.appendChild(row);
        });

        container.style.display = "block";
    }

    // ══════════════════════════════════
    //  STATISTICS MODAL
    // ══════════════════════════════════

    async function showStats() {
        openModal("modal-stats");
        const body = document.getElementById("stats-body");
        body.innerHTML = '<div class="loading-state">Loading statistics...</div>';

        try {
            const res = await fetch("/api/stats");
            const data = await res.json();

            if (!data.success) {
                body.innerHTML = '<div class="loading-state">Failed to load statistics</div>';
                return;
            }

            const stats = data.stats;
            const sections = stats.sections || {};
            const maxCount = Math.max.apply(null, Object.values(sections).concat([1]));

            let sectionsHTML = "";
            Object.keys(sections).forEach(function (sec) {
                const count = sections[sec];
                const pct = Math.round((count / maxCount) * 100);
                sectionsHTML +=
                    '<div class="section-bar">' +
                        '<span class="section-name">' + formatSectionName(sec) + '</span>' +
                        '<div style="flex:1; background:#eee; border-radius:4px; height:8px;">' +
                            '<div class="section-fill" style="width:' + pct + '%;"></div>' +
                        '</div>' +
                        '<span class="section-count">' + count + '</span>' +
                    '</div>';
            });

            body.innerHTML =
                '<div class="stat-grid">' +
                    '<div class="stat-card">' +
                        '<div class="stat-number">' + stats.total_entries + '</div>' +
                        '<div class="stat-label">Total Entries</div>' +
                    '</div>' +
                    '<div class="stat-card">' +
                        '<div class="stat-number">' + stats.unique_english_phrases + '</div>' +
                        '<div class="stat-label">English Phrases</div>' +
                    '</div>' +
                    '<div class="stat-card">' +
                        '<div class="stat-number">' + stats.unique_yoruba_phrases + '</div>' +
                        '<div class="stat-label">Yorùbá Phrases</div>' +
                    '</div>' +
                    '<div class="stat-card">' +
                        '<div class="stat-number">' + Object.keys(sections).length + '</div>' +
                        '<div class="stat-label">Sections</div>' +
                    '</div>' +
                '</div>' +
                '<div class="stat-sections">' +
                    '<h4>Dataset Sections</h4>' +
                    sectionsHTML +
                '</div>';
        } catch (err) {
            body.innerHTML = '<div class="loading-state">Error: ' + err.message + '</div>';
        }
    }

    // ══════════════════════════════════
    //  EVALUATION MODAL
    // ══════════════════════════════════

    async function runEvaluation() {
        const direction = document.getElementById("eval-direction").value;
        const sampleVal = parseInt(document.getElementById("eval-sample").value);
        const sampleSize = sampleVal === 0 ? null : sampleVal;
        const results = document.getElementById("eval-results");

        results.innerHTML = '<div class="loading-state">Running evaluation... Please wait.</div>';

        try {
            const res = await fetch("/api/evaluate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    direction: direction,
                    sample_size: sampleSize,
                }),
            });

            const data = await res.json();

            if (!data.success) {
                results.innerHTML = '<div class="loading-state">Evaluation failed</div>';
                return;
            }

            const dist = data.match_type_distribution || {};
            let distHTML = "";
            Object.keys(dist).forEach(function (key) {
                distHTML +=
                    '<span class="badge badge-' + key + '" style="margin:3px;">' +
                        key + ': ' + dist[key] +
                    '</span>';
            });

            results.innerHTML =
                '<div class="stat-grid" style="margin-bottom:16px;">' +
                    '<div class="stat-card">' +
                        '<div class="stat-number">' + data.exact_match_accuracy + '%</div>' +
                        '<div class="stat-label">Exact Match Accuracy</div>' +
                    '</div>' +
                    '<div class="stat-card">' +
                        '<div class="stat-number">' + data.exact_matches + '/' + data.total_evaluated + '</div>' +
                        '<div class="stat-label">Exact Matches</div>' +
                    '</div>' +
                    '<div class="stat-card">' +
                        '<div class="stat-number">' + data.high_confidence_rate + '%</div>' +
                        '<div class="stat-label">High Confidence Rate</div>' +
                    '</div>' +
                    '<div class="stat-card">' +
                        '<div class="stat-number">' + (data.processing_time || '—') + 's</div>' +
                        '<div class="stat-label">Processing Time</div>' +
                    '</div>' +
                '</div>' +
                '<div style="padding:12px 0;">' +
                    '<strong style="font-size:0.85rem;">Match Type Distribution:</strong><br>' +
                    '<div style="margin-top:8px;">' + distHTML + '</div>' +
                '</div>';

            showToast("✅", "Evaluation complete");
        } catch (err) {
            results.innerHTML = '<div class="loading-state">Error: ' + err.message + '</div>';
        }
    }

    // ══════════════════════════════════
    //  UTILITY FUNCTIONS
    // ══════════════════════════════════

    function showLoading(show) {
        if (show) {
            btnText.style.display = "none";
            loader.style.display = "flex";
        } else {
            btnText.style.display = "inline";
            loader.style.display = "none";
        }
    }

    function clearOutput() {
        outputPlaceholder.style.display = "block";
        translationText.style.display = "none";
        translationText.textContent = "";
        detailsCard.style.display = "none";
    }

    function updateCharCount() {
        charCount.textContent = sourceText.value.length;
    }

    function formatSectionName(name) {
        if (!name || name === "N/A") return "N/A";
        return name
            .replace(/_/g, " ")
            .replace(/\b\w/g, function (c) { return c.toUpperCase(); });
    }

    function escapeHTML(str) {
        var div = document.createElement("div");
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }

    function showToast(icon, message) {
        var toast = document.getElementById("toast");
        document.getElementById("toast-icon").textContent = icon;
        document.getElementById("toast-message").textContent = message;
        toast.classList.add("visible");
        setTimeout(function () {
            toast.classList.remove("visible");
        }, 2500);
    }

    function openModal(id) {
        document.getElementById(id).classList.add("visible");
    }

    // Make closeModal global for inline onclick
    window.closeModal = function (id) {
        document.getElementById(id).classList.remove("visible");
    };

    // ══════════════════════════════════
    //  EVENT LISTENERS
    // ══════════════════════════════════

    // Translate
    btnTranslate.addEventListener("click", translate);

    // Keyboard shortcut: Ctrl+Enter
    sourceText.addEventListener("keydown", function (e) {
        if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
            e.preventDefault();
            translate();
        }
    });

    // Character counter
    sourceText.addEventListener("input", updateCharCount);

    // Direction buttons
    dirEnYo.addEventListener("click", function () { setDirection("en_to_yo"); });
    dirYoEn.addEventListener("click", function () { setDirection("yo_to_en"); });
    btnSwap.addEventListener("click", swapDirection);

    // Clear
    document.getElementById("btn-clear").addEventListener("click", function () {
        sourceText.value = "";
        updateCharCount();
        clearOutput();
        sourceText.focus();
    });

    // Copy
    document.getElementById("btn-copy").addEventListener("click", function () {
        var text = translationText.textContent;
        if (text) {
            navigator.clipboard.writeText(text).then(function () {
                showToast("📋", "Copied to clipboard");
            });
        }
    });

    // Paste
    document.getElementById("btn-paste").addEventListener("click", function () {
        navigator.clipboard.readText().then(function (text) {
            sourceText.value = text;
            updateCharCount();
            showToast("📋", "Pasted from clipboard");
        }).catch(function () {
            showToast("⚠️", "Cannot access clipboard");
        });
    });

    // Close details
    document.getElementById("btn-close-details").addEventListener("click", function () {
        detailsCard.style.display = "none";
    });

    // Header buttons
    document.getElementById("btn-stats").addEventListener("click", showStats);
    document.getElementById("btn-evaluate").addEventListener("click", function () {
        openModal("modal-evaluate");
    });
    document.getElementById("btn-help").addEventListener("click", function () {
        openModal("modal-help");
    });

    // Evaluation run button
    document.getElementById("btn-run-eval").addEventListener("click", runEvaluation);

    // Batch
    document.getElementById("btn-batch").addEventListener("click", batchTranslate);

    // Close modals on overlay click
    document.querySelectorAll(".modal-overlay").forEach(function (overlay) {
        overlay.addEventListener("click", function (e) {
            if (e.target === overlay) {
                overlay.classList.remove("visible");
            }
        });
    });

    // Close modals on Escape
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            document.querySelectorAll(".modal-overlay.visible").forEach(function (m) {
                m.classList.remove("visible");
            });
        }
    });

    // ══════════════════════════════════
    //  INITIALIZE
    // ══════════════════════════════════

    loadExamples();

})();