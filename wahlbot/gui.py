import csv
import json
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from wahlbot.config import DEFAULT_CONFIG
from wahlbot.main import run_once


class WahlbotGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Wahlbot Control Panel")
        self.root.geometry("1100x700")

        self.rows: list[dict[str, str | float | int]] = []
        self.data_dir = Path("data")
        self.trade_log_path = self.data_dir / "trade_log.jsonl"
        self.run_log_path = self.data_dir / "gui_runs.jsonl"

        self._build_form()
        self._build_table()
        self._build_actions()

    def _build_form(self) -> None:
        frame = ttk.LabelFrame(self.root, text="Konfiguration")
        frame.pack(fill="x", padx=10, pady=8)

        self.bankroll_var = tk.StringVar(value="1000")
        self.poll_min_var = tk.StringVar(value=str(DEFAULT_CONFIG.poll_window_min_pct))
        self.poll_max_var = tk.StringVar(value=str(DEFAULT_CONFIG.poll_window_max_pct))
        self.close_race_var = tk.StringVar(value=str(DEFAULT_CONFIG.close_race_band_pct))
        self.max_stake_var = tk.StringVar(value=str(DEFAULT_CONFIG.max_stake_usd))
        self.min_edge_var = tk.StringVar(value=str(DEFAULT_CONFIG.min_edge_pct))
        self.min_ev_var = tk.StringVar(value=str(DEFAULT_CONFIG.min_ev))

        fields = [
            ("Bankroll (USD)", self.bankroll_var),
            ("Poll min %", self.poll_min_var),
            ("Poll max %", self.poll_max_var),
            ("Close race band %", self.close_race_var),
            ("Max stake (USD)", self.max_stake_var),
            ("Min edge %", self.min_edge_var),
            ("Min EV", self.min_ev_var),
        ]

        for idx, (label, var) in enumerate(fields):
            ttk.Label(frame, text=label).grid(row=idx // 4, column=(idx % 4) * 2, sticky="w", padx=8, pady=4)
            ttk.Entry(frame, textvariable=var, width=14).grid(row=idx // 4, column=(idx % 4) * 2 + 1, padx=8, pady=4)

    def _build_table(self) -> None:
        table_frame = ttk.LabelFrame(self.root, text="Ergebnisse")
        table_frame.pack(fill="both", expand=True, padx=10, pady=8)

        columns = ("trade_id", "market", "proposal", "agent_prob", "ev", "stake", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)
        headings = {
            "trade_id": "Trade-ID",
            "market": "Markt",
            "proposal": "Vorschlag",
            "agent_prob": "Agent Einschätzung",
            "ev": "EV",
            "stake": "Stake USD",
            "status": "Ergebnis",
        }
        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(col, width=130 if col != "market" else 360, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _build_actions(self) -> None:
        action_frame = ttk.Frame(self.root)
        action_frame.pack(fill="x", padx=10, pady=8)

        ttk.Button(action_frame, text="Bot starten", command=self.run_bot).pack(side="left", padx=4)
        ttk.Button(action_frame, text="CSV exportieren", command=self.export_csv).pack(side="left", padx=4)
        ttk.Button(action_frame, text="Beenden", command=self.root.destroy).pack(side="right", padx=4)

    def run_bot(self) -> None:
        try:
            bankroll = float(self.bankroll_var.get())
            cfg = replace(
                DEFAULT_CONFIG,
                poll_window_min_pct=float(self.poll_min_var.get()),
                poll_window_max_pct=float(self.poll_max_var.get()),
                close_race_band_pct=float(self.close_race_var.get()),
                max_stake_usd=float(self.max_stake_var.get()),
                min_edge_pct=float(self.min_edge_var.get()),
                min_ev=float(self.min_ev_var.get()),
            )
        except ValueError:
            messagebox.showerror("Ungültige Eingabe", "Bitte nur numerische Werte eintragen.")
            return

        new_rows = run_once(bankroll_usd=bankroll, config=cfg, log_path=str(self.trade_log_path))
        if not new_rows:
            messagebox.showinfo("Keine Trades", "Keine neuen Trade-Kandidaten gefunden.")
            return

        self.rows.extend(new_rows)
        for row in new_rows:
            self.table.insert(
                "",
                "end",
                values=(
                    row["trade_id"],
                    row["market"],
                    row["proposal"],
                    f"{float(row['agent_adjusted_probability']):.1%}",
                    row["ev"],
                    row["stake_usd"],
                    row["execution_status"],
                ),
            )

        self._append_gui_run_log(new_rows)
        messagebox.showinfo("Fertig", f"{len(new_rows)} Trade(s) verarbeitet.")

    def _append_gui_run_log(self, new_rows: list[dict[str, str | float | int]]) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "trades": new_rows,
        }
        with self.run_log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def export_csv(self) -> None:
        if not self.rows:
            messagebox.showwarning("Keine Daten", "Es gibt noch keine Ergebnisse zum Export.")
            return

        target = filedialog.asksaveasfilename(
            title="CSV speichern",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile="wahlbot_results.csv",
        )
        if not target:
            return

        with open(target, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=[
                    "trade_id",
                    "market",
                    "proposal",
                    "agent_adjusted_probability",
                    "ev",
                    "stake_usd",
                    "execution_status",
                ],
            )
            writer.writeheader()
            writer.writerows(self.rows)

        messagebox.showinfo("Export abgeschlossen", f"CSV gespeichert unter:\n{target}")


def launch_gui() -> None:
    root = tk.Tk()
    app = WahlbotGUI(root)
    _ = app
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
