# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\\Ryzen GamingPC\\PycharmProjects\\pythonProject\\venv\\Lib\\site-packages'],
             binaries=[],
             datas=[
                ('assets/bb_login_ex.png', 'assets'),
                ('assets/confirm.txt', 'assets'),
                ('assets/help.md', 'assets'),
                ('assets/drhphmfl.selenium_profile/*', 'assets/drhphmfl.selenium_profile'),
                ('assets/robot-head.ico', 'assets'),
                ('assets/robot-head.png', 'assets')
             ],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          [],
          exclude_binaries=True,
          name='Best Buy Scalper',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='assets/robot-head.ico',
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
