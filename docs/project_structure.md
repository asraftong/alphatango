# AlphaTango - Struktur Projek (Pro-Level SaaS)

## Tarikh Kemas Kini
- 2025-08-06 11:39:11

## 1. Struktur Direktori Semasa
```
/opt/alphatango
├── __pycache__
│   └── config.cpython-310.pyc
├── alphatango
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── __init__.py
│   │   └── models.cpython-310.pyc
│   ├── arbitrage
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── executor_selector.py
│   │   ├── logic.py
│   │   └── pnl_protection.py
│   ├── cli
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   └── main.py
│   ├── database
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── db.py
│   │   └── models.py
│   ├── exchange
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── binance_api.py
│   │   └── websocket.py
│   ├── executors
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── async_executor.py
│   │   ├── live_executor.py
│   │   └── simulation_executor.py
│   ├── scanner
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   └── symbol_selector.py
│   ├── services
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── auto_sell.py
│   │   ├── balance_simulator.py
│   │   ├── generate_all_symbols.py
│   │   ├── healthcheck.py
│   │   ├── log_monitor.py
│   │   ├── pnl_logger.py
│   │   └── update_symbol_filters.py
│   ├── streamers
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── latency_tracker.py
│   │   ├── price_streamer.py
│   │   └── price_streamer.py.bak
│   ├── telegram
│   │   ├── __pycache__
│   │   ├── commands
│   │   ├── filters
│   │   ├── __init__.py
│   │   ├── alerts.py
│   │   └── bot.py
│   ├── utils
│   │   ├── __pycache__
│   │   ├── __init__.py
│   │   ├── async_tools.py
│   │   ├── binance_helpers.py
│   │   └── logger.py
│   ├── README.md
│   ├── __init__.py
│   ├── all_code_dump.txt
│   ├── latency_monitor.py
│   └── models.py
├── alphatango.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   ├── requires.txt
│   └── top_level.txt
├── alphatelegram
│   ├── __pycache__
│   │   ├── __init__.cpython-310.pyc
│   │   ├── alerts.cpython-310.pyc
│   │   ├── bot.cpython-310.pyc
│   │   └── state.cpython-310.pyc
│   ├── commands
│   │   ├── mute.py
│   │   ├── status.py
│   │   └── unmute.py
│   ├── __init__.py
│   ├── alerts.py
│   ├── bot.py
│   └── state.py
├── autoexec
│   └── auto_sell.py
├── backup_before_migration_20250806_112409
│   ├── log
│   │   ├── core
│   │   ├── monitor
│   │   ├── trade
│   │   ├── alphatango.err.log
│   │   ├── alphatango.err.log.1
│   │   ├── alphatango.log
│   │   ├── alphatango.log.1
│   │   ├── alphatango.log.2.gz
│   │   ├── alphatango.out.log
│   │   ├── alphatango_2025-07-24.log
│   │   ├── alphatango_2025-07-24.log.1
│   │   ├── alphatango_2025-07-24.log.2.gz
│   │   ├── alphatango_2025-07-24.log.3.gz
│   │   ├── alphatango_live.log
│   │   ├── alphatango_live.log.1
│   │   ├── alphatango_live.log.2.gz
│   │   ├── alphatango_live_error.log
│   │   ├── alphatango_simulation.log
│   │   ├── app.log
│   │   ├── app.log.1
│   │   ├── app.log.2.gz
│   │   ├── app.log.3.gz
│   │   ├── cleanup.log
│   │   ├── forcecheck.log
│   │   ├── healthcheck.log
│   │   ├── healthcheck.log.1
│   │   ├── healthcheck.log.2.gz
│   │   ├── healthcheck.log.3.gz
│   │   ├── latency.log
│   │   ├── latency_monitor.log
│   │   ├── live_buy_log.csv
│   │   ├── live_error.log
│   │   ├── live_output.log
│   │   ├── live_start.log
│   │   ├── main.err
│   │   ├── main.log
│   │   ├── main.log.1
│   │   ├── restart.log
│   │   ├── service_stderr.log
│   │   ├── service_stdout.log
│   │   ├── stderr.log
│   │   ├── stdout.log
│   │   └── update_symbol.log
│   ├── logs
│   └── scripts
│       ├── healthcheck
│       ├── maintenance
│       ├── startup
│       ├── healthcheck.sh
│       └── latency_monitor.sh
├── backup_before_migration_20250806_112634
│   ├── log
│   │   ├── core
│   │   ├── monitor
│   │   ├── trade
│   │   ├── {app,errors,trade,healthcheck}
│   │   ├── alphatango.err.log
│   │   ├── alphatango.err.log.1
│   │   ├── alphatango.log
│   │   ├── alphatango.log.1
│   │   ├── alphatango.log.2.gz
│   │   ├── alphatango.out.log
│   │   ├── alphatango_2025-07-24.log
│   │   ├── alphatango_2025-07-24.log.1
│   │   ├── alphatango_2025-07-24.log.2.gz
│   │   ├── alphatango_2025-07-24.log.3.gz
│   │   ├── alphatango_live.log
│   │   ├── alphatango_live.log.1
│   │   ├── alphatango_live.log.2.gz
│   │   ├── alphatango_live_error.log
│   │   ├── alphatango_simulation.log
│   │   ├── app.log
│   │   ├── app.log.1
│   │   ├── app.log.2.gz
│   │   ├── app.log.3.gz
│   │   ├── cleanup.log
│   │   ├── forcecheck.log
│   │   ├── healthcheck.log
│   │   ├── healthcheck.log.1
│   │   ├── healthcheck.log.2.gz
│   │   ├── healthcheck.log.3.gz
│   │   ├── latency.log
│   │   ├── latency_monitor.log
│   │   ├── live_buy_log.csv
│   │   ├── live_error.log
│   │   ├── live_output.log
│   │   ├── live_start.log
│   │   ├── main.err
│   │   ├── main.log
│   │   ├── main.log.1
│   │   ├── nohup.out
│   │   ├── restart.log
│   │   ├── service_stderr.log
│   │   ├── service_stdout.log
│   │   ├── stderr.log
│   │   ├── stdout.log
│   │   └── update_symbol.log
│   └── scripts
│       ├── healthcheck
│       ├── maintenance
│       ├── startup
│       ├── {deployment,maintenance,monitoring}
│       ├── healthcheck.sh
│       └── latency_monitor.sh
├── backup_before_migration_20250806_113407
│   ├── log
│   │   ├── core
│   │   ├── monitor
│   │   ├── trade
│   │   ├── {app,errors,trade,healthcheck}
│   │   ├── alphatango.err.log
│   │   ├── alphatango.err.log.1
│   │   ├── alphatango.log
│   │   ├── alphatango.log.1
│   │   ├── alphatango.log.2.gz
│   │   ├── alphatango.out.log
│   │   ├── alphatango_2025-07-24.log
│   │   ├── alphatango_2025-07-24.log.1
│   │   ├── alphatango_2025-07-24.log.2.gz
│   │   ├── alphatango_2025-07-24.log.3.gz
│   │   ├── alphatango_live.log
│   │   ├── alphatango_live.log.1
│   │   ├── alphatango_live.log.2.gz
│   │   ├── alphatango_live_error.log
│   │   ├── alphatango_simulation.log
│   │   ├── app.log
│   │   ├── app.log.1
│   │   ├── app.log.2.gz
│   │   ├── app.log.3.gz
│   │   ├── cleanup.log
│   │   ├── forcecheck.log
│   │   ├── healthcheck.log
│   │   ├── healthcheck.log.1
│   │   ├── healthcheck.log.2.gz
│   │   ├── healthcheck.log.3.gz
│   │   ├── latency.log
│   │   ├── latency_monitor.log
│   │   ├── live_buy_log.csv
│   │   ├── live_error.log
│   │   ├── live_output.log
│   │   ├── live_start.log
│   │   ├── main.err
│   │   ├── main.log
│   │   ├── main.log.1
│   │   ├── nohup.out
│   │   ├── restart.log
│   │   ├── service_stderr.log
│   │   ├── service_stdout.log
│   │   ├── stderr.log
│   │   ├── stdout.log
│   │   └── update_symbol.log
│   └── scripts
│       ├── healthcheck
│       ├── maintenance
│       ├── startup
│       ├── {deployment,maintenance,monitoring}
│       ├── healthcheck.sh
│       └── latency_monitor.sh
├── backup_imports_20250805_155551
│   ├── alphatango
│   │   ├── arbitrage
│   │   ├── cli
│   │   ├── database
│   │   ├── exchange
│   │   ├── executors
│   │   ├── services
│   │   ├── streamers
│   │   ├── telegram
│   │   └── utils
│   ├── alphatelegram
│   │   └── bot.py
│   ├── autoexec
│   │   └── auto_sell.py
│   ├── backup_imports_20250805_155551
│   │   ├── alphatango
│   │   ├── alphatelegram
│   │   ├── autoexec
│   │   ├── config
│   │   ├── legacy
│   │   ├── venv
│   │   ├── forcecheck_runner.py
│   │   ├── funds_converter.py
│   │   ├── generate_all_symbols.py
│   │   └── update_symbol_filters.py
│   ├── config
│   │   ├── dev.py
│   │   ├── prod.py
│   │   └── tenant_alpha.py
│   ├── legacy
│   │   ├── filters
│   │   ├── handlers
│   │   └── auto_sell.py
│   ├── venv
│   │   └── lib
│   ├── forcecheck_runner.py
│   ├── funds_converter.py
│   ├── generate_all_symbols.py
│   └── update_symbol_filters.py
├── config
│   ├── __pycache__
│   │   ├── base.cpython-310.pyc
│   │   └── config.cpython-310.pyc
│   ├── base.py
│   ├── config.py
│   ├── dev.py
│   ├── eligible_symbols.json
│   ├── prod.py
│   ├── symbol_filters.json
│   └── tenant_alpha.py
├── data
│   └── all_symbols.json
├── docker
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs
│   ├── API.md
│   ├── architecture.md
│   ├── deployment.md
│   ├── project_structure.md
│   └── setup.md
├── latency
│   ├── 2025-07-27.csv
│   └── 2025-07-29.csv
├── legacy
│   ├── filters
│   │   ├── __init__.py
│   │   └── symbol_filter.py
│   ├── handlers
│   │   └── balance_handler.py
│   ├── system
│   │   └── healthcheck_logger.py
│   ├── arbitrage_executor.py
│   ├── auto_sell.py
│   └── top_symbols.py
├── log
│   ├── app
│   ├── core
│   │   └── alphatango_live.log
│   ├── errors
│   ├── healthcheck
│   ├── monitor
│   ├── trade
│   ├── {app,errors,trade,healthcheck}
│   ├── alphatango.err.log
│   ├── alphatango.err.log.1
│   ├── alphatango.log
│   ├── alphatango.log.1
│   ├── alphatango.log.2.gz
│   ├── alphatango.out.log
│   ├── alphatango_2025-07-24.log
│   ├── alphatango_2025-07-24.log.1
│   ├── alphatango_2025-07-24.log.2.gz
│   ├── alphatango_2025-07-24.log.3.gz
│   ├── alphatango_live.log
│   ├── alphatango_live.log.1
│   ├── alphatango_live.log.2.gz
│   ├── alphatango_live_error.log
│   ├── alphatango_simulation.log
│   ├── app.log
│   ├── app.log.1
│   ├── app.log.2.gz
│   ├── app.log.3.gz
│   ├── cleanup.log
│   ├── forcecheck.log
│   ├── healthcheck.log
│   ├── healthcheck.log.1
│   ├── healthcheck.log.2.gz
│   ├── healthcheck.log.3.gz
│   ├── latency.log
│   ├── latency_monitor.log
│   ├── live_buy_log.csv
│   ├── live_error.log
│   ├── live_output.log
│   ├── live_start.log
│   ├── main.err
│   ├── main.log
│   ├── main.log.1
│   ├── nohup.out
│   ├── restart.log
│   ├── service_stderr.log
│   ├── service_stdout.log
│   ├── stderr.log
│   ├── stdout.log
│   └── update_symbol.log
├── pnl_logs
│   └── 2025-07-24.csv
├── scripts
│   ├── deployment
│   ├── healthcheck
│   │   ├── check_live_ready.sh
│   │   ├── cleanup_pnl_logs.sh
│   │   ├── fix_structure.sh
│   │   ├── go_live.sh
│   │   ├── healthcheck.sh
│   │   ├── install_alphatango.sh
│   │   ├── reboot_guard.sh
│   │   ├── restart_bot.sh
│   │   ├── smart_reboot.sh
│   │   └── start_live.sh
│   ├── maintenance
│   │   ├── generate_project_structure_doc.sh
│   │   ├── migrate_logs_scripts.sh
│   │   └── push_structure_to_github.sh
│   ├── monitoring
│   │   ├── healthcheck.sh
│   │   └── latency_monitor.sh
│   ├── startup
│   └── {deployment,maintenance,monitoring}
├── users
│   ├── default
│   │   └── alphatango.db
│   └── user_001
│       ├── latency
│       ├── logs
│       ├── pnl_logs
│       └── api_status.json
├── venv
│   ├── bin
│   │   ├── Activate.ps1
│   │   ├── activate
│   │   ├── activate.csh
│   │   ├── activate.fish
│   │   ├── dateparser-download
│   │   ├── dotenv
│   │   ├── f2py
│   │   ├── httpx
│   │   ├── normalizer
│   │   ├── pip
│   │   ├── pip3
│   │   ├── pip3.10
│   │   ├── python -> python3
│   │   ├── python3 -> /usr/bin/python3
│   │   └── python3.10 -> python3
│   ├── include
│   │   └── site
│   ├── lib
│   │   └── python3.10
│   ├── lib64 -> lib
│   └── pyvenv.cfg
├── README.md
├── all_code_dump.txt
├── aux | grep main.py
├── ervice -f
├── filelist.txt
├── fix_imports.py
├── forcecheck_runner.py
├── frozen.txt
├── funds_converter.py
├── generate_all_symbols.py
├── main.pynano
├── main_config_executor.py
├── migrate_structure.py
├── purchased_coins.csv
├── requirements.txt
├── revert_wrong_imports.py
├── send_telegram_startup.py
├── setup.py
├── setup_project.sh
├── status_checker.py
├── trade_logger.py
├── udo crontab -l
└── update_symbol_filters.py

127 directories, 330 files
```

## 2. Nota
- Struktur ini dijana secara automatik.
- Pastikan sebarang perubahan folder difahami oleh semua developer.

## 3. Amalan Baik
1. **Log Centralization** - Semua log mesti berada di dalam `log/` mengikut kategori.
2. **Scripts Categorization** - Susun semua skrip ke dalam `deployment/`, `maintenance/`, dan `monitoring/`.
3. **Config & Secrets** - Semua rahsia dalam `.env` atau `.secrets`.
4. **Documentation-First** - Setiap modul ada `README.md` ringkas.
