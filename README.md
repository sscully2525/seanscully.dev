# seanscully.dev

Personal portfolio site built with Next.js, TypeScript, and Tailwind CSS.

## Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Fonts:** Inter (sans), JetBrains Mono (mono)

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## Deployment

### Option 1: Vercel (Recommended)

1. Push to GitHub
2. Import project on [vercel.com](https://vercel.com)
3. Deploy automatically on every push

### Option 2: Netlify

1. Push to GitHub
2. Connect repo on [netlify.com](https://netlify.com)
3. Build settings: `npm run build`, publish directory: `dist`

## Domain

- **Free subdomain:** `sean-scully.vercel.app` or `sean-scully.netlify.app`
- **Custom domain:** `seanscully.dev` (~$12/year on Namecheap, Cloudflare, or Google Domains)

## Project Structure

```
app/
├── layout.tsx      # Root layout with fonts & metadata
├── page.tsx        # Main page with all sections
└── globals.css     # Global styles & Tailwind
public/             # Static assets
```

## Customization

- **Colors:** Edit `tailwind.config.ts` accent color
- **Content:** Edit `app/page.tsx`
- **Metadata:** Edit `app/layout.tsx`

## Adding Projects

Replace the placeholder project cards in the Projects section with actual project data:

```tsx
const projects = [
  {
    title: 'Project Name',
    description: 'What it does',
    tech: ['Python', 'LangGraph', 'FastAPI'],
    github: 'https://github.com/...',
    demo: 'https://...',
  },
  // ...
]
```
