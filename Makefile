# Python for native ARM64 build (Homebrew)
PYTHON_ARM64 = python3

# Python for x86_64 build — requires a separate x86_64 Python installation.
# Install from https://www.python.org/downloads/macos/ (the "macOS 64-bit installer")
# then: arch -x86_64 /usr/local/bin/python3 -m pip install pyinstaller
PYTHON_X86   = arch -x86_64 /usr/local/bin/python3

APP = maraton

.PHONY: all arm64 x86 clean

all: arm64 x86

arm64:
	$(PYTHON_ARM64) -m PyInstaller --windowed --onefile --name $(APP)-arm64 maraton.py

x86:
	@if ! /usr/local/bin/python3 --version > /dev/null 2>&1; then \
		echo "x86_64 Python not found at /usr/local/bin/python3."; \
		echo "Install it from https://www.python.org/downloads/macos/"; \
		exit 1; \
	fi
	$(PYTHON_X86) -m PyInstaller --windowed --onefile --name $(APP)-x86 maraton.py

clean:
	rm -rf build dist *.spec
