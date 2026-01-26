import customtkinter as ctk
# IMPORT THE NEW DB CLASS
from DB_Service.dashboard_DB import DashboardDB


class Dashboard:
    def __init__(self, app, parent_frame):
        self.app = app
        self.main_frame = parent_frame

        # Initialize Database Helper
        self.db = DashboardDB()

        # ... (Title Label code remains the same) ...
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="EMPLOYEE INFORMATION DESK",
            font=("Arial", 32, "bold"),
            text_color=self.app.text_color_primary,
            justify="left"
        )
        title_label.grid(row=1, column=0, padx=50, pady=(10, 25), sticky="w")

        # Top Statistics Row
        self.setup_top_stats(row=2)

        # Middle Section
        middle_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        middle_container.grid(row=3, column=0, padx=50, pady=10, sticky="nsew")
        middle_container.grid_columnconfigure(0, weight=2)
        middle_container.grid_columnconfigure(1, weight=1)

        self.setup_dept_distribution(middle_container, col=0)
        self.setup_contract_alerts(middle_container, col=1)

    def setup_top_stats(self, row):
        stats_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        stats_container.grid(row=row, column=0, padx=50, pady=10, sticky="ew")
        stats_container.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # --- FETCH FROM DB ---
        stats_data = self.db.fetch_top_stats()

        # Fallback if DB is empty or fails
        if not stats_data:
            stats_data = [("No Data", "0", "#999"), ("No Data", "0", "#999"), ("No Data", "0", "#999"),
                          ("No Data", "0", "#999")]

        for i, (label, value, color) in enumerate(stats_data):
            self.create_stat_card(stats_container, i, label, value, color)

    # ... (create_stat_card method remains the same) ...
    def create_stat_card(self, parent, col_idx, title, value, border_color):
        card = ctk.CTkFrame(parent, fg_color=self.app.card_bg_color, corner_radius=8, border_width=1,
                            border_color=self.app.border_color)
        card.grid(row=0, column=col_idx, padx=8, pady=0, sticky="ew")

        strip = ctk.CTkFrame(card, width=5, fg_color=border_color, corner_radius=0)
        strip.pack(side="left", fill="y", padx=(0, 10))

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(side="left", padx=5, pady=12)

        val_label = ctk.CTkLabel(content, text=value, font=("Arial", 24, "bold"),
                                 text_color=self.app.text_color_primary)
        val_label.pack(anchor="w")

        title_label = ctk.CTkLabel(content, text=title, font=("Arial", 12), text_color="gray")
        title_label.pack(anchor="w")

    def setup_dept_distribution(self, parent, col):
        frame = ctk.CTkFrame(parent, fg_color=self.app.card_bg_color, corner_radius=10, border_width=1,
                             border_color=self.app.border_color)
        frame.grid(row=0, column=col, padx=(0, 15), sticky="nsew")

        header = ctk.CTkLabel(frame, text="Department Distribution", font=("Arial", 14, "bold"),
                              text_color=self.app.text_color_primary)
        header.pack(anchor="w", padx=15, pady=(15, 10))

        # --- FETCH FROM DB ---
        depts = self.db.fetch_dept_distribution()

        # Handle empty DB case
        if not depts:
            ctk.CTkLabel(frame, text="No department data found", text_color="gray").pack(pady=20)

        for name, count in depts:
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=6)

            lbl_frame = ctk.CTkFrame(row, fg_color="transparent")
            lbl_frame.pack(fill="x")
            ctk.CTkLabel(lbl_frame, text=name, font=("Arial", 12), text_color="#333").pack(side="left")
            ctk.CTkLabel(lbl_frame, text=count, font=("Arial", 12, "bold"),
                         text_color=self.app.text_color_primary).pack(
                side="right")

    def setup_contract_alerts(self, parent, col):
        frame = ctk.CTkFrame(parent, fg_color=self.app.alert_bg_color, corner_radius=10, border_width=1,
                             border_color="#FECACA")
        frame.grid(row=0, column=col, padx=0, sticky="nsew")

        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(header_frame, text="⚠ Contract Expiry Alerts", font=("Arial", 14, "bold"),
                     text_color="#B91C1C").pack(side="left")

        alerts = self.db.fetch_contract_alerts()

        if not alerts:
            ctk.CTkLabel(frame, text="No immediate expirations", font=("Arial", 12), text_color="gray").pack(pady=20)

        for name, time in alerts:
            item = ctk.CTkFrame(frame, fg_color="white", corner_radius=6)
            item.pack(fill="x", padx=15, pady=5)

            ctk.CTkLabel(item, text=name, font=("Arial", 12, "bold"), text_color="#333").pack(anchor="w", padx=10,
                                                                                              pady=(8, 0))
            ctk.CTkLabel(item, text=time, font=("Arial", 11), text_color="#DC2626").pack(anchor="w", padx=10,
                                                                                         pady=(0, 8))

        ctk.CTkButton(frame, text="View All", fg_color="transparent", text_color="#B91C1C",
                      hover_color="#FEE2E2", font=("Arial", 11, "bold"), height=25).pack(pady=10)

    def fetch_pending_leave_count(self):

        conn = self.get_connection()
        if not conn:
            return 0

        cursor = conn.cursor()
        count = 0
        try:
            query = "SELECT COUNT(*) FROM LeaveRecord WHERE status = 'Pending' AND Active = 1"
            cursor.execute(query)
            count = cursor.fetchone()[0]
        except Exception as e:
            print(f"Error fetching pending leaves: {e}")
        finally:
            cursor.close()
            conn.close()

        return count