import { RepositorySidebar } from '../components/RepositorySidebar';
import { DocumentationViewer } from '../components/DocumentationViewer';
import { QuestionInterface } from '../components/QuestionInterface';
import { AnimatedBackground } from '../components/AnimatedBackground';
import { Sparkles, CheckCircle2 } from 'lucide-react';

interface ResultsPageProps {
  onBack: () => void;
  showSuccessBanner?: boolean;
}

export function ResultsPage({ onBack, showSuccessBanner = false }: ResultsPageProps) {
  return (
    <div className="h-screen w-screen flex overflow-hidden bg-background relative">
      <AnimatedBackground />
      
      {/* Success Banner - Only show when prop is true */}
      {showSuccessBanner && (
        <div className="absolute top-0 left-0 right-0 z-20 bg-gradient-to-r from-secondary/10 via-primary/10 to-accent-color/10 border-b border-border/40 backdrop-blur-sm animate-slide-in-down transition-opacity duration-500">
          <div className="container mx-auto px-6 py-3 flex items-center justify-center gap-3">
            <CheckCircle2 className="w-5 h-5 text-secondary animate-bounce" />
            <span className="text-sm font-medium text-foreground">
              Documentation generated successfully!
            </span>
            <Sparkles className="w-4 h-4 text-primary animate-pulse" />
          </div>
        </div>
      )}

      {/* Left Sidebar - Compact */}
      <div className={`w-72 flex-shrink-0 animate-slide-in-left border-r border-border/40 shadow-xl shadow-primary/5 ${showSuccessBanner ? 'mt-12' : ''}`}>
        <RepositorySidebar onBack={onBack} />
      </div>

      {/* Center - Maximum space for documentation */}
      <div className={`flex-1 min-w-0 animate-fade-in-up ${showSuccessBanner ? 'mt-12' : ''}`} style={{ animationDelay: '0.1s' }}>
        <DocumentationViewer
          title="Generated README"
          content={`# E-Commerce API

Production-ready REST API for a modern e-commerce platform — authentication, products, and Stripe payments out of the box.

## Overview

This project is a **REST API** powering an online storefront. It ships with JWT authentication, a Prisma-backed Postgres layer, Stripe Checkout, and a clean controller/route/middleware architecture.

## Quick Start

### 1. Install dependencies
\`\`\`bash
npm install
\`\`\`

### 2. Configure environment
Create a \`.env\` file with:
\`\`\`
DATABASE_URL="postgresql://..."
JWT_SECRET="your-secret"
STRIPE_SECRET_KEY="sk_test_..."
\`\`\`

### 3. Run migrations
\`\`\`bash
npx prisma migrate dev
\`\`\`

### 4. Start the server
\`\`\`bash
npm run dev
\`\`\`

## Features
- JWT Authentication
- Product Management
- Stripe Integration
- PostgreSQL Database`}
          type="readme"
        />
      </div>

      {/* Right Chat - Compact */}
      <div className={`w-96 flex-shrink-0 animate-slide-in-right border-l border-border/40 shadow-xl shadow-secondary/5 ${showSuccessBanner ? 'mt-12' : ''} relative`}>
        <div className="absolute -top-2 -left-2 w-4 h-4 bg-secondary rounded-full animate-ping opacity-75" />
        <div className="absolute -top-2 -left-2 w-4 h-4 bg-secondary rounded-full" />
        <QuestionInterface />
      </div>
    </div>
  );
}
