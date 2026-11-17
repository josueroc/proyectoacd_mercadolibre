// Escribe la paleta del tema en ppt/theme/theme1.xml. pptxgenjs fija las fuentes del tema, pero deja la paleta de
// Office: sin este paso, los colores de esquema (accent1, dk2...) se verían con el azul y naranja por defecto.
const fs = require('fs');

const RANURAS = ['dk1', 'lt1', 'dk2', 'lt2', 'accent1', 'accent2', 'accent3', 'accent4', 'accent5', 'accent6',
  'hlink', 'folHlink'];

function cargarJSZip() {
  return require(require.resolve('jszip', { paths: [require.resolve('pptxgenjs')] }));
}

async function aplicarTema(ruta, tema) {
  const zip = await cargarJSZip().loadAsync(fs.readFileSync(ruta));
  const parte = 'ppt/theme/theme1.xml';
  const nombre = tema.name.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
  const esquema = `<a:clrScheme name="${nombre}">`
    + RANURAS.map((k) => `<a:${k}><a:srgbClr val="${tema.colors[k]}"/></a:${k}>`).join('')
    + '</a:clrScheme>';
  const xml = (await zip.file(parte).async('string')).replace(/<a:clrScheme\b[\s\S]*?<\/a:clrScheme>/, () => esquema);
  zip.file(parte, xml);
  for (const archivo of Object.keys(zip.files)) {
    if (zip.files[archivo].dir) { delete zip.files[archivo]; continue; }
    if (!archivo.endsWith('.xml')) continue;
    const contenido = await zip.file(archivo).async('string');
    if (contenido.includes('<c:crossesAt val="autoZero"/>')) {
      zip.file(archivo, contenido.replaceAll('<c:crossesAt val="autoZero"/>', '<c:crosses val="autoZero"/>'));
    }
  }
  fs.writeFileSync(ruta, await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
}

module.exports = { aplicarTema };
