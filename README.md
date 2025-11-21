# Aplikasi Kejaksaan

Aplikasi manajemen data kejaksaan untuk PIDUM (Pidana Umum) dan PIDSUS (Pidana Khusus).

## Struktur Folder

```
kejaksaan_app/
├── src/                          # Source code aplikasi
│   ├── app_with_db.py           # File utama aplikasi Flask
│   ├── controllers/             # Controller aplikasi
│   ├── models/                  # Model database
│   │   └── database.py          # Koneksi dan model database
│   ├── helpers/                 # Helper functions
│   │   ├── import_helper.py
│   │   ├── import_pra_penuntutan_helper.py
│   │   └── import_upaya_hukum_helper.py
│   └── utils/                   # Utility functions
│       └── CSV Tool/            # Tools untuk CSV
├── config/                      # File konfigurasi
│   ├── ecosystem-direct.config.json
│   ├── ecosystem.config.json
│   └── kejaksaan.code-workspace
├── scripts/                     # Script utility
│   ├── generate_dummy_pidum.py
│   ├── generate_realistic_pidum_dummy.py
│   ├── insert_sample_data.py
│   ├── migrate_database.py
│   ├── pm2-manager.sh
│   ├── reset_pidum.sh
│   ├── reset_pidum_data.py
│   ├── run_app.sh
│   ├── run_production.sh
│   └── simple_reset_pidum.py
├── data/                        # Data aplikasi
│   └── csv/                     # File CSV untuk import
├── docs/                        # Dokumentasi
├── static/                      # File statis (CSS, JS, images)
├── templates/                   # Template HTML
├── logs/                        # Log files
├── tests/                       # Unit tests
├── requirements.txt             # Dependencies Python
└── .gitignore                   # Git ignore file
```

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Jalankan aplikasi:
```bash
python run.py
```

Atau jalankan langsung dari folder src:
```bash
python src/app_with_db.py
```

## Fitur

- Manajemen data PIDUM
- Manajemen data PIDSUS
- Import data dari CSV
- Generate laporan
- Visualisasi data dengan chart

## Dokumentasi

Lihat folder `docs/` untuk dokumentasi lengkap.