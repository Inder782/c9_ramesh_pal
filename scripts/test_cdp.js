import { spawn } from 'child_process';
import http from 'http';
import fs from 'fs';

function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function getJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
      });
    }).on('error', reject);
  });
}

class CDPClient {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.id = 1;
    this.callbacks = new Map();
    this.events = new Map();

    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && this.callbacks.has(msg.id)) {
        const { resolve, reject } = this.callbacks.get(msg.id);
        this.callbacks.delete(msg.id);
        if (msg.error) reject(msg.error);
        else resolve(msg.result);
      } else if (msg.method) {
        const handler = this.events.get(msg.method);
        if (handler) handler(msg.params);
      }
    };
  }

  ready() {
    return new Promise((resolve, reject) => {
      if (this.ws.readyState === WebSocket.OPEN) return resolve();
      this.ws.onopen = () => resolve();
      this.ws.onerror = reject;
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.id++;
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  on(event, handler) {
    this.events.set(event, handler);
  }

  close() {
    this.ws.close();
  }
}

async function run() {
  const chromeProc = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9222',
    'about:blank'
  ]);

  try {
    await wait(1500);
    const list = await getJson('http://localhost:9222/json');
    const pageTab = list.find(t => t.type === 'page') || list[0];
    console.log('Connecting to tab:', pageTab.title, pageTab.webSocketDebuggerUrl);

    const client = new CDPClient(pageTab.webSocketDebuggerUrl);
    await client.ready();
    await client.send('Page.enable');
    await client.send('DOM.enable');

    const devices = [
      { name: '250_Ultra_Narrow', width: 250, height: 500, dpr: 2, mobile: true },
      { name: '320_Narrow', width: 320, height: 600, dpr: 2, mobile: true },
      { name: '360_Galaxy_S', width: 360, height: 780, dpr: 3, mobile: true },
      { name: '375_iPhone_SE', width: 375, height: 667, dpr: 2, mobile: true },
      { name: '393_iPhone_16', width: 393, height: 852, dpr: 3, mobile: true },
      { name: '412_Pixel_9_Galaxy_F55', width: 412, height: 915, dpr: 2.6, mobile: true },
      { name: '440_iPhone_16_Pro_Max', width: 440, height: 956, dpr: 3, mobile: true },
      { name: '600_Small_Tablet', width: 600, height: 900, dpr: 2, mobile: true },
      { name: '768_Z_Fold_6_iPad_Mini', width: 768, height: 1024, dpr: 2, mobile: true },
      { name: '820_iPad_Air', width: 820, height: 1180, dpr: 2, mobile: true },
      { name: '912_Surface_Pro_10', width: 912, height: 1368, dpr: 2, mobile: true },
      { name: '1024_iPad_Pro_13', width: 1024, height: 1366, dpr: 2, mobile: true },
      { name: '1280_Nest_Hub_Max', width: 1280, height: 800, dpr: 1.5, mobile: false },
      { name: '1440_Desktop_Baseline', width: 1440, height: 900, dpr: 1, mobile: false },
      { name: '1920_FHD_Desktop', width: 1920, height: 1080, dpr: 1, mobile: false },
      { name: '2560_QHD_Desktop', width: 2560, height: 1440, dpr: 1, mobile: false },
      { name: '2599_Custom_QHD', width: 2599, height: 1440, dpr: 1, mobile: false },
      { name: '3840_4K_UHD', width: 3840, height: 2160, dpr: 1, mobile: false },
    ];

    for (const dev of devices) {
      console.log(`\n================ Testing ${dev.name} (${dev.width}x${dev.height}) ================`);
      await client.send('Emulation.setDeviceMetricsOverride', {
        width: dev.width,
        height: dev.height,
        deviceScaleFactor: dev.dpr,
        mobile: dev.mobile
      });

      await client.send('Page.navigate', { url: 'http://localhost:4321/?bypass_disclaimer=1' });
      await wait(1500); // Wait for CSS animations to finish

      const evalRes = await client.send('Runtime.evaluate', {
        expression: `
          (() => {
            const docWidth = document.documentElement.scrollWidth;
            const winWidth = window.innerWidth;
            const header = document.querySelector('#main-header');
            const hero = document.querySelector('#home');
            const container = document.querySelector('.hero-content-container');
            const eyebrow = document.querySelector('.hero-eyebrow');
            const title = document.querySelector('.hero-title');
            const support = document.querySelector('.hero-support');
            const cta = document.querySelector('.hero-action');
            const trust = document.querySelector('.hero-mobile-trust');

            const hRect = header ? header.getBoundingClientRect() : null;
            const cRect = container ? container.getBoundingClientRect() : null;
            const eRect = eyebrow ? eyebrow.getBoundingClientRect() : null;
            const tRect = title ? title.getBoundingClientRect() : null;
            const sRect = support ? support.getBoundingClientRect() : null;
            const ctaRect = cta ? cta.getBoundingClientRect() : null;
            const trRect = trust ? trust.getBoundingClientRect() : null;

            return {
              windowWidth: winWidth,
              documentScrollWidth: docWidth,
              hasHorizontalOverflow: docWidth > winWidth,
              header: hRect ? { top: hRect.top, bottom: hRect.bottom, width: hRect.width, left: hRect.left, right: hRect.right } : null,
              hero: hero ? { top: hero.offsetTop, height: hero.offsetHeight } : null,
              container: cRect ? { top: cRect.top, bottom: cRect.bottom, width: cRect.width, height: cRect.height } : null,
              gapHeaderToContent: (eRect && hRect) ? Math.round(eRect.top - hRect.bottom) : null,
              eyebrow: eRect ? { top: eRect.top, bottom: eRect.bottom, width: eRect.width } : null,
              title: tRect ? { top: tRect.top, bottom: tRect.bottom, width: tRect.width, height: tRect.height } : null,
              support: sRect ? { top: sRect.top, bottom: sRect.bottom, width: sRect.width } : null,
              cta: ctaRect ? { top: ctaRect.top, bottom: ctaRect.bottom, width: ctaRect.width, height: ctaRect.height } : null,
              trustBadge: trRect ? { top: trRect.top, bottom: trRect.bottom, width: trRect.width, height: trRect.height } : null,
              titleFontSize: title ? window.getComputedStyle(title).fontSize : null,
              titleLineHeight: title ? window.getComputedStyle(title).lineHeight : null,
            };
          })()
        `,
        returnByValue: true
      });

      console.log('Metrics:', JSON.stringify(evalRes.result.value, null, 2));

      // Capture screenshot
      const shot = await client.send('Page.captureScreenshot', { format: 'png' });
      fs.writeFileSync(`shot_${dev.name.replace(/\s+/g, '_')}.png`, Buffer.from(shot.data, 'base64'));
      console.log(`Saved screenshot: shot_${dev.name.replace(/\s+/g, '_')}.png`);
    }

    client.close();
  } finally {
    chromeProc.kill();
  }
}

run().catch(console.error);
