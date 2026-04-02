'use client'

import { useState, useEffect } from 'react'
import { Github, Linkedin, Mail, ExternalLink, ArrowRight, Sparkles, Brain, Code2, Database, Terminal, Bot, Search, TrendingUp, Shield, GitBranch, Cpu } from 'lucide-react'
import Link from 'next/link'

const navItems = [
  { label: 'About', href: '#about' },
  { label: 'Experience', href: '#experience' },
  { label: 'Projects', href: '#projects' },
  { label: 'Learnings', href: '#learnings' },
]

const socialLinks = [
  { icon: Github, href: 'https://github.com', label: 'GitHub' },
  { icon: Linkedin, href: 'https://linkedin.com/in/seanscully5', label: 'LinkedIn' },
  { icon: Mail, href: 'mailto:srscully@umich.edu', label: 'Email' },
]

const skills = [
  { icon: Brain, label: 'LLMs & Agents', desc: 'LangGraph, LangChain, LangSmith, OpenAI, Prompt Engineering' },
  { icon: Code2, label: 'Languages', desc: 'Python, SQL, R, C++, JavaScript/TypeScript' },
  { icon: Database, label: 'Systems & Data', desc: 'Redis, MongoDB, PostgreSQL, FastAPI, REST APIs' },
  { icon: Terminal, label: 'ML & AI', desc: 'NLP, Vision Transformers, RAG, Predictive Analytics' },
  { icon: GitBranch, label: 'DevOps & Tools', desc: 'Docker, Git, CI/CD, Linux, AWS/GCP basics' },
  { icon: Cpu, label: 'Frameworks', desc: 'PyTorch, scikit-learn, pandas, NumPy, Next.js' },
]

const awards = [
  {
    title: 'CIO Award Winner',
    organization: 'Marsh McLennan',
    year: '2025',
    description: 'Recognized by Chief Information Officer Paul Beswick for designing Curie\'s schema, context engineering, and dynamic context improvements enabling robust, scalable conversational AI performance.',
    bonus: '$3,000 award',
  },
]

const experiences = [
  {
    company: 'Marsh McLennan',
    role: 'Software Developer, AI/ML',
    period: '2024 — Present',
    description: 'Building enterprise LLM systems. Led development of the first production AI chatbot serving 25+ stakeholders. Architected agent-based systems with LangGraph, reducing response latency through Redis optimization and context engineering.',
    highlights: [
      '🏆 CIO Award Winner (2025) — Recognized for designing Curie\'s schema, context engineering, and dynamic context improvements enabling robust, scalable conversational AI',
      'Reduced context size by ~50% while preserving accuracy',
      'Improved response relevance by 25-35% through iterative evaluation',
      'Migrated memory architecture from Postgres to Redis',
      'Implemented JWT-based auth with role-aware access control',
    ],
  },
  {
    company: 'Marsh McLennan',
    role: 'Application Development Analyst',
    period: 'Summer 2023',
    description: 'Built Python models for financial data analysis. Conducted exploratory analysis to improve cash flow forecasting accuracy.',
    highlights: [
      'Analyzed large financial datasets for trend identification',
      'Improved long-term projection reliability',
      'Translated findings into actionable business recommendations',
    ],
  },
]

