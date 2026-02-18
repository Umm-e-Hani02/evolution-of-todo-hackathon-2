"use client";

import { ReactNode } from "react";
import "../dashboard-styles.css";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <div className="dashboard-layout">
      <main className="dashboard-content">{children}</main>
    </div>
  );
}
