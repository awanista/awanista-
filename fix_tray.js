const fs = require('fs');
let s = fs.readFileSync('index.html', 'utf8');
const i = s.indexOf("desc:'تحفة فنية");
const j = s.indexOf("'};", i);
const seg = s.slice(i, j + 3);
const fixed = seg.replace(/\r?\n/g, "\\n");
s = s.slice(0, i) + fixed + s.slice(i + seg.length);
fs.writeFileSync('index.html', s);
console.log('fixed chars:', seg.length, '->', fixed.length);
