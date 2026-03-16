use tauri::Manager;
use tauri_plugin_shell::ShellExt;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_dialog::init())
        .plugin(tauri_plugin_fs::init())
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }

            // Spawn the Python backend sidecar
            match app.shell().sidecar("binaries/backend") {
                Ok(sidecar) => {
                    match sidecar.spawn() {
                        Ok((mut rx, _child)) => {
                            // Log sidecar output
                            tauri::async_runtime::spawn(async move {
                                use tauri_plugin_shell::process::CommandEvent;
                                while let Some(event) = rx.recv().await {
                                    match event {
                                        CommandEvent::Stdout(line) => {
                                            log::info!("[backend] {}", String::from_utf8_lossy(&line));
                                        }
                                        CommandEvent::Stderr(line) => {
                                            log::warn!("[backend] {}", String::from_utf8_lossy(&line));
                                        }
                                        CommandEvent::Terminated(status) => {
                                            log::error!("[backend] terminated: {:?}", status);
                                            break;
                                        }
                                        _ => {}
                                    }
                                }
                            });
                            log::info!("Backend sidecar spawned");
                        }
                        Err(e) => {
                            log::warn!("Could not spawn sidecar (dev mode?): {}", e);
                        }
                    }
                }
                Err(e) => {
                    log::warn!("Could not create sidecar command: {}", e);
                }
            }

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
