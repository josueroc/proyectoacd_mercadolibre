"""Exportación de .docx y .pptx a PDF con Microsoft Office o, si no está, con LibreOffice.

Word y PowerPoint se usan por automatización COM (pywin32, solo Windows). LibreOffice se busca en el PATH
(`soffice`), en la variable de entorno SOFFICE o en su carpeta de instalación habitual de Windows.
"""
import os
import shlex
import shutil
import subprocess
from pathlib import Path

RUTAS_WINDOWS = [Path(r'C:\Program Files\LibreOffice\program\soffice.exe'),
                 Path(r'C:\Program Files (x86)\LibreOffice\program\soffice.exe')]


def comando_libreoffice():
    """Devuelve el comando de LibreOffice como lista, o None si no está instalado."""
    if os.environ.get('SOFFICE'):
        return shlex.split(os.environ['SOFFICE'])
    encontrado = shutil.which('soffice') or shutil.which('libreoffice')
    if encontrado:
        return [encontrado]
    return next(([str(r)] for r in RUTAS_WINDOWS if r.exists()), None)


def _con_office(ruta, destino):
    try:
        import win32com.client
    except ImportError:
        return False
    if ruta.suffix == '.docx':
        app = win32com.client.DispatchEx('Word.Application')
        app.Visible, app.DisplayAlerts = False, 0
        documento = None
        try:
            documento = app.Documents.Open(str(ruta.resolve()))
            documento.SaveAs2(str(destino.resolve()), FileFormat=17)
        finally:
            if documento is not None:
                documento.Close(SaveChanges=0)
            app.Quit(SaveChanges=0)
    else:
        app = win32com.client.DispatchEx('PowerPoint.Application')
        presentacion = app.Presentations.Open(str(ruta.resolve()), WithWindow=False)
        try:
            presentacion.SaveAs(str(destino.resolve()), 32)
        finally:
            presentacion.Close()
            app.Quit()
    return True


def a_pdf(ruta):
    """Convierte un .docx o .pptx a PDF en la misma carpeta. Devuelve la ruta del PDF o None."""
    ruta = Path(ruta)
    destino = ruta.with_suffix('.pdf')
    try:
        if _con_office(ruta, destino):
            return destino
    except Exception as error:  # Office instalado pero falló: se intenta con LibreOffice
        print(f'Office no pudo exportar {ruta.name} ({error}); se intenta con LibreOffice.')
    comando = comando_libreoffice()
    if comando is None:
        print(f'Sin Microsoft Office ni LibreOffice: no se exporta {ruta.name} a PDF.')
        return None
    subprocess.run(comando + ['--headless', '--convert-to', 'pdf', '--outdir', str(ruta.parent), str(ruta)],
                   check=True, capture_output=True, timeout=300)
    return destino if destino.exists() else None
