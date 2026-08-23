// Tự kiểm bản .src.html trước khi báo xong.
// Dùng: node docs/html/_khung/check.mjs docs/html/<PYC>/<slug>-flow.src.html
import fs from 'node:fs';

const f = process.argv[2];
if (!f) { console.error('Thiếu đường dẫn file'); process.exit(1); }
const s = fs.readFileSync(f, 'utf8');
const than = s.split('</style>').pop();   // phần thân, bỏ head để không dính comment CSS
let bad = 0;
const say = (label, ok, extra = '') => { if (!ok) bad++; console.log(`${label}: ${ok ? 'OK' : '<<< LỖI'} ${extra}`); };

// 1. cân bằng thẻ
for (const t of ['section','figure','table','div','pre','nav','main','header','footer','tbody','thead','tr','td','th','ul','ol','li','p','figcaption','span']) {
  const o = (than.match(new RegExp('<' + t + '(?=[ \\t\\n>])', 'g')) || []).length;
  const c = (than.match(new RegExp('</' + t + '>', 'g')) || []).length;
  say('thẻ ' + t, o === c, `${o}/${c}`);
}

// 2. sơ đồ
const nPre = (than.match(/class="mermaid"/g) || []).length;
const nInit = (than.match(/%%\{init:/g) || []).length;
console.log('số sơ đồ: ' + nPre);
say('mọi block có chuỗi init', nPre === nInit, `${nInit}/${nPre}`);

// 3. head nguyên vẹn
const head = fs.readFileSync('docs/html/_khung/head.html', 'utf8');
const mineHead = s.slice(0, s.indexOf('</style>') + 8);
const refHead = head.slice(0, head.indexOf('</style>') + 8);
const strip = x => x.replace(/<title>[\s\S]*?<\/title>/, '');
say('head copy nguyên văn (chỉ khác <title>)', strip(mineHead).trim() === strip(refHead).trim());

// 4. thân không thừa thẻ
say('thân không doctype/html/body/style/script', !/<!doctype|<html|<body|<style|<script/i.test(than));
say('thân mở bằng <div class="wrap">', than.trim().startsWith('<div class="wrap">'));

// 5. nhãn mermaid
// bỏ chuỗi %%{init:…}%% khỏi phần quét nhãn — fontFamily trong đó không phải nhãn
const blocks = [...than.matchAll(/<pre class="mermaid">([\s\S]*?)<\/pre>/g)]
  .map(m => m[1].replace(/%%\{init:[\s\S]*?\}%%/g, ''));
let badChar = 0, longLine = 0, subg = 0;
blocks.forEach(b => {
  if (/^\s*subgraph/m.test(b)) subg++;
  for (const lab of b.match(/"[^"]*"/g) || []) {
    if (/<(?!\/?(b|i|br\s*\/?)>)/.test(lab)) badChar++;
    for (const part of lab.slice(1, -1).split(/<br\s*\/?>/)) if (part.replace(/<\/?[bi]>/g, '').length > 36) longLine++;
  }
});
say('không nhãn chứa thẻ lạ / < >', badChar === 0, badChar ? badChar + ' nhãn' : '');
if (longLine) console.log('cảnh báo: ' + longLine + ' dòng nhãn > 36 ký tự — nhãn dài làm sơ đồ phình ngang');
if (subg) console.log(`cảnh báo: ${subg} block có subgraph — kiểm lại bề rộng`);

// 6. class dùng nhưng khung không định nghĩa
const defined = new Set([...head.matchAll(/\.([a-z][a-z0-9-]*)\s*[,{ ]/gi)].map(m => m[1]));
const used = new Set([...than.matchAll(/class="([^"]+)"/g)].flatMap(m => m[1].split(/\s+/)));
const unknown = [...used].filter(c => !defined.has(c) && c !== 'mermaid');
say('không dùng class lạ ngoài khung', unknown.length === 0, unknown.join(' '));

console.log(bad === 0 ? '\n=== ĐẠT ===' : `\n=== CÒN ${bad} LỖI ===`);
process.exit(bad === 0 ? 0 : 1);
