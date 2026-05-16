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
      <div className="flex items-center justify-between px-12 py-8 border-b border-border/40">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-4 py-1.5 rounded-lg bg-secondary/10 border border-secondary/20">
            <div className="w-2 h-2 rounded-full bg-secondary" />
            <span className="text-sm font-medium text-secondary">Ready</span>
          </div>
          <span className="text-base text-muted-foreground">·</span>
          <h3 className="text-lg font-semibold text-foreground">{title}</h3>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="p-2.5 rounded-lg hover:bg-accent/50 transition-colors"
            title="Copy to clipboard"
          >
            {copied ? <Check className="w-5 h-5 text-secondary" /> : <Copy className="w-5 h-5 text-muted-foreground" />}
          </button>
          <button
            onClick={handleDownload}
            className="px-4 py-2.5 rounded-lg hover:bg-accent/50 transition-colors flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"
            title="Download"
          >
            <Download className="w-5 h-5" />
            Export
          </button>
        </div>
      </div>
      <div className="flex-1 overflow-y-auto px-16 py-12">
        <div className="max-w-5xl mx-auto">
          <div className="prose prose-base max-w-none dark:prose-invert">
            <pre className="text-base leading-relaxed whitespace-pre-wrap font-mono text-foreground/90">{content}</pre>
          </div>
        </div>
      </div>
    </div>
  );
}
