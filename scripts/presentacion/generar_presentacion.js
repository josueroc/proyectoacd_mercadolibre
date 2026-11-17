// Genera la presentación de la Parte II (16:9) con las cifras de data/final/metricas.json, las figuras de los
// notebooks y gráficos nativos de PowerPoint. Cada diapositiva lleva notas para quien la presenta.
//
//   cd scripts/presentacion && npm install && node generar_presentacion.js
//
// Salida: docs/parte_2/presentacion/Presentacion_Parte_II_DS3021.pptx
const path = require('path');
const fs = require('fs');
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const pptxgen = require('pptxgenjs');
const tb = require('react-icons/tb');
const { aplicarTema } = require('./aplicar_tema');

const RAIZ = path.resolve(__dirname, '..', '..');
const M = JSON.parse(fs.readFileSync(path.join(RAIZ, 'data', 'final', 'metricas.json'), 'utf8'));
const FIGURAS = path.join(RAIZ, 'docs', 'parte_2', 'figuras');
const IMAGENES = path.join(RAIZ, 'docs', 'parte_2', 'presentacion', 'imagenes');
const SALIDA = path.join(RAIZ, 'docs', 'parte_2', 'presentacion', 'Presentacion_Parte_II_DS3021.pptx');

// Notas del orador: se copian del guion que lee el equipo, para que ambos digan lo mismo.
const GUION = fs.readFileSync(path.join(RAIZ, 'docs', 'parte_2', 'presentacion', 'guion_presentacion.md'), 'utf8');
function nota(n) {
  let quien = '';
  for (const bloque of GUION.split(/^(?=##+ )/m)) {
    const h2 = bloque.match(/^## (\S+) —/);
    if (h2) quien = h2[1];
    const h3 = bloque.match(/^### (\d+) · [^\n]*?(?:\(≈ ([^)]+)\))?\n/);
    if (h3 && Number(h3[1]) === n) {
      const cuerpo = bloque.slice(h3[0].length).replace(/\*\*|\*|`/g, '').trim();
      return h3[2] ? `[${quien} · ${h3[2]}]\n${cuerpo}` : cuerpo;
    }
  }
  throw new Error(`El guion no tiene la diapositiva ${n}`);
}

// ------------------------------------------------------------------ tema
const TEMA = {
  name: 'Home office · datos',
  headFontFace: 'Bahnschrift',
  bodyFontFace: 'Segoe UI',
  colors: {
    dk1: '0B1220', lt1: 'FFFFFF', dk2: '1B2A41', lt2: 'EEF3F8',
    accent1: '2A78D6', accent2: '00B4D8', accent3: 'F59E0B', accent4: '104281', accent5: '86B6EF', accent6: 'E34948',
    hlink: '2A78D6', folHlink: '104281',
  },
};
const HEX = TEMA.colors;
const MONO = 'Consolas';
const GRIS = '52514E';
const REJILLA = 'E1E0D9';
const COMPONENTES = ['laptop', 'monitor', 'silla', 'teclado', 'mouse', 'audifonos'];
const NOMBRE = { laptop: 'Laptop', monitor: 'Monitor', silla: 'Silla', teclado: 'Teclado', mouse: 'Mouse', audifonos: 'Audífonos' };
const COLOR_COMPONENTE = { laptop: '2A78D6', monitor: 'EB6834', silla: '1BAF7A', teclado: 'EDA100', mouse: 'E87BA4', audifonos: '008300' };
const COLOR_GAMA = ['5FA0EA', '2A78D6', '104281'];

// ------------------------------------------------------------------ formato
const miles = (v) => Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
const soles = (v) => `S/ ${miles(v)}`;
const num = (v, d = 1) => v.toFixed(d).replace('.', ',');
const formatoP = (p) => (p < 0.001 ? 'p < 0,001' : `p = ${num(p, 3)}`);

async function icono(Componente, color, tam = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Componente, { color: `#${color}`, size: tam }));
  const png = await sharp(Buffer.from(svg)).png().toBuffer();
  return `image/png;base64,${png.toString('base64')}`;
}

function ejes(extra = {}) {
  return {
    catAxisLabelColor: GRIS, valAxisLabelColor: GRIS, catAxisLabelFontFace: '+mn-lt', valAxisLabelFontFace: '+mn-lt',
    catAxisLabelFontSize: 12, valAxisLabelFontSize: 11, dataLabelFontFace: '+mn-lt', dataLabelFontSize: 12,
    dataLabelColor: '0B1220', valGridLine: { color: REJILLA, size: 0.75 }, catGridLine: { style: 'none' },
    valAxisLineShow: false, catAxisLineShow: true, catAxisLineColor: 'B4B2A9', showLegend: false,
    legendFontFace: '+mn-lt', legendFontSize: 12, legendColor: GRIS, ...extra,
  };
}

async function main() {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE'; // 13,333 × 7,5 pulgadas
  pres.title = '¿Cuánto cuesta equipar un home office en el Perú?';
  pres.subject = 'DS3021 Análisis Computacional de Datos · Proyecto final, Parte II';
  pres.author = 'Riveros, Roque, Terán, Luna y García';
  pres.company = 'UTEC';
  pres.theme = { headFontFace: TEMA.headFontFace, bodyFontFace: TEMA.bodyFontFace };
  const C = pres.SchemeColor;

  // ---------------------------------------------------------------- layouts
  const pie = [
    { text: { text: 'DS3021 · ¿Cuánto cuesta equipar un home office en el Perú?',
      options: { x: 0.6, y: 6.98, w: 9, h: 0.3, fontSize: 10, color: C.text2, transparency: 40 } } },
  ];
  pres.defineSlideMaster({
    title: 'CONTENIDO',
    background: { color: C.background1 },
    margin: [0.5, 0.6, 0.6, 0.6],
    objects: [
      ...pie,
      { placeholder: { options: { name: 'etiqueta', type: 'body', x: 0.6, y: 0.32, w: 9, h: 0.34, fontFace: MONO,
        fontSize: 12, color: C.accent1, margin: 0, valign: 'middle' }, text: '' } },
      { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.66, w: 12.1, h: 0.8, fontSize: 32, bold: true,
        color: C.text1, margin: 0, valign: 'top', align: 'left' }, text: '' } },
    ],
    slideNumber: { x: 12.2, y: 6.98, w: 0.6, h: 0.3, fontSize: 10, color: C.text2, align: 'right', fontFace: MONO },
  });
  pres.defineSlideMaster({
    title: 'OSCURO',
    background: { color: C.text1 },
    objects: [
      { placeholder: { options: { name: 'etiqueta', type: 'body', x: 0.6, y: 0.5, w: 9, h: 0.34, fontFace: MONO,
        fontSize: 12, color: C.accent2, margin: 0 }, text: '' } },
      { placeholder: { options: { name: 'title', type: 'title', x: 0.6, y: 0.9, w: 7.2, h: 2.2, fontSize: 40, bold: true,
        color: C.background1, margin: 0, valign: 'top', align: 'left' }, text: '' } },
    ],
    slideNumber: { x: 12.2, y: 6.98, w: 0.6, h: 0.3, fontSize: 10, color: C.accent5, align: 'right', fontFace: MONO },
  });

  const ic = {
    ley: await icono(tb.TbScale, HEX.accent1), cifra: await icono(tb.TbCalculator, HEX.accent1),
    clave: await icono(tb.TbKey, HEX.accent1), filtro: await icono(tb.TbFilter, HEX.accent1),
    hueco: await icono(tb.TbQuestionMark, HEX.accent1), reloj: await icono(tb.TbClockHour4, HEX.accent1),
    base: await icono(tb.TbDatabase, 'FFFFFF'), web: await icono(tb.TbWorldWww, '0B1220'),
    entrada: await icono(tb.TbFileImport, '0B1220'), engranaje: await icono(tb.TbAdjustmentsHorizontal, '0B1220'),
    grafico: await icono(tb.TbChartBar, 'FFFFFF'), terminal: await icono(tb.TbTerminal2, HEX.accent2),
    escudo: await icono(tb.TbShieldCheck, HEX.accent1), balanza: await icono(tb.TbArrowsLeftRight, HEX.accent1),
    huella: await icono(tb.TbFingerprint, HEX.accent1), hash: await icono(tb.TbHash, HEX.accent1),
    cpu: await icono(tb.TbCpu, HEX.accent1), tag: await icono(tb.TbTag, HEX.accent1),
    estrella: await icono(tb.TbStar, HEX.accent1), marca: await icono(tb.TbBadge, HEX.accent1),
    rrhh: await icono(tb.TbBuildingSkyscraper, HEX.accent4), persona: await icono(tb.TbUser, HEX.accent4),
    check: await icono(tb.TbCircleCheck, HEX.accent2), alerta: await icono(tb.TbAlertTriangle, HEX.accent3),
  };

  const secciones = ['Contexto', 'Pipeline', 'Calidad de datos', 'Variables y gamas', 'Resultados', 'Demo y cierre',
    'Anexo'];
  secciones.forEach((t) => pres.addSection({ title: t }));
  let seccion = secciones[0];
  const nueva = (master = 'CONTENIDO') => pres.addSlide({ masterName: master, sectionTitle: seccion });
  const encabezado = (s, etiqueta, titulo) => {
    s.addText(etiqueta, { placeholder: 'etiqueta' });
    s.addText(titulo, { placeholder: 'title' });
  };
  const tarjeta = (s, x, y, w, h, opciones = {}) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.12, fill: { color: opciones.fill || C.background2 }, line: { type: 'none' },
    objectName: opciones.nombre,
  });
  const texto = (s, contenido, opciones) => s.addText(contenido, { isTextBox: true, margin: 0, color: C.text1,
    fontSize: 15, valign: 'top', ...opciones });

  const perf = M.costos.perfiles;
  const lim = M.limpieza;
  const integ = M.integracion;
  const at = M.atipicos;
  const car = M.caracteristicas;
  const an = M.analisis;
  const ajenas = Object.values(lim.ajenas).reduce((a, b) => a + b, 0);
  const unicasOferta = lim.ofertas_unicas + ajenas;

  // ================================================================ 1. portada
  {
    const s = nueva('OSCURO');
    s.addImage({ path: path.join(IMAGENES, 'homeoffice.jpg'), x: 8.2, y: 0, w: 5.133, h: 7.5,
      sizing: { type: 'cover', w: 5.133, h: 7.5 }, altText: 'Escritorio de home office con monitor y laptop' });
    s.addText('// DS3021 · Proyecto final · Parte II', { placeholder: 'etiqueta' });
    s.addText('¿Cuánto cuesta equipar un home office en el Perú?', { placeholder: 'title' });
    texto(s, 'Preprocesamiento, análisis y pipeline de datos de Mercado Libre Perú', {
      x: 0.6, y: 3.25, w: 7.2, h: 0.8, fontSize: 18, color: C.accent5 });
    texto(s, [
      { text: 'Yared Riveros · Franco Roque · Mauricio Terán', options: { breakLine: true } },
      { text: 'Josué Luna · Alvaro García' },
    ], { x: 0.6, y: 5.3, w: 7.2, h: 0.7, fontSize: 15, color: C.background1 });
    texto(s, 'Análisis Computacional de Datos · UTEC · 2026', {
      x: 0.6, y: 6.15, w: 7.2, h: 0.35, fontSize: 12, color: C.accent5, fontFace: MONO });
    s.addNotes(nota(1));
  }

  // ================================================================ 2. agenda
  {
    const s = nueva();
    encabezado(s, '// agenda · 15 minutos', 'Recorrido: del dato crudo a la recomendación');
    const bloques = [
      ['01', 'Problema y objetivos', 'Ley de Teletrabajo, qué cambió al mirar los datos', 'Yared', '2 min'],
      ['02', 'Pipeline e ingesta', 'Seis etapas, clave de oferta, separar lo que no es el componente', 'Franco', '2 min'],
      ['03', 'Calidad de datos', 'Faltantes, atípicos e integración de las dos capturas', 'Mauricio', '3 min'],
      ['04', 'Variables y gamas', '24 variables derivadas; terciles frente a K-Means', 'Josué', '3 min'],
      ['05', 'Resultados e insights', 'Costo por perfil, promociones, pruebas estadísticas', 'Alvaro', '3 min'],
      ['06', 'Demo y cierre', 'python pipeline.py en vivo; conclusiones', 'Franco · Alvaro', '2 min'],
    ];
    bloques.forEach(([n, t, d, quien, tiempo], i) => {
      const y = 1.75 + i * 0.82;
      tarjeta(s, 0.6, y, 12.1, 0.68, { nombre: `bloque-${n}` });
      texto(s, n, { x: 0.85, y, w: 0.8, h: 0.68, fontSize: 22, bold: true, color: C.accent1, fontFace: MONO,
        valign: 'middle' });
      texto(s, t, { x: 1.75, y, w: 3.6, h: 0.68, fontSize: 17, bold: true, valign: 'middle' });
      texto(s, d, { x: 5.4, y, w: 4.6, h: 0.68, fontSize: 14, color: C.text2, valign: 'middle' });
      texto(s, quien, { x: 10.0, y, w: 1.75, h: 0.68, fontSize: 14, bold: true, color: C.accent4, valign: 'middle' });
      texto(s, tiempo, { x: 11.75, y, w: 0.8, h: 0.68, fontSize: 12, color: C.text2, fontFace: MONO,
        valign: 'middle', align: 'right' });
    });
    s.addNotes(nota(2));
  }

  // ================================================================ 3. problema
  {
    const s = nueva();
    encabezado(s, '// 01 · problema', 'Una sola cifra no basta para compensar');
    s.addImage({ path: path.join(IMAGENES, 'caja.jpg'), x: 0.6, y: 1.75, w: 4.2, h: 4.9,
      sizing: { type: 'cover', w: 4.2, h: 4.9 }, altText: 'Cajas de envío de una compra en línea' });
    s.addImage({ data: ic.ley, x: 5.25, y: 1.8, w: 0.45, h: 0.45 });
    texto(s, [
      { text: 'La Ley N.º 31572 de Teletrabajo ', options: { bold: true } },
      { text: 'obliga al empleador a proveer los equipos o a compensar los propios según su valor de mercado. '
        + 'En el Perú nadie publica ese valor.' },
    ], { x: 5.9, y: 1.78, w: 6.8, h: 1.1, fontSize: 16 });
    tarjeta(s, 5.25, 3.15, 3.55, 2.0, { nombre: 'cifra-parte-1' });
    texto(s, soles(M.costos.suma_medianas_parte1), { x: 5.5, y: 3.35, w: 3.1, h: 0.8, fontSize: 36, bold: true,
      fontFace: TEMA.headFontFace, color: C.text2 });
    texto(s, 'Parte I: una sola cifra, suma de las medianas de seis componentes', { x: 5.5, y: 4.2, w: 3.1, h: 0.8,
      fontSize: 13, color: C.text2 });
    tarjeta(s, 9.15, 3.15, 3.55, 2.0, { fill: C.accent4, nombre: 'cifra-parte-2' });
    texto(s, `×${num(perf.alto.costo_mediano / perf['económico'].costo_mediano)}`, { x: 9.4, y: 3.35, w: 3.1, h: 0.8,
      fontSize: 36, bold: true, fontFace: TEMA.headFontFace, color: C.background1 });
    texto(s, 'Parte II: lo que cuesta el perfil alto frente al económico', { x: 9.4, y: 4.2, w: 3.1, h: 0.8,
      fontSize: 13, color: C.background1 });
    tarjeta(s, 5.25, 5.45, 7.45, 1.2, { fill: 'FFF7E6', nombre: 'pregunta-guia' });
    texto(s, [
      { text: 'Pregunta guía  ', options: { bold: true, color: 'B45309' } },
      { text: '¿Cuánto cuesta un home office según el nivel de equipamiento y qué señales del mercado ayudan o '
        + 'engañan al comprar?' },
    ], { x: 5.5, y: 5.6, w: 7.0, h: 0.95, fontSize: 15, valign: 'middle' });
    s.addNotes(nota(3));
  }

  // ================================================================ 4. contexto actualizado
  {
    const s = nueva();
    encabezado(s, '// 01 · contexto actualizado', 'Mirar los datos cambió el problema');
    const hallazgos = [
      [ic.clave, 'La unidad es la oferta',
        `Con el parámetro wid de la URL, las dos capturas comparten ${integ.comunes_por_oferta} ofertas, no ${integ.comunes_por_catalogo}.`],
      [ic.filtro, 'Búsqueda no es componente',
        `Se separaron ${ajenas} accesorios, kits y otros productos; ${lim.anuncios_patrocinados_crudo} registros crudos eran anuncios.`],
      [ic.hueco, 'Los faltantes no son aleatorios',
        'Las reseñas faltan más en los productos caros: ninguna columna es MCAR, así que no se borran filas.'],
      [ic.reloj, 'Los precios son estables',
        `El ${num(integ.sin_cambio_pct, 0)} % de las ofertas repetidas mantuvo su precio entre el 13 y el 15 de septiembre.`],
    ];
    hallazgos.forEach(([img, t, d], i) => {
      const x = 0.6 + (i % 2) * 6.15;
      const y = 1.75 + Math.floor(i / 2) * 2.5;
      tarjeta(s, x, y, 5.95, 2.25, { nombre: `hallazgo-${i + 1}` });
      s.addShape(pres.shapes.OVAL, { x: x + 0.3, y: y + 0.32, w: 0.75, h: 0.75, fill: { color: C.background1 },
        line: { type: 'none' } });
      s.addImage({ data: img, x: x + 0.45, y: y + 0.47, w: 0.45, h: 0.45 });
      texto(s, t, { x: x + 1.3, y: y + 0.28, w: 4.45, h: 0.45, fontSize: 17, bold: true, fontFace: TEMA.headFontFace });
      texto(s, d, { x: x + 1.3, y: y + 0.85, w: 4.45, h: 1.2, fontSize: 14, color: C.text2 });
    });
    s.addNotes(nota(4));
  }

  // ================================================================ 5. objetivos
  {
    const s = nueva();
    encabezado(s, '// 01 · objetivos actualizados', 'Objetivos ajustados a lo que los datos permiten');
    const objetivos = [
      ['Tratar faltantes según su tipo', 'MCAR, MAR o MNAR con chi-cuadrado', '6 columnas · ninguna MCAR'],
      ['Detectar y decidir atípicos', 'IQR, |z| > 3, K-Means y Mahalanobis', `${at.univariados} + ${at.kmeans} detectados · ${at.excluidos_por_error} excluido`],
      ['Integrar las dos capturas', 'Clave de oferta, agregar atributos', `${integ.comunes_por_oferta} ofertas comunes`],
      ['Construir variables y gamas', 'Ingeniería de características y qcut', `${car.variables_derivadas} variables · 3 gamas`],
      ['Estimar el costo por perfil', 'Mediana y rango por gama', `${soles(perf['económico'].costo_mediano)} a ${soles(perf.alto.costo_mediano)}`],
      ['Pipeline reproducible', 'Orquestador, SQLite, manifiesto SHA-256', 'Salidas idénticas entre ejecuciones'],
    ];
    texto(s, 'Objetivo', { x: 1.45, y: 1.6, w: 4, h: 0.3, fontSize: 12, color: C.text2, fontFace: MONO });
    texto(s, 'Cómo', { x: 5.6, y: 1.6, w: 3.6, h: 0.3, fontSize: 12, color: C.text2, fontFace: MONO });
    texto(s, 'Resultado', { x: 9.4, y: 1.6, w: 3.2, h: 0.3, fontSize: 12, color: C.text2, fontFace: MONO });
    objetivos.forEach(([o, como, r], i) => {
      const y = 1.98 + i * 0.78;
      tarjeta(s, 0.6, y, 12.1, 0.66, { nombre: `objetivo-${i + 1}` });
      texto(s, `${i + 1}`, { x: 0.85, y, w: 0.4, h: 0.66, fontSize: 18, bold: true, color: C.accent1, fontFace: MONO,
        valign: 'middle' });
      texto(s, o, { x: 1.45, y, w: 4.1, h: 0.66, fontSize: 16, bold: true, valign: 'middle' });
      texto(s, como, { x: 5.6, y, w: 3.7, h: 0.66, fontSize: 14, color: C.text2, valign: 'middle' });
      texto(s, r, { x: 9.4, y, w: 3.15, h: 0.66, fontSize: 14, bold: true, color: C.accent4, valign: 'middle' });
    });
    s.addNotes(nota(5));
  }

  // ================================================================ 6. pipeline
  seccion = secciones[1];
  {
    const s = nueva();
    encabezado(s, '// 02 · propuesta de pipeline', 'Una instrucción, seis etapas, salidas idénticas');
    const etapas = [
      [ic.web, 'Generación', 'Parte I', 'Scraping de Mercado Libre Perú\n15/09 y 13/09', 'E1E0D9', '0B1220'],
      [ic.entrada, 'Ingestión', 'etapa 01', 'Esquema, tipado\nclave de oferta', 'CDE2FB', '0B1220'],
      [ic.engranaje, 'Transformación', 'etapas 02–04', 'Faltantes, atípicos\nintegración, variables', '86B6EF', '0B1220'],
      [ic.base, 'Almacenamiento', 'etapa 05', 'CSV UTF-8\nSQLite, 5 tablas', '2A78D6', 'FFFFFF'],
      [ic.grafico, 'Serving', 'etapa 06', 'Consultas SQL\nanálisis e insights', '104281', 'FFFFFF'],
    ];
    etapas.forEach(([img, t, e, d, fondo, tinta], i) => {
      const x = 0.6 + i * 2.48;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.75, w: 2.2, h: 2.75, rectRadius: 0.12,
        fill: { color: fondo }, line: { type: 'none' }, objectName: `etapa-${i}` });
      s.addImage({ data: img, x: x + 0.2, y: 1.95, w: 0.5, h: 0.5 });
      texto(s, t, { x: x + 0.2, y: 2.55, w: 1.95, h: 0.45, fontSize: 15, bold: true, color: tinta,
        fontFace: TEMA.headFontFace });
      texto(s, e, { x: x + 0.2, y: 2.98, w: 1.9, h: 0.32, fontSize: 12, color: tinta, fontFace: MONO });
      texto(s, d, { x: x + 0.2, y: 3.4, w: 1.9, h: 0.9, fontSize: 13, color: tinta });
      if (i < etapas.length - 1) {
        s.addShape(pres.shapes.CHEVRON, { x: x + 2.24, y: 2.98, w: 0.2, h: 0.3,
          fill: { color: 'B4B2A9' }, line: { type: 'none' } });
      }
    });
    tarjeta(s, 0.6, 4.8, 5.6, 1.85, { fill: '0B1220', nombre: 'comando' });
    s.addImage({ data: ic.terminal, x: 0.85, y: 5.0, w: 0.4, h: 0.4 });
    texto(s, '$ python pipeline.py', { x: 1.4, y: 5.0, w: 4.6, h: 0.4, fontSize: 18, color: 'FFFFFF', fontFace: MONO,
      valign: 'middle' });
    texto(s, 'Ejecuta los notebooks 01 a 05 en orden, carga SQLite y escribe el manifiesto. Se detiene en la primera '
      + 'etapa que viola un invariante.', { x: 0.85, y: 5.55, w: 5.15, h: 1.0, fontSize: 13, color: 'C9D3E0' });
    const transversales = [
      [ic.escudo, 'Calidad', 'assert por etapa: identificador único, rangos, nulos'],
      [ic.balanza, 'Balance', 'entrada = salida + excluidos en cada etapa'],
      [ic.huella, 'Trazabilidad', 'cada registro excluido en data/evidencia/ con su motivo'],
      [ic.hash, 'Reproducibilidad', 'semilla fija y SHA-256 de cada CSV final'],
    ];
    transversales.forEach(([img, t, d], i) => {
      const x = 6.5 + (i % 2) * 3.15;
      const y = 4.8 + Math.floor(i / 2) * 0.95;
      s.addImage({ data: img, x, y: y + 0.05, w: 0.38, h: 0.38 });
      texto(s, t, { x: x + 0.5, y, w: 2.55, h: 0.35, fontSize: 15, bold: true });
      texto(s, d, { x: x + 0.5, y: y + 0.36, w: 2.55, h: 0.55, fontSize: 12, color: C.text2 });
    });
    s.addNotes(nota(6));
  }

  // ================================================================ 7. ingesta
  {
    const s = nueva();
    encabezado(s, '// 02 · ingestión y limpieza', `De ${miles(M.ingesta.filas_crudo_ho)} registros a ${miles(M.dataset_final.filas)} ofertas válidas`);
    s.addChart(pres.charts.BAR, [{ name: 'Registros', labels: ['Registros crudos', 'Ofertas únicas', 'Unidades del componente',
      'Dataset final'], values: [M.ingesta.filas_crudo_ho, unicasOferta, lim.ofertas_unicas, M.dataset_final.filas] }], {
      x: 0.6, y: 1.7, w: 6.4, h: 3.6, barDir: 'bar', catAxisOrientation: 'maxMin', chartColors: ['2A78D6'],
      showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0', valAxisHidden: true, barGapWidthPct: 45,
      showTitle: true, title: 'Registros que sobreviven a cada paso', titleFontFace: '+mj-lt', titleFontSize: 14,
      titleColor: '0B1220', ...ejes({ valGridLine: { style: 'none' } }),
    });
    const pasos = [
      [`−${lim.duplicados}`, 'repeticiones', 'Deduplicación por oferta (wid); se conserva la observación más reciente.'],
      [`−${ajenas}`, 'ajenas', `${lim.ajenas.accesorio} accesorios, ${lim.ajenas['combo de varios componentes']} kits de teclado y mouse, ${lim.ajenas['otro producto']} otros productos.`],
      [`−${at.excluidos_por_error}`, 'error', 'Laptop de 8 GB a S/ 29 000: el título contradice el precio.'],
    ];
    pasos.forEach(([n, t, d], i) => {
      const y = 5.45 + i * 0.47;
      texto(s, n, { x: 0.6, y, w: 0.85, h: 0.4, fontSize: 15, bold: true, color: C.accent6, fontFace: MONO });
      texto(s, [{ text: `${t}: `, options: { bold: true } }, { text: d }], { x: 1.5, y, w: 5.5, h: 0.42, fontSize: 13 });
    });
    const decisiones = [
      ['Tipado con expresiones regulares ancladas', `"S/ 2.199", "18 cuotas de S/ 122,17", "4.8 | +100 vendidos". `
        + `Lo que no encaja no se adivina: ${lim.textos_no_interpretables} textos no interpretables.`],
      ['Corrección de la Parte I', '"+100 vendidos" son unidades vendidas, no opiniones: la columna pasó de 100 % vacía '
        + 'a útil como cota inferior.'],
      ['Reglas revisadas a mano', 'Buscar palabras sueltas falla ("switch" está en teclados mecánicos). Se exige que el '
        + `título empiece con el accesorio; ${lim.reasignadas} publicaciones se reasignaron de componente.`],
    ];
    decisiones.forEach(([t, d], i) => {
      const y = 1.75 + i * 1.68;
      tarjeta(s, 7.4, y, 5.3, 1.5, { nombre: `decision-${i + 1}` });
      texto(s, t, { x: 7.65, y: y + 0.18, w: 4.85, h: 0.4, fontSize: 15, bold: true });
      texto(s, d, { x: 7.65, y: y + 0.6, w: 4.85, h: 0.85, fontSize: 13, color: C.text2 });
    });
    s.addNotes(nota(7));
  }

  // ================================================================ 8. faltantes
  seccion = secciones[2];
  {
    const s = nueva();
    encabezado(s, '// 03 · valores faltantes', 'Ningún faltante es aleatorio: se trata según su tipo');
    s.addImage({ path: path.join(FIGURAS, 'f02_faltantes_por_componente.png'), x: 0.6, y: 1.65, w: 6.6, h: 4.55,
      sizing: { type: 'contain', w: 6.6, h: 4.55 }, altText: 'Mapa de calor del porcentaje de faltantes por componente' });
    texto(s, 'Prueba chi-cuadrado: ¿faltar depende del componente o de la página? En las seis columnas, p < 0,001.',
      { x: 0.6, y: 6.3, w: 6.6, h: 0.55, fontSize: 12, color: C.text2 });
    const d = M.faltantes.diagnostico;
    const tipos = [
      ['MNAR estructural', 'No existe: sin promoción o sin cuotas.',
        `precio_anterior ${num(d.precio_anterior.pct)} % · numero_cuotas ${num(d.numero_cuotas.pct)} %`,
        'Descuento 0 % + indicador; cuotas "no aplica".'],
      ['MAR', 'Depende del precio: los caros tienen menos reseñas.',
        `calificacion ${num(d.calificacion.pct)} % · vendidos ${num(d.vendidos_min.pct)} %`,
        'Sin imputar: indicador tiene_resenas.'],
      ['MAR categórico', 'La tarjeta no muestra la tienda o el envío.',
        `vendedor ${num(d.vendedor.pct)} % · envio ${num(d.envio.pct)} %`,
        'Categoría explícita "no informado".'],
    ];
    tipos.forEach(([t, porque, cols, trat], i) => {
      const y = 1.7 + i * 1.72;
      tarjeta(s, 7.5, y, 5.2, 1.58, { nombre: `faltante-${i + 1}` });
      texto(s, t, { x: 7.72, y: y + 0.12, w: 4.8, h: 0.35, fontSize: 15, bold: true, color: C.accent4 });
      texto(s, porque, { x: 7.72, y: y + 0.47, w: 4.8, h: 0.35, fontSize: 12, color: C.text2 });
      texto(s, cols, { x: 7.72, y: y + 0.8, w: 4.8, h: 0.3, fontSize: 11, fontFace: MONO, color: C.text1 });
      texto(s, trat, { x: 7.72, y: y + 1.1, w: 4.8, h: 0.4, fontSize: 12, bold: true });
    });
    s.addNotes(nota(8));
  }

  // ================================================================ 9. atípicos
  {
    const s = nueva();
    encabezado(s, '// 03 · valores atípicos', 'Atípicos: casi todos son productos reales');
    s.addImage({ path: path.join(FIGURAS, 'f02_atipicos_univariados.png'), x: 0.6, y: 1.65, w: 7.3, h: 4.9,
      sizing: { type: 'contain', w: 7.3, h: 4.9 }, altText: 'Diagrama de caja del precio por componente con atípicos' });
    const tarjetas = [
      [`${at.univariados}`, 'univariados', 'IQR × 1,5 y |z| > 3 sobre el log-precio, por componente', C.background2, C.text1],
      [`${at.kmeans}`, 'multivariados', `K-Means sobre precio, descuento y posición; Mahalanobis coincide en ${at.coinciden}`, C.background2, C.text1],
      [`${at.excluidos_por_error}`, 'excluido', 'Solo se elimina un error comprobable: laptop de 8 GB a S/ 29 000', C.accent4, C.background1],
    ];
    tarjetas.forEach(([n, t, d, fondo, tinta], i) => {
      const y = 1.7 + i * 1.45;
      tarjeta(s, 8.3, y, 4.4, 1.32, { fill: fondo, nombre: `atipico-${i + 1}` });
      texto(s, n, { x: 8.55, y: y + 0.08, w: 1.3, h: 0.7, fontSize: 36, bold: true, color: tinta,
        fontFace: TEMA.headFontFace });
      texto(s, t, { x: 9.85, y: y + 0.25, w: 2.7, h: 0.4, fontSize: 16, bold: true, color: tinta });
      texto(s, d, { x: 8.55, y: y + 0.76, w: 4.0, h: 0.52, fontSize: 12, color: tinta });
    });
    texto(s, `Se conservan ${at.conservados_marcados} extremos plausibles (sillas Steelcase, audífonos premium) marcados en atipico_precio: las medianas y la escala logarítmica los absorben.`,
      { x: 8.3, y: 6.1, w: 4.4, h: 0.7, fontSize: 11, color: C.text2 });
    s.addNotes(nota(9));
  }

  // ================================================================ 10. integración
  {
    const s = nueva();
    encabezado(s, '// 03 · integración y reducción', 'La clave correcta triplica las ofertas integrables');
    s.addChart(pres.charts.BAR, [{ name: 'Ofertas comunes', labels: ['Por código de catálogo (Parte I)', 'Por oferta (wid)'],
      values: [integ.comunes_por_catalogo, integ.comunes_por_oferta] }], {
      x: 0.6, y: 1.7, w: 6.6, h: 3.0, barDir: 'bar', catAxisOrientation: 'maxMin', chartColors: ['104281'],
      showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '0', valAxisHidden: true, barGapWidthPct: 55,
      showTitle: true, title: 'Ofertas presentes en ambas capturas', titleFontFace: '+mj-lt', titleFontSize: 14,
      titleColor: '0B1220', ...ejes({ valGridLine: { style: 'none' } }),
    });
    tarjeta(s, 0.6, 4.95, 3.15, 1.7, { nombre: 'estables' });
    texto(s, `${num(integ.sin_cambio_pct, 0)} %`, { x: 0.85, y: 5.05, w: 2.7, h: 0.75, fontSize: 36, bold: true,
      fontFace: TEMA.headFontFace, color: C.accent4 });
    texto(s, 'mantuvo el mismo precio en dos días', { x: 0.85, y: 5.85, w: 2.7, h: 0.7, fontSize: 13, color: C.text2 });
    tarjeta(s, 4.05, 4.95, 3.15, 1.7, { nombre: 'variacion' });
    texto(s, `+${num(integ.variacion_mediana_cambiaron)} %`, { x: 4.3, y: 5.05, w: 2.7, h: 0.75, fontSize: 36,
      bold: true, fontFace: TEMA.headFontFace, color: C.accent4 });
    texto(s, `variación mediana de las que cambiaron (${integ.subieron} suben, ${integ.bajaron} bajan)`,
      { x: 4.3, y: 5.85, w: 2.7, h: 0.7, fontSize: 13, color: C.text2 });
    const puntos = [
      ['Dirección: agregar atributos', 'A cada oferta del home office se le añade su precio del 13/09. Las ofertas que '
        + 'solo están en categorías no tienen descuento ni reseñas: no se agregan como filas.'],
      ['Identificación de entidades', 'La misma oferta aparecía con dos códigos de catálogo en 43 casos; la clave wid '
        + 'la unifica.'],
      ['Reducción', 'busqueda y componente repiten información (V de Cramér 0,995): se retira busqueda. Se elimina '
        + 'etiqueta_texto, vacía en toda la captura.'],
    ];
    puntos.forEach(([t, d], i) => {
      const y = 1.75 + i * 1.65;
      s.addImage({ data: ic.check, x: 7.6, y: y + 0.05, w: 0.38, h: 0.38 });
      texto(s, t, { x: 8.15, y, w: 4.55, h: 0.4, fontSize: 16, bold: true });
      texto(s, d, { x: 8.15, y: y + 0.45, w: 4.55, h: 1.1, fontSize: 13, color: C.text2 });
    });
    s.addNotes(nota(10));
  }

  // ================================================================ 11. variables
  seccion = secciones[3];
  {
    const s = nueva();
    encabezado(s, '// 04 · feature engineering', `${car.variables_derivadas} variables derivadas para explicar el precio`);
    const transformaciones = [
      ['log10(precio)', 'corrige la cola derecha'], ['z por componente', 'compara un mouse con una laptop'],
      ['get_dummies(envio)', 'nominal a indicadores 0/1'], ['qcut(precio, 3)', 'gama económica, media, alta'],
    ];
    transformaciones.forEach(([f, d], i) => {
      const x = 0.6 + i * 3.08;
      tarjeta(s, x, 1.7, 2.9, 1.15, { fill: '0B1220', nombre: `transformacion-${i + 1}` });
      texto(s, f, { x: x + 0.2, y: 1.82, w: 2.55, h: 0.45, fontSize: 15, color: HEX.accent2, fontFace: MONO });
      texto(s, d, { x: x + 0.2, y: 2.3, w: 2.55, h: 0.45, fontSize: 13, color: 'C9D3E0' });
    });
    const cs = car.cobertura_specs;
    const familias = [
      [ic.cpu, 'Especificaciones del título', 'ram_gb · almacenamiento_gb · pulgadas · inalambrico · ergonomica',
        `Cobertura en su componente: RAM ${num(cs.ram_gb)} %, pulgadas ${num(cs.pulgadas)} %`],
      [ic.tag, 'Condiciones comerciales', 'tiene_descuento · descuento_pct · descuento_inflado · ofrece_cuotas · envio_gratis',
        `${car.descuento_inflado} de ${miles(car.con_descuento)} promociones exageran el ahorro`],
      [ic.estrella, 'Reputación y vendedor', 'vendidos_min · tiene_resenas · tienda_de_marca · es_publicidad',
        'vendidos_min es cota inferior: "+100" significa al menos 100'],
      [ic.marca, 'Marca, gama y precio', 'marca · es_gamer · gama · precio_relativo · variacion_precio_pct',
        `marca reconocida en más del 79 % de cada componente, salvo sillas`],
    ];
    familias.forEach(([img, t, vars, nota], i) => {
      const x = 0.6 + (i % 2) * 6.15;
      const y = 3.15 + Math.floor(i / 2) * 1.82;
      tarjeta(s, x, y, 5.95, 1.65, { nombre: `familia-${i + 1}` });
      s.addImage({ data: img, x: x + 0.25, y: y + 0.22, w: 0.42, h: 0.42 });
      texto(s, t, { x: x + 0.85, y: y + 0.2, w: 4.9, h: 0.42, fontSize: 16, bold: true });
      texto(s, vars, { x: x + 0.85, y: y + 0.65, w: 4.9, h: 0.5, fontSize: 11, fontFace: MONO, color: C.accent4 });
      texto(s, nota, { x: x + 0.85, y: y + 1.15, w: 4.9, h: 0.4, fontSize: 12, color: C.text2 });
    });
    s.addNotes(nota(11));
  }

  // ================================================================ 12. qcut frente a K-Means
  {
    const s = nueva();
    encabezado(s, '// 04 · discretización', '¿Por qué terciles (qcut) y no K-Means?');
    const comp = car.comparacion_qcut_kmeans;
    const etiquetas = [];
    const serie = { 'económica': [], media: [], alta: [] };
    COMPONENTES.forEach((c) => {
      [['qcut', 'terciles'], ['kmeans', 'K-Means']].forEach(([m, nombre]) => {
        etiquetas.push(`${NOMBRE[c]} · ${nombre}`);
        Object.keys(serie).forEach((g) => serie[g].push(comp[c][`${m}_${g}`]));
      });
    });
    s.addChart(pres.charts.BAR, Object.entries(serie).map(([g, v]) => ({ name: g, labels: etiquetas, values: v })), {
      x: 0.6, y: 1.6, w: 7.3, h: 5.2, barDir: 'bar', barGrouping: 'stacked', catAxisOrientation: 'maxMin',
      chartColors: COLOR_GAMA, showValue: true, dataLabelPosition: 'ctr', dataLabelColor: 'FFFFFF',
      dataLabelFontSize: 10, dataLabelFontBold: true, barGapWidthPct: 35, valAxisHidden: true,
      ...ejes({ catAxisLabelFontSize: 11, showLegend: true, legendPos: 't', valGridLine: { style: 'none' },
        dataLabelColor: 'FFFFFF', dataLabelFontSize: 10 }),
    });
    const silQ = COMPONENTES.reduce((a, c) => a + comp[c].silueta_qcut, 0) / 6;
    const silK = COMPONENTES.reduce((a, c) => a + comp[c].silueta_kmeans, 0) / 6;
    const menor = Math.min(...COMPONENTES.map((c) => comp[c].kmeans_grupo_menor));
    const tamQ = COMPONENTES.flatMap((c) => ['económica', 'media', 'alta'].map((g) => comp[c][`qcut_${g}`]));
    const [minQ, maxQ] = [Math.min(...tamQ), Math.max(...tamQ)];
    const pesos = COMPONENTES.map((c) => (comp[c].kmeans_alta * 100)
      / (comp[c]['kmeans_económica'] + comp[c].kmeans_media + comp[c].kmeans_alta));
    const pesoAlta = { min: Math.min(...pesos), max: Math.max(...pesos) };
    const razones = [
      ['Misma gama en todo componente', 'El perfil suma la mediana de la misma gama: "alta" debe ser el tercio más '
        + `caro en todos. Con K-Means pesa ${num(pesoAlta.min, 0)} % en sillas y ${num(pesoAlta.max, 0)} % en laptops.`],
      ['Medianas estables', `Terciles: ${minQ} a ${maxQ} ofertas por gama. K-Means deja grupos de ${menor} (sillas de gama alta).`],
      ['Reproducible y comunicable', 'Los cortes son percentiles: se explican a RR. HH. sin semilla ni centroides.'],
    ];
    razones.forEach(([t, d], i) => {
      const y = 1.65 + i * 1.38;
      tarjeta(s, 8.2, y, 4.5, 1.25, { nombre: `razon-${i + 1}` });
      texto(s, `${i + 1}`, { x: 8.4, y: y + 0.13, w: 0.35, h: 0.4, fontSize: 16, bold: true, color: C.accent1,
        fontFace: MONO });
      texto(s, t, { x: 8.75, y: y + 0.13, w: 3.8, h: 0.4, fontSize: 15, bold: true });
      texto(s, d, { x: 8.4, y: y + 0.55, w: 4.15, h: 0.68, fontSize: 12, color: C.text2 });
    });
    tarjeta(s, 8.2, 5.82, 4.5, 0.98, { fill: 'FFF7E6', nombre: 'silueta' });
    texto(s, [
      { text: 'Honestidad metodológica  ', options: { bold: true, color: 'B45309' } },
      { text: `K-Means separa mejor (silueta ${num(silK, 2)} frente a ${num(silQ, 2)}): optimiza eso. Se conserva como contraste.` },
    ], { x: 8.4, y: 5.9, w: 4.15, h: 0.85, fontSize: 12, valign: 'middle' });
    s.addNotes(nota(12));
  }

  // ================================================================ 13. validación de gamas
  {
    const s = nueva();
    encabezado(s, '// 04 · validación de gamas', 'Las gamas separan equipos distintos, no solo precios');
    const val = car.validacion_gamas;
    const gamas = ['económica', 'media', 'alta'];
    const mini = [
      ['Laptop: RAM mediana (GB)', 'laptop: RAM mediana (GB)', '0'],
      ['Monitor: pulgadas medianas', 'monitor: pulgadas medianas', '0'],
      ['Silla: % ergonómicas', 'silla: % ergonómicas', '0"%"'],
    ];
    mini.forEach(([titulo, clave, formato], i) => {
      const x = 0.6 + i * 4.1;
      s.addChart(pres.charts.BAR, [{ name: titulo, labels: gamas, values: gamas.map((g) => val[g][clave]) }], {
        x, y: 1.7, w: 3.85, h: 3.6, barDir: 'col', chartColors: ['2A78D6'], showValue: true,
        dataLabelPosition: 'outEnd', dataLabelFormatCode: formato, valAxisHidden: true, barGapWidthPct: 60,
        showTitle: true, title: titulo, titleFontFace: '+mj-lt', titleFontSize: 14, titleColor: '0B1220',
        ...ejes({ valGridLine: { style: 'none' } }),
      });
    });
    tarjeta(s, 0.6, 5.55, 12.1, 1.2, { nombre: 'lectura-validacion' });
    s.addImage({ data: ic.alerta, x: 0.85, y: 5.8, w: 0.42, h: 0.42 });
    const inal = gamas.map((g) => val[g]['periféricos: % inalámbricos']);
    texto(s, [
      { text: 'Lectura: ', options: { bold: true } },
      { text: 'la RAM distingue la gama alta de laptops; el tamaño, la económica de monitores; las sillas ergonómicas '
        + `suben de ${num(val['económica']['silla: % ergonómicas'], 0)} % a ${num(val.alta['silla: % ergonómicas'], 0)} %. `
        + `Lo inalámbrico no cambia entre gamas (${num(Math.min(...inal), 0)}–${num(Math.max(...inal), 0)} %): no es lo que encarece un periférico.` },
    ], { x: 1.45, y: 5.65, w: 11.05, h: 1.0, fontSize: 14, valign: 'middle' });
    s.addNotes(nota(13));
  }

  // ================================================================ 14. costo por perfil
  seccion = secciones[4];
  {
    const s = nueva();
    encabezado(s, '// 05 · resultado principal', `Un home office cuesta de ${soles(perf['económico'].costo_mediano)} a ${soles(perf.alto.costo_mediano)}`);
    const perfiles = [['económico', 'Perfil económico', C.background2, C.text1],
      ['medio', 'Perfil medio', C.accent1, C.background1], ['alto', 'Perfil alto', C.accent4, C.background1]];
    perfiles.forEach(([k, t, fondo, tinta], i) => {
      const x = 0.6 + i * 4.1;
      tarjeta(s, x, 1.7, 3.9, 1.9, { fill: fondo, nombre: `perfil-${k}` });
      texto(s, t, { x: x + 0.3, y: 1.85, w: 3.3, h: 0.35, fontSize: 14, color: tinta });
      texto(s, soles(perf[k].costo_mediano), { x: x + 0.3, y: 2.2, w: 3.3, h: 0.85, fontSize: 40, bold: true,
        color: tinta, fontFace: TEMA.headFontFace });
      texto(s, `rango ${soles(perf[k].costo_q1)} – ${soles(perf[k].costo_q3)}`, { x: x + 0.3, y: 3.1, w: 3.3,
        h: 0.35, fontSize: 12, color: tinta, fontFace: MONO });
    });
    const pg = an.precios_por_gama;
    const filas = { 'económico': 'económica', medio: 'media', alto: 'alta' };
    const composicion = COMPONENTES.map((c) => ({ name: NOMBRE[c], labels: ['Económico', 'Medio', 'Alto'],
      values: Object.entries(filas).map(([p, g]) => (pg[c][g] / perf[p].costo_mediano) * 100) }));
    s.addChart(pres.charts.BAR, composicion, {
      x: 0.6, y: 3.85, w: 8.4, h: 2.95, barDir: 'bar', barGrouping: 'percentStacked', catAxisOrientation: 'maxMin',
      chartColors: COMPONENTES.map((c) => COLOR_COMPONENTE[c]), barGapWidthPct: 40, valAxisHidden: true,
      showTitle: true, title: 'Participación de cada componente en el costo', titleFontFace: '+mj-lt',
      titleFontSize: 14, titleColor: '0B1220',
      ...ejes({ showLegend: true, legendPos: 'b', valGridLine: { style: 'none' } }),
    });
    const lap = an.composicion_laptop_pct;
    tarjeta(s, 9.3, 3.85, 3.4, 2.95, { fill: '0B1220', nombre: 'laptop-peso' });
    texto(s, `${num(lap.alto, 0)}–${num(lap['económico'], 0)} %`, { x: 9.55, y: 4.05, w: 3.0, h: 0.85, fontSize: 36,
      bold: true, color: HEX.accent2, fontFace: TEMA.headFontFace });
    texto(s, 'del costo de cada perfil es la laptop. Teclado, mouse y audífonos juntos no llegan al 11 %.',
      { x: 9.55, y: 4.95, w: 3.0, h: 1.6, fontSize: 14, color: 'FFFFFF' });
    s.addNotes(nota(14));
  }

  // ================================================================ 15. laptop
  {
    const s = nueva();
    encabezado(s, '// 05 · laptop', 'La RAM marca escalones de precio claros');
    const ram = an.laptop_por_ram;
    s.addChart(pres.charts.BAR, [{ name: 'Precio mediano', labels: ['8 GB', '16 GB', '32 GB'],
      values: [ram['8.0'], ram['16.0'], ram['32.0']] }], {
      x: 0.6, y: 1.7, w: 6.2, h: 5.0, barDir: 'col', chartColors: ['2A78D6'], showValue: true,
      dataLabelPosition: 'outEnd', dataLabelFormatCode: '"S/ "0', valAxisHidden: true, barGapWidthPct: 55,
      showTitle: true, title: 'Laptop: precio mediano por memoria RAM', titleFontFace: '+mj-lt', titleFontSize: 14,
      titleColor: '0B1220', ...ejes({ valGridLine: { style: 'none' }, catAxisLabelFontSize: 14 }),
    });
    s.addImage({ path: path.join(IMAGENES, 'analitica.jpg'), x: 7.2, y: 1.7, w: 5.5, h: 2.55,
      sizing: { type: 'cover', w: 5.5, h: 2.55 }, altText: 'Laptop con un panel de analítica' });
    const marcas = an.laptop_por_marca;
    const orden = Object.entries(marcas).sort((a, b) => a[1] - b[1]);
    const grafia = (m) => (['hp', 'msi'].includes(m) ? m.toUpperCase() : m[0].toUpperCase() + m.slice(1));
    tarjeta(s, 7.2, 4.5, 2.65, 2.2, { nombre: 'ram-16' });
    texto(s, `+${num((ram['16.0'] / ram['8.0'] - 1) * 100, 0)} %`, { x: 7.4, y: 4.65, w: 2.3, h: 0.75, fontSize: 32,
      bold: true, fontFace: TEMA.headFontFace, color: C.accent4 });
    texto(s, 'de 8 a 16 GB. 16 GB es la configuración más ofrecida y basta para oficina.', { x: 7.4, y: 5.4, w: 2.3,
      h: 1.25, fontSize: 12, color: C.text2 });
    tarjeta(s, 10.05, 4.5, 2.65, 2.2, { nombre: 'marcas' });
    texto(s, `${soles(orden[0][1])} a ${soles(orden[orden.length - 1][1])}`, { x: 10.25, y: 4.65, w: 2.3, h: 0.75,
      fontSize: 18, bold: true, fontFace: TEMA.headFontFace, color: C.accent4, valign: 'middle' });
    texto(s, `mediana por marca, de ${grafia(orden[0][0])} a ${grafia(orden[orden.length - 1][0])} (marcas con 10 o más laptops).`,
      { x: 10.25, y: 5.4, w: 2.3, h: 1.25, fontSize: 12, color: C.text2 });
    s.addNotes(nota(15));
  }

  // ================================================================ 16. promociones
  {
    const s = nueva();
    encabezado(s, '// 05 · promociones · Mann-Whitney', 'Un descuento no es un buen precio');
    const pc = an.promo_por_componente;
    const etiquetaP = (c) => `${NOMBRE[c]} (${pc[c]['p (Mann-Whitney)'] < 0.05 ? formatoP(pc[c]['p (Mann-Whitney)']) : 'n. s.'})`;
    s.addChart(pres.charts.BAR, [{ name: 'Diferencia', labels: COMPONENTES.map(etiquetaP),
      values: COMPONENTES.map((c) => (pc[c]['con promoción'] / pc[c]['sin promoción'] - 1) * 100) }], {
      x: 0.6, y: 1.7, w: 7.0, h: 4.4, barDir: 'bar', catAxisOrientation: 'maxMin', chartColors: ['E34948'],
      invertedColors: ['1BAF7A'], catAxisLabelPos: 'low', showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '+0"%";-0"%";0"%"',
      barGapWidthPct: 45, valAxisHidden: true, showTitle: true,
      title: 'Precio mediano con promoción frente a sin promoción', titleFontFace: '+mj-lt', titleFontSize: 14,
      titleColor: '0B1220', ...ejes({ valGridLine: { style: 'none' }, catAxisLabelFontSize: 12 }),
    });
    texto(s, 'Rojo: más caras con promoción · verde: más baratas · n. s.: diferencia no significativa (p ≥ 0,05)',
      { x: 0.6, y: 6.2, w: 7.0, h: 0.5, fontSize: 11, color: C.text2 });
    tarjeta(s, 7.95, 1.7, 4.75, 2.45, { fill: '0B1220', nombre: 'mann-whitney' });
    texto(s, 'Mann-Whitney U, todas las ofertas', { x: 8.2, y: 1.85, w: 4.3, h: 0.35, fontSize: 12, color: HEX.accent2,
      fontFace: MONO });
    texto(s, [
      { text: `${num(an.promo_mediana_con, 2)} vs ${num(an.promo_mediana_sin, 2)}`, options: { breakLine: true } },
    ], { x: 8.2, y: 2.2, w: 4.3, h: 0.7, fontSize: 30, bold: true, color: 'FFFFFF', fontFace: TEMA.headFontFace });
    texto(s, `precio relativo mediano con y sin promoción; ${formatoP(an.promo_p)}. Las ofertas con descuento son algo más caras.`,
      { x: 8.2, y: 2.95, w: 4.3, h: 1.1, fontSize: 13, color: 'C9D3E0' });
    tarjeta(s, 7.95, 4.35, 4.75, 2.35, { nombre: 'cuotas' });
    texto(s, `${num(an.cuotas_pct, 0)} %`, { x: 8.2, y: 4.5, w: 2.0, h: 0.8, fontSize: 36, bold: true,
      color: C.accent4, fontFace: TEMA.headFontFace });
    texto(s, 'ofrece cuotas, todas sin interés', { x: 10.2, y: 4.6, w: 2.35, h: 0.7, fontSize: 13, color: C.text2,
      valign: 'middle' });
    texto(s, `Perfil medio en 12 cuotas: ${soles(an.cuota_mensual.medio['12 cuotas'])} al mes. Financiar no encarece; solo reparte el gasto.`,
      { x: 8.2, y: 5.45, w: 4.3, h: 1.1, fontSize: 13 });
    s.addNotes(nota(16));
  }

  // ================================================================ 17. gamer y reputación
  {
    const s = nueva();
    encabezado(s, '// 05 · gamer y reputación · Spearman', 'Lo "gamer" y lo más vendido no son lo que parecen');
    const dg = an.gamer_diferencia;
    const gp = an.gamer_p;
    s.addChart(pres.charts.BAR, [{ name: 'Gamer', labels: COMPONENTES.map((c) => `${NOMBRE[c]} (${gp[c] < 0.05 ? formatoP(gp[c]) : 'n. s.'})`),
      values: COMPONENTES.map((c) => dg[c]) }], {
      x: 0.6, y: 1.7, w: 7.0, h: 4.4, barDir: 'bar', catAxisOrientation: 'maxMin', chartColors: ['EB6834'],
      invertedColors: ['86B6EF'], catAxisLabelPos: 'low', showValue: true, dataLabelPosition: 'outEnd', dataLabelFormatCode: '+0.00;-0.00;0',
      barGapWidthPct: 45, valAxisHidden: true, showTitle: true,
      title: 'Gamer frente al resto: diferencia de precio relativo (z)', titleFontFace: '+mj-lt', titleFontSize: 14,
      titleColor: '0B1220', ...ejes({ valGridLine: { style: 'none' }, catAxisLabelFontSize: 12 }),
    });
    texto(s, 'Mann-Whitney por componente. Solo laptop y mouse gamer cuestan más de forma significativa.',
      { x: 0.6, y: 6.2, w: 7.0, h: 0.5, fontSize: 11, color: C.text2 });
    const sv = an.spearman_vendidos;
    const sc = an.spearman_calificacion;
    const rhos = [
      [`ρ = ${num(sv.rho, 2)}`, 'ventas frente a precio', `${formatoP(sv.p)}. Débil, pero las ofertas con +1000 vendidos están 0,49 desviaciones por debajo de su componente.`],
      [`ρ = ${num(sc.rho, 2)}`, 'calificación frente a precio', `${formatoP(sc.p)}. Lo mejor calificado es más caro: lo más vendido no es lo mejor valorado.`],
    ];
    rhos.forEach(([r, t, d], i) => {
      const y = 1.7 + i * 2.1;
      tarjeta(s, 7.95, y, 4.75, 1.9, { nombre: `spearman-${i + 1}` });
      texto(s, r, { x: 8.2, y: y + 0.15, w: 2.5, h: 0.7, fontSize: 30, bold: true, color: C.accent4,
        fontFace: TEMA.headFontFace });
      texto(s, t, { x: 10.6, y: y + 0.2, w: 2.0, h: 0.6, fontSize: 12, color: C.text2, valign: 'middle' });
      texto(s, d, { x: 8.2, y: y + 0.9, w: 4.3, h: 0.95, fontSize: 12 });
    });
    texto(s, `Solo el ${num(100 - M.faltantes.diagnostico.calificacion.pct, 0)} % de las ofertas muestra reseñas y faltan más en las caras: la reputación describe sobre todo a los productos baratos.`,
      { x: 7.95, y: 5.95, w: 4.75, h: 0.75, fontSize: 11, color: C.text2 });
    s.addNotes(nota(17));
  }

  // ================================================================ 18. recomendaciones
  {
    const s = nueva();
    encabezado(s, '// 05 · insights', 'Recomendaciones para empleadores y trabajadores');
    const ins = M.insights.lista;
    const tarjetas = [
      [ic.rrhh, 'RR. HH. o empleador', 'Compensar por perfil, no con una cifra',
        `${soles(perf['económico'].costo_mediano)} / ${soles(perf.medio.costo_mediano)} / ${soles(perf.alto.costo_mediano)}, con la fecha de los precios.`],
      [ic.persona, 'Trabajador', 'Decidir primero la laptop', '16 GB de RAM basta para oficina; no buscar ahorro en periféricos.'],
      [ic.persona, 'Trabajador', 'Comparar el precio final', 'El % de descuento no indica un buen precio.'],
      [ic.persona, 'Trabajador', 'Financiar sin miedo', `12 cuotas sin interés: ${soles(an.cuota_mensual.medio['12 cuotas'])} al mes en el perfil medio.`],
      [ic.persona, 'Trabajador', 'Evitar lo gamer en mouse y laptop', 'Se paga por prestaciones que la oficina no usa.'],
      [ic.persona, 'Quien compra una silla', 'Sumar el envío', `Solo el ${num(an.silla_envio_gratis_pct, 0)} % de las sillas tiene envío gratis (más de 90 % en el resto).`],
    ];
    tarjetas.forEach(([img, quien, t, d], i) => {
      const x = 0.6 + (i % 3) * 4.1;
      const y = 1.7 + Math.floor(i / 3) * 2.55;
      tarjeta(s, x, y, 3.9, 2.35, { fill: i === 0 ? 'E6F0FB' : C.background2, nombre: `insight-${i + 1}` });
      s.addImage({ data: img, x: x + 0.25, y: y + 0.22, w: 0.36, h: 0.36 });
      texto(s, quien, { x: x + 0.72, y: y + 0.22, w: 3.0, h: 0.36, fontSize: 12, color: C.accent4, bold: true,
        valign: 'middle' });
      texto(s, t, { x: x + 0.25, y: y + 0.72, w: 3.45, h: 0.75, fontSize: 17, bold: true,
        fontFace: TEMA.headFontFace });
      texto(s, d, { x: x + 0.25, y: y + 1.45, w: 3.45, h: 0.8, fontSize: 13, color: C.text2 });
    });
    s.addNotes(nota(18));
  }

  // ================================================================ 19. demo
  seccion = secciones[5];
  {
    const s = nueva();
    encabezado(s, '// 06 · demo en vivo', 'Demo: el pipeline completo en unos 20 segundos');
    s.addImage({ path: path.join(IMAGENES, 'codigo.jpg'), x: 0.6, y: 1.7, w: 4.6, h: 5.0,
      sizing: { type: 'cover', w: 4.6, h: 5.0 }, altText: 'Teclado de laptop con código en pantalla' });
    const pasos = [
      ['$ python pipeline.py', 'Seis etapas en orden; cada una imprime OK y su tiempo. Si un assert falla, se detiene y nombra el invariante.'],
      ['05_analisis_y_visualizacion.ipynb', 'Consulta SQL al almacén: SELECT componente, gama, mediana FROM precios_por_gama.'],
      ['data/final/manifiesto.json', 'Mismo SHA-256 de cada CSV final antes y después: la ejecución es reproducible.'],
    ];
    pasos.forEach(([cmd, d], i) => {
      const y = 1.7 + i * 1.45;
      tarjeta(s, 5.5, y, 7.2, 1.3, { fill: '0B1220', nombre: `paso-demo-${i + 1}` });
      texto(s, `${i + 1}`, { x: 5.75, y: y + 0.15, w: 0.4, h: 0.45, fontSize: 18, bold: true, color: HEX.accent3,
        fontFace: MONO });
      texto(s, cmd, { x: 6.2, y: y + 0.15, w: 6.3, h: 0.45, fontSize: 15, color: HEX.accent2, fontFace: MONO });
      texto(s, d, { x: 6.2, y: y + 0.62, w: 6.3, h: 0.6, fontSize: 13, color: 'E2E8F0' });
    });
    tarjeta(s, 5.5, 6.05, 7.2, 0.65, { fill: 'FFF7E6', nombre: 'plan-b' });
    texto(s, [{ text: 'Plan B: ', options: { bold: true, color: 'B45309' } },
      { text: 'si falla la conexión, se muestran los notebooks con sus salidas guardadas en GitHub.' }],
    { x: 5.75, y: 6.05, w: 6.8, h: 0.65, fontSize: 13, valign: 'middle' });
    s.addNotes(nota(19));
  }

  // ================================================================ 20. conclusiones
  {
    const s = nueva('OSCURO');
    s.addImage({ path: path.join(IMAGENES, 'escritorio_oscuro.jpg'), x: 9.0, y: 0, w: 4.333, h: 7.5,
      sizing: { type: 'cover', w: 4.333, h: 7.5 }, altText: 'Escritorio oscuro con laptop y monitor' });
    s.addText('// conclusiones y limitaciones', { placeholder: 'etiqueta' });
    s.addText('Una referencia por perfil, fechada y reproducible', { placeholder: 'title' });
    const conclusiones = [
      `Equipar un home office cuesta ${soles(perf['económico'].costo_mediano)}, ${soles(perf.medio.costo_mediano)} o ${soles(perf.alto.costo_mediano)} según el perfil; la laptop es dos tercios o más.`,
      'Preprocesar con justificación cambió el resultado: clave de oferta, ajenas fuera, faltantes sin imputar.',
      'Descuento y etiqueta gamer no son señales de buen precio; las cuotas sin interés no encarecen.',
    ];
    texto(s, conclusiones.map((t, i) => ({ text: t, options: { bullet: { code: '25B8' }, breakLine: i < conclusiones.length - 1,
      paraSpaceAfter: 8 } })), { x: 0.6, y: 3.15, w: 7.9, h: 2.0, fontSize: 15, color: 'FFFFFF' });
    tarjeta(s, 0.6, 5.3, 7.9, 1.55, { fill: '1B2A41', nombre: 'limitaciones' });
    texto(s, 'Limitaciones', { x: 0.85, y: 5.4, w: 7.4, h: 0.35, fontSize: 13, bold: true, color: HEX.accent3,
      fontFace: MONO });
    texto(s, 'Dos capturas de un día, sin serie histórica · resultados ordenados por el sitio, no muestra aleatoria · '
      + 'reseñas en solo un tercio de las ofertas · especificaciones extraídas del título · precios publicados, sin envío.',
    { x: 0.85, y: 5.78, w: 7.4, h: 1.0, fontSize: 12, color: 'C9D3E0' });
    s.addNotes(nota(20));
  }

  // ================================================================ anexo
  seccion = secciones[6];
  {
    const s = nueva();
    encabezado(s, '// anexo · para la ronda de preguntas', 'Pruebas estadísticas: qué responden y por qué');
    const enc = (t) => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: '0B1220' }, fontSize: 13 } });
    const fila = (arr) => arr.map((t, i) => ({ text: t, options: { fontSize: 12, bold: i === 0,
      fontFace: i === 3 ? MONO : undefined } }));
    s.addTable([
      [enc('Prueba'), enc('H0 (hipótesis nula)'), enc('Por qué esta y no otra'), enc('Resultado clave')],
      fila(['Chi-cuadrado de independencia', 'Faltar es independiente del componente (o de la página)',
        'Compara frecuencias observadas y esperadas en una tabla de contingencia: dos variables categóricas',
        'p < 0,001 en las 6 columnas → ninguna MCAR']),
      fila(['Mann-Whitney U', 'Los dos grupos tienen la misma distribución de precios',
        'Usa rangos: no supone normalidad ni la mueven los extremos. Alternativa no paramétrica a la t de Student',
        `promoción ${formatoP(an.promo_p)}; gamer: laptop y mouse`]),
      fila(['Correlación de Spearman', 'No hay relación monótona entre las variables (ρ = 0)',
        'Correlación de rangos: capta relaciones monótonas no lineales; Pearson exige linealidad y se distorsiona con colas',
        `vendidos ρ = ${num(an.spearman_vendidos.rho, 2)}; calificación ρ = ${num(an.spearman_calificacion.rho, 2)}`]),
      fila(['Nivel de significancia', 'α = 0,05',
        'Un p pequeño dice que la diferencia no es casual; su tamaño se lee en las medianas, no en el p', '—']),
    ], { x: 0.6, y: 1.7, w: 12.1, colW: [2.6, 3.0, 4.0, 2.5], border: { type: 'solid', pt: 0.75, color: 'D5D9E0' },
      fill: { color: 'FFFFFF' }, color: '0B1220', valign: 'middle', margin: 0.08, rowH: [0.45, 1.0, 1.0, 1.0, 0.8] });
    s.addNotes(nota(21));
  }
  {
    const s = nueva();
    encabezado(s, '// anexo · dataset final', `Dataset final: ${miles(M.dataset_final.filas)} ofertas × ${M.dataset_final.columnas} variables`);
    const enc = (t) => ({ text: t, options: { bold: true, color: 'FFFFFF', fill: { color: '0B1220' }, fontSize: 13 } });
    const filas = COMPONENTES.map((c) => [NOMBRE[c], `${lim.ofertas_por_componente[c] - (c === 'laptop' ? at.excluidos_por_error : 0)}`,
      soles(M.costos.medianas_por_componente[c]), soles(an.precios_por_gama[c]['económica']), soles(an.precios_por_gama[c].alta)]
      .map((t) => ({ text: t, options: { fontSize: 13 } })));
    s.addTable([[enc('Componente'), enc('Ofertas'), enc('Mediana'), enc('Mediana económica'), enc('Mediana alta')], ...filas],
      { x: 0.6, y: 1.7, w: 7.4, colW: [1.7, 1.2, 1.5, 1.5, 1.5], border: { type: 'solid', pt: 0.75, color: 'D5D9E0' },
        color: '0B1220', valign: 'middle', margin: 0.08, rowH: 0.5 });
    const datos = [
      ['UTF-8 · una fila por oferta', 'data/final/homeoffice_final.csv'],
      [`${num(M.dataset_final.conservadas_pct, 2)} %`, 'de las ofertas válidas se conserva'],
      [`≤ ${num(M.dataset_final.max_nulos_no_justificado, 1)} %`, 'de nulos en toda columna no estructural'],
      ['5 tablas', 'en home_office.sqlite, con clave primaria'],
    ];
    datos.forEach(([n, d], i) => {
      const y = 1.7 + i * 1.25;
      tarjeta(s, 8.4, y, 4.3, 1.1, { nombre: `dato-${i + 1}` });
      texto(s, n, { x: 8.6, y: y + 0.12, w: 3.9, h: 0.45, fontSize: 18, bold: true, color: C.accent4,
        fontFace: TEMA.headFontFace });
      texto(s, d, { x: 8.6, y: y + 0.58, w: 3.9, h: 0.4, fontSize: 12, color: C.text2, fontFace: i === 0 ? MONO : undefined });
    });
    texto(s, 'Las columnas con más de 10 % de nulos lo son por diseño: especificaciones que solo aplican a un componente, '
      + 'precio anterior sin promoción y reseñas no mostradas. El diccionario final documenta las 41 variables.',
    { x: 0.6, y: 5.45, w: 7.4, h: 1.2, fontSize: 13, color: C.text2 });
    s.addNotes(nota(22));
  }

  await pres.writeFile({ fileName: SALIDA });
  await aplicarTema(SALIDA, TEMA);
  console.log(`${path.relative(RAIZ, SALIDA)} generado`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
