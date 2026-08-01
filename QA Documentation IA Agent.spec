# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, copy_metadata


a = Analysis(
    ['desktop_app.py'],
    pathex=[],
    binaries=[],
    datas=(
        copy_metadata('streamlit')
        + collect_data_files('streamlit')
        + [('streamlit_app.py', '.'), ('.streamlit', '.streamlit')]
    ),
    hiddenimports=[
        'errors',
        'local_config',
        'markdown_exporter',
        'prompts',
        'qa_agent',
        'qa_foundations',
        'report_storage',
        'llm_providers.base_provider',
        'llm_providers.factory',
        'llm_providers.gemini_provider',
        'llm_providers.anthropic_provider',
        'streamlit.web.bootstrap',
        'google.genai',
        'google.genai.types',
        'anthropic',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='QA Documentation IA Agent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='QA Documentation IA Agent',
)
