import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Shell } from "@/components/layout/Shell";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Universal Research GUI",
  description: "Research environment for the Modular Personality AI ecosystem",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} antialiased bg-slate-950 text-slate-300`}>
        <Shell>{children}</Shell>
      </body>
    </html>
  );
}
