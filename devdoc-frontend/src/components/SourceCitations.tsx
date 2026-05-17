import { FileCode, ExternalLink } from 'lucide-react';

interface Citation {
  id: string;
  file: string;
  line: number;
  snippet: string;
  url?: string;
}

export function SourceCitations({ citations }: { citations?: Citation[] }) {
  const defaultCitations: Citation[] = citations || [
    {
      id: '1',
      file: 'src/auth/login.ts',
      line: 42,
      snippet: 'async function authenticateUser(credentials: UserCredentials)',
      url: 'https://github.com/user/repo/blob/main/src/auth/login.ts#L42'
    },
    {
      id: '2',
      file: 'src/api/routes.ts',
      line: 18,
      snippet: 'router.post(\'/api/login\', validateCredentials, handleLogin)',
      url: 'https://github.com/user/repo/blob/main/src/api/routes.ts#L18'
    },
    {
      id: '3',
      file: 'src/database/user.model.ts',
      line: 67,
      snippet: 'interface User { id: string; email: string; role: UserRole }',
      url: 'https://github.com/user/repo/blob/main/src/database/user.model.ts#L67'
    }
  ];

  return (
    <div className="bg-card border border-border rounded-lg p-4">
      <div className="flex items-center gap-2 mb-4">
        <div className="p-2 rounded-lg bg-[var(--accent-color)]/10" style={{ color: 'var(--accent-color)' }}>
          <FileCode className="w-4 h-4" />
        </div>
        <div>
          <h3 className="text-sm font-semibold">Source Citations</h3>
          <p className="text-xs text-muted-foreground">Referenced code locations</p>
        </div>
      </div>

      <div className="space-y-2">
        {defaultCitations.map((citation) => (
          <div
            key={citation.id}
            className="p-3 rounded-lg border border-border hover:border-border/60 transition-all group"
          >
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs font-medium text-foreground">{citation.file}</span>
                  <span className="text-xs text-muted-foreground">Line {citation.line}</span>
                </div>
                <code className="text-xs text-muted-foreground bg-muted/50 px-2 py-0.5 rounded">
                  {citation.snippet}
                </code>
              </div>
              {citation.url && (
                <a
                  href={citation.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-1.5 rounded-lg hover:bg-accent transition-colors opacity-0 group-hover:opacity-100"
                  title="View source"
                >
                  <ExternalLink className="w-3.5 h-3.5 text-muted-foreground" />
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
