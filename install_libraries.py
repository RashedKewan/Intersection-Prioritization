import subprocess


libraries = [
    'pandas',
    'numpy',
    'xlrd==1.2.0',
    'openpyxl==3.0.10',
    'PyPDF2',
    'reportlab',
    'matplotlib'
]

for library in libraries:
    subprocess.run(["pip", "install", library])
