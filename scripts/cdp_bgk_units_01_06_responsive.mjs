#!/usr/bin/env node
/* Bounded CDP measurement for the local BGK Units 1--6 HTML reader. */

import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";

const endpoint = process.env.BGK_CDP_ENDPOINT || "http://127.0.0.1:9229";
const expectedUrl = process.env.BGK_READER_URL || "http://127.0.0.1:18765/index.html";
const screenshotRoot = resolve("tmp/html-qa/bgk-unit-06");
const htmlPath = resolve("build/reader-bgk-id/index.html");
const receiptPath = resolve("qa/BGK_UNITS_01_06_RESPONSIVE_QA.json");
const provenance = "OpenAI Codex gpt-5.6-sol, Ultra.";

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function fact(path) {
  return {
    path: path.replaceAll("\\", "/").replace(resolve(".").replaceAll("\\", "/") + "/", ""),
    bytes: statSync(path).size,
    sha256: sha256(path),
  };
}

function require(condition, message) {
  if (!condition) throw new Error(message);
}

const tabs = await (await fetch(`${endpoint}/json/list`)).json();
const target = tabs.find((tab) => tab.type === "page" && tab.url.startsWith(expectedUrl));
if (!target?.webSocketDebuggerUrl) {
  throw new Error(`No CDP page target for ${expectedUrl}`);
}

const socket = new WebSocket(target.webSocketDebuggerUrl);
const pending = new Map();
const eventWaiters = new Map();
let sequence = 0;

socket.addEventListener("message", (event) => {
  const message = JSON.parse(event.data);
  if (message.id && pending.has(message.id)) {
    const { resolve, reject } = pending.get(message.id);
    pending.delete(message.id);
    if (message.error) reject(new Error(JSON.stringify(message.error)));
    else resolve(message.result);
    return;
  }
  const waiters = eventWaiters.get(message.method) || [];
  eventWaiters.delete(message.method);
  for (const resolve of waiters) resolve(message.params || {});
});

await new Promise((resolve, reject) => {
  socket.addEventListener("open", resolve, { once: true });
  socket.addEventListener("error", reject, { once: true });
});

function call(method, params = {}) {
  const id = ++sequence;
  socket.send(JSON.stringify({ id, method, params }));
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
}

function waitEvent(method, timeoutMs = 10000) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`Timed out waiting for ${method}`)), timeoutMs);
    const wrapped = (value) => {
      clearTimeout(timer);
      resolve(value);
    };
    const waiters = eventWaiters.get(method) || [];
    waiters.push(wrapped);
    eventWaiters.set(method, waiters);
  });
}

const expression = String.raw`(() => {
  const documentElement = document.documentElement;
  const body = document.body;
  const main = document.querySelector('main');
  const mainRect = main.getBoundingClientRect();
  const ids = [...document.querySelectorAll('[id]')].map((node) => node.id);
  const duplicateIds = ids.filter((value, index) => ids.indexOf(value) !== index);
  const anchors = [...document.querySelectorAll('a[href^="#"]')];
  const brokenAnchors = anchors
    .map((anchor) => decodeURIComponent(anchor.hash.slice(1)))
    .filter((id) => id && !document.getElementById(id));
  const overflowNodes = [...document.body.querySelectorAll('*')]
    .filter((node) => !node.matches('.skip-link'))
    .map((node) => {
      const rect = node.getBoundingClientRect();
      return {
        tag: node.tagName.toLowerCase(),
        id: node.id || null,
        classes: typeof node.className === 'string' ? node.className : '',
        left: Number(rect.left.toFixed(2)),
        right: Number(rect.right.toFixed(2)),
        width: Number(rect.width.toFixed(2)),
        protectedByLocalScroll: Boolean(node.closest('math[display="block"], pre, table, div.column')),
        text: (node.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 100),
      };
    })
    .filter((row) => row.width > 0 && (row.left < -0.5 || row.right > documentElement.clientWidth + 0.5));
  const localScrollNodes = [...document.querySelectorAll('math[display="block"], pre, table, div.column')]
    .filter((node) => node.scrollWidth > node.clientWidth + 1)
    .map((node) => ({
      tag: node.tagName.toLowerCase(),
      id: node.id || null,
      clientWidth: node.clientWidth,
      scrollWidth: node.scrollWidth,
    }));
  return {
    title: document.title,
    viewport: {
      innerWidth,
      innerHeight,
      clientWidth: documentElement.clientWidth,
      scrollWidth: documentElement.scrollWidth,
      bodyScrollWidth: body.scrollWidth,
      documentHorizontalOverflow: documentElement.scrollWidth > documentElement.clientWidth + 1,
    },
    main: {
      left: Number(mainRect.left.toFixed(2)),
      right: Number(mainRect.right.toFixed(2)),
      width: Number(mainRect.width.toFixed(2)),
      centeringDelta: Number((((mainRect.left + mainRect.right) / 2) - documentElement.clientWidth / 2).toFixed(2)),
    },
    counts: {
      main: document.querySelectorAll('main').length,
      skipLinks: document.querySelectorAll('.skip-link').length,
      mathml: document.querySelectorAll('math').length,
      blockMath: document.querySelectorAll('math[display="block"]').length,
      images: document.querySelectorAll('img').length,
      missingAlt: document.querySelectorAll('img:not([alt])').length,
      ids: ids.length,
      duplicateIds: [...new Set(duplicateIds)].length,
      anchors: anchors.length,
      brokenAnchors: [...new Set(brokenAnchors)].length,
      headings: document.querySelectorAll('h1,h2,h3,h4,h5,h6').length,
      outsideViewportNodes: overflowNodes.length,
      unprotectedOutsideViewportNodes: overflowNodes.filter((row) => !row.protectedByLocalScroll).length,
      localHorizontalScrollNodes: localScrollNodes.length,
    },
    outsideViewportNodes: overflowNodes.slice(0, 40),
    localHorizontalScrollNodes: localScrollNodes.slice(0, 40),
  };
})()`;

