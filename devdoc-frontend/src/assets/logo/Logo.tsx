export function Logo() {
  return (
    <div className="flex items-center gap-3">
      <svg
        width="40"
        height="40"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-10 h-10"
      >
        {/* Code brackets </> */}
        <path
          d="M8 6L2 12L8 18M16 6L22 12L16 18"
          stroke="url(#logo-gradient)"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {/* AI spark in center */}
        <circle cx="12" cy="12" r="1.5" fill="url(#logo-gradient)" />
        <path
          d="M12 9v1M12 14v1M10 12h-1M15 12h-1"
          stroke="url(#logo-gradient)"
          strokeWidth="1.2"
          strokeLinecap="round"
        />
        <defs>
          <linearGradient id="logo-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="var(--primary)" />
            <stop offset="100%" stopColor="var(--secondary)" />
          </linearGradient>
        </defs>
      </svg>
      <h1 className="text-xl tracking-tight bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent font-semibold">
        DevDocs AI
      </h1>
    </div>
  );
}
