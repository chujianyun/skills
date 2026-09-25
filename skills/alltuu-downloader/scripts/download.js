#!/usr/bin/env node
/**
 * alltuu.com 相册原图批量下载脚本
 *
 * 原理：
 *   1. 通过 Chrome CDP 打开相册页面，等待 JS 渲染
 *   2. 拦截 v4c.alltuu.com 的 fpl (fetch photo list) API 响应
 *   3. 从响应中提取 ol (original) 签名 URL
 *   4. 并发下载原图到本地
 *
 * 依赖：ws (npm)
 *
 * 用法：
 *   node download.js --album <albumId> --output <dir> [--concurrency 5]
 */

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

// --- CLI 参数解析 ---
const args = process.argv.slice(2);
function getArg(name, defaultVal) {
  const idx = args.indexOf('--' + name);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : defaultVal;
}

const ALBUM_ID = getArg('album', '');
const OUTPUT_DIR = getArg('output', path.join(process.env.HOME, 'Downloads', 'alltuu'));
const CONCURRENCY = parseInt(getArg('concurrency', '5'), 10);
const CDP_PORT = parseInt(getArg('cdp-port', '9222'), 10);

if (!ALBUM_ID) {
  console.error('Usage: node download.js --album <albumId> --output <dir> [--concurrency 5] [--cdp-port 9222]');
  console.error('');
  console.error('albumId: 从 alltuu URL 中提取的数字或短码，如 1644727242');
  process.exit(1);
}

// 确保输出目录存在
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

// --- WebSocket / CDP helpers ---
let WebSocket;
try {
  WebSocket = require('ws');
} catch (e) {
  console.error('Missing dependency: ws');
  console.error('Run: cd /tmp && npm init -y && npm install ws');
  process.exit(1);
}

function cdpCommand(ws, method, params = {}, sessionId) {
  return new Promise((resolve, reject) => {
    const id = Math.floor(Math.random() * 1e6);
    const msg = sessionId
      ? { id, method, params, sessionId }
      : { id, method, params };
    ws.send(JSON.stringify(msg));
    const handler = (raw) => {
      const resp = JSON.parse(raw.toString());
      if (resp.id === id) {
        ws.removeListener('message', handler);
        resp.error ? reject(new Error(JSON.stringify(resp.error))) : resolve(resp.result);
      }
    };
    ws.on('message', handler);
    setTimeout(() => reject(new Error('CDP timeout')), 60000);
  });
}

function downloadFile(url, filepath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(filepath);
    const req = https.get(url, (res) => {
      if (res.statusCode === 301 || res.statusCode === 302) {
        file.close();
        fs.unlinkSync(filepath);
        return downloadFile(res.headers.location, filepath).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) {
        file.close();
        if (fs.existsSync(filepath)) fs.unlinkSync(filepath);
        return reject(new Error(`HTTP ${res.statusCode}`));
      }
      res.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve(fs.statSync(filepath).size);
      });
    });
    req.on('error', (err) => {
      file.close();
      if (fs.existsSync(filepath)) fs.unlinkSync(filepath);
      reject(err);
    });
    req.setTimeout(60000, () => { req.destroy(); reject(new Error('Download timeout')); });
  });
}

