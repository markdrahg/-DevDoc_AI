import { useState } from 'react';
import { Upload, ArrowRight, Loader2 } from 'lucide-react';

interface RepositoryInputProps {
  onSubmit: (data: { url?: string; file?: File; type: 'github' | 'zip' }) => void;
}

export function RepositoryInput({ onSubmit }: RepositoryInputProps) {
  const [activeTab, setActiveTab] = useState<'github' | 'zip'>('github');
  const [githubUrl, setGithubUrl] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!githubUrl.trim()) return;

    setIsProcessing(true);
    onSubmit({ url: githubUrl, type: 'github' });

    // Simulate processing
    setTimeout(() => {
      setIsProcessing(false);
    }, 2000);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-card border border-border/40 rounded-2xl overflow-hidden shadow-lg shadow-primary/5">
        <div className="flex border-b border-border/40">
          <button
            onClick={() => setActiveTab('github')}
            className={`flex-1 flex items-center justify-center gap-2 px-6 py-4 transition-all ${
              activeTab === 'github'
                ? 'bg-accent text-foreground border-b-2 border-primary'
                : 'text-muted-foreground hover:text-foreground hover:bg-accent/50'
            }`}
          >
           { /* <Github className="w-4 h-4" /> */}
            <span className="text-sm">GitHub Repository</span>
          </button>
          <button
            onClick={() => setActiveTab('zip')}
            className={`flex-1 flex items-center justify-center gap-2 px-6 py-4 transition-all ${
              activeTab === 'zip'
                ? 'bg-accent text-foreground border-b-2 border-primary'
                : 'text-muted-foreground hover:text-foreground hover:bg-accent/50'
            }`}
          >
            <Upload className="w-4 h-4" />
            <span className="text-sm">Upload ZIP</span>
          </button>
        </div>

        <div className="p-8">
          {activeTab === 'github' ? (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <label htmlFor="github-url" className="text-sm font-medium text-foreground/90">
                  Repository URL
                </label>
                <input
                  id="github-url"
                  type="text"
                  value={githubUrl}
                  onChange={(e) => setGithubUrl(e.target.value)}
                  placeholder="https://github.com/username/repository"
                  className="w-full px-4 py-3 rounded-xl bg-input-background border border-border focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 focus:shadow-lg focus:shadow-primary/10 transition-all"
                />
              </div>
              <button
                type="submit"
                disabled={!githubUrl || isProcessing}
                className="w-full flex items-center justify-center gap-2 px-6 py-3.5 bg-gradient-to-b from-primary to-primary/90 text-primary-foreground rounded-xl hover:from-primary/95 hover:to-primary/85 hover:shadow-xl hover:shadow-primary/25 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed transition-all font-medium shadow-lg shadow-primary/20"
              >
                {isProcessing ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <span>Generate Documentation</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </form>
          ) : (
            <div className="space-y-4">
              <div className="border-2 border-dashed border-border rounded-xl p-12 text-center hover:border-primary hover:bg-accent transition-all cursor-pointer group">
                <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground group-hover:text-primary transition-colors" />
                <p className="text-sm mb-1">Drop your ZIP file here</p>
                <p className="text-xs text-muted-foreground">or click to browse</p>
              </div>
              <button
                type="button"
                disabled={isProcessing}
                className="w-full flex items-center justify-center gap-2 px-6 py-3.5 bg-gradient-to-b from-primary to-primary/90 text-primary-foreground rounded-xl hover:from-primary/95 hover:to-primary/85 hover:shadow-xl hover:shadow-primary/25 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed transition-all font-medium shadow-lg shadow-primary/20"
              >
                {isProcessing ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Processing...</span>
                  </>
                ) : (
                  <>
                    <span>Generate Documentation</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      </div>

      <p className="text-center text-xs text-muted-foreground mt-6">
        Your code is processed securely and never stored permanently
      </p>
    </div>
  );
}
