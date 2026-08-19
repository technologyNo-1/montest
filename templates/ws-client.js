/* ===== ws-client.js — Local Python Bridge Client ===== */
/* Replaces Skulpt execution when --mode=local is used */

(function() {
  'use strict';

  var WS_URL = 'ws://' + window.location.hostname + ':8235';
  var HTTP_URL = window.location.origin;
  var ws = null;
  var wsReady = false;
  var pendingRequests = {};

  // ===== WebSocket 连接 =====
  function connectWS() {
    try {
      ws = new WebSocket(WS_URL);
      ws.onopen = function() {
        wsReady = true;
        console.log('[MontExam] WebSocket connected');
        showBridgeStatus('connected');
      };
      ws.onmessage = function(evt) {
        try {
          var data = JSON.parse(evt.data);
          if (data.type === 'result' && data._reqId) {
            var cb = pendingRequests[data._reqId];
            if (cb) {
              delete pendingRequests[data._reqId];
              cb(data);
            }
          }
        } catch(e) {}
      };
      ws.onclose = function() {
        wsReady = false;
        showBridgeStatus('disconnected');
        setTimeout(connectWS, 3000);
      };
      ws.onerror = function() {
        wsReady = false;
      };
    } catch(e) {
      setTimeout(connectWS, 3000);
    }
  }

  // ===== HTTP 降级模式 =====
  function httpRun(payload) {
    return fetch(HTTP_URL + '/api/run', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    }).then(function(r) { return r.json(); });
  }

  // ===== WebSocket 发送 =====
  function wsRun(payload) {
    return new Promise(function(resolve, reject) {
      if (!wsReady || !ws || ws.readyState !== WebSocket.OPEN) {
        reject(new Error('WebSocket not connected'));
        return;
      }
      var reqId = '_' + Date.now() + '_' + Math.random().toString(36).substr(2, 5);
      payload._reqId = reqId;
      pendingRequests[reqId] = resolve;
      ws.send(JSON.stringify(payload));
      // 超时
      setTimeout(function() {
        if (pendingRequests[reqId]) {
          delete pendingRequests[reqId];
          reject(new Error('Execution timeout'));
        }
      }, 15000);
    });
  }

  // ===== 统一执行接口 =====
  window.localRun = function(code, testCases, questionId) {
    var payload = {
      type: 'run',
      code: code,
      testCases: testCases || [],
      questionId: questionId || 0
    };

    // 优先 WebSocket，降级 HTTP
    if (wsReady) {
      return wsRun(payload).catch(function() {
        return httpRun(payload);
      });
    }
    return httpRun(payload);
  };

  // ===== 桥接状态指示 =====
  function showBridgeStatus(status) {
    var el = document.getElementById('bridge-status');
    if (!el) {
      el = document.createElement('div');
      el.id = 'bridge-status';
      el.style.cssText = 'position:fixed;top:0;right:0;padding:4px 12px;font-size:11px;font-weight:600;border-radius:0 0 0 8px;z-index:9999;transition:all 0.3s;';
      document.body.appendChild(el);
    }
    if (status === 'connected') {
      el.style.background = '#10b981';
      el.style.color = '#fff';
      el.textContent = '● 本地 Python 已连接';
    } else {
      el.style.background = '#f59e0b';
      el.style.color = '#000';
      el.textContent = '○ 本地 Python 未连接';
    }
  }

  // ===== 覆盖 runTests 函数 =====
  window.runTests = async function(id) {
    var c = CD.find(function(x){return x.id===id;});
    if (!c || !c.t || !c.t.length) {
      showToast(id, '该题暂无测试用例', 'warn');
      return;
    }
    var code = editors[id].getValue();
    var box = document.getElementById('tr-' + id);
    box.innerHTML = '<div class="tr-loading">&#8987; 在本地 Python 中执行...</div>';

    try {
      var result = await localRun(code, c.t, id);
      renderTestResults(id, result, c.t.length);
      if (result.file) {
        showToast(id, '已保存: ' + result.filename, 'success');
      }
    } catch(err) {
      box.innerHTML = '<div class="tc tc-fail"><span class="tc-icon">&#10007;</span><span class="tc-err">连接失败: ' + escH(String(err)) + '</span></div>' +
        '<div style="margin-top:0.5rem;font-size:0.82rem;color:var(--text-muted);">请确认 <code>python montest-serve.py</code> 已启动</div>';
    }
  };

  function renderTestResults(id, result, total) {
    var box = document.getElementById('tr-' + id);
    var passed = result.passed;
    var html = '<div class="test-panel">';

    if (result.error && (!result.results || result.results.length === 0)) {
      // 纯错误
      html += '<div class="tc tc-fail">';
      html += '<span class="tc-icon">&#10007;</span>';
      html += '<span class="tc-err">' + escH(result.error) + '</span>';
      html += '</div>';
    } else if (result.results && result.results.length > 0) {
      for (var i = 0; i < result.results.length; i++) {
        var r = result.results[i];
        var pass = r.pass;
        html += '<div class="tc ' + (pass ? 'tc-pass' : 'tc-fail') + '">';
        html += '<span class="tc-icon">' + (pass ? '&#10003;' : '&#10007;') + '</span>';
        html += '<span class="tc-detail"><code>print(' + escH(r.call) + ')</code></span>';
        html += '<span class="tc-expected">期望: <code>' + escH(String(r.expected)) + '</code></span>';
        if (!pass) {
          if (r.error) {
            html += '<span class="tc-err">错误: ' + escH(r.error) + '</span>';
          } else {
            html += '<span class="tc-actual">实际: <code>' + escH(String(r.actual)) + '</code></span>';
          }
        }
        html += '</div>';
      }
    } else if (result.output) {
      // 无测试格式，只有输出
      html += '<div class="tc tc-pass">';
      html += '<span class="tc-icon">&#9654;</span>';
      html += '<span class="tc-detail"><pre style="margin:0;background:none;border:none;padding:0;">' + escH(result.output) + '</pre></span>';
      html += '</div>';
      passed = -1; // 标记为"只有输出"
    }

    // 汇总行
    if (passed >= 0) {
      html += '<div class="tr-sum' + (passed === total ? ' tr-ok' : '') + '">';
      html += passed + ' / ' + total + ' 测试用例通过';
      html += '</div>';
    } else if (result.output) {
      html += '<div class="tr-sum">输出结果如上</div>';
    }

    if (result.error && result.results && result.results.length > 0) {
      html += '<div style="padding:0.4rem 0.9rem;font-size:0.8rem;color:var(--error);border-top:1px solid var(--border);">' + escH(result.error) + '</div>';
    }

    html += '</div>';
    box.innerHTML = html;

    if (passed === total && total > 0) celebrate();
  }

  function escH(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  // ===== 启动 =====
  // 延迟连接，等页面加载完
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(connectWS, 500);
    });
  } else {
    setTimeout(connectWS, 500);
  }

  console.log('[MontExam] Local Python bridge loaded');
})();
