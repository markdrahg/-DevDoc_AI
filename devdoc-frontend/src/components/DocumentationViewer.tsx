import { FileText, Download, Copy, Check } from 'lucide-react';
import { useState } from 'react';

interface DocumentationViewerProps {
  title: string;
  content: string;
  type: 'readme' | 'summary' | 'guide';
}

export function DocumentationViewer({ title, content, type }: DocumentationViewerProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title.toLowerCase().replace(/\s+/g, '-')}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const getColor = () => {
    switch (type) {
      case 'readme': return 'var(--primary)';
      case 'summary': return 'var(--secondary)';
      case 'guide': return 'var(--accent-color)';
      default: return 'var(--primary)';
    }
  };

  return (
    <div className="h-full flex flex-col bg-background">
      <div className="flex items-center justify-between px-12 py-8 border-b border-border/40 backdrop-blur-sm bg-background/80 sticky top-0 z-10">
        <div className="flex items-center gap-4 animate-fade-in">
          <div className="flex items-center gap-2 px-4 py-1.5 rounded-lg bg-secondary/10 border border-secondary/20 hover:bg-secondary/15 transition-all duration-200">
            <div className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
            <span className="text-sm font-medium text-secondary">Ready</span>
          </div>
          <span className="text-base text-muted-foreground">·</span>
          <h3 className="text-lg font-semibold text-foreground">{title}</h3>
        </div>
        <div className="flex items-center gap-2 animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <button
            onClick={handleCopy}
            className="group p-2.5 rounded-lg hover:bg-accent/50 transition-all duration-200 hover:scale-110 active:scale-95"
            title="Copy to clipboard"
          >
            {copied ? (
              <Check className="w-5 h-5 text-secondary animate-fade-in" />
            ) : (
              <Copy className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors duration-200" />
            )}
          </button>
          <button
            onClick={handleDownload}
            className="group px-4 py-2.5 rounded-lg hover:bg-accent/50 transition-all duration-200 flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground hover:scale-105 active:scale-95"
            title="Download"
          >
            <Download className="w-5 h-5 transition-transform duration-200 group-hover:translate-y-0.5" />
            Export
          </button>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto px-16 py-12 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
        <div className="max-w-5xl mx-auto">
          <div className="prose prose-lg max-w-none dark:prose-invert prose-headings:font-bold prose-headings:tracking-tight prose-h1:text-4xl prose-h2:text-3xl prose-h3:text-2xl prose-p:text-foreground/90 prose-p:leading-relaxed prose-strong:text-foreground prose-code:text-primary prose-code:bg-primary/10 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-pre:bg-card/50 prose-pre:border prose-pre:border-border/40 prose-pre:shadow-lg">
            <pre className="text-base leading-relaxed whitespace-pre-wrap font-mono text-foreground/90">{content}</pre>
          </div>
        </div>
      </div>
    </div>
  );
}