async function measure(name, width, height) {
  await call("Emulation.setDeviceMetricsOverride", {
    width,
    height,
    deviceScaleFactor: 1,
    mobile: false,
    screenWidth: width,
    screenHeight: height,
  });
  const loaded = waitEvent("Page.loadEventFired");
  await call("Page.reload", { ignoreCache: true });
  await loaded;
  await new Promise((resolve) => setTimeout(resolve, 500));
  await call("Runtime.evaluate", {
    expression: "window.scrollTo(0, 0); true",
    returnByValue: true,
  });
  await new Promise((resolve) => setTimeout(resolve, 100));
  const evaluated = await call("Runtime.evaluate", {
    expression,
    returnByValue: true,
    awaitPromise: true,
  });
  if (evaluated.exceptionDetails) {
    throw new Error(JSON.stringify(evaluated.exceptionDetails));
  }
  const screenshot = await call("Page.captureScreenshot", {
    format: "png",
    fromSurface: true,
    captureBeyondViewport: false,
  });
  const screenshotPath = resolve(screenshotRoot, `${name}-cdp-final.png`);
  mkdirSync(dirname(screenshotPath), { recursive: true });
  writeFileSync(screenshotPath, Buffer.from(screenshot.data, "base64"));
  return { name, width, height, screenshotPath, ...evaluated.result.value };
}

await call("Page.enable");
await call("Runtime.enable");
const desktop = await measure("desktop", 1280, 720);
const mobile = await measure("mobile", 390, 844);
await call("Runtime.evaluate", {
  expression: "document.getElementById('br-bgk-2019-w06-ex15').scrollIntoView({block:'start'}); true",
  returnByValue: true,
});
await new Promise((resolve) => setTimeout(resolve, 250));
const deepScreenshot = await call("Page.captureScreenshot", {
  format: "png",
  fromSurface: true,
  captureBeyondViewport: false,
});
const deepScreenshotPath = resolve(screenshotRoot, "mobile-unit6-ex15-cdp-final.png");
writeFileSync(deepScreenshotPath, Buffer.from(deepScreenshot.data, "base64"));
socket.close();

const html = fact(htmlPath);
require(html.bytes === 3272151 && html.sha256 === "feb45d21d6168feaedf35719fdcb0b7f5532687846041d9fd75573c6d66fc5e9", "HTML identity drifted");
for (const surface of [desktop, mobile]) {
  require(surface.title === "Bundel, Berkas, dan Kohomologi - Unit 1-6", `${surface.name} title drifted`);
  require(!surface.viewport.documentHorizontalOverflow, `${surface.name} has document overflow`);
  require(Math.abs(surface.main.centeringDelta) <= 0.5, `${surface.name} main is not centered`);
  require(surface.counts.main === 1 && surface.counts.skipLinks === 1, `${surface.name} landmark closure failed`);
  require(surface.counts.missingAlt === 0 && surface.counts.duplicateIds === 0 && surface.counts.brokenAnchors === 0,
          `${surface.name} accessibility/anchor closure failed`);
  require(surface.counts.unprotectedOutsideViewportNodes === 0, `${surface.name} has unprotected clipped content`);
}
require(desktop.main.width === 972 && mobile.main.width === 343, "responsive main-width contract drifted");
require(mobile.counts.localHorizontalScrollNodes > 0, "wide mobile mathematics is not locally scrollable");

const responsiveReceipt = {
  schema: "ag-bridge-bgk-responsive-qa-v1",
  through_unit: 6,
  status: "PASS",
  model_provenance: provenance,
  target: expectedUrl,
  html,
  reader_machine_qa: {
    path: "qa/BGK_UNITS_01_06_READER_QA.json",
    bytes: 6369,
    sha256: "8c40f147451888e3ab4c2da95d164388c4f5725d37e121f020842da9488e250c",
  },
  desktop,
  mobile,
  screenshots: [
    fact(desktop.screenshotPath),
    fact(mobile.screenshotPath),
    fact(deepScreenshotPath),
  ],
  checks: {
    desktop_centered_and_page_filling: true,
    mobile_reflow_without_document_overflow: true,
    wide_math_uses_bounded_local_scroll: true,
    no_unprotected_content_outside_viewport: true,
    skip_link_landmark_alt_id_and_anchor_closure: true,
    unit_06_exercise_15_mobile_surface_captured: true,
  },
};
writeFileSync(receiptPath, JSON.stringify(responsiveReceipt, null, 2) + "\n");
console.log(JSON.stringify({ receipt: fact(receiptPath), desktop: responsiveReceipt.desktop, mobile: responsiveReceipt.mobile }, null, 2));
