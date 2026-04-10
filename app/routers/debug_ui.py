from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["debug-ui"])


@router.get("/debug/predict", response_class=HTMLResponse)
def debug_predict_page() -> str:
    return """
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <title>Negi Debug Predict</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f7f7f8;
      color: #222;
    }
    .wrap {
      display: grid;
      grid-template-columns: 420px 1fr;
      gap: 16px;
      padding: 16px;
    }
    .panel {
      background: #fff;
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 1px 8px rgba(0,0,0,0.08);
    }
    h1, h2, h3 {
      margin-top: 0;
    }
    textarea {
      width: 100%;
      min-height: 280px;
      font-family: monospace;
      font-size: 12px;
      box-sizing: border-box;
    }
    .row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
      margin-bottom: 12px;
    }
    button {
      border: none;
      border-radius: 8px;
      padding: 10px 14px;
      cursor: pointer;
      background: #111827;
      color: white;
      font-weight: bold;
    }
    button.secondary {
      background: #6b7280;
    }
    input[type="file"] {
      max-width: 100%;
    }
    .drop-zone {
      border: 2px dashed #cbd5e1;
      border-radius: 10px;
      padding: 12px;
      background: #fafafa;
      color: #555;
      margin-bottom: 12px;
      min-height: 64px;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
    }
    .drop-zone.active {
      border-color: #2563eb;
      background: #eff6ff;
    }
    .preview-wrap {
      margin-bottom: 12px;
      border: 1px solid #e5e7eb;
      border-radius: 10px;
      background: #fafafa;
      padding: 8px;
    }
    .preview-title {
      font-size: 12px;
      color: #666;
      margin-bottom: 8px;
    }
    .image-preview {
      width: 100%;
      max-height: 240px;
      object-fit: contain;
      border-radius: 8px;
      background: #fff;
      display: block;
      border: 1px solid #e5e7eb;
    }
    .image-preview.empty {
      display: flex;
      align-items: center;
      justify-content: center;
      height: 140px;
      color: #888;
      font-size: 12px;
      background: #fff;
    }
    #canvasWrap {
      position: relative;
      width: 100%;
      overflow: auto;
      background: #e5e7eb;
      border-radius: 12px;
      padding: 8px;
      box-sizing: border-box;
    }
    canvas {
      display: block;
      background: white;
      border-radius: 8px;
      max-width: 100%;
    }
    .summary-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(120px, 1fr));
      gap: 8px;
      margin-bottom: 12px;
    }
    .summary-item {
      background: #f3f4f6;
      border-radius: 8px;
      padding: 10px;
    }
    .pill {
      display: inline-block;
      padding: 4px 8px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: bold;
    }
    .pill.ok {
      background: #dcfce7;
      color: #166534;
    }
    .pill.ng {
      background: #fee2e2;
      color: #991b1b;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }
    th, td {
      border-bottom: 1px solid #e5e7eb;
      padding: 8px;
      text-align: left;
      vertical-align: top;
    }
    tr:hover {
      background: #f9fafb;
      cursor: pointer;
    }
    #detailBox {
      white-space: pre-wrap;
      background: #111827;
      color: #f9fafb;
      padding: 12px;
      border-radius: 10px;
      font-family: monospace;
      font-size: 12px;
      min-height: 120px;
    }
    .small {
      color: #666;
      font-size: 12px;
    }
    .file-note {
      font-size: 12px;
      color: #444;
      margin-bottom: 8px;
    }
    
    .sidebar-layout {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 16px;
}

.gate-panel {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 12px;
  max-height: 720px;
  overflow: auto;
}

.gate-item {
  padding: 8px 10px;
  border-radius: 8px;
  margin-bottom: 6px;
  background: #ffffff;
  border: 1px solid #e5e7eb;
  font-size: 12px;
}

.gate-item.active {
  background: #eff6ff;
  border-color: #2563eb;
}

.gate-code {
  font-weight: bold;
  display: block;
  margin-bottom: 4px;
}

.gate-desc {
  color: #555;
  line-height: 1.4;
}

.canvas-note {
  font-size: 12px;
  color: #666;
  margin-bottom: 8px;
}
    
  </style>
</head>
<body>
  <div class="wrap">
    <div class="panel">
      <h1>CEiS マシーンラーニング<br />AI <span style="font-size:12px">とりあえずランダムフォレスト</span></h1>

      <div class="row">
        <input id="jsonFile" type="file" accept=".json,application/json" />
        <button type="button" class="secondary" id="clearJsonBtn">JSONクリア</button>
      </div>

      <div class="row">
        <input id="imageFile" type="file" accept="image/*" />
        <button type="button" class="secondary" id="clearImageBtn">画像クリア</button>
      </div>

      <div id="dropZone" class="drop-zone" tabindex="0">
        JSON / 画像 をここにドラッグ＆ドロップできます
      </div>

      <div class="file-note">
        画像は貼り付けも可能です（Ctrl+V / Cmd+V）。
      </div>

      <div class="preview-wrap">
        <div class="preview-title">画像プレビュー</div>
        <img id="imagePreview" class="image-preview" style="display:none;" />
        <div id="imagePreviewEmpty" class="image-preview empty">画像はまだ読み込まれていません</div>
      </div>

      <div class="small" style="margin-bottom:12px;">
        JSON は InspectFeaturesRequest 形式。画像があれば画像上に、なければ白キャンバス上に描画します。
      </div>

      <textarea id="jsonInput" placeholder='{"request_id":"...","clusters":[...]}'></textarea>

      <div class="row" style="margin-top:12px;">
        <button id="analyzeBtn">モデルテスト開始</button>
        <button type="button" class="secondary" id="clearBtn">全クリア</button>
      </div>
    </div>

    <div class="panel">
      <h2>可視化</h2>

      <div class="summary-grid">
        <div class="summary-item"><strong>request_id</strong><br><span id="requestId">-</span></div>
        <div class="summary-item"><strong>model_name</strong><br><span id="modelName">-</span></div>
        <div class="summary-item"><strong>cluster_count</strong><br><span id="clusterCount">-</span></div>
        <div class="summary-item"><strong>OK / NG</strong><br><span id="okNgCount">-</span></div>
      </div>

     <div class="sidebar-layout">
        <div>
            <div class="canvas-note">
            赤=NG / 緑=OK、bbox と centroid と cluster番号を表示
            </div>
            <div id="canvasWrap">
            <canvas id="vizCanvas" width="960" height="720"></canvas>
            </div>
        </div>

        <div class="gate-panel">
            <h3 style="margin-top:0;">ゲート一覧</h3>
            <div id="gateList"></div>
        </div>
    </div>

      <h3 style="margin-top:16px;">選択中クラスタ詳細</h3>
      <div id="detailBox">まだ選択されていません。</div>

      <h3 style="margin-top:16px;">クラスタ一覧</h3>
      <table>
        <thead>
          <tr>
            <th>cluster_id</th>
            <th>判定</th>
            <th>score_ng</th>
            <th>rule</th>
            <th>gate</th>
          </tr>
        </thead>
        <tbody id="resultTableBody"></tbody>
      </table>
    </div>
  </div>

  <script>
  
    const gateListEl = document.getElementById("gateList");

    const GATE_DEFINITIONS = {
    "OK": "良品判定。ルール上NG条件に入らなかったクラスタ。",
    "area_gate_01": "面積マスク側: NG 面積判定",
    "area_gate_02": "面積マスク側: NG 面積+色相",
    "area_gate_03": "面積マスク側: NG 複合スカスカ",
    "area_gate_04": "面積マスク側: NG 白色大型",
    "area_gate_05": "面積マスク側: NG 白色面積",
    "area_gate_06": "面積マスク側: NG 大型不整形",
    "area_gate_07": "面積マスク側: NG 黄白高彩度 大型ゲート内",
    "area_gate_08": "面積マスク側: NG 大型低彩度ワーク",
    "no_area_gate_01": "非面積側: NG アスペクト",
    "no_area_gate_02": "非面積側: NG アスペクト002",
    "no_area_gate_03": "非面積側: NG 細長小片",
    "no_area_gate_04": "非面積側: NG 黄色ワーク",
    "no_area_gate_05": "非面積側: NG にょろにょろ",
    "no_area_gate_06": "非面積側: NG 白色ワーク",
    "no_area_gate_07": "非面積側: NG 黄白色ワーク",
    "no_area_gate_08": "非面積側: NG 低彩度中サイズ",
    "no_area_gate_09": "非面積側: NG 黄白高彩度"
    };
    
    const jsonInput = document.getElementById("jsonInput");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const clearBtn = document.getElementById("clearBtn");
    const jsonFile = document.getElementById("jsonFile");
    const imageFile = document.getElementById("imageFile");
    const clearJsonBtn = document.getElementById("clearJsonBtn");
    const clearImageBtn = document.getElementById("clearImageBtn");
    const dropZone = document.getElementById("dropZone");

    const imagePreview = document.getElementById("imagePreview");
    const imagePreviewEmpty = document.getElementById("imagePreviewEmpty");

    const requestIdEl = document.getElementById("requestId");
    const modelNameEl = document.getElementById("modelName");
    const clusterCountEl = document.getElementById("clusterCount");
    const okNgCountEl = document.getElementById("okNgCount");
    const resultTableBody = document.getElementById("resultTableBody");
    const detailBox = document.getElementById("detailBox");

    const canvas = document.getElementById("vizCanvas");
    const ctx = canvas.getContext("2d");

    let loadedImage = null;
    let loadedImageSrc = null;
    let drawnItems = [];
    
    function getScaleFromJson(rawJson) {
        // 将来 JSON に codeblock_w / codeblock_h を入れたらそれを優先
        const sx =
            rawJson.codeblock_w ??
            rawJson.meta?.codeblock_w ??
            rawJson.clusters?.[0]?.codeblock_w ??
            4;

        const sy =
            rawJson.codeblock_h ??
            rawJson.meta?.codeblock_h ??
            rawJson.clusters?.[0]?.codeblock_h ??
            4;

        return {
            scaleX: Number(sx) || 4,
            scaleY: Number(sy) || 4,
        };
    }

    function resetCanvas(width = 960, height = 720) {
      canvas.width = width;
      canvas.height = height;
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function updateImagePreview() {
      if (loadedImageSrc) {
        imagePreview.src = loadedImageSrc;
        imagePreview.style.display = "block";
        imagePreviewEmpty.style.display = "none";
      } else {
        imagePreview.removeAttribute("src");
        imagePreview.style.display = "none";
        imagePreviewEmpty.style.display = "flex";
      }
    }

    function flashDropZone() {
      dropZone.classList.add("active");
      setTimeout(() => dropZone.classList.remove("active"), 500);
    }
    
    function renderGateList(activeGate = null) {
        gateListEl.innerHTML = "";

        Object.entries(GATE_DEFINITIONS).forEach(([code, desc]) => {
            const div = document.createElement("div");
            div.className = "gate-item" + (code === activeGate ? " active" : "");
            div.innerHTML = `
            <span class="gate-code">${code}</span>
            <span class="gate-desc">${desc}</span>
            `;
            gateListEl.appendChild(div);
        });
    }

    function setImageFromFile(file) {
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        const dataUrl = reader.result;
        const img = new Image();
        img.onload = () => {
          loadedImage = img;
          loadedImageSrc = String(dataUrl);
          updateImagePreview();
        };
        img.src = dataUrl;
      };
      reader.readAsDataURL(file);
    }

    function clearImageState() {
      loadedImage = null;
      loadedImageSrc = null;
      imageFile.value = "";
      updateImagePreview();
    }

    function setJsonFromFile(file) {
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        jsonInput.value = String(reader.result || "");
      };
      reader.readAsText(file, "utf-8");
    }

    function handleDroppedFiles(files) {
      if (!files || files.length === 0) return;

      let handledSomething = false;

      for (const file of files) {
        const name = (file.name || "").toLowerCase();
        const type = (file.type || "").toLowerCase();

        if (type.startsWith("image/")) {
          setImageFromFile(file);
          handledSomething = true;
          continue;
        }

        if (type === "application/json" || name.endsWith(".json")) {
          setJsonFromFile(file);
          handledSomething = true;
          continue;
        }
      }

      if (handledSomething) {
        flashDropZone();
      }
    }

    jsonFile.addEventListener("change", (e) => {
      const file = e.target.files?.[0];
      setJsonFromFile(file);
    });

    imageFile.addEventListener("change", (e) => {
      const file = e.target.files?.[0];
      setImageFromFile(file);
    });

    clearJsonBtn.addEventListener("click", () => {
      jsonInput.value = "";
      jsonFile.value = "";
    });

    clearImageBtn.addEventListener("click", () => {
      clearImageState();
    });

    dropZone.addEventListener("dragover", (e) => {
      e.preventDefault();
      dropZone.classList.add("active");
    });

    dropZone.addEventListener("dragleave", () => {
      dropZone.classList.remove("active");
    });

    dropZone.addEventListener("drop", (e) => {
      e.preventDefault();
      dropZone.classList.remove("active");
      handleDroppedFiles(e.dataTransfer.files);
    });

    document.addEventListener("paste", (e) => {
      const items = e.clipboardData?.items || [];
      for (const item of items) {
        if (item.type.startsWith("image/")) {
          const file = item.getAsFile();
          setImageFromFile(file);
          flashDropZone();
          e.preventDefault();
          return;
        }
      }
    });

    function getPredictionMap(predictions) {
      const map = new Map();
      for (const p of predictions || []) {
        map.set(p.cluster_id, p);
      }
      return map;
    }

function drawVisualization(rawJson, responseJson) {
  const clusters = rawJson.clusters || [];
  const predMap = getPredictionMap(responseJson.predictions || []);
  drawnItems = [];

  const first = clusters[0] || {};

  const scaleX = Number(
    rawJson.codeblock_w ??
    rawJson.meta?.codeblock_w ??
    first.codeblock_w ??
    4
  ) || 4;

  const scaleY = Number(
    rawJson.codeblock_h ??
    rawJson.meta?.codeblock_h ??
    first.codeblock_h ??
    4
  ) || 4;

  // C# の DrawResult に合わせる
  const offsetX = 150;
  const offsetY = 0;

  if (loadedImage) {
    resetCanvas(loadedImage.width, loadedImage.height);
    ctx.drawImage(loadedImage, 0, 0);
  } else {
    let maxX = 0;
    let maxY = 0;

    for (const c of clusters) {
      if (c.bbox_max_x != null) maxX = Math.max(maxX, c.bbox_max_x * scaleX + offsetX);
      if (c.bbox_max_y != null) maxY = Math.max(maxY, c.bbox_max_y * scaleY + offsetY);
      if (c.centroid_x != null) maxX = Math.max(maxX, c.centroid_x * scaleX + offsetX);
      if (c.centroid_y != null) maxY = Math.max(maxY, c.centroid_y * scaleY + offsetY);
    }

    const width = Math.max(960, Math.ceil(maxX) + 40);
    const height = Math.max(720, Math.ceil(maxY) + 40);

    resetCanvas(width, height);

    ctx.strokeStyle = "#d1d5db";
    ctx.lineWidth = 2;
    ctx.strokeRect(10, 10, width - 20, height - 20);
  }

  for (const c of clusters) {
    const pred = predMap.get(c.cluster_id);
    const label = pred ? pred.label : 0;
    const color = label === 1 ? "#ef4444" : "#22c55e";

    const hasBbox =
      c.bbox_min_x != null &&
      c.bbox_min_y != null &&
      c.bbox_w != null &&
      c.bbox_h != null;

    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx.lineWidth = 2;

    let hitArea = null;

    if (hasBbox) {
      const x = (c.bbox_min_x ?? 0) * scaleX + offsetX;
      const y = (c.bbox_min_y ?? 0) * scaleY + offsetY;
      const w = Math.max(6, (c.bbox_w ?? 0) * scaleX);
      const h = Math.max(6, (c.bbox_h ?? 0) * scaleY);

      ctx.strokeRect(x, y, w, h);

      const cx = c.centroid_x != null
        ? c.centroid_x * scaleX + offsetX
        : (x + w / 2);

      const cy = c.centroid_y != null
        ? c.centroid_y * scaleY + offsetY
        : (y + h / 2);

      ctx.beginPath();
      ctx.arc(cx, cy, 4, 0, Math.PI * 2);
      ctx.fill();

      // cluster番号
      ctx.font = "bold 12px Arial";
      ctx.textBaseline = "top";
      const labelText = `#${c.cluster_id}`;
      const textWidth = ctx.measureText(labelText).width;
      const labelX = x;
      const labelY = Math.max(0, y - 16);

      ctx.fillStyle = color;
      ctx.fillRect(labelX, labelY, textWidth + 8, 16);

      ctx.fillStyle = "#ffffff";
      ctx.fillText(labelText, labelX + 4, labelY + 2);

      ctx.fillStyle = color;

      hitArea = { x, y, w, h };
    } else {
      const cx = c.centroid_x != null
        ? c.centroid_x * scaleX + offsetX
        : 20;

      const cy = c.centroid_y != null
        ? c.centroid_y * scaleY + offsetY
        : 20;

      ctx.beginPath();
      ctx.arc(cx, cy, 6, 0, Math.PI * 2);
      ctx.fill();

      // cluster番号
      ctx.font = "bold 12px Arial";
      ctx.textBaseline = "top";
      const labelText = `#${c.cluster_id}`;
      const textWidth = ctx.measureText(labelText).width;
      const labelX = cx + 8;
      const labelY = cy - 8;

      ctx.fillStyle = color;
      ctx.fillRect(labelX, labelY, textWidth + 8, 16);

      ctx.fillStyle = "#ffffff";
      ctx.fillText(labelText, labelX + 4, labelY + 2);

      ctx.fillStyle = color;

      hitArea = { x: cx - 8, y: cy - 8, w: 16, h: 16 };
    }

    drawnItems.push({
      cluster: c,
      prediction: pred,
      hitArea,
    });
  }
}


    function updateSummary(rawJson, responseJson) {
      requestIdEl.textContent = responseJson.request_id || rawJson.request_id || "-";
      modelNameEl.textContent = responseJson.model_name || "-";
      clusterCountEl.textContent = String(responseJson.cluster_count ?? (rawJson.clusters || []).length);

      const preds = responseJson.predictions || [];
      const okCount = preds.filter(x => x.label === 0).length;
      const ngCount = preds.filter(x => x.label === 1).length;
      okNgCountEl.textContent = `OK ${okCount} / NG ${ngCount}`;
    }

    function renderTable(rawJson, responseJson) {
      resultTableBody.innerHTML = "";
      const predMap = getPredictionMap(responseJson.predictions || []);

      for (const c of rawJson.clusters || []) {
        const pred = predMap.get(c.cluster_id);
        const label = pred?.label === 1 ? "NG" : "OK";
        const pillClass = pred?.label === 1 ? "ng" : "ok";
        const score = pred?.score_ng != null ? Number(pred.score_ng).toFixed(4) : "-";

        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${c.cluster_id}</td>
          <td><span class="pill ${pillClass}">${label}</span></td>
          <td>${score}</td>
          <td>${c.label_rule_text ?? "-"}</td>
          <td>${c.ng_reason_primary ?? "-"}</td>
        `;
        tr.addEventListener("click", () => {
          showDetail(c.cluster_id);
        });
        resultTableBody.appendChild(tr);
      }
    }

    function showDetail(clusterId) {
      const item = drawnItems.find(x => x.cluster.cluster_id === clusterId);
      if (!item) return;

      const c = item.cluster;
      const p = item.prediction;
      detailBox.textContent = JSON.stringify({
        cluster_id: c.cluster_id,
        predict_label: p?.label ?? null,
        score_ng: p?.score_ng ?? null,
        label_rule_current: c.label_rule_current ?? null,
        label_rule_text: c.label_rule_text ?? null,
        ng_reason_primary: c.ng_reason_primary ?? null,
        areaCells: c.areaCells,
        perimeter: c.perimeter,
        aspect: c.aspect,
        elong: c.elong,
        oriented_fill: c.oriented_fill,
        eccentricity: c.eccentricity,
        circularity: c.circularity,
        avgY: c.avgY,
        avgHue: c.avgHue,
        avgC255: c.avgC255,
        avgNegi03: c.avgNegi03,
        avgNegi05: c.avgNegi05,
        avgS255: c.avgS255,
        bbox_min_x: c.bbox_min_x,
        bbox_min_y: c.bbox_min_y,
        bbox_w: c.bbox_w,
        bbox_h: c.bbox_h,
        centroid_x: c.centroid_x,
        centroid_y: c.centroid_y
      }, null, 2);
      
      renderGateList(c.ng_reason_primary ?? "OK");
      
    }

    canvas.addEventListener("click", (e) => {
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      const x = (e.clientX - rect.left) * scaleX;
      const y = (e.clientY - rect.top) * scaleY;

      for (let i = drawnItems.length - 1; i >= 0; i--) {
        const item = drawnItems[i];
        const h = item.hitArea;
        if (x >= h.x && x <= h.x + h.w && y >= h.y && y <= h.y + h.h) {
          showDetail(item.cluster.cluster_id);
          return;
        }
      }
    });

    analyzeBtn.addEventListener("click", async () => {
      try {
        const raw = jsonInput.value.trim();
        if (!raw) {
          alert("JSONを入れてください。");
          return;
        }

        const rawJson = JSON.parse(raw);

        const res = await fetch("/inspect/features", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(rawJson),
        });

        if (!res.ok) {
          const text = await res.text();
          alert("APIエラー: " + text);
          return;
        }

        const responseJson = await res.json();

        updateSummary(rawJson, responseJson);
        drawVisualization(rawJson, responseJson);
        renderTable(rawJson, responseJson);
        
        renderGateList("OK");

        if ((rawJson.clusters || []).length > 0) {
          showDetail(rawJson.clusters[0].cluster_id);
        }
      } catch (err) {
        alert("解析エラー: " + err);
      }
    });

    clearBtn.addEventListener("click", () => {
      jsonInput.value = "";
      jsonFile.value = "";
      clearImageState();

      requestIdEl.textContent = "-";
      modelNameEl.textContent = "-";
      clusterCountEl.textContent = "-";
      okNgCountEl.textContent = "-";
      resultTableBody.innerHTML = "";
      detailBox.textContent = "まだ選択されていません。";
      resetCanvas();
      drawnItems = [];
      
      renderGateList();
    });

    updateImagePreview();
    resetCanvas();
    renderGateList();
    
  </script>
</body>
</html>
    """