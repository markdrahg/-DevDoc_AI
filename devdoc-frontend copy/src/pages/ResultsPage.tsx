import { RepositorySidebar } from '../components/RepositorySidebar';
import { DocumentationViewer } from '../components/DocumentationViewer';
import { QuestionInterface } from '../components/QuestionInterface';

interface ResultsPageProps {
  onBack: () => void;
}

export function ResultsPage({ onBack }: ResultsPageProps) {
  return (
    <div className="h-screen w-screen flex overflow-hidden bg-background">
      {/* Left Sidebar - Compact */}
      <div className="w-72 flex-shrink-0">
        <RepositorySidebar onBack={onBack} />
      </div>

      {/* Center - Maximum space for documentation */}
      <div className="flex-1 min-w-0">
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
      <div className="w-96 flex-shrink-0">
        <QuestionInterface />
      </div>
    </div>
  );
}
