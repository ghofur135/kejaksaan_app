#!/bin/bash
# Script untuk install dependencies PDF processing
# Run dengan: bash install_pdf_dependencies.sh

echo "🚀 Installing PDF to CSV conversion dependencies..."
echo "=================================================="

# Check if Python and pip are available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python3 first."
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Please install pip3 first."
    exit 1
fi

# Install system dependencies (Ubuntu/Debian)
echo "📦 Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    echo "Detected Ubuntu/Debian system"
    sudo apt-get update
    sudo apt-get install -y default-jre ghostscript python3-tk
    echo "✅ System dependencies installed"
else
    echo "⚠️  Non-Ubuntu/Debian system detected. Please install manually:"
    echo "   - Java Runtime Environment (JRE) 8+"
    echo "   - Ghostscript"
    echo "   - Python3-tk"
fi

# Install Python packages
echo "🐍 Installing Python packages..."

# Core packages
echo "Installing core packages..."
pip3 install pandas openpyxl

# PDF processing packages
echo "Installing PDF processing packages..."
pip3 install pdfplumber==0.11.0
pip3 install PyPDF2==3.0.1

# Try to install tabula-py (requires Java)
echo "Installing tabula-py (requires Java)..."
if pip3 install tabula-py==2.9.0; then
    echo "✅ tabula-py installed successfully"
else
    echo "⚠️  tabula-py installation failed. Make sure Java is installed."
fi

# Try to install camelot with dependencies
echo "Installing camelot-py with computer vision support..."
pip3 install pdf2image==1.17.0
pip3 install opencv-python==4.8.1.78

if pip3 install camelot-py[cv]==0.10.1; then
    echo "✅ camelot-py installed successfully"
else
    echo "⚠️  camelot-py installation failed. Some features may not work."
fi

echo ""
echo "🎉 Installation complete!"
echo "=================================================="

# Test installations
echo "🔍 Testing PDF libraries..."
python3 -c "
try:
    import pdfplumber
    print('✅ pdfplumber: Available')
except ImportError:
    print('❌ pdfplumber: Not available')

try:
    import tabula
    print('✅ tabula-py: Available')
except ImportError:
    print('❌ tabula-py: Not available (check Java installation)')

try:
    import camelot
    print('✅ camelot-py: Available')
except ImportError:
    print('❌ camelot-py: Not available')

try:
    import PyPDF2
    print('✅ PyPDF2: Available')
except ImportError:
    print('❌ PyPDF2: Not available')
"

echo ""
echo "📋 Summary:"
echo "- At least pdfplumber should be available for basic PDF processing"
echo "- tabula-py provides best results for structured tables (requires Java)"
echo "- camelot-py offers advanced features with computer vision"
echo ""
echo "🚀 Ready to use PDF to CSV conversion feature!"