const projects = [
  {
    title: 'Multi-Agent Orchestrator',
    description: 'LangGraph-powered system coordinating specialized AI agents. Features intelligent routing, parallel execution, and context-aware synthesis.',
    tech: ['LangGraph', 'OpenAI', 'FastAPI', 'Redis'],
    icon: Bot,
    github: 'https://github.com/sscully2525/seanscully.dev/tree/main/projects/agent-orchestrator',
    demo: 'https://github.com/sscully2525/seanscully.dev/tree/main/projects/agent-orchestrator',
    highlights: [
      'Router agent intelligently delegates to specialized agents',
      'Parallel execution with state management',
      'Memory persistence across conversations',
      'Modular agent architecture'
    ]
  },
  {
    title: 'Advanced RAG Pipeline',
    description: 'Production RAG system with query rewriting, hybrid search (dense + sparse), reciprocal rank fusion, and cross-encoder reranking.',
    tech: ['LangChain', 'OpenAI', 'BM25', 'Vector DB'],
    icon: Search,
    github: 'https://github.com/sscully2525/seanscully.dev/tree/main/projects/rag-pipeline',
    demo: 'https://github.com/sscully2525/seanscully.dev/tree/main/projects/rag-pipeline',
    highlights: [
      'Query expansion and clarification',
      'Hybrid retrieval: embeddings + BM25',
      'Reciprocal Rank Fusion for result merging',
      '94% retrieval accuracy (vs 67% baseline)'
    ]
  },
  {
    title: 'AI Market Analyzer',
    description: 'Real-time market analysis using LLMs for sentiment, technical indicators, and trading signals. Pattern detection and risk assessment.',
    tech: ['Python', 'yfinance', 'pandas-ta', 'OpenAI'],
    icon: TrendingUp,
    github: 'https://github.com/sscully2525/seanscully.dev/tree/main/projects/market-analyzer',
    demo: 'https://github.com/sscully2525/seanscully.dev/tree/main/projects/market-analyzer',
    highlights: [
      'Technical indicator calculation (RSI, MACD, Bollinger)',
      'Pattern detection (Golden Cross, divergences)',
      'LLM-powered trend analysis',
      'Automated signal generation'
    ]
  },
  {
    title: 'AI Code Reviewer',
    description: 'Intelligent code review combining AST analysis with LLM reasoning. Detects security issues, performance problems, and style violations.',
    tech: ['Python', 'AST', 'LangChain', 'OpenAI'],
    icon: Shield,
    github: 'https://github.com/sscully2525/seanscully.dev/tree/main/projects/code-reviewer',
    demo: 'https://github.com/sscully2525/seanscully.dev/tree/main/projects/code-reviewer',
    highlights: [
      'Static analysis for security vulnerabilities',
      'Performance pattern detection',
      'Auto-fix generation with LLM',
      'Quality scoring and reporting'
    ]
  },
]

const learnings = [
  {
    title: 'LangChain Academy: LangGraph',
    source: 'LangChain',
    type: 'Course',
    description: 'Official course on building stateful, multi-actor applications with LLMs using graph-based orchestration.',
    link: 'https://academy.langchain.com/courses/intro-to-langgraph',
  },
  {
    title: 'Practical Deep Learning for Coders',
    source: 'Fast.ai',
    type: 'Course',
    description: 'Hands-on deep learning course covering CNNs, transformers, and modern neural network architectures.',
    link: 'https://course.fast.ai',
  },
  {
    title: 'Building LLM Applications for Production',
    source: 'DeepLearning.AI',
    type: 'Course',
    description: 'Andrew Ng\'s course on productionizing LLMs, covering RAG, fine-tuning, and deployment patterns.',
    link: 'https://deeplearning.ai/short-courses/building-llm-apps/',
  },
  {
    title: 'LLM Powered Autonomous Agents',
    source: 'Lil\'Log',
    type: 'Blog',
    description: 'Comprehensive survey of autonomous agent architectures, memory systems, and tool use patterns.',
    link: 'https://lilianweng.github.io/posts/2023-06-23-llm-agent/',
  },
  {
    title: 'Anthropic\'s Contextual Retrieval',
    source: 'Anthropic',
    type: 'Research',
    description: 'Advanced RAG techniques combining embeddings with contextual chunk headers for improved retrieval.',
    link: 'https://anthropic.com/news/contextual-retrieval',
  },
  {
    title: 'The Illustrated Transformer',
    source: 'Jay Alammar',
    type: 'Blog',
    description: 'Visual guide to understanding transformer architecture and attention mechanisms.',
    link: 'https://jalammar.github.io/illustrated-transformer/',
  },
]

