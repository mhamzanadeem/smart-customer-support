"use client";

import { useEffect, useState } from "react";

export default function Status() {
  const [status, setStatus] =
    useState("Checking backend...");

  useEffect(() => {
    fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/health`
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error();
        }

        return response.json();
      })
      .then((data) => {
        setStatus(
          data.database
            ? "Backend + MongoDB connected"
            : "Backend online, database unavailable"
        );
      })
      .catch(() => {
        setStatus(
          "Backend unavailable"
        );
      });
  }, []);

  return (
    <div className="status">
      {status}
    </div>
  );
}