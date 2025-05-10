import "~/styles/globals.css";

import { GeistSans } from "geist/font/sans";
import { type Metadata } from "next";
import { Header } from "~/components/header";
import { Footer } from "~/components/footer";
import { CSPostHogProvider, GlobalStateProvider } from "./providers";
import { ClerkProvider } from '@clerk/nextjs'

export const metadata: Metadata = {
  title: "GitToPod", 
  description:
    "迅速将 GitHub 代码仓库转换为播客，把代码变成有声的故事。", 
  metadataBase: new URL("https://GitPodcast.com"),
  keywords: [
    "github",
    "git 播客",
    "git 播客生成器",
    "git 播客工具",
    "git 播客制作器",
    "git 播客创建者",
    "播客",
    "仓库",
    "可视化",
    "代码结构",
    "系统设计",
    "软件架构",
    "软件设计",
    "软件工程",
    "软件开发",
    "开源",
    "开源软件",
    "bandarlabs",
    "GitToPod",
    "GitToPod.com",
  ],
  authors: [
    { name: "", url: "https://github.com/BandarLabs" },
  ],
  creator: "BandarLabs",
  openGraph: {
    type: "website",
    locale: "zh_CN", 
    url: "https://GitToPod.com",
    title: "GitToPod - 代码仓库到播客，只需几秒钟", 
    description:
      "迅速将 GitHub 代码仓库转换为播客，把代码变成有声的故事。", 
    siteName: "GitToPod", 
    images: [
      {
        url: "/og-image.png?v=2", // You'll need to create this image
        width: 1200,
        height: 630,
        alt: "GitToPod - 仓库播客工具",
      },
    ],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-snippet": -1,
    },
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="zh" className={`${GeistSans.variable}`}>
        <ClerkProvider>
            <GlobalStateProvider>
                <CSPostHogProvider>
                    <body className="flex min-h-screen flex-col">
                    <Header />
                    <main className="flex-grow">{children}</main>
                    <Footer />
                    </body>
                </CSPostHogProvider>
            </GlobalStateProvider>
        </ClerkProvider>
    </html>
  );
}