export default function Home() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return (
    <main className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-border bg-background/80 backdrop-blur-md">
        <div className="mx-auto max-w-5xl px-6 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="text-lg font-semibold tracking-tight">
              ss
            </Link>
            <div className="hidden md:flex items-center gap-8">
              {navItems.map((item) => (
                <a
                  key={item.label}
                  href={item.href}
                  className="text-sm text-muted hover:text-foreground transition-colors"
                >
                  {item.label}
                </a>
              ))}
            </div>
            <div className="flex items-center gap-4">
              {socialLinks.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-muted hover:text-foreground transition-colors"
                  aria-label={link.label}
                >
                  <link.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-20 px-6">
        <div className="mx-auto max-w-5xl">
          <div className="animate-fade-in">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 text-accent text-sm mb-6">
              <Sparkles className="w-4 h-4" />
              <span>Available for opportunities</span>
            </div>
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6">
              Sean Scully
            </h1>
            <p className="text-xl md:text-2xl text-muted max-w-2xl mb-8">
              AI engineer building production LLM systems and agent-based architectures. 
              Based in NYC.
            </p>
            <div className="flex flex-wrap gap-4">
              <a
                href="mailto:srscully@umich.edu"
                className="inline-flex items-center gap-2 px-6 py-3 bg-accent text-accent-foreground rounded-lg font-medium hover:bg-accent-hover transition-colors"
              >
                Get in touch
                <ArrowRight className="w-4 h-4" />
              </a>
              <a
                href="https://linkedin.com/in/seanscully5"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-6 py-3 border border-border rounded-lg font-medium hover:bg-card transition-colors"
              >
                <Linkedin className="w-4 h-4" />
                LinkedIn
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Skills */}
      <section id="about" className="py-20 px-6 border-t border-border">
        <div className="mx-auto max-w-5xl">
          <h2 className="text-3xl font-bold tracking-tight mb-12">Skills</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {skills.map((skill, i) => (
              <div
                key={skill.label}
                className="p-6 rounded-xl bg-card border border-border hover:border-accent/50 transition-colors group"
                style={{ animationDelay: `${i * 100}ms` }}
              >
                <skill.icon className="w-8 h-8 text-accent mb-4 group-hover:scale-110 transition-transform" />
                <h3 className="font-semibold mb-1">{skill.label}</h3>
                <p className="text-sm text-muted">{skill.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Experience */}
      <section id="experience" className="py-20 px-6 border-t border-border">
        <div className="mx-auto max-w-5xl">
          <h2 className="text-3xl font-bold tracking-tight mb-12">Experience</h2>
          <div className="space-y-12">
            {experiences.map((exp, i) => (
              <div
                key={i}
                className="group"
              >
                <div className="flex flex-col md:flex-row md:items-start md:justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-semibold">{exp.role}</h3>
                    <p className="text-muted">{exp.company}</p>
                  </div>
                  <span className="text-sm text-muted-foreground mt-2 md:mt-0">{exp.period}</span>
                </div>
                <p className="text-muted mb-4 max-w-3xl">{exp.description}</p>
                <ul className="space-y-2">
                  {exp.highlights.map((highlight, j) => (
                    <li key={j} className="flex items-start gap-3 text-sm">
                      <span className="w-1.5 h-1.5 rounded-full bg-accent mt-2 shrink-0" />
                      <span className="text-muted">{highlight}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Awards */}
      <section className="py-20 px-6 border-t border-border">
        <div className="mx-auto max-w-5xl">
          <h2 className="text-3xl font-bold tracking-tight mb-12">Awards</h2>
          <div className="space-y-6">
            {awards.map((award, i) => (
              <div
                key={i}
                className="p-6 rounded-xl bg-card border border-border hover:border-accent/50 transition-all"
              >
                <div className="flex flex-col md:flex-row md:items-start md:justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">🏆</span>
                    <div>
                      <h3 className="text-lg font-semibold">{award.title}</h3>
                      <p className="text-muted">{award.organization}</p>
                    </div>
                  </div>
                  <span className="text-sm text-accent font-medium mt-2 md:mt-0">{award.year}</span>
                </div>
                <p className="text-muted mb-2">{award.description}</p>
                <span className="inline-flex items-center gap-1 text-sm text-accent/80">
                  <Sparkles className="w-4 h-4" />
                  {award.bonus}
                </span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Projects */}
      <section id="projects" className="py-20 px-6 border-t border-border">
        <div className="mx-auto max-w-5xl">
          <div className="flex items-center justify-between mb-12">
            <h2 className="text-3xl font-bold tracking-tight">Projects</h2>
            <a 
              href="https://github.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-sm text-muted hover:text-foreground transition-colors inline-flex items-center gap-2"
            >
              <Github className="w-4 h-4" />
              View all on GitHub
            </a>
          </div>
          <div className="grid md:grid-cols-2 gap-6">
            {projects.map((project, i) => (
              <div
                key={i}
                className="group p-6 rounded-xl bg-card border border-border hover:border-accent/50 transition-all"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="p-3 rounded-lg bg-accent/10">
                    <project.icon className="w-6 h-6 text-accent" />
                  </div>
                  <div className="flex gap-2">
                    <a
                      href={project.github}
                      className="p-2 rounded-lg hover:bg-border transition-colors"
                      aria-label="GitHub"
                    >
                      <Github className="w-4 h-4 text-muted" />
                    </a>
                    <a
                      href={project.demo}
                      className="p-2 rounded-lg hover:bg-border transition-colors"
                      aria-label="Demo"
                    >
                      <ExternalLink className="w-4 h-4 text-muted" />
                    </a>
                  </div>
                </div>
                
                <h3 className="text-lg font-semibold mb-2 group-hover:text-accent transition-colors">
                  {project.title}
                </h3>
                <p className="text-sm text-muted mb-4">
                  {project.description}
                </p>
                
                <ul className="space-y-1.5 mb-4">
                  {project.highlights.slice(0, 3).map((highlight, j) => (
                    <li key={j} className="flex items-start gap-2 text-xs text-muted-foreground">
                      <span className="w-1 h-1 rounded-full bg-accent mt-1.5 shrink-0" />
                      {highlight}
                    </li>
                  ))}
                </ul>
                
                <div className="flex flex-wrap gap-2">
                  {project.tech.map((t) => (
                    <span
                      key={t}
                      className="text-xs px-2 py-1 rounded bg-border text-muted-foreground"
                    >
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Learnings */}
      <section id="learnings" className="py-20 px-6 border-t border-border">
        <div className="mx-auto max-w-5xl">
          <h2 className="text-3xl font-bold tracking-tight mb-12">Learnings</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {learnings.map((item, i) => (
              <a
                key={i}
                href={item.link}
                target="_blank"
                rel="noopener noreferrer"
                className="group p-6 rounded-xl bg-card border border-border hover:border-accent/50 transition-all"
              >
                <div className="flex items-start justify-between mb-3">
                  <span className="text-xs font-medium px-2 py-1 rounded bg-accent/10 text-accent">
                    {item.type}
                  </span>
                  <ExternalLink className="w-4 h-4 text-muted group-hover:text-foreground transition-colors" />
                </div>
                <h3 className="font-semibold mb-1 group-hover:text-accent transition-colors">
                  {item.title}
                </h3>
                <p className="text-sm text-muted-foreground mb-3">{item.source}</p>
                <p className="text-sm text-muted">{item.description}</p>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-border">
        <div className="mx-auto max-w-5xl">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-muted">
              © {new Date().getFullYear()} Sean Scully. Built with Next.js & Tailwind.
            </p>
            <div className="flex items-center gap-6">
              {socialLinks.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-muted hover:text-foreground transition-colors"
                >
                  {link.label}
                </a>
              ))}
            </div>
          </div>
        </div>
      </footer>
    </main>
  )
}
