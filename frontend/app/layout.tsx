import "./globals.css";

export const metadata = {
  title: "Smart Customer Support",
  description:
    "AI-powered customer support and knowledge management",
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