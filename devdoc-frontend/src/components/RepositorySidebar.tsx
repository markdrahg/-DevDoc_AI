import { Folder, File, ChevronRight, ChevronDown, ArrowLeft } from 'lucide-react';
import { useState } from 'react';
import { Logo } from '../assets/logo/Logo';
import { ThemeToggle } from '../assets/ThemeToggle/ThemeToggle';

interface FileNode {
  name: string;
  type: 'file' | 'folder';
  children?: FileNode[];
}

interface RepositorySidebarProps {
  onBack?: () => void;
}

export function RepositorySidebar({ onBack }: RepositorySidebarProps) {
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set(['src']));

  const fileTree: FileNode[] = [
    {
      name: 'src',
      type: 'folder',
      children: [
        { name: 'index.ts', type: 'file' },
        {
          name: 'controllers',
          type: 'folder',
          children: [
            { name: 'authController.ts', type: 'file' },
            { name: 'productController.ts', type: 'file' }
          ]
        },
        {
          name: 'middleware',
          type: 'folder',
          children: [
            { name: 'auth.ts', type: 'file' }
          ]
        },
        { name: 'routes', type: 'folder' },
        { name: 'lib', type: 'folder' }
      ]
    },
    {
      name: 'prisma',
      type: 'folder',
      children: [
        { name: 'schema.prisma', type: 'file' }
      ]
    },
    { name: 'package.json', type: 'file' },
    { name: 'tsconfig.json', type: 'file' },
    { name: '.env.example', type: 'file' }
  ];

  const toggleFolder = (name: string) => {
    const newExpanded = new Set(expandedFolders);
    if (newExpanded.has(name)) {
      newExpanded.delete(name);
    } else {
      newExpanded.add(name);
    }
    setExpandedFolders(newExpanded);
  };

  const renderTree = (nodes: FileNode[], depth = 0) => {
    return nodes.map((node) => (
      <div key={node.name}>
        <div
          className={`flex items-center gap-2.5 py-2 px-2.5 rounded-md hover:bg-accent/30 cursor-pointer group transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]`}
          style={{ paddingLeft: `${depth * 14 + 8}px` }}
          onClick={() => node.type === 'folder' && toggleFolder(node.name)}
        >
          {node.type === 'folder' ? (
            <>
              {expandedFolders.has(node.name) ? (
                <ChevronDown className="w-4 h-4 text-muted-foreground/60 transition-transform duration-200" />
              ) : (
                <ChevronRight className="w-4 h-4 text-muted-foreground/60 transition-transform duration-200" />
              )}
              <Folder className="w-4 h-4 text-primary/80 group-hover:text-primary transition-colors duration-200" />
            </>
          ) : (
            <>
              <div className="w-4" />
              <File className="w-4 h-4 text-muted-foreground/60 group-hover:text-muted-foreground transition-colors duration-200" />
            </>
          )}
          <span className="text-sm text-muted-foreground group-hover:text-foreground truncate transition-colors duration-200">
            {node.name}
          </span>
        </div>
        {node.type === 'folder' && expandedFolders.has(node.name) && node.children && (
          <div>{renderTree(node.children, depth + 1)}</div>
        )}
      </div>
    ));
  };

  return (
    <div className="h-full bg-background border-r border-border/40">
      <div className="h-full flex flex-col">
        {/* Logo and Theme Toggle */}
        <div className="px-4 py-4 border-b border-border/40 flex items-center justify-between">
          <Logo />
          <ThemeToggle />
        </div>

        {/* Back Button */}
        {onBack && (
          <div className="px-4 py-3 border-b border-border/40">
            <button
              onClick={onBack}
              className="group flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-accent/50 transition-all duration-200 text-sm text-muted-foreground hover:text-foreground w-full hover:scale-[1.02] active:scale-[0.98]"
            >
              <ArrowLeft className="w-4 h-4 transition-transform duration-200 group-hover:-translate-x-1" />
              <span className="font-medium">New analysis</span>
            </button>
          </div>
        )}

        {/* Repository Info */}
        <div className="px-4 py-4 border-b border-border/40">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">Repository</h3>
            <div className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
          </div>
          <p className="text-sm text-muted-foreground mb-3">184 files · 12.4k LOC</p>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-lg bg-primary/10 border border-primary/20 hover:bg-primary/15 transition-all duration-200 cursor-default">
            <span className="text-sm font-medium text-primary">TypeScript</span>
          </div>
        </div>
        <div className="flex-1 overflow-y-auto px-3 py-3">
          {renderTree(fileTree)}
        </div>
        <div className="px-4 py-4 border-t border-border/40">
          <div className="text-sm font-semibold text-foreground mb-3">
            Dependencies
          </div>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between items-center p-2 rounded-md hover:bg-accent/30 transition-all duration-200 cursor-pointer">
              <span className="text-muted-foreground">express</span>
              <span className="text-xs text-muted-foreground/70">^4.19.2</span>
            </div>
            <div className="flex justify-between items-center p-2 rounded-md hover:bg-accent/30 transition-all duration-200 cursor-pointer">
              <span className="text-muted-foreground">prisma</span>
              <span className="text-xs text-muted-foreground/70">^5.18.0</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