// --- 主流程 ---
async function main() {
  // 1. 连接 Chrome CDP
  console.log(`Connecting to Chrome CDP on port ${CDP_PORT}...`);
  const wsUrl = await new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${CDP_PORT}/json/version`, (res) => {
      let data = '';
      res.on('data', (c) => (data += c));
      res.on('end', () => resolve(JSON.parse(data).webSocketDebuggerUrl));
    }).on('error', () =>
      reject(new Error(`Cannot connect to Chrome on port ${CDP_PORT}. Make sure Chrome Canary is running with --remote-debugging-port=${CDP_PORT}`))
    );
  });

  const ws = new WebSocket(wsUrl);
  await new Promise((r) => ws.on('open', r));

  // 2. 打开新标签页
  const { targetId } = await cdpCommand(ws, 'Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdpCommand(ws, 'Target.attachToTarget', { targetId, flatten: true });
  const cmd = (m, p) => cdpCommand(ws, m, p || {}, sessionId);

  await cmd('Network.enable');

  // 3. 拦截 fpl 响应（支持多页）
  const allPhotos = [];
  const fplRequests = {};
  const fplBodies = [];

  ws.on('message', (raw) => {
    const msg = JSON.parse(raw.toString());
    if (msg.sessionId !== sessionId) return;

    if (msg.method === 'Network.requestWillBeSent') {
      const url = msg.params.request.url;
      if (url.includes('v4c.alltuu.com') && url.includes('fpl')) {
        fplRequests[msg.params.requestId] = url;
        console.log('Found photo list API request');
      }
    }

    if (msg.method === 'Network.loadingFinished') {
      const reqId = msg.params.requestId;
      if (fplRequests[reqId]) {
        cmd('Network.getResponseBody', { requestId: reqId })
          .then((body) => { fplBodies.push(body.body); })
          .catch(() => {});
      }
    }
  });

  // 4. 导航到相册页面
  const albumUrl = `https://m.alltuu.com/album/${ALBUM_ID}/?menu=live`;
  console.log(`Opening album: ${albumUrl}`);
  await cmd('Page.navigate', { url: albumUrl });

  // 等待首次加载
  for (let i = 0; i < 20; i++) {
    await new Promise((r) => setTimeout(r, 1000));
    if (fplBodies.length > 0) break;
  }

  if (fplBodies.length === 0) {
    console.log('Waiting for photo list...');
    await new Promise((r) => setTimeout(r, 10000));
  }

  if (fplBodies.length === 0) {
    await cdpCommand(ws, 'Target.closeTarget', { targetId });
    ws.close();
    console.error('Failed to capture photo list API response. Album may require login or does not exist.');
    process.exit(1);
  }

  // 解析第一页
  const firstData = JSON.parse(fplBodies[0]);
  firstData.d.forEach(p => allPhotos.push(p));
  console.log(`Page 1: ${firstData.d.length} photos (total: ${allPhotos.length})`);

  // 5. 滚动加载更多页面
  let noNewCount = 0;
  for (let scroll = 0; scroll < 100; scroll++) {
    const prevCount = fplBodies.length;
    // 滚动到底部
    await cmd('Runtime.evaluate', {
      expression: 'window.scrollTo(0, document.body.scrollHeight)',
      awaitPromise: false
    });
    await new Promise((r) => setTimeout(r, 2000));

    // 检查是否有新的 fpl 响应
    if (fplBodies.length > prevCount) {
      noNewCount = 0;
      for (let i = prevCount; i < fplBodies.length; i++) {
        const pageData = JSON.parse(fplBodies[i]);
        if (pageData.d) {
          pageData.d.forEach(p => allPhotos.push(p));
          console.log(`Page ${i + 1}: ${pageData.d.length} photos (total: ${allPhotos.length})`);
        }
      }
    } else {
      noNewCount++;
      if (noNewCount >= 3) {
        console.log('No more pages loaded after 3 scrolls, stopping.');
        break;
      }
    }
  }

  // 关闭标签页
  await cdpCommand(ws, 'Target.closeTarget', { targetId });
  ws.close();

  const photos = allPhotos;
  if (!photos || photos.length === 0) {
    console.error('No photos found in album.');
    process.exit(1);
  }

  console.log(`\nFound ${photos.length} photos. Starting download...`);
  console.log(`Output: ${OUTPUT_DIR}\n`);

  // 6. 批量下载
  let success = 0;
  let failed = 0;

  for (let i = 0; i < photos.length; i += CONCURRENCY) {
    const batch = photos.slice(i, i + CONCURRENCY);
    const results = await Promise.allSettled(
      batch.map(async (p, j) => {
        const idx = i + j + 1;
        // 优先原图(ol)，其次 url1920，再 bl，最后 sl
        const url = p.ol || p.url1920 || p.bl || p.sl;
        if (!url) throw new Error('No URL available');

        const ext = path.extname(url.split('?')[0]) || '.jpg';
        const filename = `photo_${String(idx).padStart(3, '0')}${ext}`;
        const filepath = path.join(OUTPUT_DIR, filename);

        // 跳过已存在的文件
        if (fs.existsSync(filepath) && fs.statSync(filepath).size > 1000) {
          return { filename, size: fs.statSync(filepath).size, skipped: true };
        }

        const size = await downloadFile(url, filepath);
        return { filename, size, w: p.w, h: p.h };
      })
    );

    results.forEach((r) => {
      if (r.status === 'fulfilled') {
        const { filename, size, w, h, skipped } = r.value;
        const sizeMB = (size / 1024 / 1024).toFixed(1);
        if (skipped) {
          console.log(`⏭️  ${filename} (already exists, ${sizeMB}MB)`);
        } else {
          console.log(`✅ ${filename} (${w}x${h}) ${sizeMB}MB`);
        }
        success++;
      } else {
        console.log(`❌ Failed: ${r.reason.message}`);
        failed++;
      }
    });
  }

  console.log(`\n🎉 Done! Success: ${success}, Failed: ${failed}`);
  console.log(`📁 Saved to: ${OUTPUT_DIR}`);
}

main().catch((err) => {
  console.error('Error:', err.message);
  process.exit(1);
});
