import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Smart Customer Support",
  description:
    "AI-powered customer support and knowledge management",
  icons: {
    icon: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
