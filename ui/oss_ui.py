OSS_UI_HTML = '''
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>Job Hunter OSS UI</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; line-height: 1.5; }
    h1 { margin-bottom: 12px; }
    .status-wrap { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 10px 14px;
      border: 1px solid #ddd;
      border-radius: 999px;
      background: #fafafa;
    }
    .buttons { display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; }
    button { padding: 12px 18px; cursor: pointer; }
    button:disabled { cursor: not-allowed; opacity: 0.6; }
    .box {
      background: #f6f6f6;
      border: 1px solid #ddd;
      padding: 16px;
      margin-top: 20px;
      white-space: pre-wrap;
    }
    table { border-collapse: collapse; width: 100%; margin-top: 24px; }
    th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
    .spinner {
      width: 16px;
      height: 16px;
      border: 2px solid #ddd;
      border-top-color: #333;
      border-radius: 50%;
      display: none;
      animation: spin 0.8s linear infinite;
    }
    .spinner.active { display: inline-block; }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    .muted { color: #666; }
  </style>
</head>
<body>
  <h1>Job Hunter OSS UI</h1>

  <div class="status-wrap">
    <div class="status-pill">
      <span id="spinner" class="spinner"></span>
      <span id="status-text">Статус: готов</span>
    </div>
    <span class="muted">Эта морда работает только через API</span>
  </div>

  <div class="buttons">
    <button data-url="/api/parsers/yandex/run" data-status="Идет парсинг вакансий...">1. Запустить парсер</button>
    <button data-url="/api/llm/run" data-status="Идет обработка вакансий через LLM...">2. Запустить обработку LLM</button>
    <button data-url="/api/report/build" data-status="Формируется отчет...">3. Сформировать отчет</button>
  </div>

  <div id="message" class="box" style="display:none;"></div>

  <h2>Сводка по базе</h2>
  <table>
    <tr><th>Показатель</th><th>Значение</th></tr>
    <tr><td>Всего вакансий</td><td id="jobs_count">—</td></tr>
    <tr><td>Необработанных LLM</td><td id="unprocessed_count">—</td></tr>
    <tr><td>Обработанных LLM</td><td id="processed_count">—</td></tr>
  </table>

  <script>
    const buttons = document.querySelectorAll("button[data-url]");
    const spinner = document.getElementById("spinner");
    const statusText = document.getElementById("status-text");
    const messageBox = document.getElementById("message");

    function setBusy(isBusy, text = "готов") {
      buttons.forEach(btn => btn.disabled = isBusy);
      spinner.classList.toggle("active", isBusy);
      statusText.textContent = "Статус: " + text;
    }

    function showMessage(obj) {
      messageBox.style.display = "block";
      messageBox.textContent = JSON.stringify(obj, null, 2);
    }

    async function refreshStats() {
      const resp = await fetch("/api/stats");
      const data = await resp.json();
      document.getElementById("jobs_count").textContent = data.jobs_count;
      document.getElementById("unprocessed_count").textContent = data.unprocessed_count;
      document.getElementById("processed_count").textContent = data.processed_count;
    }

    buttons.forEach(btn => {
      btn.addEventListener("click", async () => {
        try {
          setBusy(true, btn.dataset.status);
          const resp = await fetch(btn.dataset.url, { method: "POST" });
          const data = await resp.json();
          showMessage(data);
          await refreshStats();
        } catch (e) {
          showMessage({ error: String(e) });
        } finally {
          setBusy(false, "готов");
        }
      });
    });

    refreshStats();
  </script>
</body>
</html>
'''
