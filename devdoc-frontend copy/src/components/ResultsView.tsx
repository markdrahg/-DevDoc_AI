import { useState } from 'react';
import { ArrowLeft, FileText, BookOpen, MessageSquare } from 'lucide-react';
import { DocumentationViewer } from './DocumentationViewer';
import { ChatInterface } from './ChatInterface';

interface ResultsViewProps {
  onBack: () => void;
  repositoryName: string;
}

export function ResultsView({ onBack, repositoryName }: ResultsViewProps) {
  const [activeTab, setActiveTab] = useState<'readme' | 'summary' | 'chat'>('readme');

  // Mock data - in production this would come from the API
  const mockReadme = `# ${repositoryName}

## Overview
This is an AI-generated README for your project.

## Installation
\`\`\`bash
npm install
\`\`\`

## Usage
Your project includes the following main components:
- Authentication system
- API routes
- Database integration

## Architecture
The project follows a modular architecture with clear separation of concerns.

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct.

## License
MIT License`;

  const mockSummary = `# Documentation Summary

## Project Structure
- **/src** - Main source code
- **/components** - React components
- **/api** - Backend API endpoints
- **/utils** - Utility functions

## Key Features
1. User Authentication
2. Real-time Updates
3. Data Persistence

## Dependencies
- React 18.x
- Node.js 18+
- PostgreSQL

## API Endpoints
- GET /api/users
- POST /api/auth/login
- PUT /api/profile

## Configuration
Environment variables required:
- DATABASE_URL
- JWT_SECRET
- API_KEY`;

  return (
    <div className="min-h-screen">
      {/* Header */}
      <div className="border-b border-border bg-background/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={onBack}
              className="p-2 rounded-lg hover:bg-accent transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div>
              <h1 className="text-lg font-semibold">Documentation Generated</h1>
              <p className="text-sm text-muted-foreground">{repositoryName}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-border bg-background">
        <div className="container mx-auto px-6">
          <div className="flex gap-1">
            <button
              onClick={() => setActiveTab('readme')}
              className={`flex items-center gap-2 px-6 py-4 border-b-2 transition-all ${
                activeTab === 'readme'
                  ? 'border-primary text-foreground font-medium'
                  : 'border-transparent text-muted-foreground hover:text-foreground'
              }`}
            >
              <FileText className="w-4 h-4" />
              <span>README</span>
            </button>
            <button
              onClick={() => setActiveTab('summary')}
              className={`flex items-center gap-2 px-6 py-4 border-b-2 transition-all ${
                activeTab === 'summary'
                  ? 'border-primary text-foreground font-medium'
                  : 'border-transparent text-muted-foreground hover:text-foreground'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>Summary</span>
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex items-center gap-2 px-6 py-4 border-b-2 transition-all ${
                activeTab === 'chat'
                  ? 'border-primary text-foreground font-medium'
                  : 'border-transparent text-muted-foreground hover:text-foreground'
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              <span>AI Chat</span>
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-6 py-8">
        <div className="max-w-5xl mx-auto">
          {activeTab === 'readme' && (
            <DocumentationViewer
              title="README.md"
              content={mockReadme}
              type="readme"
            />
          )}
          {activeTab === 'summary' && (
            <DocumentationViewer
              title="Documentation Summary"
              content={mockSummary}
              type="summary"
            />
          )}
          {activeTab === 'chat' && <ChatInterface />}
        </div>
      </div>
    </div>
  );
}
