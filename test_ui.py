#!/usr/bin/env python3
import sys

print("Testing UI module import...")
try:
    from mdcx.views.MDCx import Ui_MDCx
    print("✓ UI module imported successfully")
except Exception as e:
    print(f"✗ Error importing UI module: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTesting UI initialization...")
try:
    from PyQt6.QtWidgets import QApplication, QMainWindow
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MDCx()
    ui.setupUi(window)
    print("✓ UI initialized successfully")
    print(f"  - Window size: {window.width()}x{window.height()}")
    
    # Check for vsmeta component
    if hasattr(ui, 'groupBox_vsmeta'):
        print(f"  - groupBox_vsmeta found at position: {ui.groupBox_vsmeta.geometry()}")
    else:
        print(f"  - WARNING: groupBox_vsmeta not found!")
        
    print("\nUI check passed!")
    
except Exception as e:
    print(f"✗ Error initializing UI: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
