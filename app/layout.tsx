import type { Metadata } from 'next'
import { Inter, JetBrains_Mono } from 'next/font/google'
import './globals.css'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-sans',
})

const jetbrainsMono = JetBrains_Mono({ 
  subsets: ['latin'],
  variable: '--font-mono',
})

export const metadata: Metadata = {
  title: 'Sean Scully — AI Engineer',
  description: 'AI engineer building production LLM systems and agent-based architectures. Specializing in LangGraph, LangChain, and intelligent orchestration.',
  keywords: ['AI Engineer', 'Machine Learning', 'LLM', 'LangGraph', 'Python', 'NYC'],
  authors: [{ name: 'Sean Scully' }],
  openGraph: {
    title: 'Sean Scully — AI Engineer',
    description: 'Building production LLM systems and agent-based architectures',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="antialiased">{children}</body>
    </html>
  )
}
