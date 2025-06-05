# -*- mode: python ; coding: utf-8 -*-

import os

project_root = os.path.abspath(SPECPATH)


block_cipher = None


a = Analysis([os.path.join(project_root, 'main.py')],
             pathex=[project_root],
             binaries=[],
             datas=[(os.path.join(project_root, 'pics', 'ptt.png'), 'pics')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='PTT',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
         console=False , icon=os.path.join(project_root, 'pics', 'ptt.ico'))
