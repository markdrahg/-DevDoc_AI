import { useState } from 'react';
import { Upload, ArrowRight } from 'lucide-react';
import { LoadingAnimation } from './LoadingAnimation';

interface RepositoryInputProps {
  onSubmit: (data: { url?: string; file?: File; type: 'github' | 'zip' }) => void;
}

export function RepositoryInput({ onSubmit }: RepositoryInputProps) {
  const [activeTab, setActiveTab] = useState<'github' | 'zip'>('github');
  const [githubUrl, setGithubUrl] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!githubUrl.trim()) return;

    setIsProcessing(true);
    onSubmit({ url: githubUrl, type: 'github' });

    // Simulate processing
    setTimeout(() => {
      setIsProcessing(false);
    }, 8000);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleFileSubmit = () => {
    if (selectedFile) {
      setIsProcessing(true);
      onSubmit({ file: selectedFile, type: 'zip' });
      
      setTimeout(() => {
        setIsProcessing(false);
      }, 8000);
    }
  };

  if (isProcessing) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-card border border-border/40 rounded-2xl overflow-hidden shadow-lg shadow-primary/5 p-8">
          <LoadingAnimation />
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-card border border-border/40 rounded-2xl overflow-hidden shadow-lg shadow-primary/5 hover:shadow-xl hover:shadow-primary/10 transition-all duration-300">
        <div className="flex border-b border-border/40">
          <button
            onClick={() => setActiveTab('github')}
            className={`flex-1 flex items-center justify-center gap-2 px-6 py-4 transition-all duration-300 ${
              activeTab === 'github'
                ? 'bg-accent text-foreground border-b-2 border-primary'
                : 'text-muted-foreground hover:text-foreground hover:bg-accent/50'
            }`}
          >
            <svg className="w-4 h-4 transition-transform duration-300 group-hover:scale-110" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            <span className="text-sm font-medium">GitHub Repository</span>
          </button>
          <button
            onClick={() => setActiveTab('zip')}
            className={`flex-1 flex items-center justify-center gap-2 px-6 py-4 transition-all duration-300 ${
              activeTab === 'zip'
                ? 'bg-accent text-foreground border-b-2 border-primary'
                : 'text-muted-foreground hover:text-foreground hover:bg-accent/50'
            }`}
          >
            <Upload className="w-4 h-4 transition-transform duration-300 group-hover:scale-110" />
            <span className="text-sm font-medium">Upload ZIP</span>
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
                  className="w-full px-4 py-3 rounded-xl bg-input-background border border-border focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 focus:shadow-lg focus:shadow-primary/10 transition-all duration-300 hover:border-primary/50"
                />
              </div>
              <button
                type="submit"
                disabled={!githubUrl}
                className="group w-full flex items-center justify-center gap-2 px-6 py-3.5 bg-gradient-to-r from-primary to-primary/90 text-primary-foreground rounded-xl hover:from-primary/95 hover:to-primary/85 hover:shadow-xl hover:shadow-primary/25 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 font-medium shadow-lg shadow-primary/20"
              >
                <span>Generate Documentation</span>
                <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
              </button>
            </form>
          ) : (
            <div className="space-y-4">
              <label className="block">
                <input
                  type="file"
                  accept=".zip"
                  onChange={handleFileChange}
                  className="hidden"
                />
                <div className="border-2 border-dashed border-border rounded-xl p-12 text-center hover:border-primary hover:bg-accent transition-all duration-300 cursor-pointer group">
                  <Upload className="w-12 h-12 mx-auto mb-4 text-muted-foreground group-hover:text-primary transition-all duration-300 group-hover:scale-110" />
                  <p className="text-sm mb-1 font-medium">
                    {selectedFile ? selectedFile.name : 'Drop your ZIP file here'}
                  </p>
                  <p className="text-xs text-muted-foreground">or click to browse</p>
                </div>
              </label>
              <button
                type="button"
                onClick={handleFileSubmit}
                disabled={!selectedFile}
                className="group w-full flex items-center justify-center gap-2 px-6 py-3.5 bg-gradient-to-r from-primary to-primary/90 text-primary-foreground rounded-xl hover:from-primary/95 hover:to-primary/85 hover:shadow-xl hover:shadow-primary/25 active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 font-medium shadow-lg shadow-primary/20"
              >
                <span>Generate Documentation</span>
                <ArrowRight className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" />
              </button>
            </div>
          )}
        </div>
      </div>

      <p className="text-center text-xs text-muted-foreground mt-6 animate-fade-in">
        🔒 Your code is processed securely and never stored permanently
      </p>
    </div>
  );
}
