import { RepositoryInput } from '../components/RepositoryInput';
import { Logo } from '../assets/logo/Logo';
import { ThemeToggle } from '../assets/ThemeToggle/ThemeToggle';
import { AnimatedBackground } from '../components/AnimatedBackground';
import { TypingText } from '../components/TypingText';
import { Sparkles } from 'lucide-react';

interface UploadPageProps {
  onSubmit: (data: any) => void;
  isGenerating?: boolean;
}

export function UploadPage({ onSubmit, isGenerating = false }: UploadPageProps) {
  return (
    <div className="min-h-screen flex flex-col bg-background animate-fade-in relative">
      <AnimatedBackground />
      {/* Header */}
      <div className="flex items-center justify-between px-8 py-6 border-b border-border/40 backdrop-blur-sm sticky top-0 z-10 transition-all duration-300">
        <div className="animate-slide-in-left">
          <Logo />
        </div>
        <div className="flex items-center gap-4 animate-slide-in-right">
          <div className="hidden sm:flex items-center gap-2 text-xs">
            <Sparkles className="w-3.5 h-3.5 text-[var(--accent-color)] animate-pulse" />
            <span className="text-muted-foreground">Powered by <span className="text-foreground font-medium">IBM watsonx</span></span>
          </div>
          <ThemeToggle />
        </div>
      </div>

      {/* Content - Centered */}
      <div className="flex-1 flex items-center justify-center px-6">
        <div className="max-w-4xl w-full space-y-8">
          <div className="text-center space-y-4 animate-fade-in-up">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-card border border-border shadow-sm hover:shadow-md transition-all duration-300">
              <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
              <span className="text-sm font-medium text-muted-foreground">Intelligent AI-Powered Documentation</span>
            </div>
            <h2 className="text-4xl md:text-5xl tracking-tight font-bold min-h-[120px] flex items-center">
              <TypingText
                text="Turn Your Codebase into Living Documentation"
                speed={60}
                className="bg-gradient-to-r from-foreground via-primary to-secondary bg-clip-text text-transparent animate-gradient"
              />
            </h2>
            <p className="text-base text-foreground/80 max-w-xl mx-auto animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
              Upload your repository and let AI analyze, document, and answer questions about your code instantly.
            </p>
          </div>
          <div className="animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
            <RepositoryInput onSubmit={onSubmit} />
          </div>
        </div>
      </div>
    </div>
  );
}
