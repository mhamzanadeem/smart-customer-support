"use client";

import { useEffect, useRef, useState } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "";

export default function Status() {
  const [status, setStatus] =
    useState("Checking backend...");
  const intervalRef = useRef<ReturnType<
    typeof setInterval
  > | null>(null);

  useEffect(() => {
    let alive = true;

    function check() {
      if (!API_URL) {
        setStatus("API URL not configured");
        return;
      }

      fetch(`${API_URL}/health`)
        .then((response) => {
          if (!response.ok) throw new Error();
          return response.json();
        })
        .then((data) => {
          if (!alive) return;
          setStatus(
            data.database
              ? "Backend + MongoDB connected"
              : "Backend online, database unavailable"
          );
        })
        .catch(() => {
          if (!alive) return;
          setStatus("Backend unavailable");
        });
    }

    check();

    intervalRef.current = setInterval(check, 40000);

    return () => {
      alive = false;
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  return (
    <div className="status">
      {status}
    </div>
  );
}
