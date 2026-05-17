import { RepositoryInput } from '../components/RepositoryInput';
import { Logo } from '../assets/logo/Logo';
import { ThemeToggle } from '../assets/ThemeToggle/ThemeToggle';

interface UploadPageProps {
  onSubmit: (data: any) => void;
}

export function UploadPage({ onSubmit }: UploadPageProps) {
  return (
    <div className="min-h-screen flex flex-col bg-background">
      {/* Header */}
      <div className="flex items-center justify-between px-8 py-6 border-b border-border/40">
        <Logo />
        <ThemeToggle />
      </div>

      {/* Content - Centered */}
      <div className="flex-1 flex items-center justify-center px-6">
        <div className="max-w-4xl w-full space-y-8">
          <div className="text-center space-y-4">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-card border border-border">
              <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              <span className="text-sm font-medium text-muted-foreground">Intelligent AI-Powered Documentation</span>
            </div>
            <h2 className="text-4xl md:text-5xl tracking-tight font-bold">
              Turn Your Codebase into{' '}
              <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                Living Documentation
              </span>
            </h2>
            <p className="text-base text-foreground/80 max-w-xl mx-auto">
              Upload your repository and let AI analyze, document, and answer questions about your code instantly.
            </p>
          </div>
          <RepositoryInput onSubmit={onSubmit} />
        </div>
      </div>
    </div>
  );
}
